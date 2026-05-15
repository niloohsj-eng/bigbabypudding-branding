"""Business-card-size insert for Big Baby Banana Pudding orders.

UK standard 85mm x 55mm landscape, 600dpi -> 2008 x 1299 px.
Two-color palette: cream + brown only.
Single brand font: Bradley Hand Bold (bundled in fonts/ folder).
Two-column layout: brand mark left, offer copy right.
"""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

ROOT = Path(__file__).parent
B = ROOT / "branding"
FONTS = ROOT / "fonts"
OUT = ROOT / "card_mockup.png"

CREAM = "#fffae2"
BROWN = "#39251c"

# UK business card 85x55mm at 600 dpi
W, H = 2008, 1299

# Column split
LEFT_W = 820
RIGHT_X0 = LEFT_W
RIGHT_W = W - LEFT_W

# Single brand font: try bundled first, then macOS system fallback.
BRADLEY_PATHS = [
    FONTS / "Bradley Hand Bold.ttf",
    Path("/System/Library/Fonts/Supplemental/Bradley Hand Bold.ttf"),
]
BRADLEY = next((str(p) for p in BRADLEY_PATHS if p.exists()), None)
if BRADLEY is None:
    raise SystemExit("Bradley Hand Bold not found. Expected at fonts/Bradley Hand Bold.ttf")

def font(size):
    return ImageFont.truetype(BRADLEY, size)

def text_size(d, text, fnt):
    bbox = d.textbbox((0, 0), text, font=fnt)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]

def cx_in(d, text, fnt, x0, x1):
    tw, _ = text_size(d, text, fnt)
    return x0 + ((x1 - x0) - tw) // 2

def wrap_text(d, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        test = (cur + " " + w).strip()
        if text_size(d, test, fnt)[0] <= max_w:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

# ---- Canvas ----
card = Image.new("RGB", (W, H), CREAM)
d = ImageDraw.Draw(card)

# Thin border
d.rounded_rectangle([40, 40, W - 40, H - 40], radius=60, outline=BROWN, width=3)

# Vertical divider between columns
d.line([(LEFT_W, 140), (LEFT_W, H - 140)], fill=BROWN, width=2)

# ---- LEFT: brand mark ----
mark = Image.open(B / "Logo/Logo_w_Character.png").convert("RGBA")
target_h = 920
ratio = target_h / mark.height
mark = mark.resize((int(mark.width * ratio), target_h), Image.LANCZOS)
if mark.width > LEFT_W - 60:
    ratio = (LEFT_W - 60) / mark.width
    mark = mark.resize((int(mark.width * ratio), int(mark.height * ratio)), Image.LANCZOS)
mark_x = (LEFT_W - mark.width) // 2
mark_y = (H - mark.height) // 2
card.paste(mark, (mark_x, mark_y), mark)

# ---- RIGHT: offer copy, all in Bradley Hand Bold ----
f_hook = font(78)
f_offer_big = font(180)
f_offer_sub = font(82)
f_body = font(48)
f_handle = font(64)

hook = "Loved it?"
big = "£2.50 OFF"
sub = "your next batch."
body = ("Leave a Deliveroo review with a written comment. "
        "Stars alone won't count. DM the screenshot to "
        "@bigbabypudding for your credit.")

_, hook_h = text_size(d, hook, f_hook)
_, big_h = text_size(d, big, f_offer_big)
_, sub_h = text_size(d, sub, f_offer_sub)
body_lines = wrap_text(d, body, f_body, RIGHT_W - 140)
_, body_line_h = text_size(d, "Ay", f_body)
body_total_h = len(body_lines) * (body_line_h + 18) - 18
_, handle_h = text_size(d, "@bigbabypudding", f_handle)

GAP_HOOK_BIG = 40
GAP_BIG_SUB = 90
GAP_SUB_BODY = 70
GAP_BODY_HANDLE = 50

total = (hook_h + GAP_HOOK_BIG + big_h + GAP_BIG_SUB + sub_h
         + GAP_SUB_BODY + body_total_h + GAP_BODY_HANDLE + handle_h)

y = (H - total) // 2

d.text((cx_in(d, hook, f_hook, RIGHT_X0, W), y), hook, font=f_hook, fill=BROWN)
y += hook_h + GAP_HOOK_BIG

d.text((cx_in(d, big, f_offer_big, RIGHT_X0, W), y), big, font=f_offer_big, fill=BROWN)
y += big_h + GAP_BIG_SUB

d.text((cx_in(d, sub, f_offer_sub, RIGHT_X0, W), y), sub, font=f_offer_sub, fill=BROWN)
y += sub_h + GAP_SUB_BODY

for line in body_lines:
    d.text((cx_in(d, line, f_body, RIGHT_X0, W), y), line, font=f_body, fill=BROWN)
    y += body_line_h + 18
y += GAP_BODY_HANDLE - 18

handle = "@bigbabypudding"
d.text((cx_in(d, handle, f_handle, RIGHT_X0, W), y), handle, font=f_handle, fill=BROWN)

card.save(OUT, quality=94)
print(f"Saved {OUT} {card.size}  (UK 85x55mm @ 600dpi)")
