# Remotion — Higher-quality reels and videos

React-based video creation. Replaces the PIL-GIF workflow for higher quality output (smooth 30fps, proper easings, spring physics, audio support).

## Setup (one-time)

```bash
cd remotion
npm install
```

## Commands

```bash
# Live preview in browser (best for iterating)
npm run dev

# Render a specific composition to MP4
npx remotion render SneakyBanana out/sneaky_banana.mp4
npx remotion render SneakyBananaReel out/sneaky_banana_reel_vertical.mp4
```

## Project structure

```
remotion/
├── package.json
├── tsconfig.json
├── remotion.config.ts          render config
├── src/
│   ├── index.ts                entry point
│   ├── Root.tsx                composition registry
│   └── SneakyBanana.tsx        first reel — sneaky banana
├── public/                     static assets (brand PNGs)
│   ├── banana_walking.png
│   ├── banana_dancing.png
│   └── character.png
└── out/                        rendered MP4s (gitignored)
```

## Adding a new reel

1. Write the component in `src/<Name>.tsx`
2. Register it in `src/Root.tsx` as a `<Composition>` with width/height/fps/durationInFrames
3. Run `npx remotion render <Id> out/<filename>.mp4`

## Quality vs the old PIL workflow

| | PIL GIF | Remotion |
|---|---|---|
| FPS | 8-12 | 30+ |
| Easing | linear | spring + easing functions |
| Resolution | 720 upscaled | native 1080×1080 / 1080×1920 |
| Smoothness | choppy | smooth |
| File size (7s) | 700KB GIF | 550KB MP4 |
| Iteration | re-run script | hot-reload in `npm run dev` |
| Audio | impossible | full support |

## Final renders also copied to `../posts/reels/` for easy access
