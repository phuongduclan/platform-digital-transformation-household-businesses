"use client";

import { useEffect, useMemo, useState } from "react";
import LoadingOverlay from "@/components/ui/loading-overlay";
import { showToast } from "@/components/ui/toast";
import {
  ownerService,
  OwnerCustomer,
  OwnerDebtRecord,
} from "@/services/owner.service";

type StatusFilter = "" | "INCREASE" | "DECREASE" | "ADJUST"; // FE-only labels

interface DebtRecordWithCustomer extends OwnerDebtRecord {
  customer_name?: string;
}

export default function OwnerDebtRecordsPage() {
  const [customers, setCustomers] = useState<OwnerCustomer[]>([]);
  const [records, setRecords] = useState<OwnerDebtRecord[]>([]);
  const [loading, setLoading] = useState(true);

  const [selectedCustomer, setSelectedCustomer] = useState<number | "">("");
  const [statusFilter, setStatusFilter] = useState<StatusFilter>("");
  const [dateFrom, setDateFrom] = useState<string>("");
  const [dateTo, setDateTo] = useState<string>("");

  const [detailRecord, setDetailRecord] = useState<DebtRecordWithCustomer | null>(
    null
  );

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [custs, recs] = await Promise.all([
        ownerService.listCustomers(),
        ownerService.listDebtRecords(),
      ]);
      setCustomers(custs || []);
      setRecords(recs || []);
    } catch (error: any) {
      const message =
        error?.response?.data?.error ||
        error?.message ||
        "Lỗi khi tải bản ghi công nợ";
      showToast(message, "error");
    } finally {
      setLoading(false);
    }
  };

  const customerMap = useMemo(() => {
    const m = new Map<number, OwnerCustomer>();
    customers.forEach((c) => m.set(c.id, c));
    return m;
  }, [customers]);

  const enrichedRecords: DebtRecordWithCustomer[] = useMemo(
    () =>
      records.map((r) => ({
        ...r,
        customer_name: customerMap.get(r.customer_id)?.name,
      })),
    [records, customerMap]
  );

  const filteredRecords = useMemo(() => {
    return enrichedRecords.filter((r) => {
      if (selectedCustomer && r.customer_id !== selectedCustomer) return false;

      if (dateFrom) {
        const from = new Date(dateFrom);
        const recDate = r.record_at ? new Date(r.record_at) : null;
        if (!recDate || recDate < from) return false;
      }
      if (dateTo) {
        const to = new Date(dateTo);
        const recDate = r.record_at ? new Date(r.record_at) : null;
        if (!recDate || recDate > to) return false;
      }

      if (statusFilter === "INCREASE" && !r.debit_amount) return false;
      if (statusFilter === "DECREASE" && !r.credit_amount) return false;
      if (
        statusFilter === "ADJUST" &&
        (r.debit_amount || r.credit_amount)
      )
        return false;

      return true;
    });
  }, [enrichedRecords, selectedCustomer, statusFilter, dateFrom, dateTo]);

  const formatCurrency = (value: string | null) => {
    const num = Number(value || 0);
    if (!num) return "-";
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

  const getTypeLabel = (record: OwnerDebtRecord) => {
    if (record.debit_amount && !record.credit_amount) return "Tăng nợ";
    if (record.credit_amount && !record.debit_amount) return "Giảm nợ";
    return "Điều chỉnh";
  };

  const openDetail = (record: DebtRecordWithCustomer) => {
    setDetailRecord(record);
  };

  const closeDetail = () => {
    setDetailRecord(null);
  };

  return (
    <>
      <LoadingOverlay
        isLoading={loading}
        message="Đang tải bản ghi công nợ..."
      />
      <div className="p-8">
        <h1 className="text-[28px] font-bold italic text-[#1e3a8a] mb-6">
          Bản ghi công nợ
        </h1>

        {/* Filters */}
        <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6 mb-6">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div>
              <label className="block text-sm font-normal text-[#1e3a8a] mb-1.5">
                Khách hàng
              </label>
              <select
                value={selectedCustomer}
                onChange={(e) =>
                  setSelectedCustomer(
                    e.target.value ? Number(e.target.value) : ""
                  )
                }
                className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#00897b] focus:border-transparent"
              >
                <option value="">Tất cả khách hàng</option>
                {customers.map((c) => (
                  <option key={c.id} value={c.id}>
                    {c.name}
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
                value={dateFrom}
                onChange={(e) => setDateFrom(e.target.value)}
                className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#00897b] focus:border-transparent"
              />
            </div>
            <div>
              <label className="block text-sm font-normal text-[#1e3a8a] mb-1.5">
                Đến ngày
              </label>
              <input
                type="date"
                value={dateTo}
                onChange={(e) => setDateTo(e.target.value)}
                className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#00897b] focus:border-transparent"
              />
            </div>
            <div>
              <label className="block text-sm font-normal text-[#1e3a8a] mb-1.5">
                Loại bản ghi
              </label>
              <select
                value={statusFilter}
                onChange={(e) =>
                  setStatusFilter(e.target.value as StatusFilter)
                }
                className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#00897b] focus:border-transparent"
              >
                <option value="">Tất cả</option>
                <option value="INCREASE">Tăng nợ</option>
                <option value="DECREASE">Giảm nợ</option>
                <option value="ADJUST">Điều chỉnh</option>
              </select>
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
                    Ngày ghi nhận
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-bold italic text-[#4b5563] uppercase tracking-wider">
                    Khách hàng
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-bold italic text-[#4b5563] uppercase tracking-wider">
                    Loại
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-bold italic text-[#4b5563] uppercase tracking-wider">
                    Diễn giải
                  </th>
                  <th className="px-6 py-3 text-right text-xs font-bold italic text-[#4b5563] uppercase tracking-wider">
                    Tăng nợ (+)
                  </th>
                  <th className="px-6 py-3 text-right text-xs font-bold italic text-[#4b5563] uppercase tracking-wider">
                    Giảm nợ (-)
                  </th>
                  <th className="px-6 py-3 text-right text-xs font-bold italic text-[#4b5563] uppercase tracking-wider">
                    Dư nợ sau ghi nhận
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-slate-200">
                {filteredRecords.length === 0 ? (
                  <tr>
                    <td
                      colSpan={7}
                      className="px-6 py-12 text-center text-slate-500"
                    >
                      Không có bản ghi công nợ
                    </td>
                  </tr>
                ) : (
                  filteredRecords.map((r) => (
                    <tr
                      key={r.id}
                      className="hover:bg-slate-50 cursor-pointer"
                      onClick={() =>
                        openDetail({
                          ...r,
                          customer_name:
                            customerMap.get(r.customer_id)?.name,
                        })
                      }
                    >
                      <td className="px-6 py-3 text-sm text-[#1e3a8a]">
                        {formatDateTime(r.record_at)}
                      </td>
                      <td className="px-6 py-3 text-sm text-[#1e3a8a]">
                        {customerMap.get(r.customer_id)?.name ||
                          `KH #${r.customer_id}`}
                      </td>
                      <td className="px-6 py-3 text-sm text-[#1e3a8a]">
                        {getTypeLabel(r)}
                      </td>
                      <td className="px-6 py-3 text-sm text-[#1e3a8a]">
                        {r.description || "-"}
                      </td>
                      <td className="px-6 py-3 text-sm text-right text-[#1e3a8a]">
                        {formatCurrency(r.debit_amount)}
                      </td>
                      <td className="px-6 py-3 text-sm text-right text-[#1e3a8a]">
                        {formatCurrency(r.credit_amount)}
                      </td>
                      <td className="px-6 py-3 text-sm text-right text-[#1e3a8a]">
                        {formatCurrency(r.balance)}
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      {/* Detail modal */}
      {detailRecord && (
        <div className="fixed inset-0 z-40 flex items-center justify-center bg-black/30">
          <div className="bg-white rounded-2xl shadow-xl border border-slate-200 w-full max-w-lg p-6">
            <h2 className="text-[20px] font-bold italic text-[#1e3a8a] mb-4">
              Chi tiết bản ghi công nợ
            </h2>
            <div className="space-y-3 text-sm">
              <div>
                <p className="text-xs text-[#6b7280] mb-1">Khách hàng</p>
                <p className="text-[#1e3a8a]">
                  {detailRecord.customer_name ||
                    `KH #${detailRecord.customer_id}`}
                </p>
              </div>
              <div>
                <p className="text-xs text-[#6b7280] mb-1">Loại bản ghi</p>
                <p className="text-[#1e3a8a]">
                  {getTypeLabel(detailRecord)}
                </p>
              </div>
              <div>
                <p className="text-xs text-[#6b7280] mb-1">Diễn giải</p>
                <p className="text-[#1e3a8a]">
                  {detailRecord.description || "-"}
                </p>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                  <p className="text-xs text-[#6b7280] mb-1">Tăng nợ (+)</p>
                  <p className="text-[#1e3a8a]">
                    {formatCurrency(detailRecord.debit_amount)}
                  </p>
                </div>
                <div>
                  <p className="text-xs text-[#6b7280] mb-1">Giảm nợ (-)</p>
                  <p className="text-[#1e3a8a]">
                    {formatCurrency(detailRecord.credit_amount)}
                  </p>
                </div>
                <div>
                  <p className="text-xs text-[#6b7280] mb-1">
                    Dư nợ sau ghi nhận
                  </p>
                  <p className="text-[#1e3a8a]">
                    {formatCurrency(detailRecord.balance)}
                  </p>
                </div>
              </div>
              <div>
                <p className="text-xs text-[#6b7280] mb-1">Thời điểm ghi nhận</p>
                <p className="text-[#1e3a8a]">
                  {formatDateTime(detailRecord.record_at)}
                </p>
              </div>
              {(detailRecord.invoice_id || detailRecord.payment_id) && (
                <div>
                  <p className="text-xs text-[#6b7280] mb-1">
                    Chứng từ nguồn (tham khảo)
                  </p>
                  <p className="text-[#1e3a8a]">
                    {detailRecord.invoice_id && (
                      <span className="mr-3">
                        Hóa đơn #{detailRecord.invoice_id}
                      </span>
                    )}
                    {detailRecord.payment_id && (
                      <span>Thanh toán #{detailRecord.payment_id}</span>
                    )}
                  </p>
                </div>
              )}
            </div>

            <div className="mt-6 flex items-center justify-end">
              <button
                type="button"
                onClick={closeDetail}
                className="px-5 py-2 bg-[#00897b] text-white rounded-lg text-sm font-bold hover:bg-[#007a6c] transition-colors"
              >
                Đóng
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}

