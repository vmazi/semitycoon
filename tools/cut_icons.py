#!/usr/bin/env python3
"""Cut one source image into the PWA icon set and the social card.

    python3 tools/cut_icons.py /tmp/icons/wafer_7000.png

Writes into site/icons/. Two shapes are produced from the same art:

  icon-<n>.png      the plain icon, art filling the frame
  maskable-<n>.png  the art inset to 60% so Android can crop it to any
                    shape without biting into the subject
  og.png            1200x630 social card, art on the left, title on the right
"""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

BG = (10, 12, 15)
CYAN = (73, 197, 221)
MUT = (109, 125, 140)
SIZES = (64, 128, 180, 192, 256, 384, 512)
ROOT = Path(__file__).resolve().parent.parent


def square(img: Image.Image) -> Image.Image:
    s = min(img.size)
    l, t = (img.width - s) // 2, (img.height - s) // 2
    return img.crop((l, t, l + s, t + s))


FONTS = (
    "/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
    "/usr/share/fonts/liberation/LiberationMono-Bold.ttf",
)


def font(size: int) -> ImageFont.FreeTypeFont:
    for p in FONTS:
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    # Falling back to load_default() would silently render the card in a tiny
    # bitmap face, which looks broken rather than obviously missing.
    raise SystemExit(f"no usable font; looked for {FONTS}")


def social_card(art: Image.Image, out: Path) -> None:
    W, H = 1200, 630
    card = Image.new("RGB", (W, H), BG)

    # Art bleeds off the left edge and fades into the background, so the panel
    # seam never reads as a hard rectangle against the dark card.
    a = square(art).resize((H, H), Image.LANCZOS)
    card.paste(a, (0, 0))
    fade = Image.new("L", (H, H), 255)
    fd = ImageDraw.Draw(fade)
    for x in range(140):
        fd.line([(H - 140 + x, 0), (H - 140 + x, H)], fill=int(255 * (1 - x / 140)))
    card.paste(Image.new("RGB", (H, H), BG), (0, 0), Image.eval(fade, lambda v: 255 - v))

    d = ImageDraw.Draw(card)
    x = 690
    d.text((x, 150), "KILL YOUR OWN", font=font(46), fill=(199, 210, 220))
    d.text((x, 206), "SEMICONDUCTOR", font=font(46), fill=(199, 210, 220))
    d.text((x, 262), "COMPANY", font=font(46), fill=(199, 210, 220))
    d.text((x, 318), "SIMULATOR", font=font(46), fill=CYAN)
    d.line([(x, 396), (x + 400, 396)], fill=(35, 43, 52), width=2)
    d.text((x, 420), "Forty years. Five eras.", font=font(21), fill=MUT)
    d.text((x, 452), "Most people kill the company.", font=font(21), fill=MUT)
    d.text((x, 520), "semitycoon.borgorg.org", font=font(19), fill=(240, 167, 61))
    card.save(out, optimize=True)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("source")
    ap.add_argument("--out", default=str(ROOT / "site" / "icons"))
    args = ap.parse_args()

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    art = square(Image.open(args.source).convert("RGB"))

    for n in SIZES:
        art.resize((n, n), Image.LANCZOS).save(out / f"icon-{n}.png", optimize=True)

        # Android's maskable crop can take up to 20% off each edge, so the art
        # only gets the middle 60% and the rest is the page background.
        m = Image.new("RGB", (n, n), BG)
        inner = int(n * 0.6)
        m.paste(art.resize((inner, inner), Image.LANCZOS), ((n - inner) // 2,) * 2)
        m.save(out / f"maskable-{n}.png", optimize=True)

    art.resize((32, 32), Image.LANCZOS).save(out / "favicon.png", optimize=True)
    art.resize((64, 64), Image.LANCZOS).save(
        out / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
    social_card(art, out / "og.png")
    print(f"wrote {len(list(out.iterdir()))} files to {out}")


if __name__ == "__main__":
    main()
