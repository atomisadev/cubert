import { cn } from "@/lib/utils";
import { ColorValue } from "@/lib/cube-constants";

interface StickerProps {
  color: ColorValue;
  onClick: () => void;
  sizeClassName?: string;
}

export function Sticker({
  color,
  onClick,
  sizeClassName = "w-8 h-8 sm:w-10 sm:h-10",
}: StickerProps) {
  return (
    <button
      type="button"
      aria-label={`Sticker color ${color}`}
      className={cn(
        sizeClassName,
        "border border-border/50 transition-colors hover:border-primary/50 focus:outline-none focus:ring-1 focus:ring-ring"
      )}
      style={{ backgroundColor: color }}
      onClick={onClick}
    />
  );
}
