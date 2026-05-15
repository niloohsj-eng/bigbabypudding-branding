"""Render the CURRENT state of the IG grid.

New layout: graphics distributed on the DIAGONAL (pos 1, 5, 9) so they appear in
every row and every column — never stacked in a single column.

Grid (3x3, top-left -> bottom-right):
  1: Logo poster (graphic)        2: Hand-held hero        3: Macro pudding
  4: Process shot                 5: Peel + W11 (graphic)  6: Cup stack (pending)
  7: Notting Hill (pending)       8: Spoon lift (pending)  9: Deliveroo (graphic)
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
    img = img.convert("RGB")
    w, h = img.size
    side = min(w, h)
    img = img.crop(((w - side) // 2, (h - side) // 2, (w + side) // 2, (h + side) // 2))
    return img.resize((TILE, TILE), Image.LANCZOS)

def real(path):
    return fit_to_tile(Image.open(path))

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

def build_logo_tile():
    img = Image.new("RGB", (TILE, TILE), CREAM)
    a = Image.open(B / "Logo/Logo_w_Character.png").convert("RGBA")
    target_w = int(TILE * 0.78)
    ratio = target_w / a.width
    a = a.resize((target_w, int(a.height * ratio)), Image.LANCZOS)
    img.paste(a, ((TILE - a.width) // 2, (TILE - a.height) // 2), a)
    return img

def build_peel_w11_tile():
    img = Image.new("RGB", (TILE, TILE), CREAM)
    peel = Image.open(B / "Little Bananas/Banana_3.png").convert("RGBA")
    ratio = (TILE * 0.55) / peel.width
    peel = peel.resize((int(peel.width * ratio), int(peel.height * ratio)), Image.LANCZOS)
    img.paste(peel, ((TILE - peel.width) // 2, 90), peel)
    d = ImageDraw.Draw(img)
    f = font(64)
    text = "Made fresh in W11."
    bbox = d.textbbox((0, 0), text, font=f)
    d.text(((TILE - (bbox[2] - bbox[0])) // 2, TILE - 160), text, fill=BROWN, font=f)
    return img

def build_deliveroo_tile():
    img = Image.new("RGB", (TILE, TILE), CREAM)
    sleep = Image.open(B / "Little Bananas/Banana_1.png").convert("RGBA")
    ratio = (TILE * 0.42) / sleep.width
    sleep = sleep.resize((int(sleep.width * ratio), int(sleep.height * ratio)), Image.LANCZOS)
    img.paste(sleep, ((TILE - sleep.width) // 2, TILE - sleep.height - 90), sleep)
    d = ImageDraw.Draw(img)
    f1 = font(78)
    f2 = font(52)
    for txt, fnt, y in [("Fresh stock", f1, 120), ("Mon-Fri", f1, 210), ("on Deliveroo", f2, 320)]:
        bbox = d.textbbox((0, 0), txt, font=fnt)
        d.text(((TILE - (bbox[2] - bbox[0])) // 2, y), txt, fill=BROWN, font=fnt)
    return img

# Real photos that already exist
hand_held = real(POSTS / "tile_01_handheld_hero.png") if (POSTS / "tile_01_handheld_hero.png").exists() else placeholder(CREAM, ["Hand-held", "hero", "(pending)"])
macro = real(POSTS / "tile_03_macro.png") if (POSTS / "tile_03_macro.png").exists() else placeholder(CREAM, ["Macro", "(pending)"])
process = real(POSTS / "tile_07_process.png") if (POSTS / "tile_07_process.png").exists() else placeholder(CREAM, ["Process", "(pending)"])

# New diagonal arrangement: graphics at 1, 5, 9
grid_positions = [
    build_logo_tile(),                                   # pos 1 — cream graphic
    hand_held,                                           # pos 2 — cream photo
    macro,                                               # pos 3 — cream photo
    process,                                             # pos 4 — BROWN photo (process on brown bg)
    build_peel_w11_tile(),                               # pos 5 — cream graphic
    placeholder(BROWN, ["Cup stack", "(waiting for", "new cups)"], accent=CREAM),  # pos 6 — BROWN
    placeholder(CREAM, ["Notting Hill", "street", "(pending)"]),     # pos 7 — cream
    placeholder(BROWN, ["Spoon lift", "(pending)"], accent=CREAM),   # pos 8 — BROWN
    build_deliveroo_tile(),                              # pos 9 — cream graphic
]

grid = Image.new("RGB", (GRID, GRID), "white")
for i, t in enumerate(grid_positions):
    r, c = divmod(i, 3)
    grid.paste(t, (c * (TILE + GAP), r * (TILE + GAP)))

grid.save(OUT, quality=92)
grid.save(OUT2, quality=92)
print(f"Saved {OUT}")
