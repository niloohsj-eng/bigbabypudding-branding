"""Render the CURRENT state of the IG grid using real posts where available,
placeholders for the still-to-shoot tiles.

Output: grid_current.png (saved both at repo root and posts/preview/grid_current.png)
"""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

ROOT = Path(__file__).parent
B = ROOT / "branding"
FONTS = ROOT / "fonts"
POSTS = ROOT / "posts"
PREVIEW_DIR = POSTS / "preview"
PREVIEW_DIR.mkdir(exist_ok=True)

OUT = ROOT / "grid_current.png"
OUT2 = PREVIEW_DIR / "grid_current.png"

CREAM = "#fffae2"
BROWN = "#39251c"

BRADLEY = next((str(p) for p in [
    FONTS / "Bradley Hand Bold.ttf",
    Path("/System/Library/Fonts/Supplemental/Bradley Hand Bold.ttf"),
] if p.exists()), None)

def font(size):
    return ImageFont.truetype(BRADLEY, size)

TILE = 720
GAP = 6
GRID = TILE * 3 + GAP * 2

def fit_to_tile(img):
    """Resize and center-crop to TILE x TILE."""
    img = img.convert("RGB")
    w, h = img.size
    side = min(w, h)
    img = img.crop(((w - side) // 2, (h - side) // 2, (w + side) // 2, (h + side) // 2))
    return img.resize((TILE, TILE), Image.LANCZOS)

def tile_solid(color, asset=None, asset_scale=0.7):
    img = Image.new("RGB", (TILE, TILE), color)
    if asset:
        a = Image.open(B / asset).convert("RGBA")
        target_w = int(TILE * asset_scale)
        ratio = target_w / a.width
        a = a.resize((target_w, int(a.height * ratio)), Image.LANCZOS)
        img.paste(a, ((TILE - a.width) // 2, (TILE - a.height) // 2), a)
    return img

def placeholder(bg, lines, accent=BROWN):
    img = Image.new("RGB", (TILE, TILE), bg)
    d = ImageDraw.Draw(img)
    d.rectangle([30, 30, TILE - 30, TILE - 30], outline=accent, width=4)
    f_big = font(54)
    f_sm = font(30)
    y = TILE // 2 - (len(lines) * 40)
    for i, line in enumerate(lines):
        f = f_big if i == 0 else f_sm
        bbox = d.textbbox((0, 0), line, font=f)
        x = (TILE - (bbox[2] - bbox[0])) // 2
        d.text((x, y), line, fill=accent, font=f)
        y += 70 if i == 0 else 42
    return img

# ---- Tile builders ----

def real(path):
    return fit_to_tile(Image.open(path))

# Tile 1 — real photo
t1_path = POSTS / "tile_01_handheld_hero.png"
t1 = real(t1_path) if t1_path.exists() else placeholder(BROWN, ["TILE 1", "Hand-held hero", "(pending)"], accent=CREAM)

# Tile 2 — logo on cream
t2 = tile_solid(CREAM, asset="Logo/Logo_w_Character.png", asset_scale=0.78)

# Tile 3 — real photo
t3_path = POSTS / "tile_03_macro.png"
t3 = real(t3_path) if t3_path.exists() else placeholder(CREAM, ["TILE 3", "Macro pudding", "(pending)"])

# Tile 4 — placeholder (waiting for new cups)
t4 = placeholder(BROWN, ["TILE 4", "Cup stack", "(waiting for", "new cups)"], accent=CREAM)

# Tile 5 — dancing peel + W11
t5 = Image.new("RGB", (TILE, TILE), CREAM)
peel = Image.open(B / "Little Bananas/Banana_3.png").convert("RGBA")
ratio = (TILE * 0.55) / peel.width
peel = peel.resize((int(peel.width * ratio), int(peel.height * ratio)), Image.LANCZOS)
t5.paste(peel, ((TILE - peel.width) // 2, 90), peel)
d = ImageDraw.Draw(t5)
f = font(64)
text = "Made fresh in W11."
bbox = d.textbbox((0, 0), text, font=f)
d.text(((TILE - (bbox[2] - bbox[0])) // 2, TILE - 160), text, fill=BROWN, font=f)

# Tile 6 — placeholder
t6 = placeholder(BROWN, ["TILE 6", "Notting Hill", "street", "(pending)"], accent=CREAM)

# Tile 7 — real photo
t7_path = POSTS / "tile_07_process.png"
t7 = real(t7_path) if t7_path.exists() else placeholder(CREAM, ["TILE 7", "Process shot", "(pending)"])

# Tile 8 — Deliveroo reel
t8 = Image.new("RGB", (TILE, TILE), CREAM)
sleep = Image.open(B / "Little Bananas/Banana_1.png").convert("RGBA")
ratio = (TILE * 0.42) / sleep.width
sleep = sleep.resize((int(sleep.width * ratio), int(sleep.height * ratio)), Image.LANCZOS)
t8.paste(sleep, ((TILE - sleep.width) // 2, TILE - sleep.height - 90), sleep)
d = ImageDraw.Draw(t8)
f1 = font(78)
f2 = font(52)
for txt, fnt, y in [("Fresh stock", f1, 120), ("Mon-Fri", f1, 210), ("on Deliveroo", f2, 320)]:
    bbox = d.textbbox((0, 0), txt, font=fnt)
    d.text(((TILE - (bbox[2] - bbox[0])) // 2, y), txt, fill=BROWN, font=fnt)

# Tile 9 — placeholder
t9 = placeholder(CREAM, ["TILE 9", "Spoon lift", "(pending)"])

# ---- Compose 3x3 ----
grid = Image.new("RGB", (GRID, GRID), "white")
tiles = [t1, t2, t3, t4, t5, t6, t7, t8, t9]
for i, t in enumerate(tiles):
    r, c = divmod(i, 3)
    grid.paste(t, (c * (TILE + GAP), r * (TILE + GAP)))

grid.save(OUT, quality=92)
grid.save(OUT2, quality=92)
print(f"Saved {OUT}")
print(f"Saved {OUT2}")
