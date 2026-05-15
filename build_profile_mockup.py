"""Full Instagram profile mockup for @bigbabypudding using new branding."""
from PIL import Image, ImageDraw, ImageFont, ImageOps
from pathlib import Path

ROOT = Path(__file__).parent
B = ROOT / "branding"
GRID_PNG = ROOT / "grid_mockup.png"
OUT = ROOT / "profile_mockup.png"

CREAM = "#fffae2"
BROWN = "#39251c"
# LOCKED two-color palette: cream + brown only. Yellow + blue + tan + pink not used as backgrounds.
WHITE = "#ffffff"
LIGHT_GREY = "#dbdbdb"
GREY_TEXT = "#737373"
LINK_BLUE = "#0095f6"
ICON_GREY = "#262626"

W = 1170
PAD = 40

def font(size, kind="regular"):
    paths = {
        "regular": "/System/Library/Fonts/Helvetica.ttc",
        "bold": "/System/Library/Fonts/Helvetica.ttc",
        "italic": "/System/Library/Fonts/Helvetica.ttc",
        "script": "/Library/Fonts/Arial.ttf",
    }
    candidates = ["/System/Library/Fonts/Helvetica.ttc",
                  "/System/Library/Fonts/Supplemental/Arial.ttf",
                  "/Library/Fonts/Arial.ttf"]
    for p in candidates:
        try:
            return ImageFont.truetype(p, size)
        except Exception:
            continue
    return ImageFont.load_default()

def circle_crop(im, size):
    im = im.convert("RGBA")
    im = ImageOps.fit(im, (size, size), Image.LANCZOS)
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, size, size), fill=255)
    out = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    out.paste(im, (0, 0), mask)
    return out

def draw_text(d, xy, text, fnt, fill=ICON_GREY, anchor="lt"):
    d.text(xy, text, font=fnt, fill=fill, anchor=anchor)

# ---- Top nav bar (Instagram-style) ----
NAV_H = 120
nav = Image.new("RGB", (W, NAV_H), WHITE)
d = ImageDraw.Draw(nav)
f_logo = font(54)
d.text((PAD, 28), "Instagram", font=f_logo, fill=ICON_GREY)
f_link = font(28)
d.text((W - PAD - 100, 50), "Log In", font=f_link, fill=ICON_GREY, anchor="lt")
# divider line
d.line([(0, NAV_H - 2), (W, NAV_H - 2)], fill=LIGHT_GREY, width=2)

# ---- Profile pic with gradient ring ----
PP_SIZE = 280
RING = 12
# Build profile pic from sleepy character on cream circle
pp_bg = Image.new("RGBA", (PP_SIZE, PP_SIZE), CREAM)
char = Image.open(B / "Character/Character.png").convert("RGBA")
ratio = (PP_SIZE * 0.78) / max(char.size)
char = char.resize((int(char.width * ratio), int(char.height * ratio)), Image.LANCZOS)
pp_bg.paste(char, ((PP_SIZE - char.width) // 2, (PP_SIZE - char.height) // 2 + 10), char)
pp = circle_crop(pp_bg, PP_SIZE)

# ---- Profile info column ----
PROFILE_H = 360
profile = Image.new("RGB", (W, PROFILE_H), WHITE)
d = ImageDraw.Draw(profile)

# Profile pic placement
pp_x = PAD + 30
pp_y = (PROFILE_H - PP_SIZE) // 2
profile.paste(pp, (pp_x, pp_y), pp)

# Username row
info_x = pp_x + PP_SIZE + 70
f_user = font(40)
d.text((info_x, 60), "bigbabypudding", font=f_user, fill=ICON_GREY)

# Stats row
f_stat_n = font(28)
f_stat_l = font(28)
stats_y = 135
stats = [("7", "posts"), ("208", "followers"), ("120", "following")]
sx = info_x
for n, lbl in stats:
    d.text((sx, stats_y), n, font=f_stat_n, fill=ICON_GREY)
    nw = d.textbbox((0, 0), n, font=f_stat_n)[2]
    d.text((sx + nw + 10, stats_y), lbl, font=f_stat_l, fill=ICON_GREY)
    lw = d.textbbox((0, 0), lbl, font=f_stat_l)[2]
    sx += nw + lw + 50

# Bio block
bio_y = 200
f_cat = font(24)
d.text((info_x, bio_y), "Dessert Shop", font=f_cat, fill=GREY_TEXT)
f_bio = font(26)
bio_lines = [
    "🍌  NYC-style banana pudding",
    "📍  Notting Hill, W11",
    "💛  Fresh batches Mon–Fri on Deliveroo",
]
for i, line in enumerate(bio_lines):
    d.text((info_x, bio_y + 40 + i * 38), line, font=f_bio, fill=ICON_GREY)

# ---- Highlights row ----
HL_H = 240
highlights = Image.new("RGB", (W, HL_H), WHITE)
d = ImageDraw.Draw(highlights)
HL_SIZE = 140
HL_LABELS = ["Menu", "About", "Reviews", "Delivery", "Press", "OG"]
peel = Image.open(B / "Little Bananas/Banana_3.png").convert("RGBA")
sleep = Image.open(B / "Little Bananas/Banana_1.png").convert("RGBA")
walk = Image.open(B / "Little Bananas/Banana_2.png").convert("RGBA")
char_small = Image.open(B / "Character/Character.png").convert("RGBA")
HL_ASSETS = [peel, sleep, walk, peel, char_small, sleep]

start_x = PAD + 30
gap = 50
for i, (lbl, asset) in enumerate(zip(HL_LABELS, HL_ASSETS)):
    # build a cream circle with the asset centered
    disc = Image.new("RGBA", (HL_SIZE, HL_SIZE), CREAM)
    a = asset.copy()
    r = (HL_SIZE * 0.62) / max(a.size)
    a = a.resize((int(a.width * r), int(a.height * r)), Image.LANCZOS)
    disc.paste(a, ((HL_SIZE - a.width) // 2, (HL_SIZE - a.height) // 2), a)
    disc_circ = circle_crop(disc, HL_SIZE)
    # outer ring
    ring = Image.new("RGBA", (HL_SIZE + 16, HL_SIZE + 16), (0, 0, 0, 0))
    ImageDraw.Draw(ring).ellipse((0, 0, HL_SIZE + 16, HL_SIZE + 16), outline=LIGHT_GREY, width=4)
    x = start_x + i * (HL_SIZE + gap)
    highlights.paste(ring, (x - 8, 30), ring)
    highlights.paste(disc_circ, (x, 38), disc_circ)
    # label
    f_lbl = font(22)
    bbox = d.textbbox((0, 0), lbl, font=f_lbl)
    d.text((x + (HL_SIZE - (bbox[2] - bbox[0])) // 2, HL_SIZE + 60), lbl, font=f_lbl, fill=ICON_GREY)

# ---- Tab row ----
TAB_H = 80
tab = Image.new("RGB", (W, TAB_H), WHITE)
d = ImageDraw.Draw(tab)
d.line([(0, 0), (W, 0)], fill=LIGHT_GREY, width=2)
# grid icon (active)
cx1 = W // 2 - 200
icon_y = 30
for r in range(3):
    for c in range(3):
        d.rectangle([cx1 + c * 10, icon_y + r * 10, cx1 + c * 10 + 7, icon_y + r * 10 + 7],
                    fill=ICON_GREY)
# underline for active
d.line([(cx1 - 30, TAB_H - 4), (cx1 + 60, TAB_H - 4)], fill=ICON_GREY, width=4)

# ---- Grid (reuse the existing grid_mockup.png) ----
grid = Image.open(GRID_PNG).convert("RGB")
# resize to width W (full bleed)
gw, gh = grid.size
new_h = int(gh * (W / gw))
grid = grid.resize((W, new_h), Image.LANCZOS)

# ---- Compose full page ----
TOTAL_H = NAV_H + PROFILE_H + HL_H + TAB_H + new_h
page = Image.new("RGB", (W, TOTAL_H), WHITE)
y = 0
page.paste(nav, (0, y)); y += NAV_H
page.paste(profile, (0, y)); y += PROFILE_H
page.paste(highlights, (0, y)); y += HL_H
page.paste(tab, (0, y)); y += TAB_H
page.paste(grid, (0, y))

page.save(OUT, quality=92)
print(f"Saved {OUT} {page.size}")
