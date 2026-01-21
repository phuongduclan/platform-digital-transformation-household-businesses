"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import LoadingOverlay from "@/components/ui/loading-overlay";
import { showToast } from "@/components/ui/toast";
import { adminService } from "@/services/admin.service";

type PaymentStatus = "Active" | "Inactive";

interface CreatePaymentMethodForm {
  name: string;
  status: PaymentStatus;
}

export default function CreatePaymentMethodPage() {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [form, setForm] = useState<CreatePaymentMethodForm>({
    name: "",
    status: "Active",
  });

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
      setLoading(true);

      await adminService.createPaymentMethod({
        name: form.name.trim(),
        status: form.status,
      });

      showToast("Tạo phương thức thanh toán thành công", "success");
      router.push("/admin/payment-methods");
    } catch (error: any) {
      const message =
        error?.response?.data?.error ||
        error?.message ||
        "Lỗi khi tạo phương thức thanh toán";
      showToast(message, "error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <LoadingOverlay
        isLoading={loading}
        message="Đang tạo phương thức thanh toán..."
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
          <span className="text-[#4b5563]">Tạo mới</span>
        </div>

        {/* Page Header */}
        <div className="mb-6">
          <h1 className="text-[28px] font-bold italic text-[#1e3a8a] mb-2">
            Tạo phương thức thanh toán
          </h1>
          <p className="text-sm font-normal italic text-[#4b5563]">
            Thêm phương thức thanh toán mới cho hệ thống.
          </p>
        </div>

        {/* Form Card */}
        <form onSubmit={handleSubmit}>
          <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6 mb-6 max-w-xl">
            <div className="space-y-6">
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
                  placeholder="Ví dụ: Chuyển khoản ngân hàng, Tiền mặt..."
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
                <p className="text-xs text-[#6b7280] mt-1">
                  Mặc định là Active
                </p>
              </div>
            </div>
          </div>

          {/* Action buttons */}
          <div className="flex items-center justify-end gap-3 max-w-xl">
            <button
              type="button"
              onClick={() => router.push("/admin/payment-methods")}
              className="px-4 py-2 bg-white border border-[#1e3a8a] text-[#1e3a8a] rounded-lg hover:bg-slate-50 transition-colors font-bold italic text-base"
            >
              Hủy
            </button>
            <button
              type="submit"
              disabled={loading}
              className="px-4 py-2 bg-[#00897b] text-white rounded-lg hover:bg-[#007a6c] transition-colors font-bold italic text-base disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? "Đang tạo..." : "Tạo phương thức"}
            </button>
          </div>
        </form>
      </div>
    </>
  );
}

