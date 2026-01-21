"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import LoadingOverlay from "@/components/ui/loading-overlay";
import { showToast } from "@/components/ui/toast";
import { ownerService, OwnerEmployee } from "@/services/owner.service";

type StatusType = "Active" | "Inactive";

export default function OwnerEmployeeDetailPage() {
  const params = useParams();
  const router = useRouter();
  const idParam = params?.id;
  const employeeId =
    typeof idParam === "string" ? parseInt(idParam, 10) : NaN;

  const [employee, setEmployee] = useState<OwnerEmployee | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [form, setForm] = useState<{
    user_name: string;
    email: string;
    description: string;
    status: StatusType;
    password: string;
    confirmPassword: string;
  }>({
    user_name: "",
    email: "",
    description: "",
    status: "Active",
    password: "",
    confirmPassword: "",
  });

  useEffect(() => {
    if (!Number.isNaN(employeeId)) {
      fetchEmployee();
    } else {
      setLoading(false);
      showToast("ID nhân viên không hợp lệ", "error");
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [employeeId]);

  const fetchEmployee = async () => {
    try {
      setLoading(true);
      const data = await ownerService.getEmployee(employeeId);
      setEmployee(data);
      setForm({
        user_name: data.user_name,
        email: data.email || "",
        description: data.description || "",
        status: (data.status as StatusType) || "Active",
        password: "",
        confirmPassword: "",
      });
    } catch (error: any) {
      const message =
        error?.response?.data?.error ||
        error?.message ||
        "Lỗi khi tải thông tin nhân viên";
      showToast(message, "error");
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
    setForm((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!employee) return;

    if (!form.user_name.trim()) {
      showToast("Tên đăng nhập không được để trống", "error");
      return;
    }

    if (form.password || form.confirmPassword) {
      if (!form.password) {
        showToast("Vui lòng nhập mật khẩu mới", "error");
        return;
      }
      if (form.password !== form.confirmPassword) {
        showToast("Mật khẩu xác nhận không khớp", "error");
        return;
      }
    }

    const payload: any = {
      user_name: form.user_name.trim(),
      email: form.email.trim() || null,
      description: form.description.trim() || null,
      status: form.status,
    };

    if (form.password) {
      payload.password = form.password;
    }

    try {
      setSaving(true);
      const updated = await ownerService.updateEmployee(employee.id, payload);
      setEmployee(updated);
      showToast("Cập nhật nhân viên thành công", "success");
      // Cập nhật form lại theo dữ liệu mới (trừ password)
      setForm((prev) => ({
        ...prev,
        user_name: updated.user_name,
        email: updated.email || "",
        description: updated.description || "",
        status: (updated.status as StatusType) || "Active",
        password: "",
        confirmPassword: "",
      }));
    } catch (error: any) {
      const message =
        error?.response?.data?.error ||
        error?.message ||
        "Lỗi khi cập nhật nhân viên";
      showToast(message, "error");
    } finally {
      setSaving(false);
    }
  };

  const formatDate = (dateString: string) => {
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
        message="Đang tải thông tin nhân viên..."
      />
    );
  }

  if (!employee) {
    return (
      <div className="p-8">
        <p className="text-sm text-red-600">Không tìm thấy nhân viên.</p>
      </div>
    );
  }

  return (
    <>
      <LoadingOverlay isLoading={saving} message="Đang lưu thay đổi..." />
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
          <span className="text-[#4b5563]">Chi tiết</span>
        </div>

        {/* Header */}
        <div className="mb-6 flex items-center justify-between">
          <div>
            <h1 className="text-[28px] font-bold italic text-[#1e3a8a] mb-2">
              Chi tiết Nhân viên
            </h1>
            <p className="text-sm text-[#4b5563]">
              Quản lý thông tin và trạng thái nhân viên thuộc hộ kinh doanh.
            </p>
          </div>
        </div>

        {/* Detail + Edit form */}
        <form onSubmit={handleSubmit}>
          <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6 mb-6">
            <h2 className="text-[20px] font-bold italic text-[#1e3a8a] mb-6">
              Thông tin cơ bản
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* ID */}
              <div>
                <label className="block text-sm font-normal text-[#4b5563] mb-1">
                  ID
                </label>
                <p className="text-base font-normal text-[#1e3a8a]">
                  {employee.id}
                </p>
              </div>

              {/* Username */}
              <div>
                <label className="block text-sm font-normal text-[#4b5563] mb-1">
                  Tên đăng nhập
                </label>
                <input
                  type="text"
                  name="user_name"
                  value={form.user_name}
                  onChange={handleChange}
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#00897b] focus:border-transparent"
                />
              </div>

              {/* Email */}
              <div>
                <label className="block text-sm font-normal text-[#4b5563] mb-1">
                  Email
                </label>
                <input
                  type="email"
                  name="email"
                  value={form.email}
                  onChange={handleChange}
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#00897b] focus:border-transparent"
                />
              </div>

              {/* Status */}
              <div>
                <label className="block text-sm font-normal text-[#4b5563] mb-1">
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

              {/* Description */}
              <div className="md:col-span-2">
                <label className="block text-sm font-normal text-[#4b5563] mb-1">
                  Họ tên / Mô tả
                </label>
                <textarea
                  name="description"
                  value={form.description}
                  onChange={handleChange}
                  rows={3}
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#00897b] focus:border-transparent"
                />
              </div>

              {/* New password */}
              <div>
                <label className="block text-sm font-normal text-[#4b5563] mb-1">
                  Mật khẩu mới
                </label>
                <input
                  type="password"
                  name="password"
                  value={form.password}
                  onChange={handleChange}
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#00897b] focus:border-transparent"
                  placeholder="Để trống nếu không đổi mật khẩu"
                />
              </div>
              <div>
                <label className="block text-sm font-normal text-[#4b5563] mb-1">
                  Xác nhận mật khẩu mới
                </label>
                <input
                  type="password"
                  name="confirmPassword"
                  value={form.confirmPassword}
                  onChange={handleChange}
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#00897b] focus:border-transparent"
                />
              </div>

              {/* Role (readonly) */}
              <div>
                <label className="block text-sm font-normal text-[#4b5563] mb-1">
                  Vai trò
                </label>
                <p className="text-sm font-bold italic text-[#1e3a8a] mt-2">
                  Employee
                </p>
              </div>

              {/* Household id */}
              <div>
                <label className="block text-sm font-normal text-[#4b5563] mb-1">
                  Hộ kinh doanh
                </label>
                <p className="text-base font-normal text-[#1e3a8a]">
                  ID: {employee.household_id ?? "-"}
                </p>
              </div>

              {/* Dates */}
              <div>
                <label className="block text-sm font-normal text-[#4b5563] mb-1">
                  Ngày tạo
                </label>
                <p className="text-base font-normal text-[#1e3a8a]">
                  {formatDate(employee.created_at)}
                </p>
              </div>
              <div>
                <label className="block text-sm font-normal text-[#4b5563] mb-1">
                  Ngày cập nhật
                </label>
                <p className="text-base font-normal text-[#1e3a8a]">
                  {formatDate(employee.updated_at)}
                </p>
              </div>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <button
              type="submit"
              disabled={saving}
              className="px-6 py-2.5 bg-[#00897b] text-white rounded-lg text-sm font-bold hover:bg-[#007a6c] transition-colors disabled:bg-slate-400 disabled:cursor-not-allowed"
            >
              {saving ? "Đang lưu..." : "Lưu thay đổi"}
            </button>
            <button
              type="button"
              onClick={() => router.push("/owner/employees")}
              className="px-6 py-2.5 bg-white border border-slate-300 text-sm rounded-lg hover:bg-slate-50 transition-colors"
            >
              Quay lại
            </button>
          </div>
        </form>
      </div>
    </>
  );
}

