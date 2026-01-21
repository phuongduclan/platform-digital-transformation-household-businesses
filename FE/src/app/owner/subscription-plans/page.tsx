"use client";

import { useEffect, useMemo, useState } from "react";
import LoadingOverlay from "@/components/ui/loading-overlay";
import { showToast } from "@/components/ui/toast";
import {
  ownerService,
  OwnerSubscription,
  OwnerSubscriptionPlan,
} from "@/services/owner.service";
import { useRouter } from "next/navigation";

export default function OwnerSubscriptionPlansPage() {
  const router = useRouter();
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [plans, setPlans] = useState<OwnerSubscriptionPlan[]>([]);
  const [currentSubscription, setCurrentSubscription] =
    useState<OwnerSubscription | null>(null);
  const [selectedPlanId, setSelectedPlanId] = useState<number | null>(null);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [planList, subscription] = await Promise.all([
        ownerService.listActiveSubscriptionPlans(),
        ownerService.getSubscription(),
      ]);
      setPlans(planList);
      setCurrentSubscription(subscription);
      if (subscription) {
        setSelectedPlanId(subscription.plan_id);
      }
    } catch (error: any) {
      const message =
        error?.response?.data?.error ||
        error?.message ||
        "Lỗi khi tải danh sách gói đăng ký";
      showToast(message, "error");
    } finally {
      setLoading(false);
    }
  };

  const handleBack = () => {
    router.push("/owner/household");
  };

  const handleSelectPlan = (planId: number) => {
    setSelectedPlanId(planId);
  };

  const isCurrentPlan = (planId: number) =>
    currentSubscription && currentSubscription.plan_id === planId;

  const formatPrice = (price: number) =>
    new Intl.NumberFormat("vi-VN", {
      style: "currency",
      currency: "VND",
      maximumFractionDigits: 0,
    }).format(price);

  const billingCycleLabel = (cycle: string) => {
    const v = (cycle || "").toLowerCase();
    if (v === "monthly") return "Theo tháng";
    if (v === "yearly" || v === "annual") return "Theo năm";
    return cycle;
  };

  const selectedPlan = useMemo(
    () => plans.find((p) => p.id === selectedPlanId) || null,
    [plans, selectedPlanId]
  );

  const handleConfirmUpgrade = async () => {
    if (!selectedPlanId) {
      showToast("Vui lòng chọn gói cần sử dụng", "error");
      return;
    }

    try {
      setSaving(true);
      await ownerService.upgradeSubscription({
        plan_id: selectedPlanId,
      });
      showToast("Nâng cấp gói đăng ký thành công", "success");
      router.push("/owner/household");
    } catch (error: any) {
      const message =
        error?.response?.data?.error ||
        error?.message ||
        "Lỗi khi nâng cấp gói đăng ký";
      showToast(message, "error");
    } finally {
      setSaving(false);
    }
  };

  return (
    <>
      <LoadingOverlay
        isLoading={loading || saving}
        message={
          loading ? "Đang tải danh sách gói đăng ký..." : "Đang xử lý..."
        }
      />
      <div className="p-8">
        {/* Header */}
        <div className="mb-6 flex items-center justify-between">
          <div>
            <h1 className="text-[28px] font-bold italic text-[#1e3a8a] mb-2">
              Chọn gói đăng ký
            </h1>
            <p className="text-sm text-[#4b5563]">
              Chọn gói phù hợp cho hộ kinh doanh của bạn. Chỉ hiển thị các gói
              đang hoạt động.
            </p>
          </div>
          <button
            type="button"
            onClick={handleBack}
            className="px-4 py-2 border border-[#1e3a8a] text-[#1e3a8a] rounded-lg hover:bg-slate-50 transition-colors text-sm font-medium"
          >
            Quay lại cài đặt hộ kinh doanh
          </button>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Plan cards */}
          <div className="lg:col-span-2 grid grid-cols-1 md:grid-cols-2 gap-4">
            {plans.length === 0 ? (
              <p className="text-sm text-[#6b7280]">
                Hiện chưa có gói đăng ký nào khả dụng.
              </p>
            ) : (
              plans.map((plan) => {
                const current = isCurrentPlan(plan.id);
                const selected = selectedPlanId === plan.id;
                return (
                  <button
                    key={plan.id}
                    type="button"
                    onClick={() => handleSelectPlan(plan.id)}
                    className={`text-left bg-white rounded-lg border shadow-sm p-5 transition-colors ${
                      selected
                        ? "border-[#00897b] ring-2 ring-[#b2dfdb]"
                        : "border-slate-200 hover:border-[#00897b]"
                    }`}
                  >
                    <div className="flex items-center justify-between mb-2">
                      <h2 className="text-[18px] font-bold italic text-[#1e3a8a]">
                        {plan.name}
                      </h2>
                      {current && (
                        <span className="px-2 py-1 text-xs font-bold italic rounded-lg bg-[#e0f2f1] text-[#00897b]">
                          Gói hiện tại
                        </span>
                      )}
                    </div>
                    <p className="text-lg font-bold italic text-[#00897b] mb-1">
                      {formatPrice(plan.price)}
                    </p>
                    <p className="text-xs text-[#4b5563] mb-3">
                      Chu kỳ: {billingCycleLabel(plan.billing_cycle)}
                    </p>
                    <p className="text-xs text-[#6b7280] min-h-[40px]">
                      {plan.description || "Gói đăng ký cho hộ kinh doanh."}
                    </p>
                  </button>
                );
              })
            )}
          </div>

          {/* Summary / confirmation */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6">
              <h2 className="text-[18px] font-bold italic text-[#1e3a8a] mb-4">
                Tóm tắt lựa chọn
              </h2>
              {selectedPlan ? (
                <div className="space-y-3 text-sm mb-4">
                  <div className="flex items-center justify-between">
                    <span className="text-[#4b5563]">Gói chọn</span>
                    <span className="font-bold text-[#1e3a8a]">
                      {selectedPlan.name}
                    </span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-[#4b5563]">Giá</span>
                    <span className="font-bold text-[#1e3a8a]">
                      {formatPrice(selectedPlan.price)}
                    </span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-[#4b5563]">Chu kỳ</span>
                    <span className="font-normal text-[#1e3a8a]">
                      {billingCycleLabel(selectedPlan.billing_cycle)}
                    </span>
                  </div>
                  {currentSubscription && (
                    <p className="text-xs text-[#6b7280]">
                      Gói hiện tại của bạn có mã #{currentSubscription.plan_id}.
                      Việc nâng cấp sẽ áp dụng theo chính sách hệ thống.
                    </p>
                  )}
                </div>
              ) : (
                <p className="text-sm text-[#6b7280] mb-4">
                  Chọn một gói ở bên trái để xem chi tiết và xác nhận.
                </p>
              )}

              <button
                type="button"
                onClick={handleConfirmUpgrade}
                disabled={!selectedPlanId || saving}
                className="w-full px-4 py-2 rounded-lg bg-[#00897b] text-white text-sm font-bold italic hover:bg-[#007a6c] transition-colors disabled:bg-slate-400 disabled:cursor-not-allowed"
              >
                {saving ? "Đang xử lý..." : "Xác nhận nâng cấp gói"}
              </button>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}

