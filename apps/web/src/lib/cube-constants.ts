export const RUBIKS_COLORS = {
  WHITE: "#FFFFFF",
  YELLOW: "#FFD700",
  RED: "#B71C1C",
  ORANGE: "#FF6F00",
  BLUE: "#0D47A1",
  GREEN: "#1B5E20",
  EMPTY: "#E0E0E0",
} as const;

export type ColorId = keyof typeof RUBIKS_COLORS;
export type ColorValue = (typeof RUBIKS_COLORS)[ColorId];

export const COLOR_PALETTE: ColorValue[] = [
  RUBIKS_COLORS.WHITE,
  RUBIKS_COLORS.YELLOW,
  RUBIKS_COLORS.RED,
  RUBIKS_COLORS.ORANGE,
  RUBIKS_COLORS.BLUE,
  RUBIKS_COLORS.GREEN,
];

export const FACE_NAMES = ["U", "L", "F", "R", "B", "D"] as const;
export type FaceName = (typeof FACE_NAMES)[number];

export type FaceColors = ColorValue[];

export interface CubeState {
  U: FaceColors;
  L: FaceColors;
  F: FaceColors;
  R: FaceColors;
  B: FaceColors;
  D: FaceColors;
}

export const INITIAL_CUBE_STATE: CubeState = {
  U: Array(9).fill(RUBIKS_COLORS.WHITE),
  L: Array(9).fill(RUBIKS_COLORS.ORANGE),
  F: Array(9).fill(RUBIKS_COLORS.GREEN),
  R: Array(9).fill(RUBIKS_COLORS.RED),
  B: Array(9).fill(RUBIKS_COLORS.BLUE),
  D: Array(9).fill(RUBIKS_COLORS.YELLOW),
};

export const THREE_FACE_ORDER: FaceName[] = ["R", "L", "U", "D", "F", "B"];
