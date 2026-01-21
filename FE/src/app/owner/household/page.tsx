"use client";

import { useEffect, useState } from "react";
import LoadingOverlay from "@/components/ui/loading-overlay";
import { showToast } from "@/components/ui/toast";
import {
  ownerService,
  OwnerHousehold,
  OwnerSubscription,
} from "@/services/owner.service";

interface HouseholdFormState {
  name: string;
  tax_code: string;
  address: string;
  phone: string;
  email: string;
  description: string;
}

export default function OwnerHouseholdSettingsPage() {
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [household, setHousehold] = useState<OwnerHousehold | null>(null);
  const [subscription, setSubscription] = useState<OwnerSubscription | null>(
    null
  );
  const [form, setForm] = useState<HouseholdFormState>({
    name: "",
    tax_code: "",
    address: "",
    phone: "",
    email: "",
    description: "",
  });

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [hh, sub] = await Promise.all([
        ownerService.getHousehold(),
        ownerService.getSubscription(),
      ]);
      setHousehold(hh);
      setSubscription(sub);
      setForm({
        name: hh.name || "",
        tax_code: hh.tax_code || "",
        address: hh.address || "",
        phone: hh.phone || "",
        email: "", // BE hiện chưa có trường email riêng cho household
        description: hh.description || "",
      });
    } catch (error: any) {
      const message =
        error?.response?.data?.error ||
        error?.message ||
        "Lỗi khi tải thông tin hộ kinh doanh";
      showToast(message, "error");
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (
    e: React.ChangeEvent<
      HTMLInputElement | HTMLTextAreaElement
    >
  ) => {
    const { name, value } = e.target;
    setForm((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSave = async () => {
    if (!form.name.trim()) {
      showToast("Tên hộ kinh doanh không được để trống", "error");
      return;
    }

    try {
      setSaving(true);

      const updated = await ownerService.updateHousehold({
        name: form.name.trim(),
        tax_code: form.tax_code.trim() || null,
        address: form.address.trim() || null,
        phone: form.phone.trim() || null,
        description: form.description.trim() || null,
      });

      setHousehold(updated);
      showToast("Cập nhật thông tin hộ kinh doanh thành công", "success");
    } catch (error: any) {
      const message =
        error?.response?.data?.error ||
        error?.message ||
        "Lỗi khi cập nhật thông tin hộ kinh doanh";
      showToast(message, "error");
    } finally {
      setSaving(false);
    }
  };

  const formatDate = (value?: string) => {
    if (!value) return "-";
    const d = new Date(value);
    return d.toLocaleDateString("vi-VN", {
      day: "2-digit",
      month: "2-digit",
      year: "numeric",
    });
  };

  if (loading && !household) {
    return (
      <LoadingOverlay
        isLoading={true}
        message="Đang tải thông tin hộ kinh doanh..."
      />
    );
  }

  return (
    <>
      <LoadingOverlay
        isLoading={saving}
        message="Đang lưu thông tin hộ kinh doanh..."
      />
      <div className="p-8">
        {/* Page Header */}
        <div className="mb-8">
          <h1 className="text-[28px] font-bold italic text-[#1e3a8a] mb-2">
            Cài đặt Hộ kinh doanh
          </h1>
          <p className="text-sm text-[#4b5563]">
            Quản lý thông tin hộ/đơn vị kinh doanh và gói đăng ký hiện tại.
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left: Household form */}
          <div className="lg:col-span-2">
            <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6">
              <h2 className="text-[20px] font-bold italic text-[#1e3a8a] mb-6">
                Thông tin hộ kinh doanh
              </h2>
              <div className="space-y-5">
                {/* Name */}
                <div>
                  <label className="block text-base font-normal text-[#1e3a8a] mb-2">
                    Tên hộ kinh doanh <span className="text-red-600">*</span>
                  </label>
                  <input
                    type="text"
                    name="name"
                    value={form.name}
                    onChange={handleChange}
                    className="w-full px-4 py-3 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#00897b] focus:border-transparent"
                    placeholder="Nhập tên hộ kinh doanh"
                  />
                </div>

                {/* Tax code + Phone */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-base font-normal text-[#1e3a8a] mb-2">
                      Mã số thuế
                    </label>
                    <input
                      type="text"
                      name="tax_code"
                      value={form.tax_code}
                      onChange={handleChange}
                      className="w-full px-4 py-3 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#00897b] focus:border-transparent"
                      placeholder="Nhập mã số thuế (nếu có)"
                    />
                  </div>
                  <div>
                    <label className="block text-base font-normal text-[#1e3a8a] mb-2">
                      Số điện thoại
                    </label>
                    <input
                      type="text"
                      name="phone"
                      value={form.phone}
                      onChange={handleChange}
                      className="w-full px-4 py-3 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#00897b] focus:border-transparent"
                      placeholder="Nhập số điện thoại liên hệ"
                    />
                  </div>
                </div>

                {/* Address */}
                <div>
                  <label className="block text-base font-normal text-[#1e3a8a] mb-2">
                    Địa chỉ
                  </label>
                  <input
                    type="text"
                    name="address"
                    value={form.address}
                    onChange={handleChange}
                    className="w-full px-4 py-3 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#00897b] focus:border-transparent"
                    placeholder="Nhập địa chỉ hộ kinh doanh"
                  />
                </div>

                {/* Email (hiện chỉ lưu client, vì BE chưa có field) */}
                <div>
                  <label className="block text-base font-normal text-[#1e3a8a] mb-2">
                    Email liên hệ
                  </label>
                  <input
                    type="email"
                    name="email"
                    value={form.email}
                    onChange={handleChange}
                    className="w-full px-4 py-3 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#00897b] focus:border-transparent"
                    placeholder="Nhập email liên hệ (tùy chọn)"
                  />
                  <p className="mt-1 text-xs text-[#9ca3af]">
                    Lưu ý: Email hiện chỉ dùng cho liên hệ, chưa được lưu trong
                    backend.
                  </p>
                </div>

                {/* Description */}
                <div>
                  <label className="block text-base font-normal text-[#1e3a8a] mb-2">
                    Ghi chú
                  </label>
                  <textarea
                    name="description"
                    value={form.description}
                    onChange={handleChange}
                    rows={3}
                    className="w-full px-4 py-3 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#00897b] focus:border-transparent resize-none"
                    placeholder="Ghi chú thêm về hộ kinh doanh"
                  />
                </div>

                {/* Footer actions */}
                <div className="flex items-center gap-3 pt-2">
                  <button
                    type="button"
                    onClick={handleSave}
                    disabled={saving}
                    className="px-6 py-3 bg-[#00897b] text-white rounded-lg hover:bg-[#007a6c] transition-colors font-bold italic text-base disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {saving ? "Đang lưu..." : "Lưu thay đổi"}
                  </button>
                </div>
              </div>
            </div>
          </div>

          {/* Right: Subscription panel + upgrade entry */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6">
              <h2 className="text-[18px] font-bold italic text-[#1e3a8a] mb-4">
                Gói đăng ký hiện tại
              </h2>
              {subscription ? (
                <div className="space-y-4 text-sm">
                  <div className="flex items-center justify-between">
                    <span className="text-[#4b5563]">Mã gói</span>
                    <span className="font-bold text-[#1e3a8a]">
                      #{subscription.plan_id}
                    </span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-[#4b5563]">Trạng thái</span>
                    <span
                      className={`px-2 py-1 text-xs font-bold italic rounded text-white ${
                        subscription.is_active
                          ? "bg-[#10b981]"
                          : "bg-[#6b7280]"
                      }`}
                    >
                      {subscription.is_active ? "Đang hoạt động" : "Không hoạt động"}
                    </span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-[#4b5563]">Ngày bắt đầu</span>
                    <span className="font-normal text-[#1e3a8a]">
                      {formatDate(subscription.start_date)}
                    </span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-[#4b5563]">Ngày kết thúc</span>
                    <span className="font-normal text-[#1e3a8a]">
                      {formatDate(subscription.end_date)}
                    </span>
                  </div>
                  {/* Upgrade entry */}
                  <div className="pt-3 mt-2 border-t border-slate-200">
                    <p className="text-xs text-[#6b7280] mb-3">
                      Muốn sử dụng nhiều tính năng hơn? Hãy nâng cấp lên gói cao hơn.
                    </p>
                    <a
                      href="/owner/subscription-plans"
                      className="inline-flex items-center px-4 py-2 rounded-lg bg-white border border-[#1e3a8a] text-[#1e3a8a] text-xs font-bold italic hover:bg-slate-50 transition-colors"
                    >
                      Xem và nâng cấp gói
                    </a>
                  </div>
                </div>
              ) : (
                <p className="text-sm text-[#6b7280]">
                  Hộ kinh doanh hiện chưa có gói đăng ký hoạt động. Vui lòng liên
                  hệ quản trị hoặc thực hiện đăng ký gói mới.
                </p>
              )}
            </div>
          </div>
        </div>
      </div>
    </>
  );
}

