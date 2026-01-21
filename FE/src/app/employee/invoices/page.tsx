"use client";

import { useEffect, useMemo, useState } from "react";
import { useRouter } from "next/navigation";
import LoadingOverlay from "@/components/ui/loading-overlay";
import { showToast } from "@/components/ui/toast";
import {
  employeeService,
  EmployeeInvoice,
} from "@/services/employee.service";

type InvoiceStatusFilter = "" | "Draft" | "Confirm" | "Delete";

export default function EmployeeInvoicesPage() {
  const router = useRouter();
  const [invoices, setInvoices] = useState<EmployeeInvoice[]>([]);
  const [loading, setLoading] = useState(true);
  const [statusFilter, setStatusFilter] = useState<InvoiceStatusFilter>("");
  const [searchTerm, setSearchTerm] = useState("");

  useEffect(() => {
    fetchInvoices();
  }, []);

  const fetchInvoices = async () => {
    try {
      setLoading(true);
      const data = await employeeService.listInvoices();
      setInvoices(data || []);
    } catch (error: any) {
      showToast(
        error?.response?.data?.error ||
          error?.message ||
          "Lỗi khi tải danh sách hóa đơn",
        "error"
      );
    } finally {
      setLoading(false);
    }
  };

  const filteredInvoices = useMemo(() => {
    const term = searchTerm.trim().toLowerCase();
    return invoices.filter((inv) => {
      if (statusFilter && inv.status !== statusFilter) return false;
      if (!term) return true;
      const idStr = String(inv.id);
      const desc = (inv as any).description?.toLowerCase?.() || "";
      return idStr.includes(term) || desc.includes(term);
    });
  }, [invoices, statusFilter, searchTerm]);

  const formatDate = (value?: string) => {
    if (!value) return "-";
    const d = new Date(value);
    return d.toLocaleDateString("vi-VN", {
      day: "2-digit",
      month: "2-digit",
      year: "numeric",
    });
  };

  const formatCurrency = (value: string | null) => {
    if (!value) return "-";
    const num = Number(value);
    if (Number.isNaN(num)) return value;
    return new Intl.NumberFormat("vi-VN", {
      style: "currency",
      currency: "VND",
      maximumFractionDigits: 0,
    }).format(num);
  };

  const handleDelete = async (invoice: EmployeeInvoice) => {
    if (!confirm("Bạn có chắc chắn muốn xóa hóa đơn này?")) return;
    try {
      await employeeService.deleteInvoice(invoice.id);
      showToast("Xóa hóa đơn thành công", "success");
      fetchInvoices();
    } catch (error: any) {
      showToast(
        error?.response?.data?.error ||
          error?.message ||
          "Lỗi khi xóa hóa đơn",
        "error"
      );
    }
  };

  const handleConfirm = async (invoice: EmployeeInvoice) => {
    if (invoice.status !== "Draft") return;
    if (
      !confirm(
        "Xác nhận hóa đơn sẽ tự động tạo chứng từ nhập/xuất, tồn kho và công nợ. Tiếp tục?"
      )
    )
      return;
    try {
      await employeeService.confirmInvoice(invoice.id);
      showToast("Xác nhận hóa đơn thành công", "success");
      fetchInvoices();
    } catch (error: any) {
      showToast(
        error?.response?.data?.error ||
          error?.message ||
          "Lỗi khi xác nhận hóa đơn",
        "error"
      );
    }
  };

  const getStatusBadge = (status: string) => {
    let color = "bg-slate-500";
    if (status === "Draft") color = "bg-yellow-500";
    if (status === "Confirm") color = "bg-[#10b981]";
    if (status === "Delete") color = "bg-red-500";
    return (
      <span
        className={`px-2 py-1 text-xs font-bold italic rounded-full text-white ${color}`}
      >
        {status}
      </span>
    );
  };

  return (
    <>
      <LoadingOverlay
        isLoading={loading}
        message="Đang tải danh sách hóa đơn..."
      />
      <div className="p-8">
        <div className="mb-6 flex items-center justify-between">
          <h1 className="text-[28px] font-bold italic text-[#1e3a8a]">
            Hóa đơn
          </h1>
          <button
            type="button"
            onClick={() => router.push("/employee/invoices/create")}
            className="px-4 py-2 bg-[#00897b] text-white rounded-lg hover:bg-[#007a6c] transition-colors font-bold italic text-base flex items-center gap-2"
          >
            <span>+</span>
            <span>Tạo hóa đơn</span>
          </button>
        </div>

        {/* Filter card */}
        <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6 mb-6">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="md:col-span-2">
              <label className="block text-sm font-normal text-[#1e3a8a] mb-1.5">
                Tìm kiếm
              </label>
              <input
                type="text"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#00897b] focus:border-transparent"
                placeholder="Tìm theo số hóa đơn hoặc mô tả"
              />
            </div>
            <div>
              <label className="block text-sm font-normal text-[#1e3a8a] mb-1.5">
                Trạng thái
              </label>
              <select
                value={statusFilter}
                onChange={(e) =>
                  setStatusFilter(e.target.value as InvoiceStatusFilter)
                }
                className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#00897b] focus:border-transparent"
              >
                <option value="">Tất cả</option>
                <option value="Draft">Draft</option>
                <option value="Confirm">Confirm</option>
                <option value="Delete">Delete</option>
              </select>
            </div>
            <div className="flex items-end">
              <button
                type="button"
                onClick={fetchInvoices}
                className="w-full px-4 py-2 bg-white border border-[#1e3a8a] text-[#1e3a8a] rounded-lg hover:bg-slate-50 transition-colors text-sm font-medium"
              >
                Làm mới
              </button>
            </div>
          </div>
        </div>

        {/* Table */}
        <div className="bg-white rounded-lg shadow-sm border border-slate-200 overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-slate-50 border-b border-slate-200">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-bold italic text-[#4b5563] uppercase tracking-wider">
                    Số chứng từ
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-bold italic text-[#4b5563] uppercase tracking-wider">
                    Ngày
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-bold italic text-[#4b5563] uppercase tracking-wider">
                    Mô tả
                  </th>
                  <th className="px-6 py-3 text-right text-xs font-bold italic text-[#4b5563] uppercase tracking-wider">
                    Tổng tiền
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-bold italic text-[#4b5563] uppercase tracking-wider">
                    Trạng thái
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-bold italic text-[#4b5563] uppercase tracking-wider">
                    Thao tác
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-slate-200">
                {filteredInvoices.length === 0 ? (
                  <tr>
                    <td
                      colSpan={6}
                      className="px-6 py-8 text-center text-sm text-[#6b7280]"
                    >
                      Không có hóa đơn
                    </td>
                  </tr>
                ) : (
                  filteredInvoices.map((inv) => (
                    <tr key={inv.id} className="hover:bg-slate-50">
                      <td className="px-6 py-3 text-sm text-[#1e3a8a]">
                        {inv.id}
                      </td>
                      <td className="px-6 py-3 text-sm text-[#1e3a8a]">
                        {formatDate(inv.created_at)}
                      </td>
                      <td className="px-6 py-3 text-sm text-[#4b5563]">
                        {(inv as any).description || "-"}
                      </td>
                      <td className="px-6 py-3 text-sm text-right text-[#1e3a8a]">
                        {formatCurrency((inv as any).total_amount as any)}
                      </td>
                      <td className="px-6 py-3 text-sm">
                        {getStatusBadge((inv as any).status as string)}
                      </td>
                      <td className="px-6 py-3">
                        <div className="flex items-center gap-2">
                          <button
                            type="button"
                            onClick={() =>
                              router.push(`/employee/invoices/${inv.id}`)
                            }
                            className="px-3 py-1 text-xs text-[#1e3a8a] hover:text-[#00897b] transition-colors border border-[#1e3a8a] rounded hover:border-[#00897b]"
                          >
                            Xem
                          </button>
                          {(inv as any).status === "Draft" && (
                            <button
                              type="button"
                              onClick={() => handleConfirm(inv)}
                              className="px-3 py-1 text-xs text-white bg-[#10b981] hover:bg-[#059669] transition-colors rounded"
                            >
                              Xác nhận
                            </button>
                          )}
                          <button
                            type="button"
                            onClick={() => handleDelete(inv)}
                            className="px-3 py-1 text-xs text-red-600 hover:text-red-700 transition-colors border border-red-600 rounded hover:border-red-700"
                          >
                            Xóa
                          </button>
                        </div>
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

