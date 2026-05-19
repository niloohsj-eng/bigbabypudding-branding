import { Composition } from "remotion";
import { SneakyBanana } from "./SneakyBanana";
import { WaferRoll } from "./WaferRoll";
import { SpoonScoop } from "./SpoonScoop";

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition id="SneakyBanana" component={SneakyBanana} durationInFrames={210} fps={30} width={1080} height={1080} />
      <Composition id="SneakyBananaReel" component={SneakyBanana} durationInFrames={210} fps={30} width={1080} height={1920} />
      <Composition id="WaferRoll" component={WaferRoll} durationInFrames={180} fps={30} width={1080} height={1080} />
      <Composition id="WaferRollReel" component={WaferRoll} durationInFrames={180} fps={30} width={1080} height={1920} />
      <Composition id="SpoonScoop" component={SpoonScoop} durationInFrames={210} fps={30} width={1080} height={1080} />
      <Composition id="SpoonScoopReel" component={SpoonScoop} durationInFrames={210} fps={30} width={1080} height={1920} />
    </>
  );
};
