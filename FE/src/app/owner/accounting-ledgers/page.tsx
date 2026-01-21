"use client";

import { useEffect, useMemo, useState } from "react";
import LoadingOverlay from "@/components/ui/loading-overlay";
import { showToast } from "@/components/ui/toast";
import {
  ownerService,
  OwnerAccountingLedger,
} from "@/services/owner.service";

type MovementFilter = "" | "Thu" | "Chi";

export default function OwnerAccountingLedgersPage() {
  const [ledgers, setLedgers] = useState<OwnerAccountingLedger[]>([]);
  const [loading, setLoading] = useState(true);

  const [fromDate, setFromDate] = useState("");
  const [toDate, setToDate] = useState("");
  const [movementType, setMovementType] = useState<MovementFilter>("");
  const [searchTerm, setSearchTerm] = useState("");
  const [selected, setSelected] = useState<OwnerAccountingLedger | null>(null);

  useEffect(() => {
    fetchLedgers();
  }, []);

  const fetchLedgers = async () => {
    try {
      setLoading(true);
      const data = await ownerService.listAccountingLedgers();
      setLedgers(data || []);
    } catch (error: any) {
      const message =
        error?.response?.data?.error ||
        error?.message ||
        "Lỗi khi tải sổ kế toán";
      showToast(message, "error");
    } finally {
      setLoading(false);
    }
  };

  const filteredLedgers = useMemo(() => {
    const term = searchTerm.trim().toLowerCase();
    return ledgers.filter((al) => {
      if (fromDate) {
        const from = new Date(fromDate);
        const d = al.transaction_date ? new Date(al.transaction_date) : null;
        if (!d || d < from) return false;
      }
      if (toDate) {
        const to = new Date(toDate);
        const d = al.transaction_date ? new Date(al.transaction_date) : null;
        if (!d || d > to) return false;
      }
      if (movementType && al.movement_type !== movementType) return false;

      if (!term) return true;
      const doc = (al.document_number || "").toLowerCase();
      const desc = (al.description || "").toLowerCase();
      return doc.includes(term) || desc.includes(term);
    });
  }, [ledgers, fromDate, toDate, movementType, searchTerm]);

  const formatCurrency = (value: string | null) => {
    const num = Number(value || 0);
    if (!num) return "-";
    return new Intl.NumberFormat("vi-VN", {
      style: "currency",
      currency: "VND",
      maximumFractionDigits: 0,
    }).format(num);
  };

  const formatDate = (value?: string | null) => {
    if (!value) return "-";
    const d = new Date(value);
    return d.toLocaleDateString("vi-VN", {
      day: "2-digit",
      month: "2-digit",
      year: "numeric",
    });
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
        message="Đang tải sổ kế toán..."
      />
      <div className="p-8">
        <h1 className="text-[28px] font-bold italic text-[#1e3a8a] mb-6">
          Sổ kế toán
        </h1>

        {/* Filter card */}
        <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6 mb-6">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div>
              <label className="block text-sm font-normal text-[#1e3a8a] mb-1.5">
                Từ ngày
              </label>
              <input
                type="date"
                value={fromDate}
                onChange={(e) => setFromDate(e.target.value)}
                className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#00897b] focus:border-transparent"
              />
            </div>
            <div>
              <label className="block text-sm font-normal text-[#1e3a8a] mb-1.5">
                Đến ngày
              </label>
              <input
                type="date"
                value={toDate}
                onChange={(e) => setToDate(e.target.value)}
                className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#00897b] focus:border-transparent"
              />
            </div>
            <div>
              <label className="block text-sm font-normal text-[#1e3a8a] mb-1.5">
                Loại bút toán
              </label>
              <select
                value={movementType}
                onChange={(e) =>
                  setMovementType(e.target.value as MovementFilter)
                }
                className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#00897b] focus:border-transparent"
              >
                <option value="">Tất cả</option>
                <option value="Thu">Thu</option>
                <option value="Chi">Chi</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-normal text-[#1e3a8a] mb-1.5">
                Tìm kiếm
              </label>
              <input
                type="text"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                placeholder="Số chứng từ hoặc diễn giải..."
                className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#00897b] focus:border-transparent"
              />
            </div>
          </div>
          <div className="mt-4 flex items-center justify-end gap-3">
            <button
              type="button"
              onClick={() => {
                setFromDate("");
                setToDate("");
                setMovementType("");
                setSearchTerm("");
                fetchLedgers();
              }}
              className="px-4 py-2 bg-white border border-[#1e3a8a] text-[#1e3a8a] rounded-lg hover:bg-slate-50 transition-colors text-sm font-medium"
            >
              Xóa lọc
            </button>
          </div>
        </div>

        {/* Table + side panel */}
        <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
          {/* Table */}
          <div className="xl:col-span-2 bg-white rounded-lg shadow-sm border border-slate-200 overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-slate-50 border-b border-slate-200">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-bold italic text-[#4b5563] uppercase tracking-wider">
                      Ngày hạch toán
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-bold italic text-[#4b5563] uppercase tracking-wider">
                      Số chứng từ
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-bold italic text-[#4b5563] uppercase tracking-wider">
                      Diễn giải
                    </th>
                    <th className="px-6 py-3 text-right text-xs font-bold italic text-[#4b5563] uppercase tracking-wider">
                      Nợ
                    </th>
                    <th className="px-6 py-3 text-right text-xs font-bold italic text-[#4b5563] uppercase tracking-wider">
                      Có
                    </th>
                    <th className="px-6 py-3 text-right text-xs font-bold italic text-[#4b5563] uppercase tracking-wider">
                      Số dư
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-slate-200">
                  {filteredLedgers.length === 0 ? (
                    <tr>
                      <td
                        colSpan={6}
                        className="px-6 py-12 text-center text-slate-500"
                      >
                        Không có bút toán nào trong khoảng thời gian này
                      </td>
                    </tr>
                  ) : (
                    filteredLedgers.map((al) => (
                      <tr
                        key={al.id}
                        className="hover:bg-slate-50 cursor-pointer"
                        onClick={() => setSelected(al)}
                      >
                        <td className="px-6 py-3 text-sm text-[#1e3a8a]">
                          {formatDate(al.transaction_date)}
                        </td>
                        <td className="px-6 py-3 text-sm text-[#1e3a8a]">
                          {al.document_number || "-"}
                        </td>
                        <td className="px-6 py-3 text-sm text-[#1e3a8a]">
                          {al.description || "-"}
                        </td>
                        <td className="px-6 py-3 text-sm text-right text-[#1e3a8a]">
                          {formatCurrency(al.debit_amount)}
                        </td>
                        <td className="px-6 py-3 text-sm text-right text-[#1e3a8a]">
                          {formatCurrency(al.credit_amount)}
                        </td>
                        <td className="px-6 py-3 text-sm text-right text-[#1e3a8a]">
                          {formatCurrency(al.balance)}
                        </td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>
          </div>

          {/* Side panel detail */}
          <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6 min-h-[220px]">
            <h2 className="text-[18px] font-bold italic text-[#1e3a8a] mb-4">
              Chi tiết bút toán
            </h2>
            {!selected ? (
              <p className="text-sm text-[#6b7280]">
                Chọn một dòng trong bảng để xem chi tiết bút toán.
              </p>
            ) : (
              <div className="space-y-3 text-sm">
                <div>
                  <p className="text-xs text-[#6b7280] mb-1">
                    Ngày hạch toán
                  </p>
                  <p className="text-[#1e3a8a]">
                    {formatDateTime(selected.transaction_date)}
                  </p>
                </div>
                <div>
                  <p className="text-xs text-[#6b7280] mb-1">
                    Số chứng từ / Hóa đơn liên quan
                  </p>
                  <p className="text-[#1e3a8a]">
                    {selected.document_number || "-"}{" "}
                    {selected.invoice_id && `· Hóa đơn #${selected.invoice_id}`}
                  </p>
                </div>
                <div>
                  <p className="text-xs text-[#6b7280] mb-1">Loại bút toán</p>
                  <p className="text-[#1e3a8a]">
                    {selected.movement_type || "-"}
                  </p>
                </div>
                <div>
                  <p className="text-xs text-[#6b7280] mb-1">Diễn giải</p>
                  <p className="text-[#1e3a8a]">
                    {selected.description || "-"}
                  </p>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div>
                    <p className="text-xs text-[#6b7280] mb-1">Nợ</p>
                    <p className="text-[#1e3a8a]">
                      {formatCurrency(selected.debit_amount)}
                    </p>
                  </div>
                  <div>
                    <p className="text-xs text-[#6b7280] mb-1">Có</p>
                    <p className="text-[#1e3a8a]">
                      {formatCurrency(selected.credit_amount)}
                    </p>
                  </div>
                  <div>
                    <p className="text-xs text-[#6b7280] mb-1">Số dư</p>
                    <p className="text-[#1e3a8a]">
                      {formatCurrency(selected.balance)}
                    </p>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </>
  );
}

