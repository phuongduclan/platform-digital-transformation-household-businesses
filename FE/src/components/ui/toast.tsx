"use client";

import { useEffect, useState } from "react";

export type ToastType = "success" | "error" | "info" | "warning";

export type Toast = {
  id: string;
  message: string;
  type: ToastType;
  duration?: number;
};

type ToastContextType = {
  toasts: Toast[];
  showToast: (message: string, type?: ToastType, duration?: number) => void;
  removeToast: (id: string) => void;
};

// Global toast state (simple implementation)
let toastListeners: ((toasts: Toast[]) => void)[] = [];
let toastState: Toast[] = [];

function notifyListeners() {
  toastListeners.forEach(listener => listener([...toastState]));
}

export function showToast(
  message: string,
  type: ToastType = "info",
  duration: number = 3000
) {
  const id = Math.random().toString(36).substring(2, 9);
  const toast: Toast = { id, message, type, duration };
  toastState.push(toast);
  notifyListeners();

  if (duration > 0) {
    setTimeout(() => {
      toastState = toastState.filter(t => t.id !== id);
      notifyListeners();
    }, duration);
  }
}

export function ToastContainer() {
  const [toasts, setToasts] = useState<Toast[]>([]);

  useEffect(() => {
    const listener = (newToasts: Toast[]) => {
      setToasts(newToasts);
    };
    toastListeners.push(listener);
    setToasts([...toastState]);

    return () => {
      toastListeners = toastListeners.filter(l => l !== listener);
    };
  }, []);

  const removeToast = (id: string) => {
    toastState = toastState.filter(t => t.id !== id);
    notifyListeners();
  };

  if (toasts.length === 0) return null;

  return (
    <div className="fixed top-4 right-4 z-50 flex flex-col gap-2">
      {toasts.map(toast => (
        <div
          key={toast.id}
          className={`min-w-[300px] max-w-md rounded-lg border px-4 py-3 shadow-lg transition-all ${
            toast.type === "success"
              ? "border-green-200 bg-green-50 text-green-800"
              : toast.type === "error"
              ? "border-red-200 bg-red-50 text-red-800"
              : toast.type === "warning"
              ? "border-yellow-200 bg-yellow-50 text-yellow-800"
              : "border-blue-200 bg-blue-50 text-blue-800"
          }`}
        >
          <div className="flex items-start justify-between gap-3">
            <div className="flex-1">
              <p className="text-sm font-medium">{toast.message}</p>
            </div>
            <button
              onClick={() => removeToast(toast.id)}
              className="flex-shrink-0 text-current opacity-60 hover:opacity-100"
            >
              <svg
                className="h-4 w-4"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M6 18L18 6M6 6l12 12"
                />
              </svg>
            </button>
          </div>
        </div>
      ))}
    </div>
  );
}
