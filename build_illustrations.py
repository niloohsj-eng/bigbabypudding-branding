"""Build all 10 hand-drawn illustrations for the weekly illustrated post series.

All saved to posts/illustrations/ as 1080x1080 PNGs.
Style: brown line art on cream, Bradley Hand Bold for text.
"""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import math

ROOT = Path(__file__).parent
B = ROOT / "branding"
FONTS = ROOT / "fonts"
OUT_DIR = ROOT / "posts" / "illustrations"
OUT_DIR.mkdir(exist_ok=True)

CREAM = (250, 248, 240)
BROWN = (57, 37, 28)
YELLOW = (255, 226, 86)
CANVAS = 1080
BRADLEY = str(FONTS / "Bradley Hand Bold.ttf")

def font(size):
    return ImageFont.truetype(BRADLEY, size)

def smooth_line(d, pts, fill, width):
    for i in range(len(pts) - 1):
        d.line([pts[i], pts[i+1]], fill=fill, width=width)
    for p in pts:
        r = width // 2
        d.ellipse([p[0]-r, p[1]-r, p[0]+r, p[1]+r], fill=fill)

def cx_text(d, text, fnt, canvas_w=CANVAS):
    bbox = d.textbbox((0, 0), text, font=fnt)
    return (canvas_w - (bbox[2] - bbox[0])) // 2

def draw_clean_cup(d, cx, cy_bot, cup_w_top, cup_h, cream_h, lw=9, show_cream=True):
    cup_w_bot = int(cup_w_top * 0.85)
    cup_top_y = cy_bot - cup_h
    half_top = cup_w_top // 2
    half_bot = cup_w_bot // 2
    d.polygon([(cx - half_top, cup_top_y), (cx + half_top, cup_top_y),
               (cx + half_bot, cy_bot), (cx - half_bot, cy_bot)], fill=CREAM)
    smooth_line(d, [(cx - half_top, cup_top_y), (cx - half_bot, cy_bot)], BROWN, lw)
    smooth_line(d, [(cx + half_top, cup_top_y), (cx + half_bot, cy_bot)], BROWN, lw)
    d.arc([cx - half_bot - 4, cy_bot - 14, cx + half_bot + 4, cy_bot + 14],
          start=0, end=180, fill=BROWN, width=lw)
    rim_h = max(7, cup_w_top // 26)
    d.ellipse([cx - half_top, cup_top_y - rim_h, cx + half_top, cup_top_y + rim_h],
              fill=CREAM, outline=BROWN, width=max(4, lw - 3))
    if show_cream:
        overflow = int(cup_w_top * 0.08)
        cloud_w = cup_w_top + overflow * 2
        half_cloud = cloud_w // 2
        rim_top = cup_top_y - rim_h + 3
        n = 50
        cloud_pts = []
        for i in range(n + 1):
            t = i / n
            ang = math.pi * t
            dip = -0.08 * math.exp(-((t - 0.55) / 0.15) ** 2)
            h_at = cream_h * math.sin(ang) * (1 + dip)
            x = cx + half_cloud * math.cos(math.pi - ang)
            cloud_pts.append((x, rim_top - h_at))
        base_l = (cx - half_top + 6, cup_top_y + rim_h * 0.5)
        base_r = (cx + half_top - 6, cup_top_y + rim_h * 0.5)
        d.polygon([base_l] + cloud_pts + [base_r], fill=CREAM)
        smooth_line(d, cloud_pts, BROWN, lw)
        # Swirl
        sy = rim_top - int(cream_h * 0.60)
        d.arc([cx - 30, sy - 14, cx + 30, sy + 18], start=200, end=340, fill=BROWN, width=3)
    return cup_top_y

def draw_plain_banana(d, cx, cy, length, lw=6, color=YELLOW):
    n = 40
    pts_top = []
    pts_bot = []
    for i in range(n + 1):
        t = i / n
        x = cx - length / 2 + t * length
        center_dy = -length * 0.10 * math.sin(t * math.pi)
        thickness = length * 0.42 * 0.5 * (math.sin(t * math.pi) ** 0.55)
        if t < 0.04 or t > 0.96:
            thickness *= 0.35
        pts_top.append((x, cy + center_dy - thickness))
        pts_bot.append((x, cy + center_dy + thickness))
    poly = pts_top + pts_bot[::-1]
    d.polygon(poly, fill=color)
    smooth_line(d, pts_top, BROWN, lw)
    smooth_line(d, pts_bot, BROWN, lw)
    d.line([pts_top[0], pts_bot[0]], fill=BROWN, width=lw)
    d.line([pts_top[-1], pts_bot[-1]], fill=BROWN, width=lw)
    stem = (pts_top[-1][0] + length * 0.05, pts_top[-1][1] - length * 0.10)
    smooth_line(d, [pts_top[-1], stem], BROWN, lw)
    mid_top_y = pts_top[len(pts_top) // 2][1]
    mid_bot_y = pts_bot[len(pts_bot) // 2][1]
    d.line([(cx, mid_top_y + 8), (cx, mid_bot_y - 8)], fill=BROWN, width=2)

def new_canvas():
    img = Image.new("RGB", (CANVAS, CANVAS), CREAM)
    return img, ImageDraw.Draw(img)

def title(d, text, y=85, size=76):
    f = font(size)
    d.text((cx_text(d, text, f), y), text, font=f, fill=BROWN)

# ============ 1. ANATOMY OF A BIG BABY ============
img, d = new_canvas()
title(d, "Anatomy of a Big Baby.", y=80, size=66)
cy_bot = 800
draw_clean_cup(d, cx=540, cy_bot=cy_bot, cup_w_top=320, cup_h=240, cream_h=240, lw=10)
# Arrows pointing to parts
def arrow_label(d, start_xy, end_xy, label, label_anchor="left"):
    smooth_line(d, [start_xy, end_xy], BROWN, 4)
    # Arrow head
    ax, ay = end_xy
    sx, sy = start_xy
    dx = ax - sx
    dy = ay - sy
    length = (dx**2 + dy**2) ** 0.5
    if length > 0:
        ux, uy = dx / length, dy / length
        head_size = 14
        d.polygon([
            (ax, ay),
            (ax - head_size * ux + head_size * 0.5 * uy, ay - head_size * uy - head_size * 0.5 * ux),
            (ax - head_size * ux - head_size * 0.5 * uy, ay - head_size * uy + head_size * 0.5 * ux),
        ], fill=BROWN)
    f = font(36)
    bb = d.textbbox((0, 0), label, font=f)
    if label_anchor == "left":
        lx = sx - (bb[2] - bb[0]) - 14
    else:
        lx = sx + 14
    d.text((lx, sy - (bb[3] - bb[1]) // 2), label, font=f, fill=BROWN)

# Cream mound: pointing to top
arrow_label(d, start_xy=(180, 350), end_xy=(420, 480), label="Pillowy cream")
# Wafer layer: middle of cup
arrow_label(d, start_xy=(870, 650), end_xy=(700, 720), label="Vanilla wafers", label_anchor="right")
# Banana slices: middle/lower
arrow_label(d, start_xy=(180, 700), end_xy=(420, 780), label="Banana slices")
# Made in W8: at the bottom
arrow_label(d, start_xy=(870, 820), end_xy=(700, 800), label="Made in W8.", label_anchor="right")

img.save(OUT_DIR / "illust_01_anatomy.png", quality=95)
print("01 anatomy")

# ============ 2. HOW TO BIG BABY (3-panel) ============
img, d = new_canvas()
title(d, "Step-by-step.", y=80, size=76)
# 3 panels horizontally
panel_w = (CANVAS - 80) // 3 - 20
panel_h = 600
panel_y0 = 280
gap = 30
start_x = (CANVAS - (panel_w * 3 + gap * 2)) // 2

# Panel borders (very subtle)
for i in range(3):
    x = start_x + i * (panel_w + gap)
    d.rectangle([x, panel_y0, x + panel_w, panel_y0 + panel_h], outline=BROWN, width=2)

# Panel 1: spoon dipping into cup
p1_x = start_x + panel_w // 2
draw_clean_cup(d, cx=p1_x, cy_bot=panel_y0 + 520, cup_w_top=170, cup_h=120, cream_h=120, lw=7)
# Spoon coming down
spoon_top_x, spoon_top_y = p1_x, panel_y0 + 120
spoon_bowl_x, spoon_bowl_y = p1_x, panel_y0 + 320
smooth_line(d, [(spoon_top_x, spoon_top_y), (spoon_bowl_x, spoon_bowl_y)], BROWN, 6)
d.ellipse([spoon_bowl_x - 30, spoon_bowl_y - 12, spoon_bowl_x + 30, spoon_bowl_y + 30],
          outline=BROWN, width=6, fill=CREAM)

# Panel 2: spoon lifted with cream
p2_x = start_x + (panel_w + gap) + panel_w // 2
draw_clean_cup(d, cx=p2_x, cy_bot=panel_y0 + 520, cup_w_top=170, cup_h=120, cream_h=60, lw=7)  # less cream
# Spoon up with a blob of cream
sx, sy = p2_x + 40, panel_y0 + 160
smooth_line(d, [(sx, sy), (sx, panel_y0 + 360)], BROWN, 6)
d.ellipse([sx - 28, panel_y0 + 350, sx + 28, panel_y0 + 388], outline=BROWN, width=6, fill=CREAM)
# Cream blob on top of spoon
ex, ey = sx, panel_y0 + 340
d.ellipse([ex - 35, ey - 30, ex + 35, ey + 12], fill=CREAM, outline=BROWN, width=6)
d.arc([ex - 20, ey - 18, ex + 20, ey + 8], start=200, end=340, fill=BROWN, width=3)

# Panel 3: empty cup with happy character
p3_x = start_x + 2 * (panel_w + gap) + panel_w // 2
draw_clean_cup(d, cx=p3_x, cy_bot=panel_y0 + 520, cup_w_top=170, cup_h=120, cream_h=20, lw=7, show_cream=False)
# Add small banana character beside
banana_char = Image.open(B / "Little Bananas/Banana_1.png").convert("RGBA")
ratio = 140 / banana_char.width
banana_char = banana_char.resize((140, int(banana_char.height * ratio)), Image.LANCZOS)
img.paste(banana_char, (p3_x - 70 - 110, panel_y0 + 250), banana_char)

img.save(OUT_DIR / "illust_02_step_by_step.png", quality=95)
print("02 step-by-step")

# ============ 3. WAFER WITH FACE ============
img, d = new_canvas()
title(d, "Wafer you been all my life?", y=80, size=58)
# Draw a rectangular vanilla wafer (rounded rectangle) with cute face
cx, cy = CANVAS // 2, CANVAS // 2 + 100
ww, wh = 460, 360
d.rounded_rectangle([cx - ww // 2, cy - wh // 2, cx + ww // 2, cy + wh // 2],
                    radius=40, outline=BROWN, width=10, fill=(252, 235, 180))  # subtle wafer-tan tint
# Texture lines suggesting wafer ridges (subtle)
for i in range(5):
    yy = cy - wh // 2 + 50 + i * 60
    d.line([(cx - ww // 2 + 50, yy), (cx + ww // 2 - 50, yy)], fill=BROWN, width=2)
# Face: eyes (closed slits) + smile + cheeks
eye_y = cy - 30
# Eyes
d.arc([cx - 100, eye_y - 10, cx - 50, eye_y + 20], start=200, end=340, fill=BROWN, width=6)
d.arc([cx + 50, eye_y - 10, cx + 100, eye_y + 20], start=200, end=340, fill=BROWN, width=6)
# Smile
d.arc([cx - 50, cy + 10, cx + 50, cy + 70], start=0, end=180, fill=BROWN, width=6)
# Blush cheeks
d.ellipse([cx - 145, cy + 20, cx - 110, cy + 45], fill=(234, 89, 149))
d.ellipse([cx + 110, cy + 20, cx + 145, cy + 45], fill=(234, 89, 149))

img.save(OUT_DIR / "illust_03_wafer_face.png", quality=95)
print("03 wafer face")

# ============ 4. PICKY BANANA (magnifying glass) ============
img, d = new_canvas()
title(d, "We're picky for a reason.", y=80, size=64)
# Banana lying horizontal in lower-center
ban_cx, ban_cy = CANVAS // 2, 700
draw_plain_banana(d, cx=ban_cx, cy=ban_cy, length=380, lw=8)
# Magnifying glass above-left looking down at banana
mx, my = ban_cx - 100, ban_cy - 220
mr = 110
d.ellipse([mx - mr, my - mr, mx + mr, my + mr], outline=BROWN, width=10, fill=None)
# Handle
hx, hy = mx + mr * 0.7, my + mr * 0.7
hex_, hey = hx + 80, hy + 80
smooth_line(d, [(hx, hy), (hex_, hey)], BROWN, 16)
# Subtle reflection mark on lens
d.arc([mx - mr + 18, my - mr + 18, mx, my], start=200, end=290, fill=BROWN, width=3)

img.save(OUT_DIR / "illust_04_picky_banana.png", quality=95)
print("04 picky banana")

# ============ 5. CREAM WEATHER (sun + cup) ============
img, d = new_canvas()
title(d, "Cream weather.", y=80, size=80)
# Sun upper-right
sx, sy, sr = 780, 320, 90
d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], outline=BROWN, width=8, fill=(255, 240, 150))
# Sun rays
for i in range(12):
    ang = i * math.pi / 6
    r_inner = sr + 20
    r_outer = sr + 70
    x1 = sx + r_inner * math.cos(ang)
    y1 = sy + r_inner * math.sin(ang)
    x2 = sx + r_outer * math.cos(ang)
    y2 = sy + r_outer * math.sin(ang)
    d.line([(x1, y1), (x2, y2)], fill=BROWN, width=6)
# Cup with extra cream rising like steam
draw_clean_cup(d, cx=380, cy_bot=900, cup_w_top=280, cup_h=210, cream_h=200, lw=10)

img.save(OUT_DIR / "illust_05_cream_weather.png", quality=95)
print("05 cream weather")

# ============ 6. RAINY SUNDAY (rain cloud + cup with umbrella) ============
img, d = new_canvas()
title(d, "Sunday in.", y=80, size=80)
# Cloud upper area
cx, cy = CANVAS // 2, 320
# Cloud shape: 3 overlapping circles
d.ellipse([cx - 180, cy - 70, cx - 40, cy + 60], outline=BROWN, width=8, fill=(240, 235, 218))
d.ellipse([cx - 100, cy - 110, cx + 80, cy + 70], outline=BROWN, width=8, fill=(240, 235, 218))
d.ellipse([cx + 30, cy - 70, cx + 180, cy + 60], outline=BROWN, width=8, fill=(240, 235, 218))
# Fill bottom seam with cream rectangle to merge
d.rectangle([cx - 175, cy + 30, cx + 175, cy + 60], fill=(240, 235, 218))
# Cloud outline at the bottom
d.line([(cx - 175, cy + 60), (cx + 175, cy + 60)], fill=BROWN, width=8)
# Rain drops
for i, (dx, dy) in enumerate([(-130, 110), (-70, 130), (-10, 110), (50, 130), (110, 110)]):
    rx, ry = cx + dx, cy + dy
    d.line([(rx, ry), (rx - 4, ry + 40)], fill=BROWN, width=5)
# Cup at bottom with tiny umbrella
draw_clean_cup(d, cx=cx, cy_bot=950, cup_w_top=260, cup_h=200, cream_h=160, lw=10)
# Umbrella sticking out the top of cream
umb_x, umb_y = cx, 560
d.arc([umb_x - 70, umb_y - 30, umb_x + 70, umb_y + 50], start=180, end=360, fill=BROWN, width=8)
d.line([(umb_x - 70, umb_y + 10), (umb_x + 70, umb_y + 10)], fill=BROWN, width=8)
# Umbrella handle
smooth_line(d, [(umb_x, umb_y + 10), (umb_x, umb_y + 60)], BROWN, 6)
# Hook on handle
d.arc([umb_x - 14, umb_y + 50, umb_x + 14, umb_y + 80], start=20, end=180, fill=BROWN, width=6)

img.save(OUT_DIR / "illust_06_sunday_in.png", quality=95)
print("06 sunday in")

# ============ 7. FRESH FROM THIS MORNING (clock + cup) ============
img, d = new_canvas()
title(d, "Fresh from this morning.", y=80, size=64)
# Clock face left
ccx, ccy, ccr = 360, 600, 170
d.ellipse([ccx - ccr, ccy - ccr, ccx + ccr, ccy + ccr], outline=BROWN, width=10, fill=CREAM)
# Hour markers (4 of them at 12/3/6/9)
for ang in [0, 90, 180, 270]:
    a = math.radians(ang - 90)
    r_inner = ccr - 30
    r_outer = ccr - 10
    x1 = ccx + r_inner * math.cos(a)
    y1 = ccy + r_inner * math.sin(a)
    x2 = ccx + r_outer * math.cos(a)
    y2 = ccy + r_outer * math.sin(a)
    d.line([(x1, y1), (x2, y2)], fill=BROWN, width=6)
# Hands showing ~8:30
# Hour hand pointing to 8 (about 240° from 12)
a_hour = math.radians(240 - 90)
x_h = ccx + (ccr - 60) * math.cos(a_hour)
y_h = ccy + (ccr - 60) * math.sin(a_hour)
smooth_line(d, [(ccx, ccy), (x_h, y_h)], BROWN, 8)
# Minute hand pointing to 6 (180° from 12)
a_min = math.radians(180 - 90)
x_m = ccx + (ccr - 30) * math.cos(a_min)
y_m = ccy + (ccr - 30) * math.sin(a_min)
smooth_line(d, [(ccx, ccy), (x_m, y_m)], BROWN, 6)
# Center dot
d.ellipse([ccx - 8, ccy - 8, ccx + 8, ccy + 8], fill=BROWN)
# Cup right
draw_clean_cup(d, cx=780, cy_bot=820, cup_w_top=240, cup_h=200, cream_h=180, lw=10)

img.save(OUT_DIR / "illust_07_clock.png", quality=95)
print("07 clock")

# ============ 8. CALENDAR + CUP (Wednesday) ============
img, d = new_canvas()
title(d, "Wednesday is a Big Baby day.", y=80, size=58)
# Calendar grid: simple 4x5 with one day circled
cal_x = 100
cal_y = 300
cal_w = 460
cal_h = 540
d.rectangle([cal_x, cal_y, cal_x + cal_w, cal_y + cal_h], outline=BROWN, width=8, fill=CREAM)
# Top binding
d.rectangle([cal_x, cal_y - 18, cal_x + cal_w, cal_y + 12], outline=BROWN, width=6, fill=(252, 240, 200))
# Header row
d.line([(cal_x, cal_y + 90), (cal_x + cal_w, cal_y + 90)], fill=BROWN, width=4)
# Day-of-week initials (S M T W T F S)
days = ["S", "M", "T", "W", "T", "F", "S"]
cell_w = cal_w / 7
f_day = font(34)
for i, day in enumerate(days):
    cellx = cal_x + i * cell_w + cell_w / 2
    bb = d.textbbox((0, 0), day, font=f_day)
    d.text((cellx - (bb[2] - bb[0]) / 2, cal_y + 30), day, fill=BROWN, font=f_day)
# Number cells (just dots / numbers)
f_num = font(26)
for row in range(4):
    for col in range(7):
        cellx = cal_x + col * cell_w + cell_w / 2
        celly = cal_y + 130 + row * 90
        n = row * 7 + col + 1
        if n > 28:
            break
        d.text((cellx - 10, celly), str(n), fill=BROWN, font=f_num)
# Circle around a Wednesday (col 3, row 1, day 11)
circ_col, circ_row = 3, 1
ccx = cal_x + circ_col * cell_w + cell_w / 2
ccy = cal_y + 130 + circ_row * 90 + 12
d.ellipse([ccx - 28, ccy - 22, ccx + 28, ccy + 32], outline=BROWN, width=4)
# Cup on the right side
draw_clean_cup(d, cx=820, cy_bot=820, cup_w_top=240, cup_h=200, cream_h=170, lw=10)

img.save(OUT_DIR / "illust_08_calendar.png", quality=95)
print("08 calendar")

# ============ 9. REVIEW STARS IN SPEECH BUBBLE ============
img, d = new_canvas()
title(d, "From a recent order.", y=80, size=70)
# Speech bubble
bx, by, bw, bh = 200, 320, 680, 380
d.rounded_rectangle([bx, by, bx + bw, by + bh], radius=70, outline=BROWN, width=10, fill=CREAM)
# Bubble tail pointing down to cup
tail_pts = [(bx + bw // 2 - 40, by + bh), (bx + bw // 2, by + bh + 60), (bx + bw // 2 + 40, by + bh)]
d.polygon(tail_pts, fill=CREAM, outline=BROWN)
d.line([tail_pts[0], tail_pts[1]], fill=BROWN, width=10)
d.line([tail_pts[1], tail_pts[2]], fill=BROWN, width=10)
# Clean up the line where tail meets bubble
d.line([tail_pts[0], tail_pts[2]], fill=CREAM, width=10)

# 5 stars inside bubble
star_y = by + bh // 2
star_w = 80
star_spacing = 100
total_w = 4 * star_spacing + star_w
start_x = bx + (bw - total_w) // 2 + star_w // 2

def draw_star(d, cx, cy, r_outer, r_inner, fill, outline=BROWN, lw=4):
    pts = []
    for i in range(10):
        a = math.radians(-90 + i * 36)
        r = r_outer if i % 2 == 0 else r_inner
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d.polygon(pts, fill=fill, outline=outline)
    for i in range(10):
        d.line([pts[i], pts[(i + 1) % 10]], fill=outline, width=lw)

for i in range(5):
    sx = start_x + i * star_spacing
    draw_star(d, sx, star_y, 40, 18, fill=YELLOW)

# Small cup below tail
draw_clean_cup(d, cx=CANVAS // 2, cy_bot=970, cup_w_top=180, cup_h=130, cream_h=110, lw=8)

img.save(OUT_DIR / "illust_09_review.png", quality=95)
print("09 review")

# ============ 10. QUEUE OF BANANAS ============
img, d = new_canvas()
title(d, "They lined up. So do we.", y=80, size=66)
# Counter line at bottom
counter_y = 880
d.line([(80, counter_y), (CANVAS - 80, counter_y)], fill=BROWN, width=8)
# A cup behind the counter (server)
draw_clean_cup(d, cx=CANVAS // 2, cy_bot=counter_y - 8, cup_w_top=200, cup_h=160, cream_h=140, lw=9)
# Queue of 4-5 small plain bananas to the left, walking right
queue_y = counter_y + 60
banana_size = 140
positions = [(170, queue_y), (360, queue_y + 10), (550, queue_y - 5), (740, queue_y + 8)]
for i, (qx, qy) in enumerate(positions):
    # smaller bananas
    draw_plain_banana(d, cx=qx, cy=qy, length=140, lw=5)

img.save(OUT_DIR / "illust_10_lined_up.png", quality=95)
print("10 lined up")

print(f"\nAll 10 illustrations saved to {OUT_DIR}")
