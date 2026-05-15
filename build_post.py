"""Turn a raw phone photo into an Instagram-ready post on brand background.

Usage:
    python3 build_post.py photos_in/IMG_1234.jpg --bg cream
    python3 build_post.py photos_in/IMG_1234.jpg --bg brown --pad 0.85
    python3 build_post.py photos_in/IMG_1234.jpg --bg brown --no-cutout

What it does:
  1. Loads the input photo
  2. Auto-removes the background using rembg (unless --no-cutout)
  3. Centers the subject on a 1080x1080 brand-color canvas
  4. Saves to photos_out/<name>_<bg>.png

If the subject is already a transparent PNG (e.g. from iPhone "Copy Subject"
or Mac Preview Instant Alpha), pass --no-cutout to skip rembg.
"""
import argparse
from pathlib import Path
from PIL import Image, ImageOps

ROOT = Path(__file__).parent
IN_DIR = ROOT / "photos_in"
OUT_DIR = ROOT / "photos_out"
IN_DIR.mkdir(exist_ok=True)
OUT_DIR.mkdir(exist_ok=True)

# Locked palette
BACKGROUNDS = {
    "cream": "#fffae2",
    "brown": "#39251c",
}

CANVAS = 1080  # Instagram square

def cutout(img: Image.Image) -> Image.Image:
    """Remove background with rembg, returns RGBA with transparency."""
    from rembg import remove
    if img.mode != "RGBA":
        img = img.convert("RGBA")
    return remove(img)

def trim_transparent(img: Image.Image) -> Image.Image:
    """Crop to the non-transparent bounding box."""
    bbox = img.getbbox()
    return img.crop(bbox) if bbox else img

def compose(subject: Image.Image, bg_hex: str, pad: float) -> Image.Image:
    """Center subject on a CANVAS x CANVAS canvas with bg_hex background."""
    canvas = Image.new("RGB", (CANVAS, CANVAS), bg_hex)
    subject = trim_transparent(subject)
    # Scale subject to fit within pad * CANVAS in both dimensions
    max_side = int(CANVAS * pad)
    subject.thumbnail((max_side, max_side), Image.LANCZOS)
    x = (CANVAS - subject.width) // 2
    y = (CANVAS - subject.height) // 2
    if subject.mode == "RGBA":
        canvas.paste(subject, (x, y), subject)
    else:
        canvas.paste(subject, (x, y))
    return canvas

def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("input", help="Path to input photo")
    p.add_argument("--bg", choices=BACKGROUNDS.keys(), default="cream",
                   help="Background color (default: cream)")
    p.add_argument("--pad", type=float, default=0.82,
                   help="Subject fills this fraction of canvas (default: 0.82)")
    p.add_argument("--no-cutout", action="store_true",
                   help="Input is already a transparent PNG; skip rembg")
    p.add_argument("--out", help="Output path (default: photos_out/<name>_<bg>.png)")
    args = p.parse_args()

    in_path = Path(args.input)
    img = Image.open(in_path)

    if args.no_cutout:
        if img.mode != "RGBA":
            print("Warning: --no-cutout but image has no alpha channel; treating as opaque subject")
        subject = img
    else:
        print(f"Removing background from {in_path.name} ...")
        subject = cutout(img)

    bg_hex = BACKGROUNDS[args.bg]
    final = compose(subject, bg_hex, args.pad)

    out_path = Path(args.out) if args.out else OUT_DIR / f"{in_path.stem}_{args.bg}.png"
    final.save(out_path, quality=95)
    print(f"Saved {out_path} ({final.size})")

if __name__ == "__main__":
    main()
