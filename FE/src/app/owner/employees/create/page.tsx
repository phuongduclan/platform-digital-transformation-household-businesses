"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import LoadingOverlay from "@/components/ui/loading-overlay";
import { showToast } from "@/components/ui/toast";
import { ownerService } from "@/services/owner.service";

type StatusType = "Active" | "Inactive";

interface CreateEmployeeFormState {
  user_name: string;
  email: string;
  password: string;
  confirmPassword: string;
  description: string;
  status: StatusType;
}

export default function OwnerCreateEmployeePage() {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [currentOwnerName, setCurrentOwnerName] = useState<string | null>(null);
  const [form, setForm] = useState<CreateEmployeeFormState>({
    user_name: "",
    email: "",
    password: "",
    confirmPassword: "",
    description: "",
    status: "Active",
  });

  useEffect(() => {
    if (typeof window !== "undefined") {
      const userStr = localStorage.getItem("user_info");
      if (userStr) {
        try {
          const user = JSON.parse(userStr);
          if (user?.user_name) {
            setCurrentOwnerName(user.user_name);
          }
        } catch {
          // ignore
        }
      }
    }
  }, []);

  const handleChange = (
    e: React.ChangeEvent<
      HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement
    >
  ) => {
    const { name, value } = e.target;
    setForm((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

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

      await ownerService.createEmployee({
        user_name: form.user_name.trim(),
        password: form.password,
        email: form.email.trim() || undefined,
        description: form.description.trim() || undefined,
        status: form.status,
      });

      showToast("Tạo nhân viên thành công", "success");
      router.push("/owner/employees");
    } catch (error: any) {
      const message =
        error?.response?.data?.error ||
        error?.message ||
        "Lỗi khi tạo nhân viên";
      showToast(message, "error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <LoadingOverlay
        isLoading={loading}
        message="Đang tạo nhân viên..."
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
            onClick={() => router.push("/owner/employees")}
            className="text-[#00897b] hover:underline"
          >
            Quản lý Nhân viên
          </button>
          <span className="text-[#4b5563]">/</span>
          <span className="text-[#4b5563]">Tạo mới</span>
        </div>

        {/* Page Header */}
        <div className="mb-6">
          <h1 className="text-[28px] font-bold italic text-[#1e3a8a] mb-2">
            Tạo nhân viên mới
          </h1>
          <p className="text-sm font-normal italic text-[#4b5563]">
            Nhân viên sẽ có vai trò mặc định là Employee, thuộc hộ kinh doanh
            hiện tại.
          </p>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit}>
          <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6 mb-6 max-w-3xl">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
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
                  placeholder="Nhập email (nếu có)"
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
              </div>

              {/* Confirm Password */}
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

              {/* Description */}
              <div className="md:col-span-2">
                <label className="block text-sm font-normal text-[#1e3a8a] mb-1.5">
                  Họ tên / Mô tả
                </label>
                <textarea
                  name="description"
                  value={form.description}
                  onChange={handleChange}
                  rows={3}
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#00897b] focus:border-transparent"
                  placeholder="Nhập họ tên hoặc mô tả ngắn về nhân viên"
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

              {/* Role display */}
              <div>
                <label className="block text-sm font-normal text-[#1e3a8a] mb-1.5">
                  Vai trò
                </label>
                <p className="text-sm font-bold italic text-[#1e3a8a] mt-2">
                  Employee (mặc định)
                </p>
              </div>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <button
              type="submit"
              disabled={loading}
              className="px-6 py-2.5 bg-[#00897b] text-white rounded-lg text-sm font-bold hover:bg-[#007a6c] transition-colors disabled:bg-slate-400 disabled:cursor-not-allowed"
            >
              {loading ? "Đang lưu..." : "Lưu nhân viên"}
            </button>
            <button
              type="button"
              onClick={() => router.push("/owner/employees")}
              className="px-6 py-2.5 bg-white border border-slate-300 text-sm rounded-lg hover:bg-slate-50 transition-colors"
            >
              Hủy
            </button>
          </div>
        </form>
      </div>
    </>
  );
}

