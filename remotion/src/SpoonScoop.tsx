import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  spring,
  Easing,
} from "remotion";

const BG          = "#faf8f0";
const BROWN       = "#39251c";
const YELLOW      = "#ffe256";
const NILLA       = "#b8854d";
const CREAM_FILL  = "#fff8e6";
const SW          = 5;

function CreamSurface({ width, height, surfaceY, xPhase = 0 }: { width: number; height: number; surfaceY: number; xPhase?: number }) {
  // 10 segments to stay in sync with waveAtX math, but gentle amplitude (20px) = soft swirly look
  const segs  = 12; // extra to cover the xPhase overflow on the right
  const segW  = width / 10;
  const amp   = 20; // gentle — cream mounds, not sharp zigzag
  const totalW = width + xPhase + segW;
  let d = `M 0,${surfaceY}`;
  for (let i = 0; i < segs; i++) {
    const x1 = i * segW + segW * 0.3;
    const y1 = surfaceY - (i % 2 === 0 ? amp : -amp);
    const x2 = i * segW + segW * 0.7;
    const y2 = surfaceY - (i % 2 === 0 ? amp : -amp);
    const x3 = (i + 1) * segW;
    d += ` C ${x1},${y1} ${x2},${y2} ${x3},${surfaceY}`;
  }
  d += ` L ${totalW},${height} L 0,${height} Z`;

  return (
    <svg style={{ position: "absolute", top: 0, left: -xPhase }} width={totalW} height={height}>
      {/* Cream body */}
      <path d={d} fill={CREAM_FILL} stroke={BROWN} strokeWidth={4} strokeLinejoin="round" />
      {/* Original 3 swirl positions, xPhase-adjusted to stay screen-centred */}
      <path d={`M ${width*0.12+xPhase},${surfaceY+70} Q ${width*0.22+xPhase},${surfaceY+30} ${width*0.32+xPhase},${surfaceY+70}`}
        fill="none" stroke={BROWN} strokeWidth={3} strokeLinecap="round" />
      <path d={`M ${width*0.38+xPhase},${surfaceY+100} Q ${width*0.50+xPhase},${surfaceY+55} ${width*0.62+xPhase},${surfaceY+100}`}
        fill="none" stroke={BROWN} strokeWidth={3} strokeLinecap="round" />
      <path d={`M ${width*0.68+xPhase},${surfaceY+70} Q ${width*0.78+xPhase},${surfaceY+30} ${width*0.88+xPhase},${surfaceY+70}`}
        fill="none" stroke={BROWN} strokeWidth={3} strokeLinecap="round" />
    </svg>
  );
}

// Cream pull — soft pudding blob rooted at the cream surface, stretches as wafer rises.
// No hard outline so it blends with the cream body; a swirl inside reads as pudding texture.
function CreamPull({ cx, topY, bottomY, opacity = 1 }: { cx: number; topY: number; bottomY: number; opacity?: number }) {
  const h = bottomY - topY;
  if (h <= 4) return null;
  const hw = 90; // half-width — blob bulges generously
  return (
    <svg style={{ position: "absolute", left: cx - hw, top: topY, opacity }} width={hw * 2} height={h}>
      {/* Soft rounded blob — wide at top (near wafer), pinches slightly, wide at base */}
      <path
        d={`M ${hw - 44},0
            C ${hw - 90},${h * 0.25} ${hw - 90},${h * 0.75} ${hw - 70},${h}
            L ${hw + 70},${h}
            C ${hw + 90},${h * 0.75} ${hw + 90},${h * 0.25} ${hw + 44},0
            Z`}
        fill={CREAM_FILL}
        stroke={BROWN}
        strokeWidth={1.5}
        strokeOpacity={0.3}
        strokeLinejoin="round"
      />
      {/* Cream swirl mark inside — same style as the pudding surface swirls */}
      <path
        d={`M ${hw - 28},${h * 0.35} Q ${hw},${h * 0.18} ${hw + 28},${h * 0.35}`}
        fill="none"
        stroke={BROWN}
        strokeWidth={2}
        strokeOpacity={0.45}
        strokeLinecap="round"
      />
      <path
        d={`M ${hw - 22},${h * 0.62} Q ${hw},${h * 0.48} ${hw + 22},${h * 0.62}`}
        fill="none"
        stroke={BROWN}
        strokeWidth={2}
        strokeOpacity={0.45}
        strokeLinecap="round"
      />
    </svg>
  );
}

// Slightly wobbly circle path — hand-drawn feel, centered at 0,0 radius ~120
const WAFER_PATH =
  "M 4,-123 C 68,-132 130,-62 126,4 C 122,68 58,128 -3,124 C -66,120 -130,56 -126,-5 C -122,-64 -62,-114 4,-123 Z";

function Wafer({
  cx,
  cy,
  panicked = false,
  lookingUp = false,
  opacity = 1,
  wiggle = 0,
  rotation = 0,
}: {
  cx: number;
  cy: number;
  panicked?: boolean;
  lookingUp?: boolean;
  opacity?: number;
  wiggle?: number;
  rotation?: number;
}) {
  const size = 300;
  const r = size / 2;
  return (
    <svg
      style={{
        position: "absolute",
        left: cx - r + wiggle,
        top: cy - r,
        opacity,
        transform: `rotate(${rotation}deg)`,
        transformOrigin: "center center",
      }}
      width={size}
      height={size}
      viewBox="-150 -150 300 300"
    >
      {/* Wafer body — nilla fill with brown outline */}
      <path
        d={WAFER_PATH}
        fill={NILLA}
        stroke={BROWN}
        strokeWidth={SW}
        strokeLinejoin="round"
      />
      {panicked ? (
        <>
          <circle cx="-16" cy="-10" r="4" fill={BROWN} />
          <circle cx="16" cy="-10" r="4" fill={BROWN} />
          <ellipse cx="0" cy="42" rx="7" ry="6" fill="none" stroke={BROWN} strokeWidth="3" />
        </>
      ) : lookingUp ? (
        <>
          {/* Eyes shifted up — no smile */}
          <circle cx="-16" cy="-32" r="3" fill={BROWN} />
          <circle cx="16" cy="-32" r="3" fill={BROWN} />
        </>
      ) : (
        <>
          <circle cx="-16" cy="-8" r="3" fill={BROWN} />
          <circle cx="16" cy="-8" r="3" fill={BROWN} />
          <path
            d="M -8 28 Q 0 31 8 28"
            stroke={BROWN}
            strokeWidth="3.5"
            fill="none"
            strokeLinecap="round"
          />
        </>
      )}
    </svg>
  );
}

function Spoon({ cx, tipY, bowlScale = 1, rotation = 0 }: { cx: number; tipY: number; bowlScale?: number; rotation?: number }) {
  const handleW  = 15;
  const handleH  = 310;
  const bowlRx   = 38 * bowlScale;
  const bowlRy   = 58 * bowlScale;
  const svgW     = bowlRx * 2 + 24;
  const svgH     = handleH + bowlRy * 2 + 10;
  const midX     = svgW / 2;
  const stripeH  = 18;
  // Pivot rotation around the bowl centre so the bowl stays put while the handle swings
  const pivotX   = midX;
  const pivotY   = handleH + bowlRy;

  const handlePath = `M ${midX - handleW / 2},8 Q ${midX - handleW / 2 - 3},${handleH / 2} ${midX - handleW / 2},${handleH}
      L ${midX + handleW / 2},${handleH} Q ${midX + handleW / 2 + 3},${handleH / 2} ${midX + handleW / 2},8 Z`;

  return (
    <svg
      style={{
        position: "absolute",
        left: cx - svgW / 2,
        top: tipY - svgH,
        transform: `rotate(${rotation}deg)`,
        transformOrigin: `${pivotX}px ${pivotY}px`,
      }}
      width={svgW}
      height={svgH}
      viewBox={`0 0 ${svgW} ${svgH}`}
    >
      <defs>
        {/* Alternating blue / pale yellow stripes — horizontal across handle */}
        <pattern id="rimStripes" patternUnits="userSpaceOnUse" width={svgW} height={stripeH * 2}>
          <rect width={svgW} height={stripeH} fill="#c2dff6" />
          <rect y={stripeH} width={svgW} height={stripeH} fill="#f5eec8" />
        </pattern>
        <clipPath id="handleClip">
          <path d={handlePath} />
        </clipPath>
      </defs>

      {/* Handle — striped fill, clipped to handle shape, outline on top */}
      <rect
        width={svgW}
        height={handleH + 10}
        fill="url(#rimStripes)"
        clipPath="url(#handleClip)"
      />
      <path
        d={handlePath}
        fill="none"
        stroke={BROWN}
        strokeWidth={SW}
        strokeLinejoin="round"
      />

      {/* Bowl — stays yellow */}
      <ellipse
        cx={midX}
        cy={handleH + bowlRy}
        rx={bowlRx}
        ry={bowlRy}
        fill={YELLOW}
        stroke={BROWN}
        strokeWidth={SW}
      />
    </svg>
  );
}

export const SpoonScoop: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();

  // --- Timeline ---
  const rollStart    = 0;
  const rollEnd      = 1.0 * fps;  // wafer finishes rolling in
  const settleEnd    = 1.6 * fps;  // settle wobble done, wafer sits happy
  const spoonStart   = 2.2 * fps;  // spoon starts descending
  const noticeFrame  = 3.0 * fps;  // wafer notices
  const arriveFrame  = 3.9 * fps;  // spoon arrives at wafer level
  const scoopFrame   = 5.0 * fps;  // bowl fully expanded, shoots up
  const goneFrame    = 5.6 * fps;  // everything off screen
  const captionStart = 5.9 * fps;

  const waferCX = width / 2;
  const waferCY = height * 0.50;

  // Roll-in from left
  const waferRollX = interpolate(
    frame,
    [rollStart, rollEnd],
    [-200, waferCX],
    { easing: Easing.out(Easing.cubic), extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );
  const waferCXAnimated = frame < rollEnd ? waferRollX : waferCX;

  // Phase-shift the wave so a valley (odd-segment midpoint) aligns at waferCX.
  // With xPhase = segW/2, at x=waferCX the phased coord lands at seg 5 midpoint (odd → valley).
  // Valley sits 21px below surfaceY (amp*3*0.5*0.5 = 28*0.75 ≈ 21).
  // Setting surfaceY = waferCY + 129 makes valley = waferCY + 150, so wafer center at rest = waferCY.
  const waveSegW = width / 10;
  const waveAmp  = 20; // matches CreamSurface amp
  const xPhase   = waveSegW / 2; // 54px — valley at seg 5 midpoint aligns with waferCX
  // Valley depth = 20 * 3 * 0.5 * 0.5 = 15px → surfaceY = waferCY + 135 keeps wafer center at waferCY
  const surfaceY = waferCY + 135;
  const waveAtX = (x: number): number => {
    const cx = Math.max(0, x + xPhase);
    const i  = Math.min(Math.floor(cx / waveSegW), 11);
    const t  = (cx - i * waveSegW) / waveSegW;
    return surfaceY + (i % 2 === 0 ? -1 : 1) * waveAmp * 3 * t * (1 - t);
  };

  // Rotation from rolling (distance-based) + settle wobble
  const distanceTraveled = waferRollX - (-200);
  const rollRotation = (distanceTraveled / (2 * Math.PI * 150)) * 360;
  const settleWobble =
    frame >= rollEnd && frame < settleEnd
      ? Math.sin(((frame - rollEnd) / (settleEnd - rollEnd)) * Math.PI * 3) * 18 * (1 - (frame - rollEnd) / (settleEnd - rollEnd))
      : 0;
  const waferRotation = frame < rollEnd ? rollRotation : settleWobble;

  // Idle bounce
  const idleBounce = frame >= settleEnd && frame < noticeFrame ? Math.sin(frame * 0.18) * 10 : 0;

  // Look up tilt — wafer leans back to spot the spoon before panicking
  const lookUpFrame = noticeFrame - 0.6 * fps;
  const lookUpTilt = interpolate(
    frame,
    [lookUpFrame, noticeFrame],
    [0, -22],
    { easing: Easing.inOut(Easing.quad), extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );
  const lookUp = frame >= lookUpFrame && frame < noticeFrame ? lookUpTilt : 0;

  // Panic wiggle — short burst only after looking up
  const wiggleEnd = noticeFrame + 0.5 * fps;
  const panicWiggle =
    frame >= noticeFrame && frame < wiggleEnd
      ? Math.sin(frame * 2.0) * 16
      : 0;

  // Wafer sits embedded in the cream: center 60px lower than waferCY so the
  // bottom ~60px of the wafer is submerged below the cream surface.
  const waferEmbedY = waferCY + 60;

  const waferScoopY = interpolate(
    frame,
    [scoopFrame, goneFrame],
    [waferEmbedY, -380],
    { easing: Easing.in(Easing.cubic), extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );
  // Roll-in: ride the wave surface at the embedded depth (–90 instead of –150)
  const waferOnWaveY = waveAtX(waferCXAnimated) - 90;
  const waferY = frame < rollEnd
    ? waferOnWaveY
    : frame < scoopFrame
    ? waferEmbedY + idleBounce
    : waferScoopY;

  const waferOpacity = interpolate(frame, [scoopFrame, goneFrame], [1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Spoon enters from upper-right, tilted, sweeps left as bowl digs into cream
  const spoonCX = interpolate(
    frame,
    [spoonStart, arriveFrame, scoopFrame],
    [waferCX + 180, waferCX + 30, waferCX],
    { easing: Easing.out(Easing.cubic), extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

  // Tilt: 35° clockwise on entry → -6° (scooping angle) by scoop time
  const spoonRotation = interpolate(
    frame,
    [spoonStart, arriveFrame, scoopFrame, goneFrame],
    [35, 18, -6, -6],
    { easing: Easing.inOut(Easing.cubic), extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

  // Bowl dips well below the embedded wafer to scoop underneath it
  const spoonTipY = interpolate(
    frame,
    [spoonStart, arriveFrame, scoopFrame, goneFrame],
    [-80, waferEmbedY + 230, waferEmbedY + 230, -500],
    {
      easing: Easing.in(Easing.cubic),
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    }
  );

  // Wafer tilts slightly as it tips onto the spoon
  const waferScoopTilt = interpolate(
    frame,
    [arriveFrame, scoopFrame, goneFrame],
    [0, -14, -14],
    { easing: Easing.out(Easing.cubic), extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

  // Caption
  const captionSpring = spring({
    frame: frame - captionStart,
    fps,
    config: { damping: 14, stiffness: 100 },
  });
  const captionOpacity = interpolate(captionSpring, [0, 1], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const captionTranslate = interpolate(captionSpring, [0, 1], [40, 0]);

  // Bowl expands as it scoops (slightly less dramatic — the tilt does more work now)
  const bowlScale = interpolate(
    frame,
    [arriveFrame, scoopFrame],
    [1, 2.8],
    { easing: Easing.out(Easing.cubic), extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

  const panicked  = frame >= noticeFrame && frame < goneFrame;
  const showWafer = frame < goneFrame;
  const showSpoon = frame >= spoonStart && frame < goneFrame;

  return (
    <AbsoluteFill style={{ background: BG }}>
      {/* Cream pudding surface — bottom half, wafer rolls on top */}
      <CreamSurface width={width} height={height} surfaceY={surfaceY} xPhase={xPhase} />
      {/* Spoon behind wafer — renders first so wafer stays in front */}
      {showSpoon && <Spoon cx={spoonCX} tipY={spoonTipY} bowlScale={bowlScale} rotation={spoonRotation} />}
      {/* Cream pull — tapered shape rooted at cream surface, stretches up with wafer */}
      {frame >= arriveFrame && frame < goneFrame && (
        <CreamPull
          cx={waferCX}
          topY={waferY + 120}
          bottomY={waveAtX(waferCX)}
          opacity={waferOpacity}
        />
      )}
      {showWafer && (
        <Wafer
          cx={waferCXAnimated}
          cy={waferY}
          panicked={panicked}
          lookingUp={!panicked && frame >= lookUpFrame - 0.4 * fps && frame < noticeFrame}
          opacity={waferOpacity}
          wiggle={panicWiggle}
          rotation={waferRotation + lookUp + waferScoopTilt}
        />
      )}
      {frame >= captionStart && (
        <div
          style={{
            position: "absolute",
            bottom: height * 0.08,
            width: "100%",
            textAlign: "center",
            fontFamily: "Bradley Hand, cursive",
            fontWeight: 300,
            fontSize: height < 1500 ? 80 : 96,
            color: BROWN,
            opacity: captionOpacity,
            transform: `translateY(${captionTranslate}px)`,
          }}
        >
          Gone in 3 seconds.
        </div>
      )}
    </AbsoluteFill>
  );
};
