"use client";

import { useEffect, useMemo, useState } from "react";
import { useRouter } from "next/navigation";
import LoadingOverlay from "@/components/ui/loading-overlay";
import { showToast } from "@/components/ui/toast";
import {
  ownerService,
  OwnerInvoice,
  OwnerPaymentMethod,
  OwnerCustomer,
} from "@/services/owner.service";

export default function OwnerCreatePaymentPage() {
  const router = useRouter();
  const [invoices, setInvoices] = useState<OwnerInvoice[]>([]);
  const [methods, setMethods] = useState<OwnerPaymentMethod[]>([]);
  const [customers, setCustomers] = useState<OwnerCustomer[]>([]);
  const [saving, setSaving] = useState(false);

  const [invoiceId, setInvoiceId] = useState<number | "">("");
  const [methodId, setMethodId] = useState<number | "">("");
  const [amount, setAmount] = useState<string>("");
  const [description, setDescription] = useState("");

  useEffect(() => {
    fetchMeta();
  }, []);

  const fetchMeta = async () => {
    try {
      const [invList, methodList, customerList] = await Promise.all([
        ownerService.listInvoices({ status: "Confirm" }),
        ownerService.listOwnerPaymentMethods(),
        ownerService.listCustomers(), // cần đủ để map tên khách từ customer_id
      ]);
      setInvoices(
        (invList || []).filter(
          (inv: any) =>
            inv.invoice_type === "UNPAID" && inv.customer_id !== null
        )
      );
      setMethods(methodList || []);
      setCustomers(customerList || []);
    } catch (error: any) {
      const message =
        error?.response?.data?.error ||
        error?.message ||
        "Lỗi khi tải dữ liệu thanh toán";
      showToast(message, "error");
    }
  };

  const invoiceMap = useMemo(() => {
    const m = new Map<number, OwnerInvoice>();
    (invoices || []).forEach((inv: any) => m.set(inv.id, inv));
    return m;
  }, [invoices]);

  const customerMap = useMemo(() => {
    const m = new Map<number, OwnerCustomer>();
    customers.forEach((c) => m.set(c.id, c));
    return m;
  }, [customers]);

  const selectedInvoice =
    invoiceId && typeof invoiceId === "number"
      ? invoiceMap.get(invoiceId)
      : null;

  const formatCurrency = (value: number) =>
    new Intl.NumberFormat("vi-VN", {
      style: "currency",
      currency: "VND",
      maximumFractionDigits: 0,
    }).format(value);

  const handleSubmit = async () => {
    if (!invoiceId) {
      showToast("Vui lòng chọn hóa đơn cần thanh toán", "error");
      return;
    }
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
      await ownerService.createPayment({
        invoice_id:
          typeof invoiceId === "string" ? Number(invoiceId) : invoiceId,
        method_id:
          typeof methodId === "string" ? Number(methodId) : methodId,
        amount: Number(amount),
        description: description.trim() || undefined,
      });
      showToast("Tạo thanh toán thành công", "success");
      router.push("/owner/payments");
    } catch (error: any) {
      const message =
        error?.response?.data?.error ||
        error?.message ||
        "Tạo thanh toán thất bại";
      showToast(message, "error");
    } finally {
      setSaving(false);
    }
  };

  return (
    <>
      <LoadingOverlay
        isLoading={saving}
        message="Đang lưu thanh toán..."
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
          <span className="text-[#4b5563]">Tạo mới</span>
        </div>

        {/* Header */}
        <div className="mb-6 flex items-center justify-between">
          <h1 className="text-[28px] font-bold italic text-[#1e3a8a]">
            Tạo thanh toán
          </h1>
        </div>

        {/* Form */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 bg-white rounded-lg shadow-sm border border-slate-200 p-6">
            <h2 className="text-[18px] font-bold italic text-[#1e3a8a] mb-4">
              Thông tin thanh toán
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="md:col-span-2">
                <label className="block text-sm font-normal text-[#1e3a8a] mb-1.5">
                  Hóa đơn cần thanh toán
                </label>
                <select
                  value={invoiceId}
                  onChange={(e) =>
                    setInvoiceId(
                      e.target.value ? Number(e.target.value) : ""
                    )
                  }
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#00897b] focus:border-transparent"
                >
                  <option value="">
                    Chọn hóa đơn UNPAID đã xác nhận (có khách hàng)
                  </option>
                  {invoices.map((inv: any) => {
                    const customer =
                      inv.customer_id && customerMap.get(inv.customer_id);
                    const customerName = customer?.name || `#${inv.customer_id}`;
                    return (
                      <option key={inv.id} value={inv.id}>
                        {`Hóa đơn #${inv.id} - Khách: ${customerName} - ${formatCurrency(
                          Number(inv.total_amount || 0)
                        )}`}
                      </option>
                    );
                  })}
                </select>
              </div>

              <div>
                <label className="block text-sm font-normal text-[#1e3a8a] mb-1.5">
                  Phương thức thanh toán
                </label>
                <select
                  value={methodId}
                  onChange={(e) =>
                    setMethodId(
                      e.target.value ? Number(e.target.value) : ""
                    )
                  }
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#00897b] focus:border-transparent"
                >
                  <option value="">Chọn phương thức</option>
                  {methods.map((m) => (
                    <option key={m.id} value={m.id}>
                      {m.name}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-normal text-[#1e3a8a] mb-1.5">
                  Số tiền thanh toán
                </label>
                <input
                  type="number"
                  value={amount}
                  onChange={(e) => setAmount(e.target.value)}
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#00897b] focus:border-transparent"
                  placeholder="Nhập số tiền (VND)"
                />
              </div>

              <div className="md:col-span-2">
                <label className="block text-sm font-normal text-[#1e3a8a] mb-1.5">
                  Ghi chú
                </label>
                <textarea
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  rows={3}
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#00897b] focus:border-transparent"
                />
              </div>
            </div>
          </div>

          {/* Summary */}
          <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6">
            <h2 className="text-[18px] font-bold italic text-[#1e3a8a] mb-4">
              Tóm tắt
            </h2>
            {selectedInvoice ? (
              <div className="space-y-2 text-sm text-[#1e3a8a]">
                <p>
                  <span className="font-semibold">Hóa đơn:</span> #
                  {selectedInvoice.id}
                </p>
                <p>
                  <span className="font-semibold">Khách hàng:</span>{" "}
                  {selectedInvoice.customer_id
                    ? customerMap.get(selectedInvoice.customer_id)?.name ||
                      `#${selectedInvoice.customer_id}`
                    : "-"}
                </p>
                <p>
                  <span className="font-semibold">Tổng tiền hóa đơn:</span>{" "}
                  {formatCurrency(Number(selectedInvoice.total_amount || 0))}
                </p>
                <p>
                  <span className="font-semibold">Số tiền thanh toán:</span>{" "}
                  {amount ? formatCurrency(Number(amount)) : "-"}
                </p>
              </div>
            ) : (
              <p className="text-sm text-[#6b7280]">
                Chọn hóa đơn UNPAID đã xác nhận để ghi nhận thanh toán công nợ.
              </p>
            )}
          </div>
        </div>

        <div className="mt-6 flex items-center justify-end gap-3">
          <button
            type="button"
            onClick={() => router.push("/owner/payments")}
            className="px-4 py-2 bg-white border border-slate-300 text-sm rounded-lg hover:bg-slate-50 transition-colors"
          >
            Hủy
          </button>
          <button
            type="button"
            onClick={handleSubmit}
            disabled={saving}
            className="px-6 py-2 bg-[#00897b] text-white rounded-lg text-sm font-bold hover:bg-[#007a6c] transition-colors disabled:bg-slate-400 disabled:cursor-not-allowed"
          >
            {saving ? "Đang lưu..." : "Lưu thanh toán"}
          </button>
        </div>
      </div>
    </>
  );
}

