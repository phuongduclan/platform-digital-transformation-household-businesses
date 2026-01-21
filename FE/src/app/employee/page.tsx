"use client";

import { useEffect, useMemo, useState } from "react";
import LoadingOverlay from "@/components/ui/loading-overlay";
import { showToast } from "@/components/ui/toast";
import {
  employeeService,
  EmployeeInvoice,
  EmployeeDebtRecord,
} from "@/services/employee.service";
import Link from "next/link";

interface EmployeeDashboardStats {
  draft_invoices: number;
  customers_in_debt: number;
  total_debt_amount: number;
}

export default function EmployeeDashboardPage() {
  const [stats, setStats] = useState<EmployeeDashboardStats>({
    draft_invoices: 0,
    customers_in_debt: 0,
    total_debt_amount: 0,
  });
  const [draftInvoices, setDraftInvoices] = useState<EmployeeInvoice[]>([]);
  const [debtRecords, setDebtRecords] = useState<EmployeeDebtRecord[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);

      const [invoices, debts] = await Promise.all([
        employeeService.listInvoices({ status: "Draft" }),
        employeeService.listDebtRecords(),
      ]);

      setDraftInvoices(invoices || []);
      setDebtRecords(debts || []);

      // Tính dư nợ hiện tại theo từng khách hàng: lấy balance mới nhất
      const customerLatest: Record<number, EmployeeDebtRecord> = {};
      for (const dr of debts || []) {
        if (!dr.customer_id) continue;
        const current = customerLatest[dr.customer_id];
        if (!current) {
          customerLatest[dr.customer_id] = dr;
        } else {
          // so sánh theo record_at hoặc id (fallback)
          const curTime = current.record_at || "";
          const newTime = dr.record_at || "";
          if (newTime > curTime || (!curTime && dr.id > current.id)) {
            customerLatest[dr.customer_id] = dr;
          }
        }
      }

      let customersInDebt = 0;
      let totalDebtAmount = 0;
      Object.values(customerLatest).forEach((dr) => {
        const bal = dr.balance ? Number(dr.balance) : 0;
        if (bal > 0) {
          customersInDebt += 1;
          totalDebtAmount += bal;
        }
      });

      setStats({
        draft_invoices: invoices.length,
        customers_in_debt: customersInDebt,
        total_debt_amount: totalDebtAmount,
      });
    } catch (error: any) {
      const message =
        error?.response?.data?.error ||
        error?.message ||
        "Lỗi khi tải dữ liệu tổng quan nhân viên";
      showToast(message, "error");
    } finally {
      setLoading(false);
    }
  };

  const formatCurrency = (value: number) =>
    new Intl.NumberFormat("vi-VN", {
      style: "currency",
      currency: "VND",
      maximumFractionDigits: 0,
    }).format(value);

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

  const draftInvoicesTop = useMemo(
    () =>
      [...draftInvoices]
        .sort((a, b) => {
          const ta = a.created_at || "";
          const tb = b.created_at || "";
          return tb.localeCompare(ta);
        })
        .slice(0, 10),
    [draftInvoices]
  );

  const customersInDebt = useMemo(() => {
    const customerLatest: Record<number, EmployeeDebtRecord> = {};
    for (const dr of debtRecords || []) {
      if (!dr.customer_id) continue;
      const current = customerLatest[dr.customer_id];
      if (!current) {
        customerLatest[dr.customer_id] = dr;
      } else {
        const curTime = current.record_at || "";
        const newTime = dr.record_at || "";
        if (newTime > curTime || (!curTime && dr.id > current.id)) {
          customerLatest[dr.customer_id] = dr;
        }
      }
    }
    return Object.values(customerLatest)
      .map((dr) => ({
        customer_id: dr.customer_id,
        balance: dr.balance ? Number(dr.balance) : 0,
      }))
      .filter((x) => x.balance > 0)
      .sort((a, b) => b.balance - a.balance)
      .slice(0, 10);
  }, [debtRecords]);

  return (
    <>
      <LoadingOverlay
        isLoading={loading}
        message="Đang tải dữ liệu tổng quan nhân viên..."
      />
      <div className="p-8">
        {/* Page Header */}
        <div className="mb-8">
          <h1 className="text-[28px] font-bold italic text-[#1e3a8a] mb-2">
            Tổng quan nhân viên
          </h1>
          <p className="text-[16px] font-normal text-[#4b5563]">
            Tổng hợp nhanh hóa đơn nháp và công nợ khách hàng để bạn xử lý
            trong ngày.
          </p>
        </div>

        {/* Top stats */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6">
            <p className="text-sm font-normal text-[#4b5563] mb-2">
              Hóa đơn nháp
            </p>
            <p className="text-[32px] font-bold italic text-[#1e3a8a]">
              {stats.draft_invoices}
            </p>
          </div>

          <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6">
            <p className="text-sm font-normal text-[#4b5563] mb-2">
              Khách hàng còn dư nợ
            </p>
            <p className="text-[32px] font-bold italic text-[#1e3a8a]">
              {stats.customers_in_debt}
            </p>
          </div>

          <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6">
            <p className="text-sm font-normal text-[#4b5563] mb-2">
              Tổng dư nợ khách hàng
            </p>
            <p className="text-[32px] font-bold italic text-[#1e3a8a]">
              {formatCurrency(stats.total_debt_amount)}
            </p>
          </div>
        </div>

        {/* Tables */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Draft invoices */}
          <div className="bg-white rounded-lg shadow-sm border border-slate-200 overflow-hidden">
            <div className="px-6 py-4 border-b border-slate-200 flex items-center justify-between">
              <h2 className="text-base font-bold italic text-[#1e3a8a]">
                Hóa đơn nháp gần đây
              </h2>
              <Link
                href="/employee/invoices"
                className="text-xs text-[#00897b] hover:underline"
              >
                Xem tất cả
              </Link>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-slate-50 border-b border-slate-200">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-bold italic text-[#4b5563] uppercase tracking-wider">
                      Mã hóa đơn
                    </th>
                    <th className="px-6 py-3 text-right text-xs font-bold italic text-[#4b5563] uppercase tracking-wider">
                      Tổng tiền
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-bold italic text-[#4b5563] uppercase tracking-wider">
                      Thời gian
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-bold italic text-[#4b5563] uppercase tracking-wider">
                      Thao tác
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-slate-200">
                  {draftInvoicesTop.length === 0 ? (
                    <tr>
                      <td
                        colSpan={4}
                        className="px-6 py-8 text-center text-[#6b7280] text-sm"
                      >
                        Chưa có hóa đơn nháp
                      </td>
                    </tr>
                  ) : (
                    draftInvoicesTop.map((inv) => (
                      <tr key={inv.id} className="hover:bg-slate-50">
                        <td className="px-6 py-3 text-sm font-normal text-[#1e3a8a]">
                          {inv.id}
                        </td>
                        <td className="px-6 py-3 text-sm font-bold text-right text-[#1e3a8a]">
                          {inv.total_amount
                            ? formatCurrency(Number(inv.total_amount))
                            : "-"}
                        </td>
                        <td className="px-6 py-3 text-sm font-normal text-[#4b5563]">
                          {formatDateTime(inv.created_at)}
                        </td>
                        <td className="px-6 py-3 text-sm">
                          <Link
                            href={`/employee/invoices/${inv.id}`}
                            className="px-3 py-1 text-xs text-[#1e3a8a] hover:text-[#00897b] transition-colors border border-[#1e3a8a] rounded hover:border-[#00897b]"
                          >
                            Xem
                          </Link>
                        </td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>
          </div>

          {/* Customers in debt */}
          <div className="bg-white rounded-lg shadow-sm border border-slate-200 overflow-hidden">
            <div className="px-6 py-4 border-b border-slate-200 flex items-center justify-between">
              <h2 className="text-base font-bold italic text-[#1e3a8a]">
                Khách hàng còn dư nợ
              </h2>
              <Link
                href="/employee/debt-records"
                className="text-xs text-[#00897b] hover:underline"
              >
                Xem chi tiết
              </Link>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-slate-50 border-b border-slate-200">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-bold italic text-[#4b5563] uppercase tracking-wider">
                      Mã khách hàng
                    </th>
                    <th className="px-6 py-3 text-right text-xs font-bold italic text-[#4b5563] uppercase tracking-wider">
                      Dư nợ hiện tại
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-bold italic text-[#4b5563] uppercase tracking-wider">
                      Thao tác
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-slate-200">
                  {customersInDebt.length === 0 ? (
                    <tr>
                      <td
                        colSpan={3}
                        className="px-6 py-8 text-center text-[#6b7280] text-sm"
                      >
                        Không có khách hàng còn dư nợ
                      </td>
                    </tr>
                  ) : (
                    customersInDebt.map((c) => (
                      <tr key={c.customer_id} className="hover:bg-slate-50">
                        <td className="px-6 py-3 text-sm font-normal text-[#1e3a8a]">
                          {c.customer_id}
                        </td>
                        <td className="px-6 py-3 text-sm font-bold text-right text-[#1e3a8a]">
                          {formatCurrency(c.balance)}
                        </td>
                        <td className="px-6 py-3 text-sm">
                          <Link
                            href={`/employee/debt-records/${c.customer_id}`}
                            className="px-3 py-1 text-xs text-[#1e3a8a] hover:text-[#00897b] transition-colors border border-[#1e3a8a] rounded hover:border-[#00897b]"
                          >
                            Xem công nợ
                          </Link>
                        </td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}

