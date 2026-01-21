"use client";

import { useEffect, useMemo, useState } from "react";
import Link from "next/link";
import LoadingOverlay from "@/components/ui/loading-overlay";
import { showToast } from "@/components/ui/toast";
import {
  ownerService,
  OwnerPayment,
  OwnerPaymentMethod,
  OwnerInvoice,
} from "@/services/owner.service";

export default function OwnerPaymentsPage() {
  const [payments, setPayments] = useState<OwnerPayment[]>([]);
  const [methods, setMethods] = useState<OwnerPaymentMethod[]>([]);
  const [invoices, setInvoices] = useState<OwnerInvoice[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState("");

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [payList, methodList, invList] = await Promise.all([
        ownerService.listPayments(),
        ownerService.listOwnerPaymentMethods(),
        ownerService.listInvoices({ status: "Confirm" }),
      ]);
      setPayments(payList || []);
      setMethods(methodList || []);
      setInvoices(invList || []);
    } catch (error: any) {
      const message =
        error?.response?.data?.error ||
        error?.message ||
        "Lỗi khi tải danh sách thanh toán";
      showToast(message, "error");
    } finally {
      setLoading(false);
    }
  };

  const methodMap = useMemo(() => {
    const m = new Map<number, OwnerPaymentMethod>();
    methods.forEach((pm) => m.set(pm.id, pm));
    return m;
  }, [methods]);

  const invoiceMap = useMemo(() => {
    const m = new Map<number, OwnerInvoice>();
    invoices.forEach((inv: any) => m.set(inv.id, inv));
    return m;
  }, [invoices]);

  const filteredPayments = useMemo(() => {
    const term = searchTerm.trim().toLowerCase();
    if (!term) return payments;
    return payments.filter((p) => {
      const inv = invoiceMap.get(p.invoice_id);
      const method = methodMap.get(p.method_id);
      const invoiceText = inv ? `HD ${inv.id}` : "";
      const customerText = (inv?.customer_name || "").toLowerCase();
      const methodText = (method?.name || "").toLowerCase();
      const descText = (p.description || "").toLowerCase();
      const idText = String(p.id);
      return (
        idText.includes(term) ||
        invoiceText.toLowerCase().includes(term) ||
        customerText.includes(term) ||
        methodText.includes(term) ||
        descText.includes(term)
      );
    });
  }, [payments, searchTerm, invoiceMap, methodMap]);

  const formatCurrency = (value: string | null) => {
    const num = Number(value || 0);
    return new Intl.NumberFormat("vi-VN", {
      style: "currency",
      currency: "VND",
      maximumFractionDigits: 0,
    }).format(num);
  };

  const formatDateTime = (value?: string | null) => {
    if (!value) return "-";
    const d = new Date(value);
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
        message="Đang tải danh sách thanh toán..."
      />
      <div className="p-8">
        {/* Header */}
        <div className="mb-6 flex items-center justify-between">
          <h1 className="text-[28px] font-bold italic text-[#1e3a8a]">
            Thanh toán
          </h1>
          <Link
            href="/owner/payments/create"
            className="px-4 py-2 bg-[#00897b] text-white rounded-lg hover:bg-[#007a6c] transition-colors font-bold italic text-base flex items-center gap-2"
          >
            <span>+</span>
            <span>Tạo thanh toán</span>
          </Link>
        </div>

        {/* Filter */}
        <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6 mb-6">
          <div className="flex gap-2">
            <input
              type="text"
              placeholder="Tìm theo mã thanh toán, hóa đơn, khách hàng, phương thức..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="flex-1 px-4 py-2.5 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#00897b] focus:border-transparent"
            />
            <button
              type="button"
              onClick={() => {
                setSearchTerm("");
                fetchData();
              }}
              className="px-4 py-2 bg-white border border-[#1e3a8a] text-[#1e3a8a] rounded-lg hover:bg-slate-50 transition-colors text-sm font-medium"
            >
              Làm mới
            </button>
          </div>
        </div>

        {/* Table */}
        <div className="bg-white rounded-lg shadow-sm border border-slate-200 overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-slate-50 border-b border-slate-200">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-bold italic text-[#4b5563] uppercase tracking-wider">
                    Mã thanh toán
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-bold italic text-[#4b5563] uppercase tracking-wider">
                    Hóa đơn
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-bold italic text-[#4b5563] uppercase tracking-wider">
                    Phương thức
                  </th>
                  <th className="px-6 py-3 text-right text-xs font-bold italic text-[#4b5563] uppercase tracking-wider">
                    Số tiền
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-bold italic text-[#4b5563] uppercase tracking-wider">
                    Trạng thái
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-bold italic text-[#4b5563] uppercase tracking-wider">
                    Ngày thanh toán
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-bold italic text-[#4b5563] uppercase tracking-wider">
                    Thao tác
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-slate-200">
                {filteredPayments.length === 0 ? (
                  <tr>
                    <td
                      colSpan={7}
                      className="px-6 py-12 text-center text-slate-500"
                    >
                      Không có thanh toán
                    </td>
                  </tr>
                ) : (
                  filteredPayments.map((p) => {
                    const inv = invoiceMap.get(p.invoice_id);
                    const method = methodMap.get(p.method_id);
                    return (
                      <tr
                        key={p.id}
                        className="hover:bg-slate-50 transition-colors"
                      >
                        <td className="px-6 py-4 text-sm font-normal text-[#1e3a8a]">
                          {p.id}
                        </td>
                        <td className="px-6 py-4 text-sm font-normal text-[#1e3a8a]">
                          {inv ? `Hóa đơn #${inv.id}` : `Hóa đơn #${p.invoice_id}`}
                        </td>
                        <td className="px-6 py-4 text-sm font-normal text-[#1e3a8a]">
                          {method?.name || `PT #${p.method_id}`}
                        </td>
                        <td className="px-6 py-4 text-sm font-normal text-right text-[#1e3a8a]">
                          {formatCurrency(p.amount)}
                        </td>
                        <td className="px-6 py-4 text-sm font-normal text-[#1e3a8a]">
                          {p.status || "-"}
                        </td>
                        <td className="px-6 py-4 text-sm font-normal text-[#1e3a8a]">
                          {formatDateTime(p.created_at)}
                        </td>
                        <td className="px-6 py-4">
                          <div className="flex items-center gap-3">
                            <Link
                              href={`/owner/payments/${p.id}`}
                              className="px-3 py-1 text-sm text-[#1e3a8a] hover:text-[#00897b] transition-colors border border-[#1e3a8a] rounded hover:border-[#00897b]"
                            >
                              Xem
                            </Link>
                          </div>
                        </td>
                      </tr>
                    );
                  })
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </>
  );
}

