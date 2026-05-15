"""3x3 Instagram grid mockup for @bigbabypudding using new branding assets."""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

ROOT = Path(__file__).parent
B = ROOT / "branding"
FONTS = ROOT / "fonts"
OUT = ROOT / "grid_mockup.png"

CREAM = "#fffae2"
BROWN = "#39251c"
# LOCKED two-color palette: cream + brown only. Yellow + blue + tan + pink not used as backgrounds.

TILE = 720
GAP = 6
GRID = TILE * 3 + GAP * 2

BRADLEY_PATHS = [
    FONTS / "Bradley Hand Bold.ttf",
    Path("/System/Library/Fonts/Supplemental/Bradley Hand Bold.ttf"),
]
BRADLEY = next((str(p) for p in BRADLEY_PATHS if p.exists()), None)
if BRADLEY is None:
    raise SystemExit("Bradley Hand Bold not found. Expected at fonts/Bradley Hand Bold.ttf")

def font(size, weight="Regular"):
    return ImageFont.truetype(BRADLEY, size)

def tile_solid(color, label, sub=None, asset=None, asset_scale=0.7, asset_offset=(0,0)):
    img = Image.new("RGB", (TILE, TILE), color)
    if asset:
        a = Image.open(B / asset).convert("RGBA")
        target_w = int(TILE * asset_scale)
        ratio = target_w / a.width
        a = a.resize((target_w, int(a.height * ratio)), Image.LANCZOS)
        x = (TILE - a.width) // 2 + asset_offset[0]
        y = (TILE - a.height) // 2 + asset_offset[1]
        img.paste(a, (x, y), a)
    d = ImageDraw.Draw(img)
    f = font(40)
    bbox = d.textbbox((0, 0), label, font=f)
    d.text(((TILE - (bbox[2] - bbox[0])) // 2, TILE - 90), label, fill=BROWN, font=f)
    if sub:
        fs = font(26)
        bbox2 = d.textbbox((0, 0), sub, font=fs)
        d.text(((TILE - (bbox2[2] - bbox2[0])) // 2, TILE - 50), sub, fill=BROWN, font=fs)
    return img

def tile_placeholder(bg, label_lines, accent=BROWN):
    img = Image.new("RGB", (TILE, TILE), bg)
    d = ImageDraw.Draw(img)
    margin = 30
    d.rectangle([margin, margin, TILE - margin, TILE - margin], outline=accent, width=4)
    f_big = font(54)
    f_sm = font(30)
    y = TILE // 2 - (len(label_lines) * 40)
    for i, line in enumerate(label_lines):
        f = f_big if i == 0 else f_sm
        bbox = d.textbbox((0, 0), line, font=f)
        x = (TILE - (bbox[2] - bbox[0])) // 2
        d.text((x, y), line, fill=accent, font=f)
        y += 70 if i == 0 else 42
    return img

# Tile 1: Hand-held hero (placeholder — needs real photo)
t1 = tile_placeholder(BROWN, ["TILE 1", "Hand holding cup", "wrap visible", "soft daylight"], accent=CREAM)

# Tile 2: Logo on cream (full brand poster)
t2 = tile_solid(CREAM, "", asset="Logo/Logo_w_Character.png", asset_scale=0.78)

# Tile 3: Macro pudding texture (placeholder)
t3 = tile_placeholder(CREAM, ["TILE 3", "Macro close-up", "of pudding layers", "no text, no logo"])

# Tile 4: Cup stack hero (placeholder)
t4 = tile_placeholder(BROWN, ["TILE 4", "Cup stack", "showing wrap +", "lid design"], accent=CREAM)

# Tile 5: Dancing peel on cream with line
t5_bg = Image.new("RGB", (TILE, TILE), CREAM)
peel = Image.open(B / "Little Bananas/Banana_3.png").convert("RGBA")
ratio = (TILE * 0.55) / peel.width
peel = peel.resize((int(peel.width * ratio), int(peel.height * ratio)), Image.LANCZOS)
t5_bg.paste(peel, ((TILE - peel.width) // 2, 90), peel)
d = ImageDraw.Draw(t5_bg)
f = font(64)
text = "Made fresh in W11."
bbox = d.textbbox((0, 0), text, font=f)
d.text(((TILE - (bbox[2] - bbox[0])) // 2, TILE - 160), text, fill=BROWN, font=f)
t5 = t5_bg

# Tile 6: Notting Hill street lifestyle (placeholder)
t6 = tile_placeholder(BROWN, ["TILE 6", "Notting Hill", "pastel street +", "cup in hand"], accent=CREAM)

# Tile 7: Process / overhead pudding being made (placeholder)
t7 = tile_placeholder(CREAM, ["TILE 7", "Process shot:", "banana slices,", "wafer layers"])

# Tile 8: Reel cover — "ON DELIVEROO" announcement on cream
t8_bg = Image.new("RGB", (TILE, TILE), CREAM)
sleep = Image.open(B / "Little Bananas/Banana_1.png").convert("RGBA")
ratio = (TILE * 0.42) / sleep.width
sleep = sleep.resize((int(sleep.width * ratio), int(sleep.height * ratio)), Image.LANCZOS)
t8_bg.paste(sleep, ((TILE - sleep.width) // 2, TILE - sleep.height - 90), sleep)
d = ImageDraw.Draw(t8_bg)
f1 = font(78)
f2 = font(52)
for txt, fnt, y in [("Fresh stock", f1, 120), ("Mon–Fri", f1, 210), ("on Deliveroo", f2, 320)]:
    bbox = d.textbbox((0, 0), txt, font=fnt)
    d.text(((TILE - (bbox[2] - bbox[0])) // 2, y), txt, fill=BROWN, font=fnt)
t8 = t8_bg

# Tile 9: Spoon/bite (placeholder)
t9 = tile_placeholder(CREAM, ["TILE 9", "Spoon lift,", "single bite,", "no text"])

# Compose 3x3
grid = Image.new("RGB", (GRID, GRID), "white")
tiles = [t1, t2, t3, t4, t5, t6, t7, t8, t9]
for i, t in enumerate(tiles):
    r, c = divmod(i, 3)
    grid.paste(t, (c * (TILE + GAP), r * (TILE + GAP)))

grid.save(OUT, quality=92)
print(f"Saved {OUT} ({grid.size})")
