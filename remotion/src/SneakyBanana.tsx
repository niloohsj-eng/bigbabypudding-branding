import { AbsoluteFill, Img, staticFile, useCurrentFrame, useVideoConfig, interpolate, spring, Easing } from "remotion";

const CREAM = "#fffae2";
const BROWN = "#39251c";
const PUDDING_WHITE = "#fff8e6";

// ---- The cup ----
const Cup: React.FC<{ creamH: number }> = ({ creamH }) => {
  // Drawn with CSS — clean cup shape with rim + cream mound
  const cupWidth = 280;
  const cupHeight = 250;
  const rimHeight = 16;
  return (
    <div style={{ position: "absolute", left: "50%", bottom: 200, transform: "translateX(-50%)", width: cupWidth }}>
      {/* Cup body */}
      <div
        style={{
          position: "absolute",
          bottom: 0,
          left: 0,
          width: cupWidth,
          height: cupHeight,
          background: CREAM,
          border: `8px solid ${BROWN}`,
          borderRadius: "0 0 18% 18%",
          clipPath: `polygon(2% 0, 98% 0, 92% 100%, 8% 100%)`,
        }}
      />
      {/* Rim ellipse at the top of cup */}
      <div
        style={{
          position: "absolute",
          bottom: cupHeight - rimHeight / 2,
          left: 0,
          width: cupWidth,
          height: rimHeight,
          background: PUDDING_WHITE,
          border: `6px solid ${BROWN}`,
          borderRadius: "50%",
        }}
      />
      {/* Cream mound — sized by creamH prop */}
      {creamH > 5 && (
        <div
          style={{
            position: "absolute",
            bottom: cupHeight + rimHeight / 2 - 6,
            left: -8,
            width: cupWidth + 16,
            height: creamH,
            background: PUDDING_WHITE,
            border: `8px solid ${BROWN}`,
            borderTopLeftRadius: "50% 90%",
            borderTopRightRadius: "50% 90%",
            borderBottomLeftRadius: 0,
            borderBottomRightRadius: 0,
            borderBottom: "none",
          }}
        >
          {/* Swirl marks inside the mound */}
          {creamH > 60 && (
            <>
              <div
                style={{
                  position: "absolute",
                  bottom: creamH * 0.3,
                  left: "20%",
                  width: "60%",
                  height: 20,
                  borderBottom: `3px solid ${BROWN}`,
                  borderRadius: "0 0 50% 50%",
                }}
              />
              <div
                style={{
                  position: "absolute",
                  bottom: creamH * 0.6,
                  left: "30%",
                  width: "40%",
                  height: 16,
                  borderBottom: `3px solid ${BROWN}`,
                  borderRadius: "0 0 50% 50%",
                }}
              />
            </>
          )}
        </div>
      )}
    </div>
  );
};

// ---- Counter line ----
const Counter: React.FC = () => (
  <div
    style={{
      position: "absolute",
      bottom: 180,
      left: 0,
      right: 0,
      borderBottom: `4px solid ${BROWN}`,
    }}
  />
);

// ---- The banana character ----
const Banana: React.FC<{ x: number; y: number; rotation: number; scale: number }> = ({
  x, y, rotation, scale,
}) => {
  return (
    <Img
      src={staticFile("banana_walking.png")}
      style={{
        position: "absolute",
        left: x - 110 * scale,
        top: y - 90 * scale,
        width: 220 * scale,
        height: 180 * scale,
        transform: `rotate(${rotation}deg)`,
        transformOrigin: "center center",
      }}
    />
  );
};

// ---- Main composition ----
export const SneakyBanana: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();

  // ============ Animation timeline ============
  // Phase 1 (0-1s): empty stage with full mound
  // Phase 2 (1-3s): banana sneaks in from left, bobbing
  // Phase 3 (3-4s): looks left, then right
  // Phase 4 (4-5s): chomps mound (mound shrinks)
  // Phase 5 (5-6s): walks away with bigger scale (full belly)
  // Phase 6 (6-7s): empty stage

  // ----- Banana X position -----
  const enterStart = 1 * fps;
  const enterEnd = 3 * fps;
  const lookStart = enterEnd;
  const lookEnd = 4 * fps;
  const chompStart = lookEnd;
  const chompEnd = 5 * fps;
  const exitStart = chompEnd;
  const exitEnd = 6.5 * fps;

  // Banana position: from off-screen left to near cup (sneaky entry with easing)
  const bananaX = interpolate(
    frame,
    [enterStart, enterEnd, lookEnd, chompEnd, exitEnd],
    [-200, width * 0.42, width * 0.42, width * 0.45, width + 200],
    {
      easing: Easing.inOut(Easing.quad),
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    }
  );

  // ----- Walking bob (sinewave during walking phases) -----
  const isWalking = (frame >= enterStart && frame <= enterEnd) || (frame >= exitStart && frame <= exitEnd);
  const bobAmount = isWalking
    ? Math.sin(frame * 0.55) * 18
    : 0;
  const bananaY = height * 0.65 + bobAmount;

  // ----- Banana scale (gets bigger after eating = full belly) -----
  const fullBellyScale = spring({
    frame: frame - chompEnd,
    fps,
    config: { damping: 12, stiffness: 150 },
  });
  const bananaScale = 1 + fullBellyScale * 0.25;

  // ----- Banana rotation -----
  // Look left/right during look phase, lean forward during chomp
  let rotation = 0;
  if (frame >= lookStart && frame < lookStart + (lookEnd - lookStart) * 0.5) {
    // Look left (tilt body left = clockwise rotate)
    const t = (frame - lookStart) / ((lookEnd - lookStart) * 0.5);
    rotation = interpolate(t, [0, 0.3, 0.7, 1], [0, 18, 18, 0], {
      easing: Easing.inOut(Easing.quad),
    });
  } else if (frame >= lookStart + (lookEnd - lookStart) * 0.5 && frame < lookEnd) {
    // Look right
    const t = (frame - lookStart - (lookEnd - lookStart) * 0.5) / ((lookEnd - lookStart) * 0.5);
    rotation = interpolate(t, [0, 0.3, 0.7, 1], [0, -18, -18, 0], {
      easing: Easing.inOut(Easing.quad),
    });
  } else if (frame >= chompStart && frame < chompEnd) {
    // Lean forward into cup
    const t = (frame - chompStart) / (chompEnd - chompStart);
    rotation = interpolate(t, [0, 0.5, 1], [0, -25, -15], {
      easing: Easing.inOut(Easing.quad),
    });
  } else if (isWalking) {
    // Tiny sway while walking
    rotation = Math.sin(frame * 0.55) * 4;
  }

  // ----- Cream mound height (shrinks during chomp) -----
  const creamH = interpolate(
    frame,
    [chompStart, chompStart + (chompEnd - chompStart) * 0.4, chompEnd],
    [180, 80, 0],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

  // ----- Munch shake (small jitter during chomp) -----
  const chompShake = (frame >= chompStart && frame <= chompEnd)
    ? Math.sin(frame * 2.5) * 3
    : 0;

  return (
    <AbsoluteFill style={{ background: CREAM }}>
      <Counter />
      <Cup creamH={creamH} />
      {/* Show banana only after it enters */}
      {frame >= enterStart && frame <= exitEnd && (
        <Banana
          x={bananaX + chompShake}
          y={bananaY}
          rotation={rotation}
          scale={bananaScale}
        />
      )}
    </AbsoluteFill>
  );
};
