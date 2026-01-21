"use client";

import { useEffect, useState } from "react";

interface LoadingTruckProps {
  message?: string;
  size?: "sm" | "md" | "lg";
}

export default function LoadingTruck({
  message = "Đang xử lý...",
  size = "md"
}: LoadingTruckProps) {
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  const scaleClass =
    size === "sm" ? "scale-75" : size === "lg" ? "scale-125" : "scale-100";

  if (!mounted) return null;

  return (
    <div className="flex flex-col items-center justify-center gap-4 p-8">
      <div className={`relative ${scaleClass}`}>
        <div className="bizflow-loader">
          <div className="car-container">
            <div className="car" />
            <div className="front-part" />
            <div className="front-part2" />
            <div className="front-part3" />
            <div className="bottom-part" />
            <div className="wheel-container wheel-container1" />
            <div className="wheel-container wheel-container2" />
            <div className="wheel-back" />
            <div className="window" />
            <div className="window2" />
            <div className="window3" />
            <div className="details" />
            <div className="details2" />
            <div className="details3" />
            <div className="details4" />
            <div className="details5" />
            <div className="bumper" />
            <div className="bumper2" />
            <div className="head-lights" />
            <div className="tail-lights" />
            <div className="extra-lighting-details" />
            <div className="extra-lighting-details2" />
            <div className="extra-lighting-details3" />
          </div>

          <div className="container-wheel1">
            <div className="wheel-break" />
            <div className="wheel-ring wheel-ring1">
              <div className="wheel-center" />
              <div className="wheel-center2" />
              <div className="wheel-ring-stick" />
              <div className="wheel-ring-stick wheel-ring-stick2" />
              <div className="wheel-ring-stick wheel-ring-stick3" />
              <div className="wheel-ring-stick wheel-ring-stick4" />
              <div className="wheel-ring-stick wheel-ring-stick5" />
              <div className="wheel-logo" />
            </div>
          </div>

          <div className="container-wheel2">
            <div className="wheel-break2" />
            <div className="wheel-ring2 wheel-ring">
              <div className="wheel-center" />
              <div className="wheel-center2" />
              <div className="wheel-ring-stick" />
              <div className="wheel-ring-stick wheel-ring-stick2" />
              <div className="wheel-ring-stick wheel-ring-stick3" />
              <div className="wheel-ring-stick wheel-ring-stick4" />
              <div className="wheel-ring-stick wheel-ring-stick5" />
              <div className="wheel-logo" />
            </div>
          </div>

          <div className="street">
            <div className="line" />
            <div className="obstacles" />
          </div>
        </div>
      </div>

      {message && (
        <p className="text-sm font-medium text-[#4b5563] animate-pulse">
          {message}
        </p>
      )}
    </div>
  );
}

