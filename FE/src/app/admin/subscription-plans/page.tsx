"use client";

import { useEffect, useState } from "react";
import { adminService } from "@/services/admin.service";
import { showToast } from "@/components/ui/toast";
import LoadingOverlay from "@/components/ui/loading-overlay";
import Link from "next/link";

interface SubscriptionPlan {
  id: number;
  name: string;
  billing_cycle: string | null;
  price: number;
  description: string | null;
  status: string;
  created_at: string;
  updated_at: string;
}

export default function AdminSubscriptionPlansPage() {
  const [plans, setPlans] = useState<SubscriptionPlan[]>([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState<{ status?: string; billing_cycle?: string }>({});

  useEffect(() => {
    fetchPlans();
  }, [filters]);

  const fetchPlans = async () => {
    try {
      setLoading(true);
      const data = await adminService.listSubscriptionPlans();
      // Apply client-side filters
      let filtered = data;
      if (filters.status) {
        filtered = filtered.filter(p => p.status.toLowerCase() === filters.status?.toLowerCase());
      }
      if (filters.billing_cycle) {
        filtered = filtered.filter(p => p.billing_cycle === filters.billing_cycle);
      }
      setPlans(filtered);
    } catch (error: any) {
      showToast(error.message || "Lỗi khi tải danh sách gói đăng ký", "error");
    } finally {
      setLoading(false);
    }
  };

  const handleRefresh = () => {
    setFilters({});
    fetchPlans();
  };

  const handleDelete = async (id: number) => {
    if (!confirm("Bạn có chắc chắn muốn xóa gói đăng ký này?")) return;
    try {
      await adminService.deleteSubscriptionPlan(id);
      showToast("Xóa gói đăng ký thành công", "success");
      fetchPlans();
    } catch (error: any) {
      showToast(error.message || "Lỗi khi xóa gói đăng ký", "error");
    }
  };

  const formatPrice = (price: number) => {
    return new Intl.NumberFormat("vi-VN").format(price);
  };

  const formatDate = (dateString: string) => {
    if (!dateString) return "-";
    const date = new Date(dateString);
    return date.toLocaleDateString("vi-VN", { day: "2-digit", month: "2-digit", year: "numeric" });
  };

  const getBillingCycleText = (cycle: string | null) => {
    if (!cycle) return "";
    switch (cycle.toLowerCase()) {
      case "monthly":
        return "/ tháng";
      case "yearly":
        return "/ năm";
      default:
        return `/${cycle}`;
    }
  };

  // Parse features from description if available, otherwise show description
  const getPlanFeatures = (plan: SubscriptionPlan) => {
    if (!plan.description) return [];
    // Try to parse features from description (if formatted as bullet points or list)
    // For now, just return empty array - features should come from BE
    return [];
  };

  const isPopularPlan = (planName: string) => {
    return planName.toLowerCase().includes("pro");
  };

  return (
    <>
      <LoadingOverlay isLoading={loading} message="Đang tải danh sách gói đăng ký..." />
      
      <div className="p-8">
        {/* Page Header */}
        <div className="mb-6 flex items-center justify-between">
          <h1 className="text-[28px] font-bold italic text-[#1e3a8a]">
            Quản lý Gói đăng ký
          </h1>
          <Link
            href="/admin/subscription-plans/create"
            className="px-4 py-2 bg-[#00897b] text-white rounded-lg hover:bg-[#007a6c] transition-colors font-bold italic text-base flex items-center gap-2"
          >
            <span>+</span>
            <span>Tạo gói mới</span>
          </Link>
        </div>

        {/* Filter Section */}
        <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6 mb-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-normal text-[#1e3a8a] mb-1.5">
                Trạng thái
              </label>
              <select
                value={filters.status || ""}
                onChange={(e) => setFilters(prev => ({ ...prev, status: e.target.value || undefined }))}
                className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#00897b] focus:border-transparent"
              >
                <option value="">Tất cả</option>
                <option value="active">Active</option>
                <option value="inactive">Inactive</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-normal text-[#1e3a8a] mb-1.5">
                Chu kỳ thanh toán
              </label>
              <select
                value={filters.billing_cycle || ""}
                onChange={(e) => setFilters(prev => ({ ...prev, billing_cycle: e.target.value || undefined }))}
                className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#00897b] focus:border-transparent"
              >
                <option value="">Tất cả</option>
                <option value="monthly">Tháng</option>
                <option value="yearly">Năm</option>
              </select>
            </div>
            <div className="flex items-end">
              <button
                onClick={handleRefresh}
                className="w-full px-4 py-2 bg-white border border-[#1e3a8a] text-[#1e3a8a] rounded-lg hover:bg-slate-50 transition-colors font-normal text-base"
              >
                Làm mới
              </button>
            </div>
          </div>
        </div>

        {/* Plans Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {plans.length === 0 ? (
            <div className="col-span-full text-center py-12 text-slate-500">
              Không có gói đăng ký nào
            </div>
          ) : (
            plans.map((plan) => {
              const isPopular = isPopularPlan(plan.name);
              const isActive = plan.status.toLowerCase() === "active";

              return (
                <div
                  key={plan.id}
                  className="bg-white rounded-lg shadow-sm border border-slate-200 overflow-hidden relative"
                >
                  {/* Popular Badge */}
                  {isPopular && (
                    <div className="absolute top-4 right-4 z-10">
                      <div className="bg-[#00897b] px-2 py-1 rounded">
                        <p className="text-[11px] font-bold italic text-white">PHỔ BIẾN</p>
                      </div>
                    </div>
                  )}

                  {/* Card Header */}
                  <div className="p-6 pb-4">
                    <div className="flex items-start justify-between mb-4">
                      <h3 className="text-[20px] font-bold italic text-[#1e3a8a]">
                        {plan.name}
                      </h3>
                      <span className={`px-2 py-1 text-xs font-bold italic rounded ${
                        isActive
                          ? "bg-[#10b981] text-white"
                          : "bg-[#6b7280] text-white"
                      }`}>
                        {isActive ? "ACTIVE" : "INACTIVE"}
                      </span>
                    </div>

                    {/* Price Section */}
                    <div className="mb-4">
                      <div className="flex items-baseline gap-2">
                        <p className="text-[32px] font-bold italic text-[#00897b]">
                          {formatPrice(plan.price)} đ
                        </p>
                        <p className="text-base font-normal text-[#4b5563]">
                          {getBillingCycleText(plan.billing_cycle)}
                        </p>
                      </div>
                    </div>

                    {/* Description */}
                    {plan.description && (
                      <div className="mb-4">
                        <p className="text-sm font-normal text-[#4b5563] leading-relaxed">
                          {plan.description}
                        </p>
                      </div>
                    )}

                    {/* Metadata */}
                    <div className="pt-4 border-t border-slate-200 mb-4">
                      <p className="text-xs font-normal text-[#6b7280]">
                        ID: {plan.id} • Ngày tạo: {formatDate(plan.created_at)}
                      </p>
                    </div>

                    {/* Action Buttons */}
                    <div className="flex gap-2">
                      <Link
                        href={`/admin/subscription-plans/${plan.id}/edit`}
                        className="flex-1 px-4 py-2 bg-white border border-[#1e3a8a] text-[#1e3a8a] rounded-lg hover:bg-slate-50 transition-colors font-bold italic text-sm text-center"
                      >
                        Chỉnh sửa
                      </Link>
                      <button
                        onClick={() => handleDelete(plan.id)}
                        className="flex-1 px-4 py-2 bg-white border border-[#dc2626] text-[#dc2626] rounded-lg hover:bg-red-50 transition-colors font-bold italic text-sm"
                      >
                        Xóa
                      </button>
                    </div>
                  </div>
                </div>
              );
            })
          )}
        </div>
      </div>
    </>
  );
}
