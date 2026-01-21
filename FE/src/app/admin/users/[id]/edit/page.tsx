"use client";

import { useEffect, useState } from "react";
import { useRouter, useParams } from "next/navigation";
import { adminService, User } from "@/services/admin.service";
import { showToast } from "@/components/ui/toast";
import LoadingOverlay from "@/components/ui/loading-overlay";
import Link from "next/link";

export default function EditUserPage() {
  const router = useRouter();
  const params = useParams();
  const userId = Number(params.id);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [user, setUser] = useState<User | null>(null);
  const [currentUserRole, setCurrentUserRole] = useState<number | null>(null);
  const [formData, setFormData] = useState({
    status: "Active",
  });

  useEffect(() => {
    if (userId) {
      fetchUserData();
    }
    // Get current user role
    if (typeof window !== "undefined") {
      const roleId = localStorage.getItem("role_id");
      if (roleId) {
        setCurrentUserRole(Number(roleId));
      }
    }
  }, [userId]);

  const fetchUserData = async () => {
    try {
      setLoading(true);
      const userData = await adminService.getUser(userId);
      setUser(userData);
      setFormData({
        status: userData.status || "Active",
      });
    } catch (error: any) {
      showToast(error.message || "Lỗi khi tải thông tin người dùng", "error");
      router.push("/admin/users");
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!formData.status) {
      showToast("Trạng thái không được để trống", "error");
      return;
    }

    try {
      setSaving(true);
      
      // Get current user info for updated_by
      const currentUserStr = localStorage.getItem("user_info");
      const currentUser = currentUserStr ? JSON.parse(currentUserStr) : null;
      
      // API này chỉ dùng để activate/deactivate Owner accounts
      // Chỉ gửi status field
      const updateData: any = {
        status: formData.status,
      };
      
      if (currentUser?.user_name) {
        updateData.updated_by = currentUser.user_name;
      }

      await adminService.updateUser(userId, updateData);
      showToast("Cập nhật trạng thái tài khoản thành công", "success");
      router.push(`/admin/users/${userId}`);
    } catch (error: any) {
      showToast(error.message || "Lỗi khi cập nhật trạng thái tài khoản", "error");
    } finally {
      setSaving(false);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value,
    }));
  };

  if (loading) {
    return <LoadingOverlay isLoading={true} message="Đang tải thông tin người dùng..." />;
  }

  if (!user) {
    return (
      <div className="p-8">
        <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6 text-center">
          <p className="text-[#4b5563]">Không tìm thấy người dùng</p>
          <Link href="/admin/users" className="text-[#00897b] hover:underline mt-4 inline-block">
            Quay lại danh sách
          </Link>
        </div>
      </div>
    );
  }

  return (
    <>
      <LoadingOverlay isLoading={saving} message="Đang cập nhật thông tin..." />
      <div className="p-8">
        {/* Page Header */}
          <div className="mb-6 flex items-center justify-between">
          <div>
            <h1 className="text-[28px] font-bold italic text-[#1e3a8a] mb-2">
              Cập nhật trạng thái tài khoản
            </h1>
            <div className="flex items-center gap-2">
              <Link href="/admin/users" className="text-[#00897b] hover:underline text-sm">
                Quản lý Người dùng
              </Link>
              <span className="text-[#4b5563]">/</span>
              <Link href={`/admin/users/${userId}`} className="text-[#00897b] hover:underline text-sm">
                Chi tiết
              </Link>
              <span className="text-[#4b5563]">/</span>
              <span className="text-sm text-[#4b5563]">Cập nhật trạng thái</span>
            </div>
          </div>
        </div>

        {/* Form Card */}
        <form onSubmit={handleSubmit}>
          <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6 mb-6">
            <h2 className="text-[20px] font-bold italic text-[#1e3a8a] mb-6">
              Cập nhật trạng thái tài khoản
            </h2>
            
            <div className="space-y-6">
              <div>
                <label className="block text-sm font-normal text-[#4b5563] mb-1.5">
                  ID
                </label>
                <p className="text-base font-normal text-[#1e3a8a] bg-slate-50 px-3 py-2 rounded border border-slate-200">
                  {user.id}
                </p>
              </div>

              <div>
                <label className="block text-sm font-normal text-[#4b5563] mb-1.5">
                  Tên đăng nhập
                </label>
                <p className="text-base font-normal text-[#1e3a8a] bg-slate-50 px-3 py-2 rounded border border-slate-200">
                  {user.user_name}
                </p>
              </div>

              <div>
                <label className="block text-sm font-normal text-[#4b5563] mb-1.5">
                  Vai trò
                </label>
                <p className="text-base font-normal text-[#1e3a8a] bg-slate-50 px-3 py-2 rounded border border-slate-200">
                  {user.role_id === 1 ? "Admin" : user.role_id === 2 ? "Owner" : "Employee"}
                </p>
              </div>

              {/* Chỉ hiển thị status field nếu user đang edit là Owner (role_id = 2) */}
              {user && user.role_id === 2 && (
                <div>
                  <label htmlFor="status" className="block text-sm font-normal text-[#4b5563] mb-1.5">
                    Trạng thái <span className="text-red-500">*</span>
                  </label>
                  <select
                    id="status"
                    name="status"
                    value={formData.status}
                    onChange={handleChange}
                    required
                    className="w-full px-3 py-2 border border-slate-300 rounded-lg text-base focus:outline-none focus:ring-2 focus:ring-[#00897b] focus:border-transparent"
                  >
                    <option value="Active">Active</option>
                    <option value="Inactive">Inactive</option>
                  </select>
                  <p className="text-xs text-[#6b7280] mt-1">Admin có thể activate/deactivate Owner accounts</p>
                </div>
              )}

              {user && user.role_id === 1 && (
                <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
                  <p className="text-sm text-yellow-800">
                    Không thể thay đổi trạng thái của tài khoản Admin. Chỉ có thể activate/deactivate Owner accounts.
                  </p>
                </div>
              )}
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex items-center justify-end gap-3">
            <Link
              href={`/admin/users/${userId}`}
              className="px-4 py-2 bg-white border border-[#1e3a8a] text-[#1e3a8a] rounded-lg hover:bg-slate-50 transition-colors font-bold italic text-base"
            >
              Hủy
            </Link>
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
