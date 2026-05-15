"""Visual shoot brief for the 6 photos that need to be taken for the IG grid.

Produces a single shoot_brief.png that shows for each tile:
- A mock preview on the target brand background
- Composition + lighting + props + caveats

Uses only Bradley Hand Bold + brand palette so it feels native to the brand.
"""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

ROOT = Path(__file__).parent
B = ROOT / "branding"
FONTS = ROOT / "fonts"
OUT = ROOT / "shoot_brief.png"

CREAM = "#fffae2"
BROWN = "#39251c"
RULE = "#39251c"

BRADLEY = next((str(p) for p in [
    FONTS / "Bradley Hand Bold.ttf",
    Path("/System/Library/Fonts/Supplemental/Bradley Hand Bold.ttf"),
] if p.exists()), None)

def font(size):
    return ImageFont.truetype(BRADLEY, size)

# ---- Panel size ----
PREVIEW = 600       # square preview area
NOTES_H = 720       # height of notes area below
PANEL_W = PREVIEW
PANEL_H = PREVIEW + NOTES_H

COLS, ROWS = 3, 2
GAP = 60
HEADER_H = 220
FOOTER_H = 80
W = COLS * PANEL_W + (COLS + 1) * GAP
H = HEADER_H + ROWS * PANEL_H + (ROWS + 1) * GAP + FOOTER_H

# ---- Helpers ----
def wrap(d, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        test = (cur + " " + w).strip()
        if d.textbbox((0, 0), test, font=fnt)[2] <= max_w:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def draw_text_block(d, x, y, fnt, text, max_w, color=BROWN, line_gap=10):
    lines = wrap(d, text, fnt, max_w)
    for line in lines:
        d.text((x, y), line, font=fnt, fill=color)
        bbox = d.textbbox((0, 0), line, font=fnt)
        y += (bbox[3] - bbox[1]) + line_gap
    return y

# ---- Preview builders for each tile ----
def make_preview(tile_num, bg_color, helper):
    """Returns a PREVIEW x PREVIEW image showing the target visual concept."""
    img = Image.new("RGB", (PREVIEW, PREVIEW), bg_color)
    if helper:
        helper(img)
    return img

def helper_hand_cup(img):
    """Tile 1: hand holding cup. Show cup wrap floating mid-frame with hand indicator."""
    d = ImageDraw.Draw(img)
    wrap_img = Image.open(B / "Cup Design JPG For Viewing Only/Cup_Wrap.jpg").convert("RGB")
    # Rotate slightly + scale
    target_w = int(PREVIEW * 0.62)
    ratio = target_w / wrap_img.width
    wrap_img = wrap_img.resize((target_w, int(wrap_img.height * ratio)), Image.LANCZOS)
    wrap_img = wrap_img.rotate(-8, resample=Image.BICUBIC, expand=True, fillcolor=BROWN)
    x = (PREVIEW - wrap_img.width) // 2
    y = (PREVIEW - wrap_img.height) // 2 - 40
    img.paste(wrap_img, (x, y))
    # caption
    f = font(34)
    cap = "your hand here"
    bbox = d.textbbox((0, 0), cap, font=f)
    cx = (PREVIEW - (bbox[2] - bbox[0])) // 2
    d.text((cx, PREVIEW - 90), cap, font=f, fill=CREAM)
    # arrow
    d.line([(PREVIEW // 2 - 10, PREVIEW - 100), (PREVIEW // 2 - 10, PREVIEW - 160)],
           fill=CREAM, width=4)
    d.polygon([(PREVIEW // 2 - 30, PREVIEW - 160), (PREVIEW // 2 + 10, PREVIEW - 160),
               (PREVIEW // 2 - 10, PREVIEW - 190)], fill=CREAM)

def helper_macro(img):
    """Tile 3: macro pudding texture. Use a hand-drawn-y annotation."""
    d = ImageDraw.Draw(img)
    f = font(60)
    lines = ["pudding fills", "the frame.", "no logo. no text."]
    y = PREVIEW // 2 - 90
    for line in lines:
        bbox = d.textbbox((0, 0), line, font=f)
        x = (PREVIEW - (bbox[2] - bbox[0])) // 2
        d.text((x, y), line, font=f, fill=BROWN)
        y += 80
    # dashed border to suggest cropping in close
    for i in range(0, PREVIEW, 30):
        d.line([(i, 30), (min(i + 14, PREVIEW), 30)], fill=BROWN, width=3)
        d.line([(i, PREVIEW - 30), (min(i + 14, PREVIEW), PREVIEW - 30)], fill=BROWN, width=3)

def helper_stack(img):
    """Tile 4: cup stack hero. Three wrap images overlapping."""
    wrap_img = Image.open(B / "Cup Design JPG For Viewing Only/Cup_Wrap.jpg").convert("RGB")
    target_w = int(PREVIEW * 0.52)
    ratio = target_w / wrap_img.width
    wrap_img = wrap_img.resize((target_w, int(wrap_img.height * ratio)), Image.LANCZOS)
    positions = [(-30, 80, -12), (30, 50, 0), (90, 100, 8)]
    for x_off, y_off, rot in positions:
        r = wrap_img.rotate(rot, resample=Image.BICUBIC, expand=True, fillcolor=BROWN)
        x = (PREVIEW - r.width) // 2 + x_off
        y = (PREVIEW - r.height) // 2 + y_off
        img.paste(r, (x, y))

def helper_lifestyle(img):
    """Tile 6: Notting Hill street lifestyle. Simple pastel-row sketch."""
    d = ImageDraw.Draw(img)
    # row of houses silhouette
    base_y = PREVIEW - 220
    house_w = 90
    colors = ["#fce3c4", "#f3c6a5", "#e8dcb9", "#cce0d8", "#f5d4d4"]  # pastel sketch tones
    x = 30
    for i, c in enumerate(colors):
        h = 220 + (i % 3) * 30
        d.rectangle([x, base_y - h + 40, x + house_w, base_y + 40], fill=c, outline=BROWN, width=3)
        # window
        d.rectangle([x + 25, base_y - h + 80, x + 60, base_y - h + 130], outline=BROWN, width=2)
        x += house_w + 12
    # tag line
    f = font(38)
    msg = "pastel street + cup in frame"
    bbox = d.textbbox((0, 0), msg, font=f)
    d.text(((PREVIEW - (bbox[2] - bbox[0])) // 2, PREVIEW - 90), msg, font=f, fill=BROWN)

def helper_process(img):
    """Tile 7: overhead process shot."""
    d = ImageDraw.Draw(img)
    # overhead bowl
    cx, cy = PREVIEW // 2, PREVIEW // 2 - 30
    d.ellipse([cx - 180, cy - 180, cx + 180, cy + 180], outline=BROWN, width=4)
    d.ellipse([cx - 160, cy - 160, cx + 160, cy + 160], outline=BROWN, width=2)
    # banana slices inside
    for off in [(-80, 0), (40, -30), (-30, 60), (70, 40)]:
        ox, oy = off
        d.ellipse([cx + ox - 25, cy + oy - 14, cx + ox + 25, cy + oy + 14],
                  outline=BROWN, width=2)
    f = font(38)
    msg = "top-down. hands working. layers."
    bbox = d.textbbox((0, 0), msg, font=f)
    d.text(((PREVIEW - (bbox[2] - bbox[0])) // 2, PREVIEW - 90), msg, font=f, fill=BROWN)

def helper_spoon(img):
    """Tile 9: spoon lift bite."""
    d = ImageDraw.Draw(img)
    cx, cy = PREVIEW // 2, PREVIEW // 2
    # spoon outline (long oval + handle)
    d.ellipse([cx - 90, cy - 130, cx + 90, cy - 10], outline=BROWN, width=4)
    d.line([(cx, cy - 10), (cx, cy + 180)], fill=BROWN, width=8)
    # blob on spoon
    d.ellipse([cx - 70, cy - 115, cx + 70, cy - 25], fill=CREAM, outline=BROWN, width=3)
    f = font(38)
    msg = "single bite. blurred bg."
    bbox = d.textbbox((0, 0), msg, font=f)
    d.text(((PREVIEW - (bbox[2] - bbox[0])) // 2, PREVIEW - 90), msg, font=f, fill=BROWN)

TILES = [
    {
        "n": 1, "title": "Hand-held hero",
        "bg": BROWN, "preview": helper_hand_cup,
        "shoot": "Hand from the side. Cup tilted, wrap fully visible.",
        "light": "Soft daylight at a window. No flash.",
        "where": "Plain dark wall or wood. We swap bg to brown after.",
        "watch": "Wrap must read clearly. Avoid harsh shadows.",
    },
    {
        "n": 3, "title": "Macro pudding texture",
        "bg": CREAM, "preview": helper_macro,
        "shoot": "Top-down or 45 degrees. Pudding fills the frame edge to edge.",
        "light": "Side light from a window to rake across the layers.",
        "where": "White plate or cream cloth on the counter.",
        "watch": "No text. No cup. No logo. Just pudding.",
    },
    {
        "n": 4, "title": "Cup stack hero",
        "bg": BROWN, "preview": helper_stack,
        "shoot": "Three to five cups stacked or fanned. Front-on, not overhead.",
        "light": "Soft mid-morning daylight.",
        "where": "Dark wood or marble. We swap bg to brown after.",
        "watch": "One cup faces camera straight. Logo and lid visible.",
    },
    {
        "n": 6, "title": "Notting Hill street",
        "bg": CREAM, "preview": helper_lifestyle,
        "shoot": "Cup mid-stride or resting on a bench. Phone at hip height.",
        "light": "Golden hour or soft cloudy. No harsh midday sun.",
        "where": "Portobello, Lancaster Rd, or any pastel row.",
        "watch": "Cream, pink, or blue facade only. No red or green.",
    },
    {
        "n": 7, "title": "Process shot",
        "bg": CREAM, "preview": helper_process,
        "shoot": "Overhead. Bowl, hands working, slices and crumbs.",
        "light": "Bright soft daylight from above-side at a window.",
        "where": "Counter, parchment paper, or cream cloth.",
        "watch": "Tight crop. No background clutter.",
    },
    {
        "n": 9, "title": "Spoon lift",
        "bg": CREAM, "preview": helper_spoon,
        "shoot": "Single spoonful lifted from the cup. Side angle, slight tilt.",
        "light": "Soft daylight. Subject sharp, background blurred.",
        "where": "Same setup as the macro and process shots.",
        "watch": "Creamy, not dry. Spoon clean. No drips on the rim.",
    },
]

# ---- Compose ----
page = Image.new("RGB", (W, H), CREAM)
d = ImageDraw.Draw(page)

# Header
f_h1 = font(110)
f_h2 = font(42)
d.text((GAP + 20, 40), "Photo shoot brief", font=f_h1, fill=BROWN)
d.text((GAP + 20, 160), "Six tiles to shoot for the new IG grid. Bg can be swapped after via build_post.py.",
       font=f_h2, fill=BROWN)
d.line([(GAP, HEADER_H - 10), (W - GAP, HEADER_H - 10)], fill=BROWN, width=3)

# Panels
f_title = font(54)
f_lbl = font(36)
f_body_small = font(34)

for i, tile in enumerate(TILES):
    r, c = divmod(i, COLS)
    x0 = GAP + c * (PANEL_W + GAP)
    y0 = HEADER_H + GAP + r * (PANEL_H + GAP)

    # Preview
    preview = make_preview(tile["n"], tile["bg"], tile["preview"])
    # tile number badge top-left
    badge = font(58)
    pd = ImageDraw.Draw(preview)
    pd.text((24, 18), f"#{tile['n']}", font=badge, fill=CREAM if tile["bg"] == BROWN else BROWN)
    # bg label top-right
    bg_label = "BROWN BG" if tile["bg"] == BROWN else "CREAM BG"
    bl_font = font(30)
    bbbox = pd.textbbox((0, 0), bg_label, font=bl_font)
    pd.text((PREVIEW - (bbbox[2] - bbbox[0]) - 24, 24), bg_label,
            font=bl_font,
            fill=CREAM if tile["bg"] == BROWN else BROWN)
    page.paste(preview, (x0, y0))

    # Notes area
    notes_x = x0 + 8
    notes_y = y0 + PREVIEW + 20

    # Title
    d.text((notes_x, notes_y), tile["title"], font=f_title, fill=BROWN)
    notes_y += 76

    for label, key in [("SHOOT", "shoot"), ("LIGHT", "light"), ("WHERE", "where"), ("WATCH", "watch")]:
        d.text((notes_x, notes_y), label, font=f_lbl, fill=BROWN)
        notes_y += 48
        notes_y = draw_text_block(d, notes_x + 10, notes_y, f_body_small, tile[key],
                                  PANEL_W - 28, color=BROWN, line_gap=4)
        notes_y += 10

# Footer
f_foot = font(30)
foot_text = "Run: python3 build_post.py photos_in/<your_photo>.jpg --bg brown   (or --bg cream)"
d.text((GAP + 20, H - 60), foot_text, font=f_foot, fill=BROWN)

page.save(OUT, quality=92)
print(f"Saved {OUT} {page.size}")
