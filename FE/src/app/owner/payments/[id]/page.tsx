"use client";

import { useEffect, useMemo, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import LoadingOverlay from "@/components/ui/loading-overlay";
import { showToast } from "@/components/ui/toast";
import {
  ownerService,
  OwnerPayment,
  OwnerPaymentMethod,
  OwnerInvoice,
  OwnerCustomer,
} from "@/services/owner.service";

export default function OwnerPaymentDetailPage() {
  const params = useParams();
  const router = useRouter();
  const idParam = params?.id;
  const paymentId =
    typeof idParam === "string" ? Number(idParam) : NaN;

  const [payment, setPayment] = useState<OwnerPayment | null>(null);
  const [methods, setMethods] = useState<OwnerPaymentMethod[]>([]);
  const [invoice, setInvoice] = useState<OwnerInvoice | null>(null);
  const [customers, setCustomers] = useState<OwnerCustomer[]>([]);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [editMode, setEditMode] = useState(false);

  const [methodId, setMethodId] = useState<number | "">("");
  const [amount, setAmount] = useState<string>("");
  const [description, setDescription] = useState("");

  useEffect(() => {
    if (!Number.isNaN(paymentId)) {
      fetchData();
    } else {
      showToast("ID thanh toán không hợp lệ", "error");
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [paymentId]);

  const fetchData = async () => {
    try {
      setLoading(true);
      const pay = await ownerService.getPayment(paymentId);
      const [methodList, inv, customerList] = await Promise.all([
        ownerService.listOwnerPaymentMethods(),
        ownerService.getInvoice(pay.invoice_id),
        ownerService.listCustomers(),
      ]);
      setPayment(pay);
      setMethods(methodList || []);
      setInvoice(inv);
      setCustomers(customerList || []);
      setMethodId(pay.method_id);
      setAmount(pay.amount || "");
      setDescription(pay.description || "");
    } catch (error: any) {
      const message =
        error?.response?.data?.error ||
        error?.message ||
        "Lỗi khi tải thanh toán";
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

  const selectedMethod =
    methodId && typeof methodId === "number"
      ? methodMap.get(methodId)
      : null;

  const customerMap = useMemo(() => {
    const m = new Map<number, OwnerCustomer>();
    customers.forEach((c) => m.set(c.id, c));
    return m;
  }, [customers]);

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

  const handleSave = async () => {
    if (!payment) return;
    if (!methodId) {
      showToast("Vui lòng chọn phương thức thanh toán", "error");
      return;
    }
    if (!amount || Number(amount) <= 0) {
      showToast("Số tiền thanh toán phải lớn hơn 0", "error");
      return;
    }

    try {
      setSaving(true);
      const updated = await ownerService.updatePayment(payment.id, {
        method_id:
          typeof methodId === "string" ? Number(methodId) : methodId,
        amount: Number(amount),
        description: description.trim() || undefined,
      });
      setPayment(updated);
      setEditMode(false);
      showToast("Cập nhật thanh toán thành công", "success");
    } catch (error: any) {
      showToast("Cập nhật thanh toán thất bại", "error");
    } finally {
      setSaving(false);
    }
  };

  const handleDelete = async () => {
    if (!payment) return;
    if (!confirm("Bạn có chắc chắn muốn xóa thanh toán này?")) return;
    try {
      setSaving(true);
      await ownerService.deletePayment(payment.id);
      showToast("Xóa thanh toán thành công", "success");
      router.push("/owner/payments");
    } catch (error: any) {
      showToast("Xóa thanh toán thất bại", "error");
    } finally {
      setSaving(false);
    }
  };

  if (loading || !payment) {
    return (
      <LoadingOverlay
        isLoading={true}
        message="Đang tải thanh toán..."
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
            onClick={() => router.push("/owner/payments")}
            className="text-[#00897b] hover:underline"
          >
            Thanh toán
          </button>
          <span className="text-[#4b5563]">/</span>
          <span className="text-[#4b5563]">#{payment.id}</span>
        </div>

        {/* Header */}
        <div className="mb-6 flex items-center justify-between">
          <div>
            <h1 className="text-[28px] font-bold italic text-[#1e3a8a] mb-1">
              Thanh toán #{payment.id}
            </h1>
            <p className="text-xs text-[#6b7280]">
              Ngày tạo: {formatDateTime(payment.created_at)}
            </p>
          </div>
          <div className="flex items-center gap-3">
            <span className="px-3 py-1 text-xs font-bold italic rounded-full text-white bg-[#10b981]">
              {payment.status || "N/A"}
            </span>
            <button
              type="button"
              onClick={() => setEditMode((prev) => !prev)}
              className="px-4 py-2 bg-white border border-[#1e3a8a] text-[#1e3a8a] rounded-lg hover:bg-slate-50 transition-colors text-sm font-medium"
            >
              {editMode ? "Hủy chỉnh sửa" : "Chỉnh sửa"}
            </button>
            <button
              type="button"
              onClick={handleDelete}
              className="px-4 py-2 bg-red-50 border border-red-600 text-red-600 rounded-lg hover:bg-red-100 transition-colors text-sm font-medium"
            >
              Xóa
            </button>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Thông tin thanh toán */}
          <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6">
            <h2 className="text-[18px] font-bold italic text-[#1e3a8a] mb-4">
              Thông tin thanh toán
            </h2>
            <div className="space-y-4 text-sm">
              <div>
                <p className="text-xs text-[#6b7280] mb-1">Hóa đơn</p>
                <p className="text-[#1e3a8a]">
                  {invoice ? (
                    <>
                      {`Hóa đơn #${invoice.id} - Khách: ${
                        invoice.customer_id
                          ? customerMap.get(invoice.customer_id)?.name ||
                            `#${invoice.customer_id}`
                          : "-"
                      }`}
                    </>
                  ) : (
                    `Hóa đơn #${payment.invoice_id}`
                  )}
                </p>
              </div>
              <div>
                <p className="text-xs text-[#6b7280] mb-1">
                  Phương thức thanh toán
                </p>
                {editMode ? (
                  <select
                    value={methodId}
                    onChange={(e) =>
                      setMethodId(
                        e.target.value ? Number(e.target.value) : ""
                      )
                    }
                    className="w-full max-w-xs px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#00897b] focus:border-transparent"
                  >
                    <option value="">Chọn phương thức</option>
                    {methods.map((m) => (
                      <option key={m.id} value={m.id}>
                        {m.name}
                      </option>
                    ))}
                  </select>
                ) : (
                  <p className="text-[#1e3a8a]">
                    {selectedMethod?.name || `PT #${payment.method_id}`}
                  </p>
                )}
              </div>
              <div>
                <p className="text-xs text-[#6b7280] mb-1">Số tiền</p>
                {editMode ? (
                  <input
                    type="number"
                    value={amount}
                    onChange={(e) => setAmount(e.target.value)}
                    className="w-full max-w-xs px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#00897b] focus:border-transparent"
                  />
                ) : (
                  <p className="text-[#1e3a8a]">
                    {formatCurrency(payment.amount)}
                  </p>
                )}
              </div>
              <div>
                <p className="text-xs text-[#6b7280] mb-1">Ghi chú</p>
                {editMode ? (
                  <textarea
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                    rows={3}
                    className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#00897b] focus:border-transparent"
                  />
                ) : (
                  <p className="text-[#1e3a8a]">
                    {payment.description || "-"}
                  </p>
                )}
              </div>
              {editMode && (
                <div className="pt-2 flex items-center justify-end">
                  <button
                    type="button"
                    onClick={handleSave}
                    disabled={saving}
                    className="px-5 py-2 bg-[#00897b] text-white rounded-lg text-sm font-bold hover:bg-[#007a6c] transition-colors disabled:bg-slate-400 disabled:cursor-not-allowed"
                  >
                    {saving ? "Đang lưu..." : "Lưu thay đổi"}
                  </button>
                </div>
              )}
            </div>
          </div>

          {/* Tóm tắt & audit */}
          <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6">
            <h2 className="text-[18px] font-bold italic text-[#1e3a8a] mb-4">
              Tóm tắt
            </h2>
            <div className="space-y-2 text-sm text-[#1e3a8a]">
              <p>
                <span className="font-semibold">Số tiền thanh toán:</span>{" "}
                {formatCurrency(payment.amount)}
              </p>
              <p>
                <span className="font-semibold">Trạng thái:</span>{" "}
                {payment.status || "-"}
              </p>
              <p>
                <span className="font-semibold">Người tạo:</span>{" "}
                {payment.created_by || "-"}
              </p>
              <p>
                <span className="font-semibold">Người cập nhật:</span>{" "}
                {payment.updated_by || "-"}
              </p>
              <p>
                <span className="font-semibold">Cập nhật lần cuối:</span>{" "}
                {formatDateTime(payment.updated_at)}
              </p>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}

