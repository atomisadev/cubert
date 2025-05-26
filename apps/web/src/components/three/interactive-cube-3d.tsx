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
      for (let y = 0; y < N; y++) {
        for (let z = 0; z < N; z++) {
          if (x > 0 && x < N - 1 && y > 0 && y < N - 1 && z > 0 && z < N - 1) {
            continue;
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

          if (x === N - 1) {
            pieceColors[0] = cubeState.R[(N - 1 - y) * N + z];
          }
          if (x === 0) {
            pieceColors[1] = cubeState.L[(N - 1 - y) * N + (N - 1 - z)];
          }
          if (y === N - 1) {
            pieceColors[2] = cubeState.U[z * N + x];
          }
          if (y === 0) {
            pieceColors[3] = cubeState.D[(N - 1 - z) * N + x];
          }
          if (z === N - 1) {
            pieceColors[4] = cubeState.F[(N - 1 - y) * N + x];
          }
          if (z === 0) {
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
