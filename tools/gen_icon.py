#!/usr/bin/env python3
"""Generate app-icon candidates for the game on the ComfyUI box.

    python3 tools/gen_icon.py --out /tmp/icons --seeds 2

ComfyUI lives on the LAN, so the OneCLI proxy has to be out of the way:
the script strips the proxy variables from its own environment at import.
"""

from __future__ import annotations

import argparse
import json
import os
import time
import urllib.parse
import urllib.request
from io import BytesIO
from pathlib import Path

for _v in ("http_proxy", "https_proxy", "HTTP_PROXY", "HTTPS_PROXY", "all_proxy", "ALL_PROXY"):
    os.environ.pop(_v, None)

from PIL import Image  # noqa: E402  (must follow the proxy strip)

HOST = "http://bazzite:8188"
CKPT = "flux1-dev-fp8.safetensors"

PALETTE = (
    "Colours restricted to near-black #0a0c0f, luminous cyan #49c5dd and "
    "ember amber #f0a73d. High contrast, no other hues."
)

CONCEPTS = {
    "wafer": (
        "A single polished silicon wafer shot perfectly straight on, centred on a "
        "near-black background. The wafer is a dark disc tiled with a fine grid of "
        "rectangular chip dies that glow faint cyan. A jagged fracture splits it from "
        "the centre outward and the silicon along the crack is scorched amber, the "
        "glow falling off into the dark. Studio lighting, generous empty margin. " + PALETTE
    ),
    "skull": (
        "A silicon wafer seen top-down on a black background, its grid of chip dies "
        "lit cyan — except the dead unlit dies in the middle, which form the clear "
        "silhouette of a skull. Graphic, symmetrical, centred, lots of dark margin. " + PALETTE
    ),
    "fab": (
        "A tiny isometric semiconductor fabrication plant rendered as a glowing model "
        "floating on pitch black, clean geometric cyan-lit buildings and cooling "
        "towers, one wing of the plant burning with amber flame and a thin ribbon of "
        "smoke. Viewed from above at 45 degrees, centred, wide dark margins, minimal "
        "game-icon art. " + PALETTE
    ),
    "die": (
        "Extreme close-up of a microchip die, top-down, filling a dark frame. "
        "Intricate circuitry drawn as thin luminous cyan lines on black silicon. One "
        "quadrant is burnt out: its traces dead, charred amber and cracked. "
        "Symmetrical, centred, cinematic, high contrast. " + PALETTE
    ),
}

NEG = "text, letters, words, watermark, signature, logo type, caption, frame, border"


def flux_graph(prompt: str, seed: int, size: int = 1024, steps: int = 24, guidance: float = 3.2):
    # Flux-dev is guidance-distilled: cfg stays at 1.0 and FluxGuidance carries
    # the prompt strength. Raising cfg here only burns the image.
    return {
        "1": {"class_type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": CKPT}},
        "2": {"class_type": "CLIPTextEncode", "inputs": {"text": prompt, "clip": ["1", 1]}},
        "3": {"class_type": "CLIPTextEncode", "inputs": {"text": NEG, "clip": ["1", 1]}},
        "4": {"class_type": "FluxGuidance", "inputs": {"guidance": guidance, "conditioning": ["2", 0]}},
        "5": {"class_type": "EmptySD3LatentImage", "inputs": {"width": size, "height": size, "batch_size": 1}},
        "6": {
            "class_type": "KSampler",
            "inputs": {
                "seed": seed, "steps": steps, "cfg": 1.0,
                "sampler_name": "euler", "scheduler": "simple", "denoise": 1.0,
                "model": ["1", 0], "positive": ["4", 0],
                "negative": ["3", 0], "latent_image": ["5", 0],
            },
        },
        "7": {"class_type": "VAEDecode", "inputs": {"samples": ["6", 0], "vae": ["1", 2]}},
        "8": {"class_type": "SaveImage", "inputs": {"filename_prefix": "semitycoon", "images": ["7", 0]}},
    }


def run(graph: dict, timeout: int = 600) -> list[Image.Image]:
    req = urllib.request.Request(
        f"{HOST}/prompt",
        data=json.dumps({"prompt": graph}).encode(),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        prompt_id = json.loads(r.read())["prompt_id"]

    deadline = time.time() + timeout
    while time.time() < deadline:
        with urllib.request.urlopen(f"{HOST}/history/{prompt_id}", timeout=30) as r:
            hist = json.loads(r.read())
        entry = hist.get(prompt_id)
        if entry:
            if entry.get("status", {}).get("status_str") == "error":
                raise RuntimeError(json.dumps(entry["status"])[:600])
            out = []
            for node in entry.get("outputs", {}).values():
                for img in node.get("images", []):
                    q = urllib.parse.urlencode({
                        "filename": img["filename"],
                        "subfolder": img.get("subfolder", ""),
                        "type": img["type"],
                    })
                    with urllib.request.urlopen(f"{HOST}/view?{q}", timeout=120) as ir:
                        out.append(Image.open(BytesIO(ir.read())).convert("RGB"))
            if out:
                return out
        time.sleep(2)
    raise TimeoutError(f"generation exceeded {timeout}s")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="/tmp/icons")
    ap.add_argument("--seeds", type=int, default=2)
    ap.add_argument("--concepts", default=",".join(CONCEPTS))
    ap.add_argument("--base-seed", type=int, default=7000)
    args = ap.parse_args()

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    for name in args.concepts.split(","):
        for k in range(args.seeds):
            seed = args.base_seed + k
            t0 = time.time()
            img = run(flux_graph(CONCEPTS[name], seed))[0]
            path = out / f"{name}_{seed}.png"
            img.save(path)
            print(f"{path}  {time.time() - t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()
