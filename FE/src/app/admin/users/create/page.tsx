"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { adminService } from "@/services/admin.service";
import LoadingOverlay from "@/components/ui/loading-overlay";
import { showToast } from "@/components/ui/toast";

type StatusType = "Active" | "Inactive";

interface CreateUserFormState {
  role_id: number | "";
  user_name: string;
  email: string;
  password: string;
  confirmPassword: string;
  status: StatusType;
  household_id: string;
  description: string;
}

export default function CreateUserPage() {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [currentAdminName, setCurrentAdminName] = useState<string | null>(null);
  const [form, setForm] = useState<CreateUserFormState>({
    role_id: "",
    user_name: "",
    email: "",
    password: "",
    confirmPassword: "",
    status: "Active",
    household_id: "",
    description: "",
  });

  // Lấy tên admin hiện tại để hiển thị ở ô "Người tạo"
  useState(() => {
    if (typeof window !== "undefined") {
      const userStr = localStorage.getItem("user_info");
      if (userStr) {
        try {
          const user = JSON.parse(userStr);
          if (user?.user_name) {
            setCurrentAdminName(user.user_name);
          }
        } catch {
          // ignore
        }
      }
    }
  });

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>
  ) => {
    const { name, value } = e.target;
    setForm((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!form.role_id) {
      showToast("Vui lòng chọn vai trò (Admin hoặc Owner)", "error");
      return;
    }
    if (!form.user_name.trim()) {
      showToast("Tên đăng nhập không được để trống", "error");
      return;
    }
    if (!form.password) {
      showToast("Mật khẩu không được để trống", "error");
      return;
    }
    if (form.password !== form.confirmPassword) {
      showToast("Mật khẩu xác nhận không khớp", "error");
      return;
    }

    try {
      setLoading(true);

      const payload: any = {
        role_id: typeof form.role_id === "string" ? Number(form.role_id) : form.role_id,
        user_name: form.user_name.trim(),
        password: form.password,
        status: form.status,
      };

      if (form.email.trim()) {
        payload.email = form.email.trim();
      }
      if (form.description.trim()) {
        payload.description = form.description.trim();
      }
      if (form.household_id.trim()) {
        const householdIdNum = Number(form.household_id.trim());
        if (!Number.isNaN(householdIdNum)) {
          payload.household_id = householdIdNum;
        }
      }
      if (currentAdminName) {
        payload.created_by = currentAdminName;
      }

      await adminService.createUser(payload);
      showToast("Tạo người dùng thành công", "success");
      router.push("/admin/users");
    } catch (error: any) {
      const message =
        error?.response?.data?.error ||
        error?.message ||
        "Lỗi khi tạo người dùng";
      showToast(message, "error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <LoadingOverlay isLoading={loading} message="Đang tạo người dùng..." />
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
            onClick={() => router.push("/admin/users")}
            className="text-[#00897b] hover:underline"
          >
            Quản lý Người dùng
          </button>
          <span className="text-[#4b5563]">/</span>
          <span className="text-[#4b5563]">Tạo mới</span>
        </div>

        {/* Page Header */}
        <div className="mb-6">
          <div>
            <h1 className="text-[28px] font-bold italic text-[#1e3a8a] mb-2">
              Tạo người dùng mới
            </h1>
            <p className="text-sm font-normal italic text-[#4b5563] flex items-center gap-2">
              <span>
                Chỉ tạo Admin hoặc Owner. Không thể tạo Employee.
              </span>
            </p>
          </div>
        </div>

        {/* Form Card */}
        <form onSubmit={handleSubmit}>
          <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6 mb-6 max-w-3xl">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Role */}
              <div>
                <label className="block text-sm font-normal text-[#1e3a8a] mb-1.5">
                  Vai trò <span className="text-red-600">*</span>
                </label>
                <select
                  name="role_id"
                  value={form.role_id}
                  onChange={handleChange}
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#00897b] focus:border-transparent"
                >
                  <option value="">Chọn vai trò</option>
                  <option value={1}>Admin</option>
                  <option value={2}>Owner</option>
                </select>
              </div>

              {/* User name */}
              <div>
                <label className="block text-sm font-normal text-[#1e3a8a] mb-1.5">
                  Tên đăng nhập <span className="text-red-600">*</span>
                </label>
                <input
                  type="text"
                  name="user_name"
                  value={form.user_name}
                  onChange={handleChange}
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#00897b] focus:border-transparent"
                  placeholder="Nhập tên đăng nhập"
                />
              </div>

              {/* Email */}
              <div>
                <label className="block text-sm font-normal text-[#1e3a8a] mb-1.5">
                  Email
                </label>
                <input
                  type="email"
                  name="email"
                  value={form.email}
                  onChange={handleChange}
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#00897b] focus:border-transparent"
                  placeholder="Nhập email"
                />
              </div>

              {/* Password */}
              <div>
                <label className="block text-sm font-normal text-[#1e3a8a] mb-1.5">
                  Mật khẩu <span className="text-red-600">*</span>
                </label>
                <input
                  type="password"
                  name="password"
                  value={form.password}
                  onChange={handleChange}
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#00897b] focus:border-transparent"
                  placeholder="Nhập mật khẩu"
                />
                <p className="text-xs text-[#6b7280] mt-1">
                  Tối thiểu 8 ký tự, kết hợp chữ và số (tùy theo chính sách nội bộ).
                </p>
              </div>

              {/* Confirm password */}
              <div>
                <label className="block text-sm font-normal text-[#1e3a8a] mb-1.5">
                  Xác nhận mật khẩu <span className="text-red-600">*</span>
                </label>
                <input
                  type="password"
                  name="confirmPassword"
                  value={form.confirmPassword}
                  onChange={handleChange}
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#00897b] focus:border-transparent"
                  placeholder="Nhập lại mật khẩu"
                />
              </div>

              {/* Status */}
              <div>
                <label className="block text-sm font-normal text-[#1e3a8a] mb-1.5">
                  Trạng thái <span className="text-red-600">*</span>
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

              {/* Household ID */}
              <div>
                <label className="block text-sm font-normal text-[#1e3a8a] mb-1.5">
                  ID Hộ kinh doanh
                </label>
                <input
                  type="number"
                  name="household_id"
                  value={form.household_id}
                  onChange={handleChange}
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#00897b] focus:border-transparent"
                  placeholder="Nhập ID hộ kinh doanh (nếu có)"
                />
                <p className="text-xs text-[#6b7280] mt-1">Thường dùng cho Owner</p>
              </div>

              {/* Description */}
              <div className="md:col-span-2">
                <label className="block text-sm font-normal text-[#1e3a8a] mb-1.5">
                  Mô tả
                </label>
                <textarea
                  name="description"
                  value={form.description}
                  onChange={handleChange}
                  rows={3}
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#00897b] focus:border-transparent resize-none"
                  placeholder="Ghi chú thêm về tài khoản này (tùy chọn)"
                />
              </div>
            </div>

            {/* Created by (readonly) */}
            <div className="mt-6 space-y-2">
              <label className="block text-sm font-normal text-[#1e3a8a]">
                Người tạo
              </label>
              <div className="w-full px-3 py-2 border border-slate-200 rounded-lg bg-slate-50 text-sm text-[#4b5563]">
                Admin hiện tại: {currentAdminName || "-"}
              </div>
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex items-center justify-end gap-3 max-w-3xl">
            <button
              type="button"
              onClick={() => router.push("/admin/users")}
              className="px-4 py-2 bg-white border border-[#1e3a8a] text-[#1e3a8a] rounded-lg hover:bg-slate-50 transition-colors font-bold italic text-base"
            >
              Hủy
            </button>
            <button
              type="submit"
              disabled={loading}
              className="px-4 py-2 bg-[#00897b] text-white rounded-lg hover:bg-[#007a6c] transition-colors font-bold italic text-base disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? "Đang tạo..." : "Tạo người dùng"}
            </button>
          </div>
        </form>
      </div>
    </>
  );
}

