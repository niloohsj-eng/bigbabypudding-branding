"""Business-card-size insert for Big Baby Banana Pudding orders.

UK standard 85mm x 55mm landscape, 600dpi -> 2008 x 1299 px.
Two-color palette: cream + brown only.
Two-column layout: brand mark left, offer copy right.
"""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

ROOT = Path(__file__).parent
B = ROOT / "branding"
OUT = ROOT / "card_mockup.png"

CREAM = "#fffae2"
BROWN = "#39251c"

# UK business card 85x55mm at 600 dpi
W, H = 2008, 1299
SAFE = 100  # ~4mm safe inset from trim

# Column split
LEFT_W = 820
RIGHT_X0 = LEFT_W
RIGHT_W = W - LEFT_W

def font(size):
    for c in [
        "/System/Library/Fonts/Helvetica.ttc",
        "/Library/Fonts/Arial.ttf",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
    ]:
        try:
            return ImageFont.truetype(c, size)
        except Exception:
            continue
    return ImageFont.load_default()

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

# Thin border, generous radius — a business-card-feel frame
d.rounded_rectangle([40, 40, W - 40, H - 40], radius=60, outline=BROWN, width=3)

# Vertical divider between the two columns
div_x = LEFT_W
d.line([(div_x, 140), (div_x, H - 140)], fill=BROWN, width=2)

# ---- LEFT: brand mark ----
mark = Image.open(B / "Logo/Logo_w_Character.png").convert("RGBA")
target_h = 920
ratio = target_h / mark.height
mark = mark.resize((int(mark.width * ratio), target_h), Image.LANCZOS)
# fit horizontally if too wide
if mark.width > LEFT_W - 60:
    ratio = (LEFT_W - 60) / mark.width
    mark = mark.resize((int(mark.width * ratio), int(mark.height * ratio)), Image.LANCZOS)
mark_x = (LEFT_W - mark.width) // 2
mark_y = (H - mark.height) // 2
card.paste(mark, (mark_x, mark_y), mark)

# ---- RIGHT: offer copy ----
# Vertically center the whole text block within the right column

f_hook = font(64)
f_offer_big = font(220)
f_offer_sub = font(82)
f_body = font(46)
f_handle = font(54)

hook = "Loved it?"
big = "20% OFF"
sub = "your next batch."
body = ("Leave us a review on Deliveroo and DM the screenshot "
        "to @bigbabypudding. We'll send your code within 24 hours.")

# Compute heights
_, hook_h = text_size(d, hook, f_hook)
_, big_h = text_size(d, big, f_offer_big)
_, sub_h = text_size(d, sub, f_offer_sub)
body_lines = wrap_text(d, body, f_body, RIGHT_W - 2 * 70)
_, body_line_h = text_size(d, "Ay", f_body)
body_total_h = len(body_lines) * (body_line_h + 16) - 16
_, handle_h = text_size(d, "@bigbabypudding", f_handle)

GAP_HOOK_BIG = 20
GAP_BIG_SUB = 25
GAP_SUB_BODY = 60
GAP_BODY_HANDLE = 60

total = (hook_h + GAP_HOOK_BIG + big_h + GAP_BIG_SUB + sub_h
         + GAP_SUB_BODY + body_total_h + GAP_BODY_HANDLE + handle_h)

y = (H - total) // 2

# Hook
d.text((cx_in(d, hook, f_hook, RIGHT_X0, W), y), hook, font=f_hook, fill=BROWN)
y += hook_h + GAP_HOOK_BIG

# Big offer
d.text((cx_in(d, big, f_offer_big, RIGHT_X0, W), y), big, font=f_offer_big, fill=BROWN)
y += big_h + GAP_BIG_SUB

# Sub
d.text((cx_in(d, sub, f_offer_sub, RIGHT_X0, W), y), sub, font=f_offer_sub, fill=BROWN)
y += sub_h + GAP_SUB_BODY

# Body
for line in body_lines:
    d.text((cx_in(d, line, f_body, RIGHT_X0, W), y), line, font=f_body, fill=BROWN)
    y += body_line_h + 16
y += GAP_BODY_HANDLE - 16

# Handle
handle = "@bigbabypudding"
d.text((cx_in(d, handle, f_handle, RIGHT_X0, W), y), handle, font=f_handle, fill=BROWN)

card.save(OUT, quality=94)
print(f"Saved {OUT} {card.size}  (UK 85x55mm @ 600dpi)")
