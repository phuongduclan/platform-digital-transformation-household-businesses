"use client";

import { useEffect, useState } from "react";
import { fetchActivePlans } from "@/services/registration.service";
import type { SubscriptionPlanDto } from "@/lib/api";
import { useRouter } from "next/navigation";
import { useRegistration } from "@/context/registration-context";
import { showToast } from "@/components/ui/toast";
import LoadingOverlay from "@/components/ui/loading-overlay";

export default function Step1PlanPage() {
  const router = useRouter();
  const { state, setPlanId } = useRegistration();
  const [plans, setPlans] = useState<SubscriptionPlanDto[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedId, setSelectedId] = useState<number | null>(state.planId);

  useEffect(() => {
    let mounted = true;
    fetchActivePlans()
      .then(data => {
        if (mounted) {
          setPlans(data);
        }
      })
      .catch(err => {
        // Sử dụng error.message từ interceptor đã được xử lý
        const message =
          err?.message ||
          err?.response?.data?.message ||
          err?.response?.data?.error ||
          "Không tải được danh sách gói. Vui lòng thử lại.";
        if (mounted) {
          setError(message);
          showToast(message, "error");
        }
      })
      .finally(() => {
        if (mounted) setLoading(false);
      });

    return () => {
      mounted = false;
    };
  }, []);

  const handleNext = () => {
    if (!selectedId) {
      showToast("Vui lòng chọn một gói đăng ký", "warning");
      return;
    }
    setPlanId(selectedId);
    const selectedPlan = plans.find(p => p.id === selectedId);
    showToast(
      `Đã chọn gói "${selectedPlan?.name || ""}". Chuyển sang bước tiếp theo...`,
      "success",
      1500
    );
    setTimeout(() => {
      router.push("/register/step2-household");
    }, 1000);
  };

  return (
    <>
      <LoadingOverlay isLoading={loading} message="Đang tải danh sách gói đăng ký..." />
      <div className="w-full">
      {/* Title & Subtitle */}
      <div className="mb-8">
        <h2 className="mb-3 text-[28px] font-bold italic text-[#1e3a8a]">
          Chọn gói đăng ký
        </h2>
        <p className="text-base text-[#4b5563] leading-relaxed">
          Bạn có thể thay đổi/ nâng cấp gói sau này để phù hợp với nhu cầu phát
          triển của hộ kinh doanh.
        </p>
      </div>

      {/* Error Message */}
      {error && (
        <div className="mb-6 rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
          {error}
        </div>
      )}

      {/* Plan Cards */}
      {loading ? (
        <div className="grid gap-6 md:grid-cols-3">
          {Array.from({ length: 3 }).map((_, idx) => (
            <div
              key={idx}
              className="h-64 animate-pulse rounded-xl border border-slate-200 bg-slate-50 opacity-70"
            >
              <div className="p-6 space-y-4">
                <div className="h-6 w-3/4 rounded bg-slate-200"></div>
                <div className="h-8 w-1/2 rounded bg-slate-200"></div>
                <div className="space-y-2">
                  <div className="h-4 w-full rounded bg-slate-200"></div>
                  <div className="h-4 w-5/6 rounded bg-slate-200"></div>
                  <div className="h-4 w-4/6 rounded bg-slate-200"></div>
                </div>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="grid gap-6 md:grid-cols-3">
          {plans.map(plan => {
            const isSelected = selectedId === plan.id;
            const billing =
              plan.billing_cycle?.toLowerCase() === "yearly"
                ? "/năm"
                : "/tháng";

            return (
              <button
                key={plan.id}
                type="button"
                onClick={() => setSelectedId(plan.id)}
                className={`group relative flex h-full flex-col rounded-xl border-2 p-6 text-left transition-all ${
                  isSelected
                    ? "border-[#00897b] bg-[#00897b] text-white shadow-lg"
                    : "border-slate-200 bg-white hover:border-[#00897b] hover:shadow-md"
                }`}
              >
                {isSelected && (
                  <div className="absolute -top-3 right-4 rounded-full bg-white px-3 py-1 text-xs font-medium text-[#00897b]">
                    Đã chọn
                  </div>
                )}

                <div className="mb-4">
                  <h3
                    className={`text-lg font-semibold ${
                      isSelected ? "text-white" : "text-slate-900"
                    }`}
                  >
                    {plan.name}
                  </h3>
                </div>

                <div className="mb-4">
                  <div className="flex items-baseline gap-1">
                    <span
                      className={`text-2xl font-bold ${
                        isSelected ? "text-white" : "text-slate-900"
                      }`}
                    >
                      {plan.price.toLocaleString("vi-VN")}
                    </span>
                    <span
                      className={`text-base ${
                        isSelected ? "text-white/80" : "text-slate-500"
                      }`}
                    >
                      đ{billing}
                    </span>
                  </div>
                </div>

                {plan.description && (
                  <p
                    className={`text-sm leading-relaxed ${
                      isSelected ? "text-white/90" : "text-slate-600"
                    }`}
                  >
                    {plan.description}
                  </p>
                )}

                {/* Selection Indicator */}
                {isSelected && (
                  <div className="mt-auto pt-4">
                    <div className="flex items-center justify-center gap-2 text-sm font-medium text-white">
                      <svg
                        className="h-5 w-5"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth={2}
                          d="M5 13l4 4L19 7"
                        />
                      </svg>
                      <span>Đã chọn gói này</span>
                    </div>
                  </div>
                )}
              </button>
            );
          })}
        </div>
      )}

      {/* Footer Buttons */}
      <div className="mt-12 flex items-center justify-between border-t border-slate-200 pt-6">
        <button
          type="button"
          onClick={() => router.push("/login")}
          className="rounded-lg border border-slate-300 bg-white px-6 py-2.5 text-base font-normal text-[#1e3a8a] transition hover:bg-slate-50 disabled:opacity-50"
        >
          Quay lại
        </button>
        <button
          type="button"
          onClick={handleNext}
          disabled={!selectedId || loading}
          className="rounded-lg bg-[#00897b] px-6 py-2.5 text-base font-normal text-white transition hover:bg-[#007a6c] disabled:cursor-not-allowed disabled:opacity-50"
        >
          Tiếp tục
        </button>
      </div>
    </div>
    </>
  );
}
