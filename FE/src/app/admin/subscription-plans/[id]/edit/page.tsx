"use client";

import { useEffect, useState } from "react";
import { useRouter, useParams } from "next/navigation";
import LoadingOverlay from "@/components/ui/loading-overlay";
import { showToast } from "@/components/ui/toast";
import { adminService } from "@/services/admin.service";

type BillingCycle = "monthly" | "yearly" | "";

interface PlanDetail {
  id: number;
  name: string;
  price: number;
  billing_cycle: BillingCycle | null;
  status: string;
  description?: string | null;
  created_at?: string | null;
  updated_at?: string | null;
}

interface EditPlanForm {
  name: string;
  price: string;
  billing_cycle: BillingCycle;
  status: string;
  description: string;
}

export default function EditSubscriptionPlanPage() {
  const router = useRouter();
  const params = useParams();
  const id = Number(params?.id);

  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [plan, setPlan] = useState<PlanDetail | null>(null);
  const [form, setForm] = useState<EditPlanForm>({
    name: "",
    price: "",
    billing_cycle: "",
    status: "active",
    description: "",
  });

  useEffect(() => {
    if (!Number.isNaN(id)) {
      fetchPlan();
    } else {
      setLoading(false);
      showToast("ID gói đăng ký không hợp lệ", "error");
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [id]);

  const fetchPlan = async () => {
    try {
      setLoading(true);
      const data = await adminService.getSubscriptionPlan(id);

      const detail: PlanDetail = {
        id: data.id,
        name: data.name,
        price: data.price,
        billing_cycle: (data.billing_cycle as BillingCycle) || "",
        status: data.status || "active",
        description: data.description ?? "",
        created_at: data.created_at ?? null,
        updated_at: data.updated_at ?? null,
      };

      setPlan(detail);
      setForm({
        name: detail.name,
        price: String(detail.price ?? ""),
        billing_cycle: detail.billing_cycle || "",
        status: detail.status || "active",
        description: detail.description || "",
      });
    } catch (error: any) {
      const message =
        error?.response?.data?.error ||
        error?.message ||
        "Lỗi khi tải thông tin gói đăng ký";
      showToast(message, "error");
      router.push("/admin/subscription-plans");
    } finally {
      setLoading(false);
    }
  };

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
      setSaving(true);

      let updatedBy: string | undefined;
      if (typeof window !== "undefined") {
        const userStr = localStorage.getItem("user_info");
        if (userStr) {
          try {
            const user = JSON.parse(userStr);
            if (user?.user_name) {
              updatedBy = user.user_name;
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
      if (updatedBy) {
        payload.updated_by = updatedBy;
      }

      await adminService.updateSubscriptionPlan(id, payload);
      showToast("Cập nhật gói đăng ký thành công", "success");
      router.push("/admin/subscription-plans");
    } catch (error: any) {
      const message =
        error?.response?.data?.error ||
        error?.message ||
        "Lỗi khi cập nhật gói đăng ký";
      showToast(message, "error");
    } finally {
      setSaving(false);
    }
  };

  const handleCancel = () => {
    router.push("/admin/subscription-plans");
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
        message="Đang tải thông tin gói đăng ký..."
      />
    );
  }

  if (!plan) {
    return (
      <div className="p-8">
        <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6 text-center">
          <p className="text-[#4b5563] mb-4">Không tìm thấy gói đăng ký</p>
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
        message="Đang cập nhật gói đăng ký..."
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
          <span className="text-[#4b5563]">Chỉnh sửa</span>
        </div>

        {/* Page Header */}
        <div className="mb-6">
          <h1 className="text-[28px] font-bold italic text-[#1e3a8a] mb-2">
            Chỉnh sửa gói đăng ký
          </h1>
        </div>

        {/* Form Card */}
        <form onSubmit={handleSubmit}>
          <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6 mb-6 max-w-3xl">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* ID (readonly) */}
              <div>
                <label className="block text-sm font-normal text-[#4b5563] mb-1.5">
                  ID
                </label>
                <div className="px-3 py-2 border border-slate-200 rounded-lg bg-slate-50 text-sm text-[#1e3a8a]">
                  {plan.id}
                </div>
              </div>

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
                  placeholder="Nhập tên gói"
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
                  placeholder="Mô tả ngắn gọn về gói"
                />
              </div>

              {/* Metadata */}
              <div className="md:col-span-2">
                <div className="mt-2 rounded-lg border border-slate-200 bg-slate-50 px-4 py-3">
                  <p className="text-sm font-normal text-[#1e3a8a] mb-1">
                    Thông tin tự động
                  </p>
                  <p className="text-sm font-normal text-[#6b7280]">
                    Ngày tạo: {formatDate(plan.created_at || undefined)} • Ngày
                    cập nhật: {formatDate(plan.updated_at || undefined)}
                  </p>
                </div>
              </div>
            </div>
          </div>

          {/* Actions */}
          <div className="flex items-center justify-end gap-3 max-w-3xl">
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

