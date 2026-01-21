"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { showToast } from "@/components/ui/toast";
import LoadingOverlay from "@/components/ui/loading-overlay";
import { adminService } from "@/services/admin.service";

interface DashboardStats {
  total_owners: number;
  subscriptions_active: number;
  subscription_plans: number;
  revenue_this_month: string;
}

interface QuickAction {
  title: string;
  description: string;
  href: string;
  disabled?: boolean;
  note?: string;
}

export default function AdminDashboard() {
  const router = useRouter();
  const [stats, setStats] = useState<DashboardStats>({
    total_owners: 42,
    subscriptions_active: 38,
    subscription_plans: 5,
    revenue_this_month: "8.5M",
  });
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      const data = await adminService.getDashboardStats();
      // Format revenue
      const revenue = data.revenue_this_month || 0;
      const revenueFormatted = revenue >= 1000000
        ? `${(revenue / 1000000).toFixed(1)}M`
        : revenue >= 1000
          ? `${(revenue / 1000).toFixed(1)}K`
          : revenue.toString();

      setStats({
        total_owners: data.total_owners || 0,
        subscriptions_active: data.subscriptions_active || 0,
        subscription_plans: data.subscription_plans || 0,
        revenue_this_month: revenueFormatted,
      });
    } catch (error: any) {
      showToast(error.message || "Lỗi khi tải dữ liệu dashboard", "error");
    } finally {
      setLoading(false);
    }
  };

  const quickActions: QuickAction[] = [
    {
      title: "Tạo người dùng mới",
      description: "Thêm Admin hoặc Owner",
      href: "/admin/users/create",
    },
    {
      title: "Tạo gói đăng ký",
      description: "Thiết lập gói dịch vụ mới",
      href: "/admin/subscription-plans/create",
    },
    {
      title: "Xem báo cáo",
      description: "Phân tích và thống kê",
      href: "/admin/analytics",
    },
    {
      title: "Cài đặt hệ thống",
      description: "Cấu hình tổng thể",
      href: "/admin/config",
    },
  ];

  return (
    <>
      <LoadingOverlay isLoading={loading} message="Đang tải dữ liệu..." />
      <div className="p-8">
        {/* Page Header */}
        <div className="mb-8">
          <h1 className="text-[28px] font-bold italic text-[#1e3a8a] mb-2">
            Dashboard
          </h1>
          <p className="text-[16px] font-normal text-[#4b5563]">
            Tổng quan hoạt động hệ thống BizFlow
          </p>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {/* Total Owners */}
          <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6">
            <div className="flex items-start justify-between mb-4">
              <div className="flex-1">
                <p className="text-sm font-normal text-[#4b5563] mb-2">Tổng số Owner</p>
                <p className="text-[32px] font-bold italic text-[#1e3a8a]">{stats.total_owners}</p>
              </div>
            </div>
          </div>

          {/* Subscriptions Active */}
          <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6">
            <div className="flex items-start justify-between mb-4">
              <div className="flex-1">
                <p className="text-sm font-normal text-[#4b5563] mb-2">Subscriptions Active</p>
                <p className="text-[32px] font-bold italic text-[#1e3a8a]">{stats.subscriptions_active}</p>
              </div>
            </div>
          </div>

          {/* Subscription Plans */}
          <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6">
            <div className="flex items-start justify-between mb-4">
              <div className="flex-1">
                <p className="text-sm font-normal text-[#4b5563] mb-2">Subscription Plans</p>
                <p className="text-[32px] font-bold italic text-[#1e3a8a]">{stats.subscription_plans}</p>
              </div>
            </div>
          </div>

          {/* Revenue This Month */}
          <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6">
            <div className="flex items-start justify-between mb-4">
              <div className="flex-1">
                <p className="text-sm font-normal text-[#4b5563] mb-2">Doanh thu tháng này</p>
                <p className="text-[32px] font-bold italic text-[#1e3a8a]">{stats.revenue_this_month}</p>
              </div>
            </div>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="mb-8">
          <h2 className="text-[20px] font-bold italic text-[#1e3a8a] mb-4">
            Thao tác nhanh
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {quickActions.map((action, index) => (
              <button
                key={index}
                onClick={() => {
                  if (action.disabled || !action.href) return;
                  router.push(action.href);
                }}
                disabled={Boolean(action.disabled)}
                className={`bg-white rounded-lg shadow-sm border border-slate-200 p-6 transition-shadow text-left ${action.disabled
                    ? "opacity-60 cursor-not-allowed"
                    : "hover:shadow-md"
                  }`}
              >
                <div>
                  <p className="text-[15px] font-bold italic text-[#1e3a8a] mb-1">
                    {action.title}
                  </p>
                  <p className="text-[13px] font-normal text-[#4b5563]">
                    {action.description}
                  </p>
                  {action.disabled && action.note && (
                    <p className="text-[12px] font-normal text-[#9ca3af] mt-2">
                      {action.note}
                    </p>
                  )}
                </div>
              </button>
            ))}
          </div>
        </div>
      </div>
    </>
  );
}
