"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import LoadingOverlay from "@/components/ui/loading-overlay";
import { showToast } from "@/components/ui/toast";
import { adminService } from "@/services/admin.service";

type BillingCycle = "monthly" | "yearly" | "";

interface CreatePlanForm {
  name: string;
  price: string;
  billing_cycle: BillingCycle;
  status: string;
  description: string;
}

export default function CreateSubscriptionPlanPage() {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [form, setForm] = useState<CreatePlanForm>({
    name: "",
    price: "",
    billing_cycle: "",
    status: "active",
    description: "",
  });

  const handleChange = (
    e: React.ChangeEvent<
      HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement
    >
  ) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value as any }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!form.name.trim()) {
      showToast("Tên gói không được để trống", "error");
      return;
    }

    if (!form.price.trim()) {
      showToast("Giá gói không được để trống", "error");
      return;
    }

    const priceNumber = Number(form.price.trim());
    if (Number.isNaN(priceNumber) || priceNumber <= 0) {
      showToast("Giá gói phải là số lớn hơn 0", "error");
      return;
    }

    try {
      setLoading(true);

      let createdBy: string | undefined;
      if (typeof window !== "undefined") {
        const userStr = localStorage.getItem("user_info");
        if (userStr) {
          try {
            const user = JSON.parse(userStr);
            if (user?.user_name) {
              createdBy = user.user_name;
            }
          } catch {
            // ignore
          }
        }
      }

      const payload: any = {
        name: form.name.trim(),
        price: priceNumber,
        status: form.status || "active",
      };

      if (form.billing_cycle) {
        payload.billing_cycle = form.billing_cycle;
      }
      if (form.description.trim()) {
        payload.description = form.description.trim();
      }
      if (createdBy) {
        payload.created_by = createdBy;
        payload.updated_by = createdBy;
      }

      await adminService.createSubscriptionPlan(payload);
      showToast("Tạo gói đăng ký thành công", "success");
      router.push("/admin/subscription-plans");
    } catch (error: any) {
      const message =
        error?.response?.data?.error ||
        error?.message ||
        "Lỗi khi tạo gói đăng ký";
      showToast(message, "error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <LoadingOverlay
        isLoading={loading}
        message="Đang tạo gói đăng ký..."
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
            onClick={() => router.push("/admin/subscription-plans")}
            className="text-[#00897b] hover:underline"
          >
            Quản lý Gói đăng ký
          </button>
          <span className="text-[#4b5563]">/</span>
          <span className="text-[#4b5563]">Tạo mới</span>
        </div>

        {/* Page Header */}
        <div className="mb-6">
          <h1 className="text-[28px] font-bold italic text-[#1e3a8a] mb-2">
            Tạo gói đăng ký
          </h1>
          <p className="text-sm font-normal italic text-[#4b5563]">
            Định nghĩa gói dịch vụ mới cho hệ thống.
          </p>
        </div>

        {/* Form Card */}
        <form onSubmit={handleSubmit}>
          <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6 mb-6 max-w-3xl">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Name */}
              <div className="md:col-span-2">
                <label className="block text-sm font-normal text-[#1e3a8a] mb-1.5">
                  Tên gói <span className="text-red-600">*</span>
                </label>
                <input
                  type="text"
                  name="name"
                  value={form.name}
                  onChange={handleChange}
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#00897b] focus:border-transparent"
                  placeholder="Nhập tên gói (ví dụ: BizFlow Pro, BizFlow Basic...)"
                />
              </div>

              {/* Price */}
              <div>
                <label className="block text-sm font-normal text-[#1e3a8a] mb-1.5">
                  Giá (VNĐ) <span className="text-red-600">*</span>
                </label>
                <input
                  type="number"
                  name="price"
                  value={form.price}
                  onChange={handleChange}
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#00897b] focus:border-transparent"
                  placeholder="Nhập số tiền, không có dấu phân cách"
                  min={0}
                />
                <p className="text-xs text-[#6b7280] mt-1">
                  Nhập số tiền không có dấu phân cách
                </p>
              </div>

              {/* Billing cycle */}
              <div>
                <label className="block text-sm font-normal text-[#1e3a8a] mb-1.5">
                  Chu kỳ thanh toán
                </label>
                <select
                  name="billing_cycle"
                  value={form.billing_cycle}
                  onChange={handleChange}
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#00897b] focus:border-transparent"
                >
                  <option value="">Không xác định</option>
                  <option value="monthly">Tháng</option>
                  <option value="yearly">Năm</option>
                </select>
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
                  <option value="active">Active</option>
                  <option value="inactive">Inactive</option>
                </select>
                <p className="text-xs text-[#6b7280] mt-1">
                  Mặc định là Active
                </p>
              </div>

              {/* Description */}
              <div className="md:col-span-2">
                <label className="block text-sm font-normal text-[#1e3a8a] mb-1.5">
                  Mô tả gói
                </label>
                <textarea
                  name="description"
                  value={form.description}
                  onChange={handleChange}
                  rows={4}
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#00897b] focus:border-transparent resize-none"
                  placeholder="Mô tả ngắn gọn về đối tượng sử dụng, tính năng chính của gói..."
                />
              </div>

              {/* Metadata helper (auto info) */}
              <div className="md:col-span-2">
                <div className="mt-2 rounded-lg border border-slate-200 bg-slate-50 px-4 py-3">
                  <p className="text-sm font-normal text-[#1e3a8a] mb-1">
                    Thông tin tự động
                  </p>
                  <p className="text-sm font-normal text-[#6b7280]">
                    Người tạo và thời gian tạo sẽ được hệ thống ghi nhận tự động
                    khi lưu gói.
                  </p>
                </div>
              </div>
            </div>
          </div>

          {/* Actions */}
          <div className="flex items-center justify-end gap-3 max-w-3xl">
            <button
              type="button"
              onClick={() => router.push("/admin/subscription-plans")}
              className="px-4 py-2 bg-white border border-[#1e3a8a] text-[#1e3a8a] rounded-lg hover:bg-slate-50 transition-colors font-bold italic text-base"
            >
              Hủy
            </button>
            <button
              type="submit"
              disabled={loading}
              className="px-4 py-2 bg-[#00897b] text-white rounded-lg hover:bg-[#007a6c] transition-colors font-bold italic text-base disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? "Đang tạo..." : "Tạo gói"}
            </button>
          </div>
        </form>
      </div>
    </>
  );
}

