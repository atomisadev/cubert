"use client";

import { useState } from "react";
import { ColorPalette } from "./color-palette";
import { UnwrappedCubeGrid } from "./unwrapped-cube-grid";
import {
  CubeState,
  INITIAL_CUBE_STATE,
  ColorValue,
  FaceName,
  RUBIKS_COLORS,
} from "@/lib/cube-constants";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";

interface CubeEditorProps {
  initialState?: CubeState;
  onCubeStateChange?: (newState: CubeState) => void;
  className?: string;
}

export function CubeEditor({
  initialState = INITIAL_CUBE_STATE,
  onCubeStateChange,
  className,
}: CubeEditorProps) {
  const [cubeState, setCubeState] = useState<CubeState>(initialState);
  const [selectedColor, setSelectedColor] = useState<ColorValue>(
    RUBIKS_COLORS.WHITE
  );

  const handleStickerClick = (face: FaceName, stickerIndex: number) => {
    if (!selectedColor) return;

    const newFaceColors = [...cubeState[face]];
    newFaceColors[stickerIndex] = selectedColor;
    const newState = { ...cubeState, [face]: newFaceColors };
    setCubeState(newState);
    if (onCubeStateChange) {
      onCubeStateChange(newState);
    }
  };

  const handleReset = () => {
    setCubeState(INITIAL_CUBE_STATE);
    if (onCubeStateChange) {
      onCubeStateChange(INITIAL_CUBE_STATE);
    }
  };

  return (
    <div
      className={cn(
        "flex flex-col items-center gap-4 p-4 rounded-lg bg-card text-card-foreground shadow-xl w-full max-w-md",
        className
      )}
    >
      <h2 className="text-xl font-semibold text-center">Edit Cube Faces</h2>
      <ColorPalette
        selectedColor={selectedColor}
        onColorSelect={setSelectedColor}
        className="mb-4"
      />
      <UnwrappedCubeGrid
        cubeState={cubeState}
        onStickerClick={handleStickerClick}
      />
      <Button
        // appName="Cubert"
        className="mt-4 px-4 py-2 bg-primary text-primary-foreground rounded-md hover:bg-primary/90 transition-colors"
        onClick={handleReset}
      >
        Reset Cube
      </Button>
    </div>
  );
}
