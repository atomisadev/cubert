"use client";

import { useState, useEffect } from "react";

export interface DeviceInfo {
  isMobile: boolean;
  isStandalone: boolean;
  isIOS: boolean;
  isDesktop: boolean;
  isLoading: boolean;
}

export function useDeviceDetection(): DeviceInfo {
  const [deviceInfo, setDeviceInfo] = useState<DeviceInfo>({
    isMobile: false,
    isStandalone: false,
    isIOS: false,
    isDesktop: false,
    isLoading: true,
  });

  useEffect(() => {
    const userAgent =
      navigator.userAgent || navigator.vendor || (window as any).opera;

    const ios = /iPad|iPhone|iPod/.test(userAgent) && !(window as any).MSStream;

    const mobile =
      /android|iphone|ipad|ipod|blackberry|iemobile|opera mini/i.test(
        userAgent.toLowerCase()
      );

    const standalone =
      window.matchMedia(`(display-mode: standalone)`).matches ||
      (window.navigator as any).standalone === true;

    setDeviceInfo({
      isMobile: mobile || ios,
      isStandalone: standalone,
      isIOS: ios,
      isDesktop: !(mobile || ios),
      isLoading: false,
    });
  }, []);

  return deviceInfo;
}
