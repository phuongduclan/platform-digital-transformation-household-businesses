"use client";

import type { ReactNode } from "react";
import { RegisterProviders } from "./providers";
import { usePathname } from "next/navigation";
import Link from "next/link";

const steps = [
  {
    id: 1,
    label: "Chọn gói",
    href: "/register/step1-plan",
    description: "Bắt đầu với gói phù hợp nhất."
  },
  {
    id: 2,
    label: "Hộ kinh doanh",
    href: "/register/step2-household",
    description: "Thông tin cơ bản về hộ của bạn."
  },
  {
    id: 3,
    label: "Tài khoản Owner",
    href: "/register/step3-account",
    description: "Thiết lập thông tin đăng nhập."
  },
  {
    id: 4,
    label: "Hoàn tất",
    href: "/register/success",
    description: "Xác nhận và kích hoạt hệ thống."
  }
];

export default function RegisterLayout({ children }: { children: ReactNode }) {
  const pathname = usePathname();

  const getCurrentStep = () => {
    if (pathname?.includes("step1-plan")) return 1;
    if (pathname?.includes("step2-household")) return 2;
    if (pathname?.includes("step3-account")) return 3;
    if (pathname?.includes("success")) return 4;
    return 1;
  };

  const currentStep = getCurrentStep();

  return (
    <RegisterProviders>
      <main className="min-h-screen bg-slate-50">
        {/* Header */}
        <header className="border-b border-slate-200 bg-white px-6 py-4">
          <div className="mx-auto flex max-w-7xl items-center justify-center">
            <div className="text-center">
              <h1 className="text-xl font-bold italic text-[#1e3a8a]">BizFlow</h1>
              <p className="mt-1 text-sm text-[#4b5563]">
                Nền tảng quản lý hộ kinh doanh
              </p>
            </div>
          </div>
        </header>

        {/* Main Content - 2 Column Layout */}
        <div className="mx-auto flex max-w-7xl gap-8 px-6 py-8">
          {/* Left Column - Vertical Stepper */}
          <aside className="hidden lg:block w-64 flex-shrink-0">
            <div className="relative">
              {/* Vertical Line */}
              <div
                className="absolute left-6 top-8 bottom-8 w-0.5"
                style={{
                  background: `linear-gradient(to bottom, ${currentStep >= 1 ? "#10b981" : "#e5e7eb"
                    } 0%, ${currentStep >= 2 ? "#10b981" : "#e5e7eb"
                    } 25%, ${currentStep >= 3 ? "#10b981" : "#e5e7eb"
                    } 50%, ${currentStep >= 4 ? "#10b981" : "#e5e7eb"
                    } 75%, #e5e7eb 100%)`
                }}
              />

              {/* Steps */}
              <div className="space-y-8">
                {steps.map((step, index) => {
                  const isActive = currentStep === step.id;
                  const isCompleted = currentStep > step.id;

                  return (
                    <div key={step.id} className="relative flex items-start gap-4">
                      {/* Circle */}
                      <div className="relative z-10 flex-shrink-0">
                        <div
                          className={`flex h-12 w-12 items-center justify-center rounded-full border-2 ${isActive
                            ? "border-[#10b981] bg-[#10b981]"
                            : isCompleted
                              ? "border-[#10b981] bg-[#10b981]"
                              : "border-slate-300 bg-white"
                            }`}
                        >
                          {(isActive || isCompleted) && (
                            <span className="text-sm font-normal text-white">
                              {isCompleted ? "✓" : step.id}
                            </span>
                          )}
                          {!isActive && !isCompleted && (
                            <span className="text-sm font-normal text-[#4b5563]">
                              {step.id}
                            </span>
                          )}
                        </div>
                      </div>

                      {/* Content */}
                      <div className="flex-1 pt-1">
                        <h3
                          className={`text-base font-bold italic ${isActive ? "text-[#1e3a8a]" : "text-[#4b5563]"
                            }`}
                        >
                          {step.label}
                        </h3>
                        <p className="mt-1 text-sm text-[#4b5563] leading-relaxed">
                          {step.description}
                        </p>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          </aside>

          {/* Right Column - Form Content */}
          <div className="flex-1">
            <div className="rounded-2xl bg-white px-8 py-10 shadow-xl">
              {children}
            </div>
          </div>
        </div>
      </main>
    </RegisterProviders>
  );
}
