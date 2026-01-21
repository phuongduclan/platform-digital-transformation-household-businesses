"use client";

import { useEffect, useState } from "react";
import { adminService } from "@/services/admin.service";
import { showToast } from "@/components/ui/toast";
import LoadingOverlay from "@/components/ui/loading-overlay";
import Link from "next/link";

interface Subscription {
  id: number;
  plan_id: number;
  household_id: number;
  start_date: string;
  end_date: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

interface Household {
  id: number;
  name: string;
}

interface SubscriptionPlan {
  id: number;
  name: string;
}

export default function AdminSubscriptionsPage() {
  const [subscriptions, setSubscriptions] = useState<Subscription[]>([]);
  const [households, setHouseholds] = useState<Household[]>([]);
  const [plans, setPlans] = useState<SubscriptionPlan[]>([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState<{
    is_active?: boolean;
    plan_id?: number;
    start_date?: string;
    end_date?: string;
  }>({});
  const [currentPage, setCurrentPage] = useState(1);
  const [totalSubscriptions, setTotalSubscriptions] = useState(0);
  const itemsPerPage = 5;

  useEffect(() => {
    fetchHouseholds();
    fetchPlans();
    fetchSubscriptions();
  }, [filters, currentPage]);

  const fetchHouseholds = async () => {
    // REMOVED: Admin không có quyền quản lý Household
    // Không fetch households vì không có API Admin cho households
    setHouseholds([]);
  };

  const fetchPlans = async () => {
    try {
      const data = await adminService.listSubscriptionPlans();
      setPlans(data);
    } catch (error: any) {
      // Silently fail
    }
  };

  const fetchSubscriptions = async () => {
    try {
      setLoading(true);
      // Fetch all subscriptions (BE doesn't support filtering yet)
      const allData = await adminService.listSubscriptions();
      
      // Apply client-side filters
      let filtered = allData;
      
      if (filters.is_active !== undefined) {
        filtered = filtered.filter((sub: Subscription) => sub.is_active === filters.is_active);
      }
      
      if (filters.plan_id) {
        filtered = filtered.filter((sub: Subscription) => sub.plan_id === filters.plan_id);
      }
      
      if (filters.start_date) {
        const startDate = new Date(filters.start_date);
        filtered = filtered.filter((sub: Subscription) => {
          const subStartDate = new Date(sub.start_date);
          return subStartDate >= startDate;
        });
      }
      
      if (filters.end_date) {
        const endDate = new Date(filters.end_date);
        filtered = filtered.filter((sub: Subscription) => {
          const subEndDate = new Date(sub.end_date);
          return subEndDate <= endDate;
        });
      }
      
      setSubscriptions(filtered);
      setTotalSubscriptions(filtered.length);
    } catch (error: any) {
      showToast(error.message || "Lỗi khi tải danh sách đăng ký", "error");
    } finally {
      setLoading(false);
    }
  };

  const handleRefresh = () => {
    setFilters({});
    setCurrentPage(1);
    fetchSubscriptions();
  };

  const handleDeactivate = async (id: number) => {
    if (!confirm("Bạn có chắc chắn muốn vô hiệu hóa đăng ký này?")) return;
    try {
      await adminService.updateSubscription(id, { is_active: false });
      showToast("Vô hiệu hóa đăng ký thành công", "success");
      fetchSubscriptions();
    } catch (error: any) {
      showToast(error.message || "Lỗi khi vô hiệu hóa đăng ký", "error");
    }
  };

  const getHouseholdName = (householdId: number) => {
    // Chỉ hiển thị household_id vì Admin không có quyền xem household details
    if (!householdId) return "-";
    return `ID: ${householdId}`;
  };

  const getPlanName = (planId: number) => {
    const plan = plans.find(p => p.id === planId);
    return plan ? plan.name : `ID: ${planId}`;
  };

  const formatDate = (dateString: string) => {
    if (!dateString) return "-";
    const date = new Date(dateString);
    return date.toLocaleDateString("vi-VN", { day: "2-digit", month: "2-digit", year: "numeric" });
  };

  const getStatusBadge = (isActive: boolean) => {
    return (
      <span className={`px-2 py-1 text-xs font-bold italic rounded text-white ${
        isActive ? "bg-[#10b981]" : "bg-[#6b7280]"
      }`}>
        {isActive ? "Active" : "Inactive"}
      </span>
    );
  };

  const getPlanBadge = (planName: string) => {
    return (
      <span className="px-2 py-1 text-xs font-bold italic rounded text-[#00897b] bg-[#e0f2f1]">
        {planName}
      </span>
    );
  };

  // Pagination
  const totalPages = Math.ceil(totalSubscriptions / itemsPerPage);
  const startIndex = (currentPage - 1) * itemsPerPage;
  const endIndex = startIndex + itemsPerPage;
  const paginatedSubscriptions = subscriptions.slice(startIndex, endIndex);

  return (
    <>
      <LoadingOverlay isLoading={loading} message="Đang tải danh sách đăng ký..." />
      
      <div className="p-8">
        {/* Page Header */}
        <div className="mb-6">
          <h1 className="text-[28px] font-bold italic text-[#1e3a8a] mb-2">
            Quản lý Đăng ký
          </h1>
          <p className="text-sm font-thin italic text-[#4b5563]">
            Chỉ xem và vô hiệu hóa đăng ký
          </p>
        </div>

        {/* Filter Card */}
        <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6 mb-6">
          <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
            <div>
              <label className="block text-sm font-normal text-[#1e3a8a] mb-1.5">
                Trạng thái
              </label>
              <select
                value={filters.is_active === undefined ? "" : filters.is_active ? "true" : "false"}
                onChange={(e) => setFilters(prev => ({ 
                  ...prev, 
                  is_active: e.target.value === "" ? undefined : e.target.value === "true"
                }))}
                className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#00897b] focus:border-transparent"
              >
                <option value="">Tất cả</option>
                <option value="true">Active</option>
                <option value="false">Inactive</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-normal text-[#1e3a8a] mb-1.5">
                Gói đăng ký
              </label>
              <select
                value={filters.plan_id || ""}
                onChange={(e) => setFilters(prev => ({ 
                  ...prev, 
                  plan_id: e.target.value ? Number(e.target.value) : undefined
                }))}
                className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#00897b] focus:border-transparent"
              >
                <option value="">Tất cả</option>
                {plans.map((plan) => (
                  <option key={plan.id} value={plan.id}>
                    {plan.name}
                  </option>
                ))}
              </select>
            </div>
            <div>
              <label className="block text-sm font-normal text-[#1e3a8a] mb-1.5">
                Từ ngày
              </label>
              <input
                type="date"
                value={filters.start_date || ""}
                onChange={(e) => setFilters(prev => ({ ...prev, start_date: e.target.value || undefined }))}
                className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#00897b] focus:border-transparent"
              />
            </div>
            <div>
              <label className="block text-sm font-normal text-[#1e3a8a] mb-1.5">
                Đến ngày
              </label>
              <input
                type="date"
                value={filters.end_date || ""}
                onChange={(e) => setFilters(prev => ({ ...prev, end_date: e.target.value || undefined }))}
                className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#00897b] focus:border-transparent"
              />
            </div>
            <div className="flex items-end">
              <button
                onClick={handleRefresh}
                className="w-full px-4 py-2 bg-white border border-[#1e3a8a] text-[#1e3a8a] rounded-lg hover:bg-slate-50 transition-colors font-bold italic text-sm"
              >
                Làm mới
              </button>
            </div>
          </div>
        </div>

        {/* Table Card */}
        <div className="bg-white rounded-lg shadow-sm border border-slate-200 overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-slate-50 border-b border-slate-200">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-bold italic text-[#4b5563] uppercase tracking-wider">
                    ID
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-bold italic text-[#4b5563] uppercase tracking-wider">
                    HỘ KINH DOANH
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-bold italic text-[#4b5563] uppercase tracking-wider">
                    GÓI ĐĂNG KÝ
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-bold italic text-[#4b5563] uppercase tracking-wider">
                    NGÀY BẮT ĐẦU
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-bold italic text-[#4b5563] uppercase tracking-wider">
                    NGÀY KẾT THÚC
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-bold italic text-[#4b5563] uppercase tracking-wider">
                    TRẠNG THÁI
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-bold italic text-[#4b5563] uppercase tracking-wider">
                    THAO TÁC
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-slate-200">
                {paginatedSubscriptions.length === 0 ? (
                  <tr>
                    <td colSpan={7} className="px-6 py-12 text-center text-slate-500">
                      Không có dữ liệu
                    </td>
                  </tr>
                ) : (
                  paginatedSubscriptions.map((sub) => (
                    <tr key={sub.id} className="hover:bg-slate-50 transition-colors">
                      <td className="px-6 py-4 text-sm font-normal text-[#1e3a8a]">
                        {sub.id}
                      </td>
                      <td className="px-6 py-4">
                        <span className="text-sm font-normal text-[#1e3a8a]">
                          {getHouseholdName(sub.household_id)}
                        </span>
                      </td>
                      <td className="px-6 py-4">
                        {getPlanBadge(getPlanName(sub.plan_id))}
                      </td>
                      <td className="px-6 py-4 text-sm font-normal text-[#1e3a8a]">
                        {formatDate(sub.start_date)}
                      </td>
                      <td className="px-6 py-4 text-sm font-normal text-[#1e3a8a]">
                        {formatDate(sub.end_date)}
                      </td>
                      <td className="px-6 py-4">
                        {getStatusBadge(sub.is_active)}
                      </td>
                      <td className="px-6 py-4">
                        <div className="flex items-center gap-3">
                          {sub.is_active && (
                            <button
                              onClick={() => handleDeactivate(sub.id)}
                              className="px-3 py-1 text-sm text-red-600 hover:text-red-700 transition-colors border border-red-600 rounded hover:border-red-700"
                            >
                              Vô hiệu hóa
                            </button>
                          )}
                        </div>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>

          {/* Pagination */}
          {totalSubscriptions > 0 && (
            <div className="px-6 py-4 border-t border-slate-200 flex items-center justify-between">
              <p className="text-sm text-[#4b5563]">
                Hiển thị {startIndex + 1}-{Math.min(endIndex, totalSubscriptions)} của {totalSubscriptions} đăng ký
              </p>
              <div className="flex items-center gap-2">
                <button
                  onClick={() => setCurrentPage(prev => Math.max(1, prev - 1))}
                  disabled={currentPage === 1}
                  className={`px-3 py-1.5 rounded text-sm ${
                    currentPage === 1
                      ? "text-slate-300 cursor-not-allowed opacity-50"
                      : "text-[#4b5563] hover:bg-slate-100"
                  }`}
                >
                  Trước
                </button>
                {Array.from({ length: totalPages }, (_, i) => i + 1).map((page) => (
                  <button
                    key={page}
                    onClick={() => setCurrentPage(page)}
                    className={`px-3 py-1.5 rounded text-sm font-normal ${
                      currentPage === page
                        ? "bg-[#00897b] text-white"
                        : "text-[#4b5563] hover:bg-slate-100"
                    }`}
                  >
                    {page}
                  </button>
                ))}
                <button
                  onClick={() => setCurrentPage(prev => Math.min(totalPages, prev + 1))}
                  disabled={currentPage === totalPages}
                  className={`px-3 py-1.5 rounded text-sm ${
                    currentPage === totalPages
                      ? "text-slate-300 cursor-not-allowed opacity-50"
                      : "text-[#4b5563] hover:bg-slate-100"
                  }`}
                >
                  Sau
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </>
  );
}
