import { AbsoluteFill, Img, staticFile, useCurrentFrame, useVideoConfig, interpolate, spring, Easing } from "remotion";

const CREAM = "#faf8f0";
const BROWN = "#39251c";

export const WaferRoll: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();

  const rollStart = 0.5 * fps;
  const rollEnd = 2.5 * fps;
  const settleEnd = 3 * fps;
  const captionStart = 3 * fps;

  const wafer_x = interpolate(
    frame,
    [rollStart, rollEnd],
    [-400, width / 2],
    {
      easing: Easing.out(Easing.cubic),
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    }
  );

  const radius = 220;
  const distanceTravelled = wafer_x - (-400);
  const rotationFromRoll = (distanceTravelled / (2 * Math.PI * radius)) * 360;

  let wobble = 0;
  if (frame >= rollEnd && frame <= settleEnd) {
    const t = (frame - rollEnd) / (settleEnd - rollEnd);
    wobble = Math.sin(t * Math.PI * 4) * 15 * (1 - t);
  }
  const rotation = rotationFromRoll + wobble;

  const wafer_y = height / 2 + 50;

  const captionProgress = spring({
    frame: frame - captionStart,
    fps,
    config: { damping: 14, stiffness: 100 },
  });
  const captionOpacity = interpolate(captionProgress, [0, 1], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const captionY = interpolate(captionProgress, [0, 1], [40, 0]);

  return (
    <AbsoluteFill style={{ background: CREAM, alignItems: "center", justifyContent: "center" }}>
      <div
        style={{
          position: "absolute",
          top: height * 0.13,
          width: "100%",
          textAlign: "center",
          fontFamily: "Bradley Hand, cursive",
          fontWeight: "bold",
          fontSize: height < 1500 ? 64 : 80,
          color: BROWN,
          opacity: captionOpacity,
          transform: `translateY(${captionY}px)`,
        }}
      >
        Wafer you been all my life?
      </div>
      {frame >= rollStart && (
        <Img
          src={staticFile("wafer.png")}
          style={{
            position: "absolute",
            left: wafer_x - radius,
            top: wafer_y - radius,
            width: radius * 2,
            height: radius * 2,
            transform: `rotate(${rotation}deg)`,
            transformOrigin: "center center",
          }}
        />
      )}
    </AbsoluteFill>
  );
};
