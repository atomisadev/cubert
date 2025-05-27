import React from "react";

export function DesktopUnsupported() {
  return (
    <div className="fixed inset-0 z-50 flex h-screen w-screen flex-col items-center justify-center bg-red-600 p-4">
      <div className="text-center">
        <h1 className="text-4xl font-bold text-white sm:text-5xl">
          Desktop Not Supported
        </h1>
        <p className="mt-4 text-lg text-red-100 sm:text-xl">
          Cubert is designed for mobile devices only.
        </p>
        <p className="mt-2 text-red-100">
          Please access this application from your mobile phone or tablet.
        </p>
      </div>
    </div>
  );
}
