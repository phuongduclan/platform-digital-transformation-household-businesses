"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import LoadingOverlay from "@/components/ui/loading-overlay";
import { showToast } from "@/components/ui/toast";
import {
  ownerService,
  OwnerExportReceipt,
  OwnerWarehouse,
} from "@/services/owner.service";

export default function OwnerExportReceiptsPage() {
  const router = useRouter();
  const [receipts, setReceipts] = useState<OwnerExportReceipt[]>([]);
  const [warehouses, setWarehouses] = useState<OwnerWarehouse[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [rs, whs] = await Promise.all([
        ownerService.listExportReceipts(),
        ownerService.listWarehouses(),
      ]);
      setReceipts(rs);
      setWarehouses(whs);
    } catch (error: any) {
      showToast(
        error?.response?.data?.error ||
          error?.message ||
          "Lỗi khi tải phiếu xuất",
        "error"
      );
    } finally {
      setLoading(false);
    }
  };

  const warehouseMap = new Map<number, string>();
  warehouses.forEach((w) => warehouseMap.set(w.id, w.name));

  const formatDate = (value?: string | null) => {
    if (!value) return "-";
    const d = new Date(value);
    return d.toLocaleDateString("vi-VN", {
      day: "2-digit",
      month: "2-digit",
      year: "numeric",
    });
  };

  return (
    <>
      <LoadingOverlay
        isLoading={loading}
        message="Đang tải phiếu xuất..."
      />
      <div className="p-8">
        <h1 className="text-[28px] font-bold italic text-[#1e3a8a] mb-6">
          Phiếu xuất
        </h1>

        <div className="bg-white rounded-lg shadow-sm border border-slate-200 overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-slate-50 border-b border-slate-200">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-bold italic text-[#4b5563] uppercase tracking-wider">
                    Số phiếu
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-bold italic text-[#4b5563] uppercase tracking-wider">
                    Ngày xuất
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-bold italic text-[#4b5563] uppercase tracking-wider">
                    Kho
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-bold italic text-[#4b5563] uppercase tracking-wider">
                    Hóa đơn
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-bold italic text-[#4b5563] uppercase tracking-wider">
                    Lý do
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
                {receipts.length === 0 ? (
                  <tr>
                    <td
                      colSpan={7}
                      className="px-6 py-8 text-center text-sm text-[#6b7280]"
                    >
                      Không có phiếu xuất
                    </td>
                  </tr>
                ) : (
                  receipts.map((r) => (
                    <tr key={r.id} className="hover:bg-slate-50">
                      <td className="px-6 py-3 text-sm text-[#1e3a8a]">
                        {r.id}
                      </td>
                      <td className="px-6 py-3 text-sm text-[#1e3a8a]">
                        {formatDate(r.export_date)}
                      </td>
                      <td className="px-6 py-3 text-sm text-[#1e3a8a]">
                        {warehouseMap.get(r.warehouse_id) ||
                          `Kho #${r.warehouse_id}`}
                      </td>
                      <td className="px-6 py-3 text-sm text-[#1e3a8a]">
                        {r.invoice_id ?? "-"}
                      </td>
                      <td className="px-6 py-3 text-sm text-[#4b5563]">
                        {r.reason || "-"}
                      </td>
                      <td className="px-6 py-3 text-sm text-[#4b5563]">
                        {r.status}
                      </td>
                      <td className="px-6 py-3">
                        <button
                          type="button"
                          onClick={() =>
                            router.push(`/owner/export-receipts/${r.id}`)
                          }
                          className="px-3 py-1 text-xs text-[#1e3a8a] hover:text-[#00897b] transition-colors border border-[#1e3a8a] rounded hover:border-[#00897b]"
                        >
                          Xem
                        </button>
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

