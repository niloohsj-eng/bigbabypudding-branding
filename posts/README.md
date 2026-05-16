# posts/ — All Instagram-ready content, organized by type

This folder is your **weekly posting library**. Each subfolder is a different *type* of post. Pick from whichever vibe fits the day.

## Folder structure

```
posts/
├── illustrations/    Hand-drawn brown-line illustrations — the Wednesday signature series
├── photos/           Real product photos — pudding, cups, hands
├── lifestyle/        Candid / behind-the-scenes / Notting Hill street shots
├── reels/            Video content + custom reel covers
├── seasonal/         Holiday and occasion posts
├── preview/          Auto-generated grid mockups (don't edit by hand)
├── _exploration/     Old experiments and abandoned variants (safe to ignore)
└── tile_*.png        The 9 LOCKED tiles for the initial grid launch (don't edit until launch is done)
```

## The weekly content rhythm (recommended)

| Day | Post type | Folder to open |
|---|---|---|
| Monday | Photo or reel | `photos/` or `reels/` |
| Wednesday | Illustration | `illustrations/` |
| Friday | Lifestyle | `lifestyle/` |

Three posts per week — sustainable, consistent, won't burn you out.

## Initial 9-tile launch grid

Locked in this folder root (`tile_01_handheld_hero.png` through `tile_08_notting_hill.png`).

Post in **reverse order** so the grid resolves to the designed layout:
1. Spoon lift (pending photo)
2. Notting Hill houses
3. Process shot
4. Deliveroo (graphic)
5. Hand-held hero (center)
6. Peel + W8 (graphic)
7. Cup stack illustration
8. Logo poster
9. Macro pudding

After all 9 are posted, drop into the regular weekly rhythm above using the subfolders.

## How to add new content

- **Illustrations:** edit `build_illustrations.py` at the repo root, add a new function, re-run. The PNG appears in `illustrations/`.
- **Photos:** drop the raw phone photo in `photos_in/`, run `python3 build_post.py photos_in/your.jpg --bg cream` (or `--bg brown`). The result lands in `photos_out/`. Then move it to `photos/` (or `lifestyle/` if it's candid).
- **Reels:** save the video and cover thumbnail directly into `reels/`.
- **Seasonal:** edit `build_illustrations.py` to add a holiday-themed function, OR save a themed photo directly to `seasonal/`.

## Captions

Each subfolder's `README.md` has caption guidelines and examples specific to that post type. The universal rules:
- End with a period.
- Max 8 words for most posts.
- One emoji or none.
- Never use: *indulgent, delicious, yummy, drool, OBSESSED, the goat, hits different*.
- Personality > information.
