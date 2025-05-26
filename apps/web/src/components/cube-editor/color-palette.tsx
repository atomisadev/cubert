import { cn } from "@/lib/utils";
import { ColorValue, COLOR_PALETTE } from "@/lib/cube-constants";

interface ColorPaletteProps {
  selectedColor: ColorValue | null;
  onColorSelect: (color: ColorValue) => void;
  className?: string;
}

export function ColorPalette({
  selectedColor,
  onColorSelect,
  className,
}: ColorPaletteProps) {
  return (
    <div
      className={cn(
        "flex flex-wrap justify-center gap-2 p-2 bg-muted rounded-md",
        className
      )}
    >
      {COLOR_PALETTE.map((color) => (
        <button
          key={color}
          type="button"
          aria-label={`Select color ${color}`}
          className={cn(
            "w-8 h-8 sm:w-10 sm:h-10 rounded-md border-2 transition-all focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 focus:ring-offset-background",
            selectedColor === color
              ? "border-primary ring-2 ring-primary"
              : "border-border hover:border-primary/70"
          )}
          style={{ backgroundColor: color }}
          onClick={() => onColorSelect(color)}
        />
      ))}
    </div>
  );
}
