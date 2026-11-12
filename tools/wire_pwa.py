#!/usr/bin/env python3
"""Add the icon / manifest / social-card tags to every page.

Idempotent: re-running replaces the block it wrote last time rather than
stacking a second copy, so it is safe to run after regenerating the art.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
BASE = "https://semitycoon.borgorg.org"
PAGES = ("demo", "about", "design", "mockups")

START, END = "<!-- pwa:start -->", "<!-- pwa:end -->"


def block(is_game: bool) -> str:
    lines = [
        START,
        '<link rel="icon" href="/icons/favicon.ico" sizes="any">',
        '<link rel="icon" type="image/png" href="/icons/favicon.png">',
        '<link rel="apple-touch-icon" href="/icons/icon-180.png">',
        f'<meta property="og:image" content="{BASE}/icons/og.png">',
        '<meta property="og:image:width" content="1200">',
        '<meta property="og:image:height" content="630">',
        f'<meta name="twitter:image" content="{BASE}/icons/og.png">',
    ]
    if is_game:
        # Only the game is installable; the docs pages share its icons but
        # should not each offer themselves as a separate home-screen app.
        lines += [
            '<link rel="manifest" href="/manifest.webmanifest">',
            '<meta name="apple-mobile-web-app-capable" content="yes">',
            '<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">',
            '<meta name="apple-mobile-web-app-title" content="Semi Tycoon">',
            '<script>if("serviceWorker" in navigator)addEventListener("load",'
            '()=>navigator.serviceWorker.register("/sw.js").catch(()=>{}));</script>',
        ]
    lines.append(END)
    return "\n".join(lines)


def main() -> None:
    for page in PAGES:
        p = SITE / page / "index.html"
        text = p.read_text()
        new = block(page == "demo")

        if START in text:
            text = re.sub(re.escape(START) + r".*?" + re.escape(END), new, text, flags=re.S)
        else:
            # twitter:card is the last tag of the meta run added for the rename,
            # so the icon block lands immediately after it and before the CSS.
            anchor = re.search(r'^<meta name="twitter:description".*?>$', text, re.M)
            if not anchor:
                raise SystemExit(f"{p}: no meta block to anchor to")
            text = text[: anchor.end()] + "\n" + new + text[anchor.end():]

        # A summary card is a small square; with a 1200x630 image we want the
        # big one, and only now that an image actually exists.
        text = text.replace('<meta name="twitter:card" content="summary">',
                            '<meta name="twitter:card" content="summary_large_image">')
        p.write_text(text)
        print("wired", p.relative_to(ROOT))


if __name__ == "__main__":
    main()
