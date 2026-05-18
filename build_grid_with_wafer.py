"""Grid preview WITH the wafer included.

IG shows newest top-left. This previews what the grid would look like once the
wafer post goes live (alongside cup tile, picky banana, Notting Hill, etc.).

Persistent output — re-runnable. Lives at posts/preview/grid_with_wafer.png."""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).parent
POSTS = ROOT / "posts"
PREVIEW = POSTS / "preview"
PREVIEW.mkdir(exist_ok=True)
OUT = PREVIEW / "grid_with_wafer.png"

TILE = 720
GAP = 6
GRID = TILE * 3 + GAP * 2


def load(p):
    img = Image.open(p).convert("RGB")
    w, h = img.size
    s = min(w, h)
    img = img.crop(((w - s) // 2, (h - s) // 2, (w + s) // 2, (h + s) // 2))
    return img.resize((TILE, TILE), Image.LANCZOS)


tile_paths = [
    POSTS / "illustrations" / "illust_03_wafer_face.png",     # 1 newest — the wafer
    POSTS / "tile_03_cup_stack.png",                           # 2 cup tile (brown bg)
    POSTS / "illustrations" / "illust_04_picky_banana.png",   # 3 picky banana
    POSTS / "tile_08_notting_hill.png",                        # 4 Notting Hill houses
    POSTS / "tile_01_handheld_hero.png",                       # 5 handheld hero (center)
    POSTS / "tile_07_process.png",                             # 6 process shot
    POSTS / "illustrations" / "illust_02_step_by_step.png",   # 7 step-by-step
    POSTS / "tile_03_macro.png",                               # 8 macro
    POSTS / "illustrations" / "illust_05_cream_weather.png",  # 9 cream weather
]

grid = Image.new("RGB", (GRID, GRID), "white")
for i, p in enumerate(tile_paths):
    if not p.exists():
        print(f"missing {p}")
        continue
    grid.paste(load(p), ((i % 3) * (TILE + GAP), (i // 3) * (TILE + GAP)))

grid.save(OUT, quality=92)
print(f"Saved {OUT}")
