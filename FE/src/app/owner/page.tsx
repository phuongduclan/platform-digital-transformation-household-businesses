"use client";

import { useEffect, useMemo, useState } from "react";
import LoadingOverlay from "@/components/ui/loading-overlay";
import { showToast } from "@/components/ui/toast";
import {
  ownerService,
  OwnerDebtPoint,
  OwnerInvoice,
  OwnerRevenuePoint,
} from "@/services/owner.service";

interface DashboardStats {
  today_revenue: number;
  month_revenue: number;
  total_invoices: number;
  total_outstanding_debt: number;
}

export default function OwnerDashboardPage() {
  const [stats, setStats] = useState<DashboardStats>({
    today_revenue: 0,
    month_revenue: 0,
    total_invoices: 0,
    total_outstanding_debt: 0,
  });
  const [revenueSeries, setRevenueSeries] = useState<OwnerRevenuePoint[]>([]);
  const [debtSeries, setDebtSeries] = useState<OwnerDebtPoint[]>([]);
  const [recentInvoices, setRecentInvoices] = useState<OwnerInvoice[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);

      const now = new Date();
      const todayStr = now.toISOString().slice(0, 10);

      const month = now.getMonth() + 1;
      const year = now.getFullYear();

      // chạy song song các request
      const [dailyRes, monthRevenue, outstandingDebt, invoices] =
        await Promise.all([
          ownerService.getDailyRevenue(todayStr),
          ownerService.getMonthlyRevenue(month, year),
          ownerService.getOutstandingDebt(),
          // Lấy hóa đơn nháp để chủ hộ theo dõi các chứng từ đang xử lý
          ownerService.listInvoices({ status: "Draft" }),
        ]);

      const totalInvoices = invoices.length;
      const totalDebt = outstandingDebt.reduce(
        (sum, x) => sum + x.balance,
        0
      );

      // build series doanh thu 7 ngày gần nhất (tạm thời: dùng lại doanh thu ngày hiện tại cho các điểm nếu chưa có API riêng)
      const days: OwnerRevenuePoint[] = [];
      for (let i = 6; i >= 0; i--) {
        const d = new Date(now);
        d.setDate(now.getDate() - i);
        const ds = d.toISOString().slice(0, 10);
        days.push({
          date: ds,
          total_revenue: ds === dailyRes.date ? dailyRes.total_revenue : 0,
        });
      }

      setStats({
        today_revenue: dailyRes.total_revenue,
        month_revenue: monthRevenue,
        total_invoices: totalInvoices,
        total_outstanding_debt: totalDebt,
      });
      setRevenueSeries(days);
      setDebtSeries(outstandingDebt);
      // Hiển thị toàn bộ hóa đơn nháp để owner dễ kiểm tra và giao việc cho nhân viên
      setRecentInvoices(invoices);
    } catch (error: any) {
      const message =
        error?.response?.data?.error ||
        error?.message ||
        "Lỗi khi tải dữ liệu dashboard Owner";
      showToast(message, "error");
    } finally {
      setLoading(false);
    }
  };

  const formattedRevenueSeries = useMemo(
    () =>
      revenueSeries.map((p) => ({
        label: new Date(p.date).toLocaleDateString("vi-VN", {
          day: "2-digit",
          month: "2-digit",
        }),
        value: p.total_revenue,
      })),
    [revenueSeries]
  );

  const maxRevenue = useMemo(
    () =>
      formattedRevenueSeries.reduce(
        (max, p) => (p.value > max ? p.value : max),
        0
      ) || 1,
    [formattedRevenueSeries]
  );

  const topDebt = useMemo(
    () => debtSeries.slice(0, 6),
    [debtSeries]
  );

  const maxDebt = useMemo(
    () =>
      topDebt.reduce((max, p) => (p.balance > max ? p.balance : max), 0) || 1,
    [topDebt]
  );

  const formatCurrency = (value: number | string | null | undefined) => {
    if (value === null || value === undefined) return "-";
    const num = Number(value);
    if (Number.isNaN(num)) return String(value);
    return new Intl.NumberFormat("vi-VN", {
      style: "currency",
      currency: "VND",
      maximumFractionDigits: 0,
    }).format(num);
  };

  const formatDateTime = (input?: string) => {
    if (!input) return "-";
    const d = new Date(input);
    return d.toLocaleString("vi-VN", {
      day: "2-digit",
      month: "2-digit",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  };

  return (
    <>
      <LoadingOverlay
        isLoading={loading}
        message="Đang tải dữ liệu tổng quan..."
      />
      <div className="p-8">
        {/* Page Header */}
        <div className="mb-8">
          <h1 className="text-[28px] font-bold italic text-[#1e3a8a] mb-2">
            Tổng quan hoạt động
          </h1>
          <p className="text-[16px] font-normal text-[#4b5563]">
            Tình hình doanh thu, công nợ và hóa đơn của hộ kinh doanh
          </p>
        </div>

        {/* Top stats */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6">
            <p className="text-sm font-normal text-[#4b5563] mb-2">
              Doanh thu hôm nay
            </p>
            <p className="text-[32px] font-bold italic text-[#1e3a8a]">
              {formatCurrency(stats.today_revenue)}
            </p>
          </div>

          <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6">
            <p className="text-sm font-normal text-[#4b5563] mb-2">
              Doanh thu tháng này
            </p>
            <p className="text-[32px] font-bold italic text-[#1e3a8a]">
              {formatCurrency(stats.month_revenue)}
            </p>
          </div>

          <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6">
            <p className="text-sm font-normal text-[#4b5563] mb-2">
              Tổng số hóa đơn nháp
            </p>
            <p className="text-[32px] font-bold italic text-[#1e3a8a]">
              {stats.total_invoices}
            </p>
          </div>

          <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6">
            <p className="text-sm font-normal text-[#4b5563] mb-2">
              Công nợ còn lại
            </p>
            <p className="text-[32px] font-bold italic text-[#1e3a8a]">
              {formatCurrency(stats.total_outstanding_debt)}
            </p>
          </div>
        </div>

        {/* Charts */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          {/* Revenue chart */}
          <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-base font-bold italic text-[#1e3a8a]">
                Doanh thu 7 ngày gần nhất
              </h2>
              <p className="text-xs font-normal text-[#4b5563]">
                Đơn vị: VND
              </p>
            </div>
            <div className="h-64">
              <svg
                className="w-full h-full"
                viewBox="0 0 500 220"
                preserveAspectRatio="none"
              >
                {/* Grid */}
                <line
                  x1="50"
                  y1="190"
                  x2="480"
                  y2="190"
                  stroke="#e5e7eb"
                  strokeWidth="1"
                />
                <line
                  x1="50"
                  y1="150"
                  x2="480"
                  y2="150"
                  stroke="#e5e7eb"
                  strokeWidth="1"
                />
                <line
                  x1="50"
                  y1="110"
                  x2="480"
                  y2="110"
                  stroke="#e5e7eb"
                  strokeWidth="1"
                />
                <line
                  x1="50"
                  y1="70"
                  x2="480"
                  y2="70"
                  stroke="#e5e7eb"
                  strokeWidth="1"
                />
                <line
                  x1="50"
                  y1="30"
                  x2="480"
                  y2="30"
                  stroke="#e5e7eb"
                  strokeWidth="1"
                />

                {/* Line & area */}
                {formattedRevenueSeries.length > 0 && (
                  <>
                    <path
                      d={
                        "M " +
                        formattedRevenueSeries
                          .map((p, index) => {
                            const x =
                              50 +
                              (index * (480 - 50)) /
                              Math.max(formattedRevenueSeries.length - 1, 1);
                            const ratio = p.value / maxRevenue;
                            const y = 190 - ratio * 160;
                            return `${x} ${y}`;
                          })
                          .join(" L ")
                      }
                      fill="none"
                      stroke="#00897b"
                      strokeWidth="2"
                    />
                    {/* Points */}
                    {formattedRevenueSeries.map((p, index) => {
                      const x =
                        50 +
                        (index * (480 - 50)) /
                        Math.max(formattedRevenueSeries.length - 1, 1);
                      const ratio = p.value / maxRevenue;
                      const y = 190 - ratio * 160;
                      return (
                        <circle
                          key={p.label}
                          cx={x}
                          cy={y}
                          r="4"
                          fill="#00897b"
                        />
                      );
                    })}
                  </>
                )}

                {/* X labels */}
                {formattedRevenueSeries.map((p, index) => {
                  const x =
                    50 +
                    (index * (480 - 50)) /
                    Math.max(formattedRevenueSeries.length - 1, 1);
                  return (
                    <text
                      key={p.label}
                      x={x}
                      y={210}
                      textAnchor="middle"
                      className="text-xs fill-[#1e3a8a]"
                    >
                      {p.label}
                    </text>
                  );
                })}
              </svg>
            </div>
          </div>

          {/* Outstanding debt chart */}
          <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-base font-bold italic text-[#1e3a8a]">
                Công nợ theo khách hàng (top)
              </h2>
              <p className="text-xs font-normal text-[#4b5563]">
                Đơn vị: VND
              </p>
            </div>
            <div className="h-64">
              {topDebt.length === 0 ? (
                <div className="h-full flex items-center justify-center text-sm text-[#6b7280]">
                  Chưa có dữ liệu công nợ
                </div>
              ) : (
                <svg
                  className="w-full h-full"
                  viewBox="0 0 500 220"
                  preserveAspectRatio="none"
                >
                  {/* Grid */}
                  <line
                    x1="50"
                    y1="190"
                    x2="480"
                    y2="190"
                    stroke="#e5e7eb"
                    strokeWidth="1"
                  />
                  <line
                    x1="50"
                    y1="150"
                    x2="480"
                    y2="150"
                    stroke="#e5e7eb"
                    strokeWidth="1"
                  />
                  <line
                    x1="50"
                    y1="110"
                    x2="480"
                    y2="110"
                    stroke="#e5e7eb"
                    strokeWidth="1"
                  />
                  <line
                    x1="50"
                    y1="70"
                    x2="480"
                    y2="70"
                    stroke="#e5e7eb"
                    strokeWidth="1"
                  />
                  <line
                    x1="50"
                    y1="30"
                    x2="480"
                    y2="30"
                    stroke="#e5e7eb"
                    strokeWidth="1"
                  />

                  {/* Bars */}
                  {topDebt.map((p, index) => {
                    const barWidth = 50;
                    const gap = 20;
                    const x =
                      50 +
                      index * (barWidth + gap) +
                      (480 - 50 - topDebt.length * barWidth - (topDebt.length - 1) * gap) /
                      2;
                    const ratio = p.balance / maxDebt;
                    const barHeight = ratio * 150;
                    const y = 190 - barHeight;
                    return (
                      <g key={p.customer_id}>
                        <rect
                          x={x}
                          y={y}
                          width={barWidth}
                          height={barHeight}
                          rx={4}
                          fill="#00897b"
                        />
                        <text
                          x={x + barWidth / 2}
                          y={y - 4}
                          textAnchor="middle"
                          className="text-xs fill-[#1e3a8a]"
                        >
                          {Math.round(p.balance / 1000)}k
                        </text>
                        <text
                          x={x + barWidth / 2}
                          y={210}
                          textAnchor="middle"
                          className="text-xs fill-[#1e3a8a]"
                        >
                          KH {p.customer_id}
                        </text>
                      </g>
                    );
                  })}
                </svg>
              )}
            </div>
          </div>
        </div>

        {/* Recent invoices table */}
        <div className="bg-white rounded-lg shadow-sm border border-slate-200 overflow-hidden">
          <div className="px-6 py-4 border-b border-slate-200 flex items-center justify-between">
            <h2 className="text-base font-bold italic text-[#1e3a8a]">
              Hoạt động gần đây (hóa đơn nháp)
            </h2>
            <p className="text-xs font-normal text-[#6b7280]">
              Hiển thị tất cả hóa đơn nháp để tiện rà soát và xác nhận
            </p>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-slate-50 border-b border-slate-200">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-bold italic text-[#4b5563] uppercase tracking-wider">
                    Mã hóa đơn
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-bold italic text-[#4b5563] uppercase tracking-wider">
                    Khách hàng
                  </th>
                  <th className="px-6 py-3 text-right text-xs font-bold italic text-[#4b5563] uppercase tracking-wider">
                    Tổng tiền
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-bold italic text-[#4b5563] uppercase tracking-wider">
                    Trạng thái
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-bold italic text-[#4b5563] uppercase tracking-wider">
                    Thời gian
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-slate-200">
                {recentInvoices.length === 0 ? (
                  <tr>
                    <td colSpan={5} className="px-6 py-8 text-center text-[#6b7280] text-sm">
                      Chưa có hóa đơn nháp
                    </td>
                  </tr>
                ) : (
                  recentInvoices.map((inv) => (
                    <tr key={inv.id} className="hover:bg-slate-50">
                      <td className="px-6 py-3 text-sm font-normal text-[#1e3a8a]">
                        {inv.invoice_number || `HD-${inv.id}`}
                      </td>
                      <td className="px-6 py-3 text-sm font-normal text-[#4b5563]">
                        {inv.customer_name || "-"}
                      </td>
                      <td className="px-6 py-3 text-sm font-bold text-right text-[#1e3a8a]">
                        {inv.total_amount != null
                          ? formatCurrency(inv.total_amount)
                          : "-"}
                      </td>
                      <td className="px-6 py-3 text-sm font-normal text-[#4b5563]">
                        {inv.status || "-"}
                      </td>
                      <td className="px-6 py-3 text-sm font-normal text-[#4b5563]">
                        {formatDateTime(inv.created_at)}
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </>
  );
}

