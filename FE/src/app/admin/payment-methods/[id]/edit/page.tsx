"use client";

import { useEffect, useState } from "react";
import { useRouter, useParams } from "next/navigation";
import LoadingOverlay from "@/components/ui/loading-overlay";
import { showToast } from "@/components/ui/toast";
import { adminService } from "@/services/admin.service";

type PaymentStatus = "Active" | "Inactive";

interface PaymentMethodDetail {
  id: number;
  name: string;
  status: PaymentStatus;
  created_at?: string | null;
  updated_at?: string | null;
}

interface EditPaymentMethodForm {
  name: string;
  status: PaymentStatus;
}

export default function EditPaymentMethodPage() {
  const router = useRouter();
  const params = useParams();
  const id = Number(params?.id);

  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [paymentMethod, setPaymentMethod] = useState<PaymentMethodDetail | null>(
    null
  );
  const [form, setForm] = useState<EditPaymentMethodForm>({
    name: "",
    status: "Active",
  });

  useEffect(() => {
    if (!Number.isNaN(id)) {
      fetchPaymentMethod();
    } else {
      setLoading(false);
      showToast("ID phương thức thanh toán không hợp lệ", "error");
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [id]);

  const fetchPaymentMethod = async () => {
    try {
      setLoading(true);
      const data = await adminService.getPaymentMethod(id);

      const detail: PaymentMethodDetail = {
        id: data.id,
        name: data.name,
        status: (data.status as PaymentStatus) || "Active",
        created_at: data.created_at ?? null,
        updated_at: data.updated_at ?? null,
      };

      setPaymentMethod(detail);
      setForm({
        name: detail.name,
        status: detail.status,
      });
    } catch (error: any) {
      const message =
        error?.response?.data?.error ||
        error?.message ||
        "Lỗi khi tải thông tin phương thức thanh toán";
      showToast(message, "error");
      router.push("/admin/payment-methods");
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value as any }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!form.name.trim()) {
      showToast("Tên phương thức thanh toán không được để trống", "error");
      return;
    }

    try {
      setSaving(true);

      await adminService.updatePaymentMethod(id, {
        name: form.name.trim(),
        status: form.status,
      });

      showToast("Cập nhật phương thức thanh toán thành công", "success");
      router.push("/admin/payment-methods");
    } catch (error: any) {
      const message =
        error?.response?.data?.error ||
        error?.message ||
        "Lỗi khi cập nhật phương thức thanh toán";
      showToast(message, "error");
    } finally {
      setSaving(false);
    }
  };

  const handleCancel = () => {
    router.push("/admin/payment-methods");
  };

  const formatDate = (dateString?: string | null) => {
    if (!dateString) return "-";
    const date = new Date(dateString);
    return date.toLocaleDateString("vi-VN", {
      day: "2-digit",
      month: "2-digit",
      year: "numeric",
    });
  };

  if (loading) {
    return (
      <LoadingOverlay
        isLoading={true}
        message="Đang tải thông tin phương thức thanh toán..."
      />
    );
  }

  if (!paymentMethod) {
    return (
      <div className="p-8">
        <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6 text-center">
          <p className="text-[#4b5563] mb-4">
            Không tìm thấy phương thức thanh toán
          </p>
          <button
            type="button"
            onClick={handleCancel}
            className="px-4 py-2 bg-[#00897b] text-white rounded-lg hover:bg-[#007a6c] transition-colors text-sm font-medium"
          >
            Quay lại danh sách
          </button>
        </div>
      </div>
    );
  }

  return (
    <>
      <LoadingOverlay
        isLoading={saving}
        message="Đang cập nhật phương thức thanh toán..."
      />
      <div className="p-8">
        {/* Breadcrumb */}
        <div className="mb-4 flex items-center gap-2 text-sm">
          <button
            type="button"
            onClick={() => router.push("/admin")}
            className="text-[#00897b] hover:underline"
          >
            Dashboard
          </button>
          <span className="text-[#4b5563]">/</span>
          <button
            type="button"
            onClick={() => router.push("/admin/payment-methods")}
            className="text-[#00897b] hover:underline"
          >
            Phương thức Thanh toán
          </button>
          <span className="text-[#4b5563]">/</span>
          <span className="text-[#4b5563]">Chỉnh sửa</span>
        </div>

        {/* Page Header */}
        <div className="mb-6">
          <h1 className="text-[28px] font-bold italic text-[#1e3a8a] mb-2">
            Chỉnh sửa phương thức thanh toán
          </h1>
        </div>

        {/* Form Card */}
        <form onSubmit={handleSubmit}>
          <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6 mb-6 max-w-xl">
            <div className="space-y-6">
              {/* ID (readonly) */}
              <div>
                <label className="block text-sm font-normal text-[#4b5563] mb-1.5">
                  ID
                </label>
                <div className="px-3 py-2 border border-slate-200 rounded-lg bg-slate-50 text-sm text-[#1e3a8a]">
                  {paymentMethod.id}
                </div>
              </div>

              {/* Name */}
              <div>
                <label className="block text-sm font-normal text-[#1e3a8a] mb-1.5">
                  Tên phương thức thanh toán{" "}
                  <span className="text-red-600">*</span>
                </label>
                <input
                  type="text"
                  name="name"
                  value={form.name}
                  onChange={handleChange}
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#00897b] focus:border-transparent"
                  placeholder="Nhập tên phương thức thanh toán"
                />
              </div>

              {/* Status */}
              <div>
                <label className="block text-sm font-normal text-[#1e3a8a] mb-1.5">
                  Trạng thái
                </label>
                <select
                  name="status"
                  value={form.status}
                  onChange={handleChange}
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#00897b] focus:border-transparent"
                >
                  <option value="Active">Active</option>
                  <option value="Inactive">Inactive</option>
                </select>
              </div>

              {/* Metadata */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-2 border-t border-slate-200">
                <div>
                  <label className="block text-xs font-normal text-[#6b7280] mb-1">
                    Ngày tạo
                  </label>
                  <p className="text-sm font-normal text-[#1e3a8a]">
                    {formatDate(paymentMethod.created_at || undefined)}
                  </p>
                </div>
                <div>
                  <label className="block text-xs font-normal text-[#6b7280] mb-1">
                    Ngày cập nhật
                  </label>
                  <p className="text-sm font-normal text-[#1e3a8a]">
                    {formatDate(paymentMethod.updated_at || undefined)}
                  </p>
                </div>
              </div>
            </div>
          </div>

          {/* Actions */}
          <div className="flex items-center justify-end gap-3 max-w-xl">
            <button
              type="button"
              onClick={handleCancel}
              className="px-4 py-2 bg-white border border-[#1e3a8a] text-[#1e3a8a] rounded-lg hover:bg-slate-50 transition-colors font-bold italic text-base"
            >
              Hủy
            </button>
            <button
              type="submit"
              disabled={saving}
              className="px-4 py-2 bg-[#00897b] text-white rounded-lg hover:bg-[#007a6c] transition-colors font-bold italic text-base disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {saving ? "Đang lưu..." : "Lưu thay đổi"}
            </button>
          </div>
        </form>
      </div>
    </>
  );
}

