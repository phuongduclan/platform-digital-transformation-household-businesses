"use client";

import { useEffect, useState } from "react";
import LoadingOverlay from "@/components/ui/loading-overlay";
import { showToast } from "@/components/ui/toast";
import { getCurrentUser, updateProfile } from "@/services/auth.service";

export default function EmployeeSettingsPage() {
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [user, setUser] = useState<any>(null);
  const [formData, setFormData] = useState({
    email: "",
    description: "",
  });

  useEffect(() => {
    fetchUserProfile();
  }, []);

  const fetchUserProfile = async () => {
    try {
      setLoading(true);
      const userData = await getCurrentUser();
      setUser(userData);
      setFormData({
        email: userData.email || "",
        description: userData.description || "",
      });
    } catch (error: any) {
      const message =
        error?.response?.data?.error ||
        error?.message ||
        "Lỗi khi tải thông tin tài khoản";
      showToast(message, "error");
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      setSaving(true);
      await updateProfile({
        email: formData.email || undefined,
        description: formData.description || undefined,
      });
      showToast("Cập nhật thông tin thành công", "success");
      // Refresh user data
      await fetchUserProfile();
    } catch (error: any) {
      const message =
        error?.response?.data?.error ||
        error?.message ||
        "Cập nhật thông tin thất bại";
      showToast(message, "error");
    } finally {
      setSaving(false);
    }
  };

  return (
    <>
      <LoadingOverlay
        isLoading={loading}
        message="Đang tải thông tin tài khoản..."
      />
      <div className="p-8">
        <h1 className="text-[28px] font-bold italic text-[#1e3a8a] mb-6">
          Cài đặt tài khoản
        </h1>

        <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6 max-w-2xl">
          <form onSubmit={handleSubmit} className="space-y-6">
            {/* User Name (Read-only) */}
            <div>
              <label className="block text-sm font-normal text-[#1e3a8a] mb-1.5">
                Tên đăng nhập
              </label>
              <input
                type="text"
                value={user?.user_name || ""}
                disabled
                className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm bg-slate-50 text-slate-500 cursor-not-allowed"
              />
              <p className="text-xs text-slate-500 mt-1">
                Tên đăng nhập không thể thay đổi
              </p>
            </div>

            {/* Email (Editable) */}
            <div>
              <label className="block text-sm font-normal text-[#1e3a8a] mb-1.5">
                Email
              </label>
              <input
                type="email"
                value={formData.email}
                onChange={(e) =>
                  setFormData({ ...formData, email: e.target.value })
                }
                className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#00897b] focus:border-transparent"
                placeholder="Nhập email"
              />
            </div>

            {/* Description (Editable) */}
            <div>
              <label className="block text-sm font-normal text-[#1e3a8a] mb-1.5">
                Mô tả
              </label>
              <textarea
                value={formData.description}
                onChange={(e) =>
                  setFormData({ ...formData, description: e.target.value })
                }
                rows={4}
                className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#00897b] focus:border-transparent resize-none"
                placeholder="Nhập mô tả"
              />
            </div>

            {/* Status (Read-only) */}
            {user?.status && (
              <div>
                <label className="block text-sm font-normal text-[#1e3a8a] mb-1.5">
                  Trạng thái
                </label>
                <input
                  type="text"
                  value={user.status}
                  disabled
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm bg-slate-50 text-slate-500 cursor-not-allowed"
                />
                <p className="text-xs text-slate-500 mt-1">
                  Trạng thái không thể thay đổi
                </p>
              </div>
            )}

            {/* Submit Button */}
            <div className="flex items-center justify-end gap-3 pt-4 border-t border-slate-200">
              <button
                type="button"
                onClick={() => {
                  setFormData({
                    email: user?.email || "",
                    description: user?.description || "",
                  });
                }}
                className="px-5 py-2 text-sm font-medium text-[#4b5563] bg-white border border-slate-300 rounded-lg hover:bg-slate-50 transition-colors"
                disabled={saving}
              >
                Hủy
              </button>
              <button
                type="submit"
                disabled={saving}
                className="px-5 py-2 bg-[#00897b] text-white rounded-lg text-sm font-bold hover:bg-[#007a6c] transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {saving ? "Đang lưu..." : "Lưu thay đổi"}
              </button>
            </div>
          </form>
        </div>
      </div>
    </>
  );
}
