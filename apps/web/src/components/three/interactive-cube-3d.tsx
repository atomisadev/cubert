"use client";

import { useRef, useMemo } from "react";
import { Canvas, useFrame } from "@react-three/fiber";
import { OrbitControls } from "@react-three/drei";
import * as THREE from "three";
import {
  CubeState,
  FaceName,
  ColorValue,
  THREE_FACE_ORDER,
} from "@/lib/cube-constants";

const STICKER_SIZE = 0.95;
const CUBELET_SIZE = 1;
const GAP = 0.05;

interface CubePieceProps {
  position: [number, number, number];
  colors: (ColorValue | null)[];
}

function CubePiece({ position, colors }: CubePieceProps) {
  const materials = useMemo(() => {
    return colors.map((color) => {
      if (color) {
        return new THREE.MeshStandardMaterial({
          color: new THREE.Color(color),
          roughness: 0.7,
          metalness: 0.1,
        });
      }
      return new THREE.MeshBasicMaterial({ visible: false });
    });
  }, [colors]);

  return (
    <mesh position={position}>
      <boxGeometry args={[CUBELET_SIZE, CUBELET_SIZE, CUBELET_SIZE]} />
      {materials.map((material, index) => (
        <primitive key={index} attach={`material-${index}`} object={material} />
      ))}
    </mesh>
  );
}

interface RubiksCubeProps {
  cubeState: CubeState;
}

function RubiksCube({ cubeState }: RubiksCubeProps) {
  const groupRef = useRef<THREE.Group>(null!);

  // Optional: add rotation for demonstration
  // useFrame((_state, delta) => {
  //   if (groupRef.current) {
  //     groupRef.current.rotation.y += delta * 0.05;
  //     groupRef.current.rotation.x += delta * 0.02;
  //   }
  // });

  const cubelets = useMemo(() => {
    const pieces = [];
    const N = 3;
    const offset = (N - 1) / 2;

    for (let x = 0; x < N; x++) {
      // Iterates from "left" to "right" in model space
      for (let y = 0; y < N; y++) {
        // Iterates from "bottom" to "top" in model space
        for (let z = 0; z < N; z++) {
          // Iterates from "back" to "front" in model space

          if (x > 0 && x < N - 1 && y > 0 && y < N - 1 && z > 0 && z < N - 1) {
            continue; // Skip internal piece
          }

          const pos: [number, number, number] = [
            (x - offset) * (CUBELET_SIZE + GAP),
            (y - offset) * (CUBELET_SIZE + GAP),
            (z - offset) * (CUBELET_SIZE + GAP),
          ];

          const pieceColors: (ColorValue | null)[] = [
            null,
            null,
            null,
            null,
            null,
            null,
          ];
          // Material order for BoxGeometry: Right (+X), Left (-X), Top (+Y), Bottom (-Y), Front (+Z), Back (-Z)

          // For each face, we want 2D array row 0 to be the "top" row of the 3D face.
          // 2D array index: row * N + col.
          // (N-1-y_on_face_coord) for row index to flip from 3D bottom-up (y) to 2D top-down.

          // Right Face (+X), when x = N-1
          if (x === N - 1) {
            // y is vertical (0=bottom, N-1=top), z is depth (0=back, N-1=front on this face)
            // 2D row should be (N-1-y), 2D col should be z
            pieceColors[0] = cubeState.R[(N - 1 - y) * N + z];
          }
          // Left Face (-X), when x = 0
          if (x === 0) {
            // y is vertical (0=bottom, N-1=top), z is depth (0=back on this face, N-1=front)
            // For L face, viewed from outside, (N-1-z) maps 3D front to 2D left-col
            // 2D row (N-1-y), 2D col (N-1-z)
            pieceColors[1] = cubeState.L[(N - 1 - y) * N + (N - 1 - z)];
          }
          // Top Face (+Y), when y = N-1
          if (y === N - 1) {
            // z is depth "down" the face (0=back, N-1=front), x is horizontal
            // 2D row should be z (to map 2D top row (idx 0) to 3D back row (z=0))
            // 2D col should be x
            pieceColors[2] = cubeState.U[z * N + x];
          }
          // Bottom Face (-Y), when y = 0
          if (y === 0) {
            // z is depth "up" the face (0=back, N-1=front), x is horizontal
            // 2D row should be (N-1-z) (to map 2D top row (idx 0) to 3D front row (z=N-1))
            // 2D col should be x
            pieceColors[3] = cubeState.D[(N - 1 - z) * N + x];
          }
          // Front Face (+Z), when z = N-1
          if (z === N - 1) {
            // y is vertical (0=bottom, N-1=top), x is horizontal
            // 2D row (N-1-y), 2D col x
            pieceColors[4] = cubeState.F[(N - 1 - y) * N + x];
          }
          // Back Face (-Z), when z = 0
          if (z === 0) {
            // y is vertical (0=bottom, N-1=top), x is horizontal (0=left, N-1=right on this face)
            // For B face, viewed from outside, (N-1-x) maps 3D right to 2D left-col
            // 2D row (N-1-y), 2D col (N-1-x)
            pieceColors[5] = cubeState.B[(N - 1 - y) * N + (N - 1 - x)];
          }

          pieces.push({
            id: `${x}-${y}-${z}`,
            position: pos,
            colors: pieceColors,
          });
        }
      }
    }
    return pieces;
  }, [cubeState]);

  return (
    <group ref={groupRef}>
      {cubelets.map((piece) => (
        <CubePiece
          key={piece.id}
          position={piece.position}
          colors={piece.colors}
        />
      ))}
    </group>
  );
}

interface InteractiveCube3DProps {
  cubeState: CubeState;
  className?: string;
}

export default function InteractiveCube3D({
  cubeState,
  className,
}: InteractiveCube3DProps) {
  return (
    <div
      className={
        className ||
        "w-full h-64 sm:h-96 md:h-[500px] bg-muted rounded-lg shadow-xl"
      }
    >
      <Canvas camera={{ position: [4, 3, 5], fov: 50 }}>
        {" "}
        {/* Adjusted camera for better initial view */}
        <ambientLight intensity={Math.PI / 1.2} />
        <spotLight
          position={[10, 10, 10]}
          angle={0.3}
          penumbra={1}
          decay={0}
          intensity={Math.PI * 0.8}
          castShadow
        />
        <spotLight
          position={[-10, -10, -10]}
          angle={0.3}
          penumbra={1}
          decay={0}
          intensity={Math.PI * 0.3}
        />
        <pointLight position={[0, 5, 0]} intensity={Math.PI * 0.2} />
        <RubiksCube cubeState={cubeState} />
        <OrbitControls enableZoom={true} enablePan={true} />
      </Canvas>
    </div>
  );
}
