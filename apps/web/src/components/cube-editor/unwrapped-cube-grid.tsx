import { FaceGrid } from "./face-grid";
import { CubeState, FaceName, ColorValue } from "@/lib/cube-constants";

interface UnwrappedCubeGridProps {
  cubeState: CubeState;
  onStickerClick: (face: FaceName, stickerIndex: number) => void;
}

export function UnwrappedCubeGrid({
  cubeState,
  onStickerClick,
}: UnwrappedCubeGridProps) {
  const faceOrderForNet: { face: FaceName; area: string }[] = [
    { face: "U", area: "top" },
    { face: "L", area: "left" },
    { face: "F", area: "front" },
    { face: "R", area: "right" },
    { face: "B", area: "back" },
    { face: "D", area: "bottom" },
  ];

  return (
    <div className="grid grid-cols-[repeat(4,minmax(0,1fr))] grid-rows-[repeat(3,minmax(0,1fr))] gap-1 w-full max-w-xs sm:max-w-sm md:max-w-md aspect-[4/3]">
      {/*
        Layout for a common Rubik's cube net:
            U
          L F R B
            D
        Grid areas:
        ". top . ."
        "left front right back"
        ". bottom . ."
      */}
      {faceOrderForNet.map(({ face, area }) => (
        <div
          key={face}
          style={{ gridArea: area }}
          className="flex items-center justify-center"
        >
          <FaceGrid
            faceColors={cubeState[face]}
            onStickerClick={(stickerIndex) =>
              onStickerClick(face, stickerIndex)
            }
          />
        </div>
      ))}
      <style jsx>{`
        .grid {
          grid-template-areas:
            ". top . ."
            "left front right back"
            ". bottom . .";
        }
      `}</style>
    </div>
  );
}
