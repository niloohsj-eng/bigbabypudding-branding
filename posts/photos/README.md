# Photos — Real food shots

Pure product photography. Macro pudding, hand-held cup, cup stacks, plating shots. Whenever you take a food photo, process it through `build_post.py` and drop the final 1080x1080 here.

**Cadence:** ideally **2x per week** — these are the workhorses of an Instagram food account.

## What goes here

- Hand-held cup shots (the hero pose — cup at angle, hand holding from below)
- Macro close-ups (pudding fills the frame, layers visible)
- Spoon-lift shots (single bite, blurred bg)
- Cup-on-counter still life
- Overhead "flat lay" of the product

## What does NOT go here

- Lifestyle / behind-the-scenes (those go in `lifestyle/`)
- Illustrated graphics (those go in `illustrations/`)
- Reels / video covers (`reels/`)

## How to add a photo

1. Take the photo on your phone — soft natural daylight, plain background.
2. AirDrop or save to `photos_in/` at repo root.
3. Run: `python3 build_post.py photos_in/IMG_XXXX.jpg --bg cream` (or `--bg brown`).
4. Move the result from `photos_out/` into this folder with a clear filename like `photo_handheld_2026-05-22.png`.
5. Add a caption note to a `captions.md` file in this folder if you want to remember a good caption.

## Visual rules for food photos

- Soft daylight, no flash
- Plain background (we swap it to brand color after)
- Cup wrap visible when possible (when new cups arrive)
- Hand visible adds personality
- Avoid harsh midday sun and direct ceiling lights

## Caption rules

Same as the illustrations:
- Short, period at end, no clichés
- Examples that work: *Fresh batch in hand. / Cream, wafer, banana, repeat. / Trust us. / One spoonful in.*
