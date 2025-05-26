import { Sticker } from "./sticker";
import { FaceColors, ColorValue } from "@/lib/cube-constants";
import { cn } from "@/lib/utils";

interface FaceGridProps {
  faceColors: FaceColors;
  onStickerClick: (stickerIndex: number) => void;
  className?: string;
}

export function FaceGrid({
  faceColors,
  onStickerClick,
  className,
}: FaceGridProps) {
  return (
    <div
      className={cn(
        "grid grid-cols-3 gap-0.5 bg-border p-0.5 rounded-sm shadow-md",
        className
      )}
    >
      {faceColors.map((color, index) => (
        <Sticker
          key={index}
          color={color}
          onClick={() => onStickerClick(index)}
        />
      ))}
    </div>
  );
}
