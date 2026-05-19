"""LOCKED: illust_03_wafer_face.png — C2 design picked 2026-05-17.
Pastel yellow bg + deeper nilla wafer, clean round shape, tiny tight face.
Inline lock script — survives re-runs of build_illustrations.py."""
import math
import random
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

REPO = Path("/Users/niloofarhsj/Desktop/Big Baby Pudding/bigbabypudding-branding")
OUT = REPO / "posts/illustrations/illust_03_wafer_face.png"

CANVAS = 1080
BROWN = "#39251c"
PASTEL_YELLOW = "#faf8f0"  # matches reel/animation bg for consistency across posts
NILLA_DEEP = "#b8854d"
FONT_PATH = str(REPO / "fonts" / "Bradley Hand Bold.ttf")


def wobbly_circle_points(cx, cy, r, n=120, jitter=2.0, seed=22):
    rng = random.Random(seed)
    pts = []
    for i in range(n):
        ang = 2 * math.pi * i / n
        rr = r + rng.uniform(-jitter, jitter)
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    return pts


def draw_locked_wafer(d, cx, cy, r=180):
    """LOCKED wafer — HeyTea minimalism update 2026-05-19.
    Smaller (r=180), more breathing room, face scaled accordingly."""
    s = r / 125  # scale factor from SpoonScoop SVG coords
    body = wobbly_circle_points(cx, cy, r, n=120, jitter=2.0, seed=22)
    d.polygon(body, fill=NILLA_DEEP)
    out = wobbly_circle_points(cx, cy, r, n=120, jitter=1.8, seed=33)
    d.line(out + [out[0]], fill=BROWN, width=7)
    # Eyes scaled from SpoonScoop (cx=±16, cy=-8, r=3)
    eye_r  = max(3, round(3 * s))
    eye_dx = round(16 * s)
    eye_y  = cy - round(8 * s)
    d.ellipse([cx - eye_dx - eye_r, eye_y - eye_r, cx - eye_dx + eye_r, eye_y + eye_r], fill=BROWN)
    d.ellipse([cx + eye_dx - eye_r, eye_y - eye_r, cx + eye_dx + eye_r, eye_y + eye_r], fill=BROWN)
    # Smile scaled from SpoonScoop (M -8 28 Q 0 31 8 28)
    sm_w = round(16 * s)
    sm_y = cy + round(28 * s)
    d.arc([cx - sm_w, sm_y, cx + sm_w, sm_y + round(10 * s)], start=15, end=165, fill=BROWN, width=3)


img = Image.new("RGB", (CANVAS, CANVAS), PASTEL_YELLOW)
d = ImageDraw.Draw(img)
font = ImageFont.truetype(FONT_PATH, 78)  # matches Today's batch. visual weight
text = "Wafer you been all my life?"
bbox = d.textbbox((0, 0), text, font=font)
tw = bbox[2] - bbox[0]
d.text(((CANVAS - tw) // 2, 160), text, font=font, fill=BROWN)
draw_locked_wafer(d, cx=CANVAS // 2, cy=CANVAS // 2 + 140)  # floats lower, more space above
img.save(OUT, quality=95)
print(f"Locked: {OUT}")
