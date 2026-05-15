# Big Baby Banana Pudding — Brand Repo

Working folder for `@bigbabypudding` Instagram, packaging, and print collateral.

## Contents

```
branding/                       Source brand assets
  Character/                    Mascot character art (PNG + AI)
  Cup Design JPG For Viewing/   Cup wrap, lid, rim previews
  Little Bananas/               Three banana characters (PNG + AI)
  Logo/                         Wordmark variants (with / without character / bg)
  Vector Files for Print/       Print-ready AI files for the cup wrap and lid
  Coloursheet.jpg               Full original 6-color sheet from the designer
  Deliveroo_Hero_Image.jpg      Hero image for Deliveroo listing
  Visualiser_Final_Version.pdf  Designer's full visualiser

fonts/
  Bradley Hand Bold.ttf         The only display font used in designs

build_grid_mockup.py            Renders the 3x3 IG grid plan
build_profile_mockup.py         Renders the full IG profile page (header + bio + grid)
build_card.py                   Renders the Deliveroo bag-insert business card

grid_mockup.png                 Output: 3x3 grid plan
profile_mockup.png              Output: full IG profile mockup
card_mockup.png                 Output: business card (UK 85x55mm @ 600dpi)
```

## Locked brand rules

### Palette (two colors only)
- `#fffae2` cream — default background
- `#39251c` dark brown — typography, character outlines, dark tile backgrounds

Yellow (`#ffe256`) and baby blue (`#c2dff6`) only appear inside the character art and real product photos. Never use them as tile backgrounds.

Tan and pink from the original colour sheet are not used.

### Font
**Bradley Hand Bold** is the only display font. It matches the hand-drawn brush feel of the "Big Baby Banana Pudding" logo wordmark. Already included in `fonts/`.

### Voice rules for copy
- Friendly, storybook tone — like a note from the character
- Short sentences, no corporate phrasing
- No em-dashes or colons in body copy (use periods, commas, or restructure)
- "Batch" instead of "order" for the homemade feel

## How to use (on any Mac)

```bash
# clone the repo
git clone git@github.com:amirhajian-keyrock/bigbabypudding-branding.git
cd bigbabypudding-branding

# install Python deps (Pillow is the only one)
pip install -r requirements.txt

# regenerate any mockup
python3 build_card.py
python3 build_grid_mockup.py
python3 build_profile_mockup.py
```

The scripts look for `Bradley Hand Bold.ttf` in `fonts/` first, then fall back to the macOS system copy at `/System/Library/Fonts/Supplemental/`. Either path works.

## Print specs

### Business card (`card_mockup.png`)
- Trim: 85 x 55 mm (UK standard, landscape)
- Resolution: 600 dpi (2008 x 1299 px)
- Add 3 mm bleed when sending to a printer (final 91 x 61 mm / 2150 x 1441 px)
- 2-color print: cream + dark brown
- Matte uncoated or recycled kraft stock recommended

### Instagram tiles
- Square 1080 x 1080 px minimum
- Same two-color palette
- Bradley Hand Bold for any text overlay

## Workflow notes

- Always commit and push generated mockups so the latest preview is visible on GitHub
- When editing copy or design, edit the relevant `build_*.py` script and re-run — don't hand-edit the output PNGs
- New brand assets from the designer go in `branding/` keeping the existing folder structure

## Instagram transformation plan

Move from the current scattered grid toward the @beignetbeignetuk style of coherence, but using the storybook character world (not minimalist food photography).

The 9-post plan in `grid_mockup.png`:
1. Hand-held cup hero (dark/neutral bg, soft daylight)
2. Logo poster (cream, brand anchor)
3. Macro pudding texture (cream)
4. Cup stack showing wrap + lid (dark/neutral)
5. Dancing peel + "Made fresh in W11." (cream)
6. Notting Hill street lifestyle (dark/neutral)
7. Process shot — banana slices + wafer layers (cream)
8. Reel cover: Deliveroo announcement (cream)
9. Spoon lift / single bite (cream)

Three tiles (2, 5, 8) are production-ready. The other six need real photos shot to spec.
