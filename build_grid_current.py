"""Render the CURRENT state of the IG grid.

Layout principle: no two pudding photos are edge-adjacent.
- Pudding photos at corners + center (positions 1, 3, 5, 7, 9)
- Non-pudding tiles (graphics + lifestyle) at edges (positions 2, 4, 6, 8)

Grid (3x3, top-left -> bottom-right):
  1: Macro (pudding, cream)        2: Logo poster (graphic)         3: Cup stack (pudding, BROWN)
  4: Peel + W11 (graphic)          5: Hand-held hero (pudding, cream) 6: Deliveroo (graphic)
  7: Process (pudding, BROWN)      8: Notting Hill (lifestyle, cream) 9: Spoon lift (pudding, BROWN)
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
    """Fixed: text fully at top, banana fully at bottom, no overlap."""
    img = Image.new("RGB", (TILE, TILE), CREAM)
    d = ImageDraw.Draw(img)
    f1 = font(68)
    f2 = font(48)
    # Text block — all in upper half
    text_block = [
        ("Fresh stock", f1, 70),
        ("Mon-Fri", f1, 150),
        ("on Deliveroo", f2, 240),
    ]
    for txt, fnt, y in text_block:
        bbox = d.textbbox((0, 0), txt, font=fnt)
        d.text(((TILE - (bbox[2] - bbox[0])) // 2, y), txt, fill=BROWN, font=fnt)
    # Banana — bottom half, smaller, clear separation
    sleep = Image.open(B / "Little Bananas/Banana_1.png").convert("RGBA")
    target_w = int(TILE * 0.34)
    ratio = target_w / sleep.width
    sleep = sleep.resize((target_w, int(sleep.height * ratio)), Image.LANCZOS)
    img.paste(sleep, ((TILE - sleep.width) // 2, TILE - sleep.height - 60), sleep)
    return img

# Photos and illustrated tiles
def use_real_or_placeholder(filename, fallback):
    p = POSTS / filename
    return real(p) if p.exists() else fallback

macro = use_real_or_placeholder("tile_03_macro.png", placeholder(CREAM, ["Macro", "(pending)"]))
hand_held = use_real_or_placeholder("tile_01_handheld_hero.png", placeholder(CREAM, ["Hand-held", "(pending)"]))
process = use_real_or_placeholder("tile_07_process.png", placeholder(BROWN, ["Process", "(pending)"], accent=CREAM))
cup_stack = use_real_or_placeholder("tile_03_cup_stack.png", placeholder(BROWN, ["Cup stack", "(pending)"], accent=CREAM))
notting_hill = use_real_or_placeholder("tile_08_notting_hill.png", placeholder(CREAM, ["Notting Hill", "(pending)"]))

# Grid order matches positions 1-9 (top-left to bottom-right)
grid_positions = [
    macro,                                                                        # 1: pudding cream
    build_logo_tile(),                                                            # 2: graphic
    cup_stack,                                                                    # 3: pudding brown (lid illustration)
    build_peel_w11_tile(),                                                        # 4: graphic
    hand_held,                                                                    # 5: pudding cream (center anchor)
    build_deliveroo_tile(),                                                       # 6: graphic
    process,                                                                      # 7: pudding brown
    notting_hill,                                                                 # 8: lifestyle illustration
    placeholder(BROWN, ["Spoon lift", "(pending)"], accent=CREAM),                # 9: pudding brown placeholder (kept as is)
]

grid = Image.new("RGB", (GRID, GRID), "white")
for i, t in enumerate(grid_positions):
    r, c = divmod(i, 3)
    grid.paste(t, (c * (TILE + GAP), r * (TILE + GAP)))

grid.save(OUT, quality=92)
grid.save(OUT2, quality=92)
print(f"Saved {OUT}")
