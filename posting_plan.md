# Big Baby Posting Plan

Three posts per week, Monday + Wednesday + Friday. Best window for food in London is **5pm-8pm UK time** (people scroll on the way home, ordering dinner).

The 9 tiles go up in this order so the grid resolves to the designed layout. Instagram puts the newest post in the top-left slot, so we post the bottom-right tile *first* and work backward.

## Posting order

| Week | Mon | Wed | Fri |
|---|---|---|---|
| 1 | Tile 9 (spoon lift) | Tile 8 (Deliveroo reel) | Tile 7 (process) |
| 2 | Tile 6 (Notting Hill) | Tile 5 (peel + W11) | Tile 4 (cup stack) |
| 3 | Tile 3 (macro) | Tile 2 (logo) | Tile 1 (hand-held hero) |

Once the 9 are up, the grid shows the planned layout. After that, post new content in the same three-mood rotation: **product hero -> illustration tile -> lifestyle/process**.

## Caption drafts

Tone rules: short, lowercase-friendly, no corporate phrasing. Talk like the character. Never use "indulgent", "delicious", "must-try". One emoji max per caption.

### Tile 1 - Hand-held hero
> Fresh batch in hand.
> Order on Deliveroo, link in bio.

### Tile 2 - Logo poster
> Hi. We're Big Baby.
> NYC-style banana pudding, made fresh in Notting Hill.

### Tile 3 - Macro pudding
> Cream. Wafer. Banana. Repeat.

### Tile 4 - Cup stack
> Today's batch is ready.
> Fresh stock Mon-Fri on Deliveroo.

### Tile 5 - Dancing peel + W11
> Notting Hill's softest secret. 🍌

### Tile 6 - Notting Hill street
> Caught in the wild on Portobello.

### Tile 7 - Process shot
> Layer by layer. This is how a Big Baby gets made.

### Tile 8 - Deliveroo reel cover
> On Deliveroo every weekday. Tap the link in bio.

### Tile 9 - Spoon lift
> The first bite. Trust us.

## Hashtag set (use sparingly, max 6 per post)

Always include `#bananapudding`. Mix in 2-3 of:
`#nottinghill` `#w11` `#londonfood` `#londondessert` `#homemadepudding` `#smallbatch` `#portobellomarket` `#deliveroo`

Avoid: `#foodporn`, `#yum`, `#delicious`, any 40-tag spam blocks.

## Working photo cadence

Every shoot session, capture:
- 1 product hero (hand-held or cup stack)
- 1 macro texture or spoon shot
- 1 lifestyle (street, behind counter, plating)
- 1 candid extra for stories

That's a week of grid content in 30 minutes.

## Workflow

1. Take photo on phone, natural light, plain background.
2. AirDrop or save into `photos_in/` folder of this repo.
3. Run `python3 build_post.py photos_in/your_photo.jpg --bg brown` (or `--bg cream`).
4. Result lands in `photos_out/` as a 1080x1080 PNG, ready to post.
5. Caption from the list above. Schedule the post.
