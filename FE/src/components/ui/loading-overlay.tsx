"use client";

import LoadingTruck from "./loading-truck";

interface LoadingOverlayProps {
  isLoading: boolean;
  message?: string;
  size?: "sm" | "md" | "lg";
}

export default function LoadingOverlay({
  isLoading,
  message,
  size = "md"
}: LoadingOverlayProps) {
  if (!isLoading) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-white/80 backdrop-blur-sm">
      <LoadingTruck message={message} size={size} />
    </div>
  );
}
