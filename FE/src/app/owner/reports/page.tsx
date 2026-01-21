"use client";

import { useEffect, useMemo, useState } from "react";
import LoadingOverlay from "@/components/ui/loading-overlay";
import { showToast } from "@/components/ui/toast";
import {
  ownerService,
  OwnerDebtPoint,
} from "@/services/owner.service";

export default function OwnerReportsPage() {
  const [dailyDate, setDailyDate] = useState("");
  const [dailyRevenue, setDailyRevenue] = useState<number | null>(null);
  const [monthlyYear, setMonthlyYear] = useState<number>(
    new Date().getFullYear()
  );
  const [monthlyMonth, setMonthlyMonth] = useState<number>(
    new Date().getMonth() + 1
  );
  const [monthlyRevenue, setMonthlyRevenue] = useState<number | null>(null);
  const [outstanding, setOutstanding] = useState<OwnerDebtPoint[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const today = new Date().toISOString().slice(0, 10);
    setDailyDate(today);
    fetchDaily(today);
    fetchMonthly(monthlyMonth, monthlyYear);
    fetchOutstanding();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const fetchDaily = async (date: string) => {
    try {
      setLoading(true);
      const res = await ownerService.getDailyRevenue(date);
      setDailyRevenue(res.total_revenue);
    } catch (error: any) {
      showToast(
        error?.response?.data?.error ||
          error?.message ||
          "Lỗi khi tải doanh thu theo ngày",
        "error"
      );
    } finally {
      setLoading(false);
    }
  };

  const fetchMonthly = async (month: number, year: number) => {
    try {
      setLoading(true);
      const val = await ownerService.getMonthlyRevenue(month, year);
      setMonthlyRevenue(val);
    } catch (error: any) {
      showToast(
        error?.response?.data?.error ||
          error?.message ||
          "Lỗi khi tải doanh thu theo tháng",
        "error"
      );
    } finally {
      setLoading(false);
    }
  };

  const fetchOutstanding = async () => {
    try {
      setLoading(true);
      const data = await ownerService.getOutstandingDebt();
      setOutstanding(data || []);
    } catch (error: any) {
      showToast(
        error?.response?.data?.error ||
          error?.message ||
          "Lỗi khi tải báo cáo công nợ",
        "error"
      );
    } finally {
      setLoading(false);
    }
  };

  const totalOutstanding = useMemo(
    () => outstanding.reduce((sum, x) => sum + x.balance, 0),
    [outstanding]
  );

  const formatCurrency = (value: number) =>
    new Intl.NumberFormat("vi-VN", {
      style: "currency",
      currency: "VND",
      maximumFractionDigits: 0,
    }).format(value || 0);

  return (
    <>
      <LoadingOverlay
        isLoading={loading}
        message="Đang tải báo cáo..."
      />
      <div className="p-8 space-y-6">
        <h1 className="text-[28px] font-bold italic text-[#1e3a8a]">
          Báo cáo
        </h1>

        {/* Daily revenue */}
        <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-[18px] font-bold italic text-[#1e3a8a]">
              Doanh thu theo ngày
            </h2>
            <div className="flex items-center gap-3">
              <input
                type="date"
                value={dailyDate}
                onChange={(e) => setDailyDate(e.target.value)}
                className="px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#00897b] focus:border-transparent"
              />
              <button
                type="button"
                onClick={() => dailyDate && fetchDaily(dailyDate)}
                className="px-4 py-2 bg-[#00897b] text-white rounded-lg text-sm font-bold hover:bg-[#007a6c] transition-colors"
              >
                Xem
              </button>
            </div>
          </div>
          <p className="text-sm text-[#4b5563] mb-1">
            Tổng doanh thu ngày {dailyDate || "-"}:
          </p>
          <p className="text-2xl font-bold italic text-[#00897b]">
            {formatCurrency(dailyRevenue || 0)}
          </p>
        </div>

        {/* Monthly revenue */}
        <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-[18px] font-bold italic text-[#1e3a8a]">
              Doanh thu theo tháng
            </h2>
            <div className="flex items-center gap-3">
              <select
                value={monthlyMonth}
                onChange={(e) => setMonthlyMonth(Number(e.target.value))}
                className="px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#00897b] focus:border-transparent"
              >
                {Array.from({ length: 12 }).map((_, idx) => (
                  <option key={idx + 1} value={idx + 1}>
                    Tháng {idx + 1}
                  </option>
                ))}
              </select>
              <input
                type="number"
                value={monthlyYear}
                onChange={(e) => setMonthlyYear(Number(e.target.value))}
                className="w-24 px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#00897b] focus:border-transparent"
              />
              <button
                type="button"
                onClick={() => fetchMonthly(monthlyMonth, monthlyYear)}
                className="px-4 py-2 bg-[#00897b] text-white rounded-lg text-sm font-bold hover:bg-[#007a6c] transition-colors"
              >
                Xem
              </button>
            </div>
          </div>

          <p className="text-sm text-[#4b5563] mb-1">
            Tổng doanh thu {`tháng ${monthlyMonth}/${monthlyYear}`}:
          </p>
          <p className="text-2xl font-bold italic text-[#00897b]">
            {formatCurrency(monthlyRevenue || 0)}
          </p>
        </div>

        {/* Outstanding debt */}
        <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-[18px] font-bold italic text-[#1e3a8a]">
              Báo cáo công nợ
            </h2>
          </div>
          <p className="text-sm text-[#4b5563] mb-2">
            Tổng công nợ hiện tại:
          </p>
          <p className="text-2xl font-bold italic text-[#ef4444] mb-4">
            {formatCurrency(totalOutstanding)}
          </p>

          <h3 className="text-sm font-bold italic text-[#1e3a8a] mb-2">
            Khách hàng còn nợ
          </h3>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-slate-50 border-b border-slate-200">
                <tr>
                  <th className="px-4 py-2 text-left text-xs font-bold italic text-[#4b5563] uppercase tracking-wider">
                    Khách hàng (ID)
                  </th>
                  <th className="px-4 py-2 text-right text-xs font-bold italic text-[#4b5563] uppercase tracking-wider">
                    Dư nợ
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-slate-200">
                {outstanding.length === 0 ? (
                  <tr>
                    <td
                      colSpan={2}
                      className="px-4 py-6 text-center text-sm text-[#6b7280]"
                    >
                      Không có khách hàng nợ.
                    </td>
                  </tr>
                ) : (
                  outstanding.map((item) => (
                    <tr key={item.customer_id}>
                      <td className="px-4 py-2 text-sm text-[#1e3a8a]">
                        Khách #{item.customer_id}
                      </td>
                      <td className="px-4 py-2 text-sm text-right text-[#ef4444]">
                        {formatCurrency(item.balance)}
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

