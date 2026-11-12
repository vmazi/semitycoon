#!/usr/bin/env python3
"""Telemetry sink for the game: append-only era/run records in SQLite.

Standard library only, on purpose -- the rest of this repo has no build step
and this is a handful of writes a day, so a threaded stdlib server with SQLite
is the whole requirement. There is nothing here worth a dependency tree.

    POST /api/ingest   one event, JSON body
    GET  /api/health
    GET  /api/summary  aggregate counts, for a quick does-it-work check

The endpoint is public and unauthenticated, so it assumes bad input: bodies are
size-capped, every field is pulled out defensively, and each IP gets a token
bucket. Nothing here is PII -- run ids are random and generated client-side.
"""

from __future__ import annotations

import json
import os
import sqlite3
import threading
import time
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

DB = os.environ.get("ST_DB", "/data/telemetry.db")
PORT = int(os.environ.get("ST_PORT", "8099"))
MAX_BODY = 96 * 1024
GAME = "semitycoon"

RATE_BURST = 60        # events an IP may send back-to-back
RATE_PER_SEC = 1.0     # steady-state refill; one full run is a handful of events

# The balance harness plays hundreds of runs back to back from a single address
# and would sit permanently rate-limited. It presents this key to skip the
# bucket; without one set, nothing can skip it.
TRUSTED_KEY = os.environ.get("ST_KEY") or None

SCHEMA = """
CREATE TABLE IF NOT EXISTS events(
  id        INTEGER PRIMARY KEY,
  ts        TEXT    NOT NULL,
  run_id    TEXT    NOT NULL,
  build     TEXT,
  source    TEXT,
  policy    TEXT,
  kind      TEXT    NOT NULL,
  era       INTEGER,
  placement INTEGER,
  points    INTEGER,
  share     REAL,
  payload   TEXT    NOT NULL
);
CREATE INDEX IF NOT EXISTS ix_events_run    ON events(run_id);
CREATE INDEX IF NOT EXISTS ix_events_kind   ON events(kind, era);
CREATE INDEX IF NOT EXISTS ix_events_source ON events(source, build);
"""


class Store:
    def __init__(self, path: str):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        # One connection guarded by a lock: SQLite serialises writers anyway and
        # this keeps WAL checkpointing in a single place.
        self._lock = threading.Lock()
        self._db = sqlite3.connect(path, check_same_thread=False)
        self._db.execute("PRAGMA journal_mode=WAL")
        self._db.executescript(SCHEMA)
        self._db.commit()

    def add(self, ev: dict) -> None:
        row = (
            datetime.now(timezone.utc).isoformat(timespec="seconds"),
            str(ev.get("run_id", ""))[:64],
            str(ev.get("build", ""))[:32],
            str(ev.get("source", "human"))[:16],
            (str(ev["policy"])[:64] if ev.get("policy") else None),
            str(ev.get("kind", "era"))[:16],
            _int(ev.get("era")),
            _int(ev.get("placement")),
            _int(ev.get("points")),
            _float(ev.get("share")),
            json.dumps(ev, separators=(",", ":"))[:MAX_BODY],
        )
        with self._lock:
            self._db.execute(
                "INSERT INTO events(ts,run_id,build,source,policy,kind,era,"
                "placement,points,share,payload) VALUES(?,?,?,?,?,?,?,?,?,?,?)", row)
            self._db.commit()

    def summary(self) -> dict:
        with self._lock:
            q = self._db.execute(
                "SELECT source, build, COUNT(DISTINCT run_id), COUNT(*) "
                "FROM events GROUP BY source, build ORDER BY 3 DESC").fetchall()
            fin = self._db.execute(
                "SELECT source, placement, COUNT(*) FROM events "
                "WHERE kind='final' GROUP BY source, placement").fetchall()
        return {
            "runs": [{"source": s, "build": b, "runs": r, "events": e} for s, b, r, e in q],
            "finishes": [{"source": s, "placement": p, "n": n} for s, p, n in fin],
        }


def _int(v):
    try:
        return int(v)
    except (TypeError, ValueError):
        return None


def _float(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


class Buckets:
    """Token bucket per client address."""

    def __init__(self):
        self._lock = threading.Lock()
        self._b: dict[str, tuple[float, float]] = {}

    def allow(self, key: str) -> bool:
        now = time.monotonic()
        with self._lock:
            tokens, last = self._b.get(key, (RATE_BURST, now))
            tokens = min(RATE_BURST, tokens + (now - last) * RATE_PER_SEC)
            if tokens < 1:
                self._b[key] = (tokens, now)
                return False
            self._b[key] = (tokens - 1, now)
            if len(self._b) > 4096:
                self._b = {k: v for k, v in self._b.items() if now - v[1] < 600}
            return True


STORE = Store(DB)
BUCKETS = Buckets()


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    server_version = "semitycoon-telemetry"

    def log_message(self, *a):  # BaseHTTPRequestHandler's signature
        pass

    def _send(self, code: int, body: bytes = b"", ctype="application/json"):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if body:
            self.wfile.write(body)

    def _client(self) -> str:
        # nginx is the only thing in front, so its X-Forwarded-For is trustworthy.
        fwd = self.headers.get("X-Forwarded-For", "")
        return (fwd.split(",")[0].strip() or self.client_address[0])[:64]

    def do_GET(self):
        if self.path == "/api/health":
            return self._send(200, b'{"ok":true}')
        if self.path == "/api/summary":
            return self._send(200, json.dumps(STORE.summary()).encode())
        self._send(404, b'{"error":"not found"}')

    def do_POST(self):
        if self.path != "/api/ingest":
            return self._send(404, b'{"error":"not found"}')
        trusted = bool(TRUSTED_KEY) and self.headers.get("X-ST-Key") == TRUSTED_KEY
        if not trusted and not BUCKETS.allow(self._client()):
            return self._send(429, b'{"error":"slow down"}')

        try:
            n = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            return self._send(400, b'{"error":"bad length"}')
        if n <= 0 or n > MAX_BODY:
            return self._send(413, b'{"error":"body too large"}')

        try:
            ev = json.loads(self.rfile.read(n))
        except (ValueError, OSError):
            return self._send(400, b'{"error":"bad json"}')

        # A stray crawler POSTing junk should not become a row.
        if not isinstance(ev, dict) or ev.get("game") != GAME or not ev.get("run_id"):
            return self._send(400, b'{"error":"not a game event"}')

        # The server decides what a run is, not the client: an untrusted caller
        # claiming source=harness would otherwise quietly poison the dataset the
        # balance decisions are read from.
        if not trusted:
            ev["source"] = "human"
            ev.pop("policy", None)

        STORE.add(ev)
        self._send(202, b'{"ok":true}')


if __name__ == "__main__":
    srv = ThreadingHTTPServer(("0.0.0.0", PORT), Handler)
    srv.daemon_threads = True
    print(f"telemetry on :{PORT} -> {DB}", flush=True)
    srv.serve_forever()
