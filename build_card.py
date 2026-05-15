"""Thank-you card insert for Big Baby Banana Pudding orders.

Portrait 3.5"x5" card. Rendered at 600dpi (2100x3000) for crisp print + preview.
Two-color palette: cream + brown only.
"""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

ROOT = Path(__file__).parent
B = ROOT / "branding"
OUT = ROOT / "card_mockup.png"

CREAM = "#fffae2"
BROWN = "#39251c"

W, H = 2100, 3000
MARGIN = 140
USABLE_W = W - 2 * MARGIN

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

def text_w(d, text, fnt):
    bbox = d.textbbox((0, 0), text, font=fnt)
    return bbox[2] - bbox[0]

def text_h(d, text, fnt):
    bbox = d.textbbox((0, 0), text, font=fnt)
    return bbox[3] - bbox[1]

def cx(d, text, fnt):
    return (W - text_w(d, text, fnt)) // 2

def wrap(d, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        test = (cur + " " + w).strip()
        if text_w(d, test, fnt) <= max_w:
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

# Subtle rounded border
d.rounded_rectangle([60, 60, W - 60, H - 60], radius=80, outline=BROWN, width=4)

# ---- 1) Brand mark: Logo with character ----
mark = Image.open(B / "Logo/Logo_w_Character.png").convert("RGBA")
target_w = 1100
ratio = target_w / mark.width
mark = mark.resize((target_w, int(mark.height * ratio)), Image.LANCZOS)
mark_x = (W - mark.width) // 2
mark_y = 180
card.paste(mark, (mark_x, mark_y), mark)

# ---- 2) Divider rule ----
sep_y = mark_y + mark.height + 80
d.line([(W // 2 - 240, sep_y), (W // 2 + 240, sep_y)], fill=BROWN, width=5)

# ---- 3) Soft headline ----
f_hook = font(72)
hook = "Loved it?"
hook_y = sep_y + 80
d.text((cx(d, hook, f_hook), hook_y), hook, font=f_hook, fill=BROWN)

# ---- 4) Big offer (two stacked lines for emphasis) ----
f_offer1 = font(150)
f_offer2 = font(80)
line1 = "20% OFF"
line2 = "your next batch."
offer_y = hook_y + text_h(d, hook, f_hook) + 50
d.text((cx(d, line1, f_offer1), offer_y), line1, font=f_offer1, fill=BROWN)
offer_y2 = offer_y + text_h(d, line1, f_offer1) + 40
d.text((cx(d, line2, f_offer2), offer_y2), line2, font=f_offer2, fill=BROWN)

# ---- 5) Instructions body ----
f_body = font(50)
body = ("Leave us a written review on Deliveroo, "
        "then DM the screenshot to @bigbabypudding. "
        "We'll send your code within 24 hours.")
body_y = offer_y2 + text_h(d, line2, f_offer2) + 100
lines = wrap(d, body, f_body, USABLE_W - 60)
for line in lines:
    d.text((cx(d, line, f_body), body_y), line, font=f_body, fill=BROWN)
    body_y += text_h(d, line, f_body) + 22

# ---- 6) Footer handle, anchored to bottom ----
f_handle = font(56)
handle = "@bigbabypudding"
handle_y = H - MARGIN - 50
d.text((cx(d, handle, f_handle), handle_y), handle, font=f_handle, fill=BROWN)

card.save(OUT, quality=94)
print(f"Saved {OUT} {card.size}")
