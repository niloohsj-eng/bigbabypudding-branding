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
PASTEL_YELLOW = "#f0e6bc"  # warm pastel yellow — vanilla vibe, breaks grid monotony
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


def draw_locked_wafer(d, cx, cy, r=260):
    """LOCKED wafer — updated 2026-05-19 to match SpoonScoop character face.
    Tiny close-together dot eyes, barely-bent mini smile dash."""
    body = wobbly_circle_points(cx, cy, r, n=120, jitter=2.0, seed=22)
    d.polygon(body, fill=NILLA_DEEP)
    out = wobbly_circle_points(cx, cy, r, n=120, jitter=1.8, seed=33)
    d.line(out + [out[0]], fill=BROWN, width=9)
    # Eyes: small dots, close together (matching SpoonScoop cx=±16, cy=-8, r=3 scaled by 260/125)
    eye_r = 6
    eye_y = cy - 17
    eye_dx = 33
    d.ellipse([cx - eye_dx - eye_r, eye_y - eye_r, cx - eye_dx + eye_r, eye_y + eye_r], fill=BROWN)
    d.ellipse([cx + eye_dx - eye_r, eye_y - eye_r, cx + eye_dx + eye_r, eye_y + eye_r], fill=BROWN)
    # Smile: tiny barely-bent dash (matching SpoonScoop M -8 28 Q 0 31 8 28 scaled)
    d.arc([cx - 16, cy + 50, cx + 16, cy + 70], start=15, end=165, fill=BROWN, width=4)


img = Image.new("RGB", (CANVAS, CANVAS), PASTEL_YELLOW)
d = ImageDraw.Draw(img)
font = ImageFont.truetype(FONT_PATH, 70)
text = "Wafer you been all my life?"
bbox = d.textbbox((0, 0), text, font=font)
tw = bbox[2] - bbox[0]
d.text(((CANVAS - tw) // 2, 130), text, font=font, fill=BROWN)
draw_locked_wafer(d, cx=CANVAS // 2, cy=CANVAS // 2 + 110)
img.save(OUT, quality=95)
print(f"Locked: {OUT}")
