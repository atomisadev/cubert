// apps/web/src/app/page.tsx
"use client"; // Required for useState and dynamic import

import Image from "next/image";
import { useState } from "react";
import dynamic from "next/dynamic";
import { CubeEditor } from "@/components/cube-editor/cube-editor";
import { INITIAL_CUBE_STATE, CubeState } from "@/lib/cube-constants";
import { cn } from "@/lib/utils";

// Dynamically import the 3D cube component to ensure it's client-side only
const InteractiveCube3D = dynamic(
  () => import("@/components/three/interactive-cube-3d"),
  {
    ssr: false,
    loading: () => (
      <div className="w-full h-64 sm:h-96 md:h-[500px] flex items-center justify-center bg-muted rounded-lg text-muted-foreground">
        <p>Loading 3D Cube...</p>
      </div>
    ),
  }
);

export default function Home() {
  const [currentCubeState, setCurrentCubeState] =
    useState<CubeState>(INITIAL_CUBE_STATE);

  const handleCubeChange = (newState: CubeState) => {
    setCurrentCubeState(newState);
  };

  return (
    <div className="flex flex-col items-center min-h-screen p-4 sm:p-8 bg-background text-foreground font-[family-name:var(--font-geist-sans)]">
      <header className="w-full max-w-5xl mb-8 text-center">
        <div className="flex justify-center items-center gap-2 mb-4">
          <Image
            className="dark:invert" // Assuming next.svg is black and needs inverting for dark mode
            src="/next.svg" // Replace with your actual logo if desired
            alt="App Logo"
            width={100}
            height={21}
            priority
          />
          <h1 className="text-3xl sm:text-4xl font-bold text-primary">
            Cubert
          </h1>
        </div>
        <p className="text-sm sm:text-md text-muted-foreground">
          Edit the unwrapped cube faces below and see the 3D model update in
          real-time.
        </p>
      </header>

      <main className="flex flex-col lg:flex-row gap-6 sm:gap-8 w-full max-w-5xl items-start">
        <div className="w-full lg:w-1/2 flex justify-center">
          <CubeEditor
            initialState={currentCubeState}
            onCubeStateChange={handleCubeChange}
            className="flex-grow"
          />
        </div>
        <div className="w-full lg:w-1/2 flex justify-center">
          <InteractiveCube3D
            cubeState={currentCubeState}
            className="aspect-square w-full max-w-md lg:max-w-none"
          />
        </div>
      </main>

      <footer className="w-full max-w-5xl mt-12 pt-8 border-t border-border text-center text-muted-foreground text-sm">
        <p>
          &copy; {new Date().getFullYear()} Cubert Project. Powered by Next.js &
          Vercel.
        </p>
        <div className="mt-4 flex gap-4 items-center justify-center">
          <a
            className="rounded-full border border-solid border-transparent transition-colors flex items-center justify-center bg-foreground text-background gap-2 hover:bg-foreground/80 dark:hover:bg-foreground/90 font-medium text-xs sm:text-sm h-8 sm:h-10 px-3 sm:px-4"
            href="https://vercel.com/new?utm_source=create-next-app&utm_medium=appdir-template-tw&utm_campaign=create-next-app"
            target="_blank"
            rel="noopener noreferrer"
          >
            <Image
              className="dark:invert"
              src="/vercel.svg"
              alt="Vercel logomark"
              width={16}
              height={16}
            />
            Deploy
          </a>
          <a
            className="rounded-full border border-solid border-border transition-colors flex items-center justify-center hover:bg-muted hover:border-transparent font-medium text-xs sm:text-sm h-8 sm:h-10 px-3 sm:px-4"
            href="https://nextjs.org/docs?utm_source=create-next-app&utm_medium=appdir-template-tw&utm_campaign=create-next-app"
            target="_blank"
            rel="noopener noreferrer"
          >
            Next.js Docs
          </a>
        </div>
      </footer>
    </div>
  );
}
