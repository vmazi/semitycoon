#!/usr/bin/env python3
"""Upscale a small source image through Flux img2img.

    python3 tools/upscale.py ref.png --out /tmp/up --denoise 0.4

A plain resize of a ~200px source just gives you big soft pixels. This lifts it
to 1024 and lets Flux repaint the detail, with denoise controlling how much
licence it takes: ~0.3 cleans up the lines and keeps the face, ~0.6 starts
redrawing the subject into something that is no longer recognisably the source.
Sweep a few values -- the right one is a judgement call on the picture.
"""

from __future__ import annotations

import argparse
import json
import os
import time
import urllib.parse
import urllib.request
import uuid
from io import BytesIO
from pathlib import Path

for _v in ("http_proxy", "https_proxy", "HTTP_PROXY", "HTTPS_PROXY", "all_proxy", "ALL_PROXY"):
    os.environ.pop(_v, None)

from PIL import Image  # noqa: E402

HOST = "http://bazzite:8188"
CKPT = "flux1-dev-fp8.safetensors"
NEG = "watermark, signature, text, caption, jpeg artifacts, blurry"


def upload(path: Path) -> str:
    """POST an image into ComfyUI's input dir and return its server-side name."""
    name = f"up_{uuid.uuid4().hex[:10]}.png"
    boundary = "----" + uuid.uuid4().hex
    body = b"".join([
        f"--{boundary}\r\n".encode(),
        f'Content-Disposition: form-data; name="image"; filename="{name}"\r\n'.encode(),
        b"Content-Type: image/png\r\n\r\n",
        path.read_bytes(),
        f"\r\n--{boundary}--\r\n".encode(),
    ])
    req = urllib.request.Request(
        f"{HOST}/upload/image", data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read())["name"]


def graph(image_name: str, prompt: str, denoise: float, seed: int, size: int, steps: int):
    return {
        "1": {"class_type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": CKPT}},
        "2": {"class_type": "CLIPTextEncode", "inputs": {"text": prompt, "clip": ["1", 1]}},
        "3": {"class_type": "CLIPTextEncode", "inputs": {"text": NEG, "clip": ["1", 1]}},
        "4": {"class_type": "FluxGuidance", "inputs": {"guidance": 3.0, "conditioning": ["2", 0]}},
        "9": {"class_type": "LoadImage", "inputs": {"image": image_name}},
        "10": {"class_type": "ImageScale", "inputs": {
            "upscale_method": "lanczos", "width": size, "height": size,
            "crop": "disabled", "image": ["9", 0]}},
        "11": {"class_type": "VAEEncode", "inputs": {"pixels": ["10", 0], "vae": ["1", 2]}},
        "6": {"class_type": "KSampler", "inputs": {
            "seed": seed, "steps": steps, "cfg": 1.0,
            "sampler_name": "euler", "scheduler": "simple", "denoise": denoise,
            "model": ["1", 0], "positive": ["4", 0],
            "negative": ["3", 0], "latent_image": ["11", 0]}},
        "7": {"class_type": "VAEDecode", "inputs": {"samples": ["6", 0], "vae": ["1", 2]}},
        "8": {"class_type": "SaveImage", "inputs": {"filename_prefix": "upscale", "images": ["7", 0]}},
    }


def run(g: dict, timeout: int = 600):
    req = urllib.request.Request(
        f"{HOST}/prompt", data=json.dumps({"prompt": g}).encode(),
        headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        pid = json.loads(r.read())["prompt_id"]
    deadline = time.time() + timeout
    while time.time() < deadline:
        with urllib.request.urlopen(f"{HOST}/history/{pid}", timeout=30) as r:
            hist = json.loads(r.read())
        e = hist.get(pid)
        if e:
            if e.get("status", {}).get("status_str") == "error":
                raise RuntimeError(json.dumps(e["status"])[:600])
            for node in e.get("outputs", {}).values():
                for img in node.get("images", []):
                    q = urllib.parse.urlencode({
                        "filename": img["filename"],
                        "subfolder": img.get("subfolder", ""), "type": img["type"]})
                    with urllib.request.urlopen(f"{HOST}/view?{q}", timeout=120) as ir:
                        return Image.open(BytesIO(ir.read())).convert("RGB")
        time.sleep(2)
    raise TimeoutError(f"exceeded {timeout}s")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("source")
    ap.add_argument("--out", default="/tmp/upscaled")
    ap.add_argument("--prompt", default=(
        "A crisp high-resolution illustration, clean confident linework, smooth "
        "flat shading, sharp edges, centred, app icon artwork"))
    ap.add_argument("--denoise", default="0.3,0.45,0.6",
                    help="comma-separated sweep; low preserves, high redraws")
    ap.add_argument("--size", type=int, default=1024)
    ap.add_argument("--steps", type=int, default=24)
    ap.add_argument("--seed", type=int, default=5150)
    args = ap.parse_args()

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    name = upload(Path(args.source))
    print("uploaded as", name, flush=True)

    for d in [float(x) for x in args.denoise.split(",")]:
        t0 = time.time()
        img = run(graph(name, args.prompt, d, args.seed, args.size, args.steps))
        p = out / f"up_d{d:.2f}.png"
        img.save(p)
        print(f"{p}  {time.time()-t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()
