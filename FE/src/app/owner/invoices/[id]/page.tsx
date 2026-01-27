"use client";

import { useEffect, useMemo, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import LoadingOverlay from "@/components/ui/loading-overlay";
import { showToast } from "@/components/ui/toast";
import {
  ownerService,
  OwnerInvoice,
  OwnerInvoiceDetail,
  OwnerProduct,
  OwnerUnit,
} from "@/services/owner.service";
import { generateInvoicePDF } from "@/lib/invoice-pdf";

export default function OwnerInvoiceDetailPage() {
  const params = useParams();
  const router = useRouter();
  const idParam = params?.id;
  const invoiceId =
    typeof idParam === "string" ? Number(idParam) : NaN;

  const [invoice, setInvoice] = useState<OwnerInvoice | null>(null);
  const [details, setDetails] = useState<OwnerInvoiceDetail[]>([]);
  const [products, setProducts] = useState<OwnerProduct[]>([]);
  const [units, setUnits] = useState<OwnerUnit[]>([]);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);

  const [editingDesc, setEditingDesc] = useState("");
  const [editingDetailId, setEditingDetailId] = useState<number | null>(null);
  const [editingPrice, setEditingPrice] = useState<number | string>("");
  const [editingQuantity, setEditingQuantity] = useState<number | string>("");
  const [editingVat, setEditingVat] = useState<number | string>("");
  const [editingDiscount, setEditingDiscount] = useState<number | string>("");
  const [editingDescription, setEditingDescription] = useState("");

  const isDraft = invoice?.status === "Draft";

  useEffect(() => {
    if (!Number.isNaN(invoiceId)) {
      fetchData();
    } else {
      showToast("ID hóa đơn không hợp lệ", "error");
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [invoiceId]);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [inv, dets, prods, uns] = await Promise.all([
        ownerService.getInvoice(invoiceId),
        ownerService.listInvoiceDetails(invoiceId),
        ownerService.listProducts(),
        ownerService.listUnits(),
      ]);
      setInvoice(inv);
      setDetails(dets);
      setProducts(prods);
      setUnits(uns);
      setEditingDesc(inv.description || "");
    } catch (error: any) {
      showToast(
        error?.response?.data?.error ||
        error?.message ||
        "Lỗi khi tải chi tiết hóa đơn",
        "error"
      );
    } finally {
      setLoading(false);
    }
  };

  const productMap = useMemo(() => {
    const m = new Map<number, OwnerProduct>();
    products.forEach((p) => m.set(p.id, p));
    return m;
  }, [products]);

  const unitMap = useMemo(() => {
    const m = new Map<number, OwnerUnit>();
    units.forEach((u) => m.set(u.id, u));
    return m;
  }, [units]);

  const totalAmount = useMemo(() => {
    return details.reduce((sum, d) => {
      const qty = d.quantity || 0;
      const price = Number(d.price || 0);
      const discount = d.discount || 0;
      const vat = d.vat || 0;
      const base = qty * price;
      const val = base - (base * discount) / 100 + (base * vat) / 100;
      return sum + val;
    }, 0);
  }, [details]);

  const formatCurrency = (value: number) =>
    new Intl.NumberFormat("vi-VN", {
      maximumFractionDigits: 0,
    }).format(value);

  const formatDateTime = (value?: string) => {
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

  const handleUpdateHeader = async () => {
    if (!invoice) return;
    try {
      setSaving(true);
      await ownerService.updateInvoice(invoice.id, {
        seller_id: invoice.seller_id,
        customer_id: invoice.customer_id,
        invoice_type: invoice.invoice_type,
        description: editingDesc.trim() || undefined,
      });
      showToast("Cập nhật mô tả hóa đơn thành công", "success");
      fetchData();
    } catch (error: any) {
      showToast(
        error?.response?.data?.error ||
        error?.message ||
        "Lỗi khi cập nhật hóa đơn",
        "error"
      );
    } finally {
      setSaving(false);
    }
  };

  const handleConfirm = async () => {
    if (!invoice || !isDraft) return;
    if (
      !confirm(
        "Xác nhận hóa đơn sẽ tự động tạo chứng từ nhập/xuất, tồn kho và công nợ. Tiếp tục?"
      )
    )
      return;
    try {
      setSaving(true);
      await ownerService.confirmInvoice(invoice.id);
      showToast("Xác nhận hóa đơn thành công", "success");
      fetchData();
    } catch (error: any) {
      showToast(
        error?.response?.data?.error ||
        error?.message ||
        "Lỗi khi xác nhận hóa đơn",
        "error"
      );
    } finally {
      setSaving(false);
    }
  };

  const handleEditDetail = (detail: OwnerInvoiceDetail) => {
    setEditingDetailId(detail.id);
    setEditingPrice(detail.price || 0);
    setEditingQuantity(detail.quantity || 0);
    setEditingVat(detail.vat || 0);
    setEditingDiscount(detail.discount || 0);
    setEditingDescription(detail.description || "");
  };

  const handleSaveDetail = async (detailId: number) => {
    if (!invoice || !isDraft) return;

    try {
      setSaving(true);
      const priceNumber = Number(editingPrice);
      const quantityNumber = Number(editingQuantity);
      const vatNumber = Number(editingVat);
      const discountNumber = Number(editingDiscount);

      if (Number.isNaN(priceNumber)) {
        showToast("Đơn giá phải là số", "error");
        return;
      }
      if (Number.isNaN(quantityNumber)) {
        showToast("Số lượng phải là số", "error");
        return;
      }
      if (Number.isNaN(vatNumber) || vatNumber < 0 || vatNumber > 100) {
        showToast("VAT phải là số từ 0-100", "error");
        return;
      }
      if (Number.isNaN(discountNumber) || discountNumber < 0 || discountNumber > 100) {
        showToast("Chiết khấu phải là số từ 0-100", "error");
        return;
      }

      await ownerService.updateInvoiceDetail(invoice.id, detailId, {
        price: priceNumber,
        quantity: quantityNumber,
        vat: vatNumber,
        discount: discountNumber,
        description: editingDescription.trim() || undefined,
      });

      showToast("Cập nhật dòng chi tiết thành công", "success");
      setEditingDetailId(null);
      setEditingPrice("");
      setEditingQuantity("");
      setEditingVat("");
      setEditingDiscount("");
      setEditingDescription("");
      fetchData();
    } catch (error: any) {
      showToast(
        error?.response?.data?.error ||
        error?.message ||
        "Lỗi khi cập nhật dòng chi tiết",
        "error"
      );
    } finally {
      setSaving(false);
    }
  };

  const handleDeleteDetail = async (detailId: number) => {
    if (!invoice || !isDraft) return;
    if (!confirm("Bạn chắc chắn muốn xóa dòng chi tiết này?")) return;

    try {
      setSaving(true);
      await ownerService.deleteInvoiceDetail(invoice.id, detailId);
      showToast("Xóa dòng chi tiết thành công", "success");
      fetchData();
    } catch (error: any) {
      showToast(
        error?.response?.data?.error ||
        error?.message ||
        "Lỗi khi xóa dòng chi tiết",
        "error"
      );
    } finally {
      setSaving(false);
    }
  };

  const handleCancelEdit = () => {
    setEditingDetailId(null);
    setEditingPrice("");
    setEditingQuantity("");
    setEditingVat("");
    setEditingDiscount("");
    setEditingDescription("");
  };

  const handlePrintInvoice = async () => {
    if (!invoice) return;
    if (isDraft) {
      showToast("Vui lòng xác nhận hóa đơn trước khi in", "error");
      return;
    }
    try {
      setSaving(true);
      const printData = await ownerService.printInvoice(invoice.id);
      // Convert total_amount to string to match PDF generator requirement
      const pdfData = {
        ...printData,
        invoice: {
          ...printData.invoice,
          total_amount: String(printData.invoice?.total_amount || 0),
        },
      };
      await generateInvoicePDF(pdfData as any);
      showToast("Đã tạo file PDF thành công", "success");
    } catch (error: any) {
      showToast(
        error?.response?.data?.error ||
        error?.message ||
        "Lỗi khi in hóa đơn",
        "error"
      );
    } finally {
      setSaving(false);
    }
  };

  if (loading || !invoice) {
    return (
      <LoadingOverlay
        isLoading={true}
        message="Đang tải chi tiết hóa đơn..."
      />
    );
  }

  return (
    <>
      <LoadingOverlay
        isLoading={saving}
        message="Đang xử lý..."
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
            onClick={() => router.push("/owner/invoices")}
            className="text-[#00897b] hover:underline"
          >
            Hóa đơn
          </button>
          <span className="text-[#4b5563]">/</span>
          <span className="text-[#4b5563]">#{invoice.id}</span>
        </div>

        {/* Header */}
        <div className="mb-6 flex items-center justify-between">
          <div>
            <h1 className="text-[28px] font-bold italic text-[#1e3a8a] mb-1">
              Hóa đơn #{invoice.id}
            </h1>
            <p className="text-xs text-[#6b7280]">
              Ngày tạo: {formatDateTime(invoice.created_at)}
            </p>
          </div>
          <div className="flex items-center gap-3">
            <button
              type="button"
              onClick={handlePrintInvoice}
              disabled={isDraft}
              className={`px-4 py-2 rounded-lg text-sm font-bold transition-colors ${isDraft
                ? "bg-slate-300 text-slate-500 cursor-not-allowed"
                : "bg-[#00897b] text-white hover:bg-[#007a6c]"
                }`}
            >
              In hóa đơn
            </button>
            {invoice.status === "Draft" && (
              <button
                type="button"
                onClick={handleConfirm}
                className="px-4 py-2 bg-[#10b981] text-white rounded-lg text-sm font-bold hover:bg-[#059669] transition-colors"
              >
                Xác nhận
              </button>
            )}
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
          {/* Thông tin hóa đơn */}
          <div className="lg:col-span-2 bg-white rounded-lg shadow-sm border border-slate-200 p-6">
            <h2 className="text-[18px] font-bold italic text-[#1e3a8a] mb-4">
              Thông tin chung
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
              <div>
                <p className="text-xs text-[#6b7280] mb-1">Người bán (seller_id)</p>
                <p className="text-[#1e3a8a]">{invoice.seller_id ?? "-"}</p>
              </div>
              <div>
                <p className="text-xs text-[#6b7280] mb-1">
                  Khách hàng (customer_id)
                </p>
                <p className="text-[#1e3a8a]">
                  {invoice.customer_id ?? "-"}
                </p>
              </div>
              <div>
                <p className="text-xs text-[#6b7280] mb-1">Loại hóa đơn</p>
                <p className="text-[#1e3a8a]">{invoice.invoice_type}</p>
              </div>
              <div>
                <p className="text-xs text-[#6b7280] mb-1">Trạng thái</p>
                <p className="inline-flex px-3 py-1 text-xs font-bold italic rounded-full text-white bg-[#10b981]">
                  {invoice.status}
                </p>
              </div>
              <div className="md:col-span-2">
                <p className="text-xs text-[#6b7280] mb-1">Mô tả</p>
                {isDraft ? (
                  <div className="space-y-2">
                    <textarea
                      value={editingDesc}
                      onChange={(e) => setEditingDesc(e.target.value)}
                      rows={3}
                      className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#00897b] focus:border-transparent"
                    />
                    <button
                      type="button"
                      onClick={handleUpdateHeader}
                      className="px-4 py-1.5 bg-[#00897b] text-white rounded-lg text-xs font-bold hover:bg-[#007a6c] transition-colors"
                    >
                      Lưu mô tả
                    </button>
                  </div>
                ) : (
                  <p className="text-[#1e3a8a]">
                    {invoice.description || "-"}
                  </p>
                )}
              </div>
            </div>
          </div>

          {/* Tổng tiền */}
          <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6">
            <h2 className="text-[18px] font-bold italic text-[#1e3a8a] mb-4">
              Tổng cộng
            </h2>
            <p className="text-sm text-[#4b5563] mb-2">
              Tổng tiền tính từ chi tiết:
            </p>
            <p className="text-2xl font-bold italic text-[#00897b] mb-2">
              {formatCurrency(totalAmount)}
            </p>
            <p className="text-xs text-[#6b7280]">
              Tổng tiền ghi nhận trong hóa đơn:{" "}
              <span className="font-bold text-[#1e3a8a]">
                {invoice.total_amount
                  ? formatCurrency(Number(invoice.total_amount))
                  : "-"}
              </span>
            </p>
          </div>
        </div>

        {/* Chi tiết hóa đơn (read-only để bám chắc business rule) */}
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
                    SL
                  </th>
                  <th className="px-4 py-2 text-right text-xs font-bold italic text-[#4b5563] uppercase">
                    Đơn giá
                  </th>
                  <th className="px-4 py-2 text-right text-xs font-bold italic text-[#4b5563] uppercase">
                    VAT %
                  </th>
                  <th className="px-4 py-2 text-right text-xs font-bold italic text-[#4b5563] uppercase">
                    CK %
                  </th>
                  <th className="px-4 py-2 text-right text-xs font-bold italic text-[#4b5563] uppercase">
                    Thành tiền
                  </th>
                  <th className="px-4 py-2 text-left text-xs font-bold italic text-[#4b5563] uppercase">
                    Ghi chú
                  </th>
                  <th className="px-4 py-2 text-center text-xs font-bold italic text-[#4b5563] uppercase">
                    Thao tác
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-200">
                {details.length === 0 ? (
                  <tr>
                    <td
                      colSpan={8}
                      className="px-4 py-6 text-center text-sm text-[#6b7280]"
                    >
                      Chưa có dòng hàng
                    </td>
                  </tr>
                ) : (
                  details.map((d) => {
                    const prod = productMap.get(d.product_id);
                    const unit = unitMap.get(d.unit_id);
                    const qty = d.quantity || 0;
                    const price = Number(d.price || 0);
                    const base = qty * price;
                    const vat = d.vat || 0;
                    const discount = d.discount || 0;
                    const total =
                      base - (base * discount) / 100 + (base * vat) / 100;
                    return (
                      <tr key={d.id}>
                        <td className="px-4 py-2 text-sm text-[#1e3a8a]">
                          {prod?.name || `SP #${d.product_id}`}
                        </td>
                        <td className="px-4 py-2 text-sm text-[#1e3a8a]">
                          {unit?.name || `ĐV #${d.unit_id}`}
                        </td>
                        <td className="px-4 py-2 text-sm text-right text-[#1e3a8a]">
                          {editingDetailId === d.id ? (
                            <input
                              type="number"
                              value={editingQuantity}
                              onChange={(e) => setEditingQuantity(e.target.value)}
                              className="w-16 px-2 py-1 border border-slate-300 rounded text-xs text-right focus:outline-none focus:ring-1 focus:ring-[#00897b]"
                            />
                          ) : (
                            <button
                              type="button"
                              onClick={() => handleEditDetail(d)}
                              disabled={!isDraft}
                              className={isDraft ? "cursor-pointer hover:underline text-[#00897b]" : ""}
                            >
                              {qty}
                            </button>
                          )}
                        </td>
                        <td className="px-4 py-2 text-sm text-right text-[#1e3a8a]">
                          {editingDetailId === d.id ? (
                            <input
                              type="number"
                              value={editingPrice}
                              onChange={(e) => setEditingPrice(e.target.value)}
                              className="w-20 px-2 py-1 border border-slate-300 rounded text-xs text-right focus:outline-none focus:ring-1 focus:ring-[#00897b]"
                            />
                          ) : (
                            <button
                              type="button"
                              onClick={() => handleEditDetail(d)}
                              disabled={!isDraft}
                              className={isDraft ? "cursor-pointer hover:underline text-[#00897b]" : ""}
                            >
                              {formatCurrency(price)}
                            </button>
                          )}
                        </td>
                        <td className="px-4 py-2 text-sm text-right text-[#1e3a8a]">
                          {editingDetailId === d.id ? (
                            <input
                              type="number"
                              value={editingVat}
                              onChange={(e) => setEditingVat(e.target.value)}
                              min="0"
                              max="100"
                              className="w-16 px-2 py-1 border border-slate-300 rounded text-xs text-right focus:outline-none focus:ring-1 focus:ring-[#00897b]"
                            />
                          ) : (
                            <button
                              type="button"
                              onClick={() => handleEditDetail(d)}
                              disabled={!isDraft}
                              className={isDraft ? "cursor-pointer hover:underline text-[#00897b]" : ""}
                            >
                              {vat}
                            </button>
                          )}
                        </td>
                        <td className="px-4 py-2 text-sm text-right text-[#1e3a8a]">
                          {editingDetailId === d.id ? (
                            <input
                              type="number"
                              value={editingDiscount}
                              onChange={(e) => setEditingDiscount(e.target.value)}
                              min="0"
                              max="100"
                              className="w-16 px-2 py-1 border border-slate-300 rounded text-xs text-right focus:outline-none focus:ring-1 focus:ring-[#00897b]"
                            />
                          ) : (
                            <button
                              type="button"
                              onClick={() => handleEditDetail(d)}
                              disabled={!isDraft}
                              className={isDraft ? "cursor-pointer hover:underline text-[#00897b]" : ""}
                            >
                              {discount}
                            </button>
                          )}
                        </td>
                        <td className="px-4 py-2 text-sm text-right text-[#1e3a8a]">
                          {formatCurrency(total)}
                        </td>
                        <td className="px-4 py-2 text-sm text-[#4b5563]">
                          {editingDetailId === d.id ? (
                            <input
                              type="text"
                              value={editingDescription}
                              onChange={(e) => setEditingDescription(e.target.value)}
                              placeholder="Ghi chú"
                              className="w-full px-2 py-1 border border-slate-300 rounded text-xs focus:outline-none focus:ring-1 focus:ring-[#00897b]"
                            />
                          ) : (
                            <button
                              type="button"
                              onClick={() => handleEditDetail(d)}
                              disabled={!isDraft}
                              className={`text-left ${isDraft ? "cursor-pointer hover:underline text-[#00897b]" : ""}`}
                            >
                              {d.description || "-"}
                            </button>
                          )}
                        </td>
                        <td className="px-4 py-2 text-sm text-[#4b5563] text-center">
                          {editingDetailId === d.id ? (
                            <div className="flex gap-1 items-center justify-center">
                              <button
                                type="button"
                                onClick={() => handleSaveDetail(d.id)}
                                className="px-2 py-1 text-xs bg-[#00897b] text-white rounded hover:bg-[#007a6c]"
                              >
                                Lưu
                              </button>
                              <button
                                type="button"
                                onClick={handleCancelEdit}
                                className="px-2 py-1 text-xs bg-slate-300 text-slate-600 rounded hover:bg-slate-400"
                              >
                                Hủy
                              </button>
                            </div>
                          ) : (
                            <button
                              type="button"
                              onClick={() => handleDeleteDetail(d.id)}
                              disabled={!isDraft}
                              className={`px-2 py-1 text-xs rounded transition-colors ${isDraft
                                ? "bg-red-100 text-red-600 hover:bg-red-200"
                                : "bg-slate-200 text-slate-400 cursor-not-allowed"
                                }`}
                            >
                              Xóa
                            </button>
                          )}
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

