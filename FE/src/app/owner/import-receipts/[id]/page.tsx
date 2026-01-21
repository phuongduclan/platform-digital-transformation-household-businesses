"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import LoadingOverlay from "@/components/ui/loading-overlay";
import { showToast } from "@/components/ui/toast";
import {
  ownerService,
  OwnerImportReceipt,
  OwnerWarehouse,
  OwnerProduct,
  OwnerUnit,
} from "@/services/owner.service";

export default function OwnerImportReceiptDetailPage() {
  const params = useParams();
  const router = useRouter();
  const idParam = params?.id;
  const receiptId =
    typeof idParam === "string" ? Number(idParam) : NaN;

  const [receipt, setReceipt] = useState<OwnerImportReceipt | null>(null);
  const [warehouses, setWarehouses] = useState<OwnerWarehouse[]>([]);
  const [products, setProducts] = useState<OwnerProduct[]>([]);
  const [units, setUnits] = useState<OwnerUnit[]>([]);
  const [details, setDetails] = useState<
    { id: number; import_id: number; product_id: number; unit_id: number; quantity: number }[]
  >([]);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [warehouseId, setWarehouseId] = useState<number | "">("");
  const [importDate, setImportDate] = useState<string>("");

  useEffect(() => {
    if (!Number.isNaN(receiptId)) {
      fetchData();
    } else {
      showToast("ID phiếu nhập không hợp lệ", "error");
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [receiptId]);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [rc, whs, prods, uns, dets] = await Promise.all([
        ownerService.getImportReceipt(receiptId),
        ownerService.listWarehouses(),
        ownerService.listProducts(),
        ownerService.listUnits(),
        ownerService.listImportReceiptDetails(receiptId),
      ]);
      setReceipt(rc);
      setWarehouses(whs);
      setProducts(prods);
      setUnits(uns);
      setDetails(dets);
      setWarehouseId(rc.warehouse_id);
      setImportDate(rc.import_date ? rc.import_date.slice(0, 10) : "");
    } catch (error: any) {
      showToast(
        error?.response?.data?.error ||
          error?.message ||
          "Lỗi khi tải phiếu nhập",
        "error"
      );
    } finally {
      setLoading(false);
    }
  };

  const productMap = new Map<number, OwnerProduct>();
  products.forEach((p) => productMap.set(p.id, p));
  const unitMap = new Map<number, OwnerUnit>();
  units.forEach((u) => unitMap.set(u.id, u));
  const warehouseMap = new Map<number, OwnerWarehouse>();
  warehouses.forEach((w) => warehouseMap.set(w.id, w));

  const handleSave = async () => {
    if (!receipt) return;
    try {
      setSaving(true);
      await ownerService.updateImportReceipt(receipt.id, {
        warehouse_id:
          warehouseId === "" ? undefined : Number(warehouseId),
        import_date: importDate || undefined,
      });
      showToast("Cập nhật phiếu nhập thành công", "success");
      fetchData();
    } catch (error: any) {
      showToast(
        error?.response?.data?.error ||
          error?.message ||
          "Lỗi khi cập nhật phiếu nhập",
        "error"
      );
    } finally {
      setSaving(false);
    }
  };

  if (loading || !receipt) {
    return (
      <LoadingOverlay
        isLoading={true}
        message="Đang tải phiếu nhập..."
      />
    );
  }

  return (
    <>
      <LoadingOverlay
        isLoading={saving}
        message="Đang lưu phiếu nhập..."
      />
      <div className="p-8">
        {/* Breadcrumb */}
        <div className="mb-4 flex items-center gap-2 text-sm">
          <button
            type="button"
            onClick={() => router.push("/owner")}
            className="text-[#00897b] hover:underline"
          >
            Tổng quan
          </button>
          <span className="text-[#4b5563]">/</span>
          <button
            type="button"
            onClick={() => router.push("/owner/import-receipts")}
            className="text-[#00897b] hover:underline"
          >
            Phiếu nhập
          </button>
          <span className="text-[#4b5563]">/</span>
          <span className="text-[#4b5563]">#{receipt.id}</span>
        </div>

        <div className="mb-6 flex items-center justify-between">
          <h1 className="text-[28px] font-bold italic text-[#1e3a8a]">
            Phiếu nhập #{receipt.id}
          </h1>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
          {/* Header */}
          <div className="lg:col-span-2 bg-white rounded-lg shadow-sm border border-slate-200 p-6">
            <h2 className="text-[18px] font-bold italic text-[#1e3a8a] mb-4">
              Thông tin chung
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
              <div>
                <p className="text-xs text-[#6b7280] mb-1">Hóa đơn liên quan</p>
                <p className="text-[#1e3a8a]">
                  {receipt.invoice_id ?? "-"}
                </p>
              </div>
              <div>
                <label className="block text-xs text-[#6b7280] mb-1">
                  Kho
                </label>
                <select
                  value={warehouseId}
                  onChange={(e) =>
                    setWarehouseId(
                      e.target.value ? Number(e.target.value) : ""
                    )
                  }
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#00897b] focus:border-transparent"
                >
                  <option value="">Chọn kho</option>
                  {warehouses
                    .filter(
                      (w) => (w.status || "").toUpperCase() === "ACTIVE"
                    )
                    .map((w) => (
                    <option key={w.id} value={w.id}>
                      {w.name}
                    </option>
                  ))}
                </select>
              </div>
              <div>
                <label className="block text-xs text-[#6b7280] mb-1">
                  Ngày nhập
                </label>
                <input
                  type="date"
                  value={importDate}
                  onChange={(e) => setImportDate(e.target.value)}
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#00897b] focus:border-transparent"
                />
              </div>
              <div>
                <p className="text-xs text-[#6b7280] mb-1">Trạng thái</p>
                <p className="inline-flex px-3 py-1 text-xs font-bold italic rounded-full text-white bg-[#10b981]">
                  {receipt.status}
                </p>
              </div>
            </div>
          </div>

          {/* Actions */}
          <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6 flex flex-col justify-between">
            <div>
              <h2 className="text-[18px] font-bold italic text-[#1e3a8a] mb-2">
                Thao tác
              </h2>
              <p className="text-xs text-[#6b7280]">
                Chủ hộ chỉ được chỉnh kho nhận và ngày nhập; chi tiết dòng hàng
                được sinh từ hóa đơn đã xác nhận.
              </p>
            </div>
            <button
              type="button"
              onClick={handleSave}
              disabled={saving}
              className="mt-4 px-5 py-2 bg-[#00897b] text-white rounded-lg text-sm font-bold hover:bg-[#007a6c] transition-colors disabled:bg-slate-400 disabled:cursor-not-allowed"
            >
              {saving ? "Đang lưu..." : "Lưu thay đổi"}
            </button>
          </div>
        </div>

        {/* Details */}
        <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6">
          <h2 className="text-[18px] font-bold italic text-[#1e3a8a] mb-4">
            Dòng hàng
          </h2>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-slate-50 border-b border-slate-200">
                <tr>
                  <th className="px-4 py-2 text-left text-xs font-bold italic text-[#4b5563] uppercase">
                    Sản phẩm
                  </th>
                  <th className="px-4 py-2 text-left text-xs font-bold italic text-[#4b5563] uppercase">
                    Đơn vị
                  </th>
                  <th className="px-4 py-2 text-right text-xs font-bold italic text-[#4b5563] uppercase">
                    Số lượng
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-200">
                {details.length === 0 ? (
                  <tr>
                    <td
                      colSpan={3}
                      className="px-4 py-6 text-center text-sm text-[#6b7280]"
                    >
                      Không có dòng hàng
                    </td>
                  </tr>
                ) : (
                  details.map((d) => {
                    const prod = productMap.get(d.product_id);
                    const unit = unitMap.get(d.unit_id);
                    return (
                      <tr key={d.id}>
                        <td className="px-4 py-2 text-sm text-[#1e3a8a]">
                          {prod?.name || `SP #${d.product_id}`}
                        </td>
                        <td className="px-4 py-2 text-sm text-[#1e3a8a]">
                          {unit?.name || `ĐV #${d.unit_id}`}
                        </td>
                        <td className="px-4 py-2 text-sm text-right text-[#1e3a8a]">
                          {d.quantity}
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

