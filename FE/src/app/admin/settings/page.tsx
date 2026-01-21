"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { showToast } from "@/components/ui/toast";
import LoadingOverlay from "@/components/ui/loading-overlay";
import { getCurrentUser, updateProfile } from "@/services/auth.service";

export default function AdminSettingsPage() {
  const router = useRouter();
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [user, setUser] = useState<any>(null);
  const [isEditingProfile, setIsEditingProfile] = useState(false);
  
  // Profile form state
  const [profileForm, setProfileForm] = useState({
    user_name: "",
    email: "",
    description: "",
  });
  
  // Password form state
  const [currentPassword, setCurrentPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [showCurrentPassword, setShowCurrentPassword] = useState(false);
  const [showNewPassword, setShowNewPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);

  useEffect(() => {
    fetchUserData();
  }, []);

  const fetchUserData = async () => {
    try {
      setLoading(true);
      const userData = await getCurrentUser();
      setUser(userData);
      setProfileForm({
        user_name: userData.user_name || "",
        email: userData.email || "",
        description: userData.description || "",
      });
    } catch (error: any) {
      showToast(error.message || "Lỗi khi tải thông tin người dùng", "error");
    } finally {
      setLoading(false);
    }
  };

  const getInitials = (name: string) => {
    if (!name) return "AN";
    const parts = name.split(" ");
    if (parts.length >= 2) {
      return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
    }
    return name.substring(0, 2).toUpperCase();
  };

  const handleUpdatePassword = async () => {
    if (!currentPassword || !newPassword || !confirmPassword) {
      showToast("Vui lòng điền đầy đủ thông tin", "error");
      return;
    }

    if (newPassword !== confirmPassword) {
      showToast("Mật khẩu mới và xác nhận mật khẩu không khớp", "error");
      return;
    }

    if (newPassword.length < 8) {
      showToast("Mật khẩu mới phải có ít nhất 8 ký tự", "error");
      return;
    }

    try {
      setLoading(true);
      // TODO: Implement actual API call
      // PUT /api/admin/users/change-password
      await new Promise((resolve) => setTimeout(resolve, 1000));
      showToast("Cập nhật mật khẩu thành công", "success");
      setCurrentPassword("");
      setNewPassword("");
      setConfirmPassword("");
    } catch (error: any) {
      showToast(error.message || "Lỗi khi cập nhật mật khẩu", "error");
    } finally {
      setLoading(false);
    }
  };

  const handleEditProfile = () => {
    setIsEditingProfile(true);
  };

  const handleCancelEdit = () => {
    setIsEditingProfile(false);
    // Reset form to original values
    if (user) {
      setProfileForm({
        user_name: user.user_name || "",
        email: user.email || "",
        description: user.description || "",
      });
    }
  };

  const handleSaveProfile = async () => {
    if (!profileForm.user_name.trim()) {
      showToast("Tên đăng nhập không được để trống", "error");
      return;
    }

    try {
      setSaving(true);
      await updateProfile({
        user_name: profileForm.user_name.trim(),
        email: profileForm.email.trim() || undefined,
        description: profileForm.description.trim() || undefined,
      });
      showToast("Cập nhật thông tin cá nhân thành công", "success");
      setIsEditingProfile(false);
      await fetchUserData(); // Refresh user data
    } catch (error: any) {
      showToast(error.message || "Lỗi khi cập nhật thông tin cá nhân", "error");
    } finally {
      setSaving(false);
    }
  };

  if (!user) {
    return <LoadingOverlay isLoading={true} message="Đang tải thông tin..." />;
  }

  return (
    <>
      <LoadingOverlay isLoading={loading || saving} message={loading ? "Đang tải thông tin..." : "Đang xử lý..."} />
      <div className="p-8">
        {/* Page Header */}
        <div className="mb-8">
          <h1 className="text-[28px] font-bold italic text-[#1e3a8a]">
            Cài đặt người dùng
          </h1>
        </div>

        <div className="space-y-6 max-w-4xl">
          {/* Personal Information Section */}
          <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6">
            <h2 className="text-[20px] font-bold italic text-[#1e3a8a] mb-6">
              Thông tin cá nhân
            </h2>
            
            {!isEditingProfile ? (
              <>
                <div className="flex items-start gap-6 mb-6">
                  {/* Avatar */}
                  <div className="w-20 h-20 bg-[#e0f2f1] rounded-full flex items-center justify-center flex-shrink-0">
                    <p className="text-[32px] font-bold italic text-[#00897b]">
                      {getInitials(user.user_name)}
                    </p>
                  </div>

                  {/* User Info */}
                  <div className="flex-1">
                    <p className="text-[18px] font-bold italic text-[#1e3a8a] mb-2">
                      {user.user_name}
                    </p>
                    <p className="text-sm font-normal text-[#4b5563] mb-3">
                      {user.email || "-"}
                    </p>
                    <div className="flex items-center gap-4">
                      <div className="inline-flex items-center px-3 py-1 bg-[#e0f2f1] rounded-lg">
                        <p className="text-xs font-bold italic text-[#00897b]">
                          Admin
                        </p>
                      </div>
                      <p className="text-xs font-normal text-[#9ca3af]">
                        ID: {user.id}
                      </p>
                    </div>
                    {user.description && (
                      <p className="text-sm font-normal text-[#4b5563] mt-3">
                        {user.description}
                      </p>
                    )}
                  </div>
                </div>

                {/* Edit Button */}
                <button
                  onClick={handleEditProfile}
                  className="px-4 py-2 border border-[#1e3a8a] text-[#1e3a8a] rounded-lg hover:bg-slate-50 transition-colors font-bold italic text-base"
                >
                  Chỉnh sửa thông tin
                </button>
              </>
            ) : (
              <div className="space-y-6">
                <div>
                  <label className="block text-base font-normal text-[#1e3a8a] mb-2">
                    Tên đăng nhập <span className="text-red-600">*</span>
                  </label>
                  <input
                    type="text"
                    value={profileForm.user_name}
                    onChange={(e) => setProfileForm({ ...profileForm, user_name: e.target.value })}
                    className="w-full px-4 py-3 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#00897b] focus:border-transparent"
                    placeholder="Nhập tên đăng nhập"
                  />
                </div>

                <div>
                  <label className="block text-base font-normal text-[#1e3a8a] mb-2">
                    Email
                  </label>
                  <input
                    type="email"
                    value={profileForm.email}
                    onChange={(e) => setProfileForm({ ...profileForm, email: e.target.value })}
                    className="w-full px-4 py-3 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#00897b] focus:border-transparent"
                    placeholder="Nhập email"
                  />
                </div>

                <div>
                  <label className="block text-base font-normal text-[#1e3a8a] mb-2">
                    Mô tả
                  </label>
                  <textarea
                    value={profileForm.description}
                    onChange={(e) => setProfileForm({ ...profileForm, description: e.target.value })}
                    rows={3}
                    className="w-full px-4 py-3 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#00897b] focus:border-transparent resize-none"
                    placeholder="Nhập mô tả"
                  />
                </div>

                <div className="flex items-center gap-3">
                  <button
                    onClick={handleSaveProfile}
                    disabled={saving}
                    className="px-6 py-3 bg-[#00897b] text-white rounded-lg hover:bg-[#007a6c] transition-colors font-bold italic text-base disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {saving ? "Đang lưu..." : "Lưu thay đổi"}
                  </button>
                  <button
                    onClick={handleCancelEdit}
                    disabled={saving}
                    className="px-6 py-3 bg-white border border-[#1e3a8a] text-[#1e3a8a] rounded-lg hover:bg-slate-50 transition-colors font-bold italic text-base disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    Hủy
                  </button>
                </div>
              </div>
            )}
          </div>

          {/* Change Password Section */}
          <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6">
            <h2 className="text-[20px] font-bold italic text-[#1e3a8a] mb-6">
              Đổi mật khẩu
            </h2>

            <div className="space-y-6">
              {/* Current Password */}
              <div>
                <label className="block text-base font-normal text-[#1e3a8a] mb-2">
                  Mật khẩu hiện tại <span className="text-red-600">*</span>
                </label>
                <div className="relative">
                  <input
                    type={showCurrentPassword ? "text" : "password"}
                    value={currentPassword}
                    onChange={(e) => setCurrentPassword(e.target.value)}
                    className="w-full px-4 py-3 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#00897b] focus:border-transparent pr-12"
                    placeholder="Nhập mật khẩu hiện tại"
                  />
                  <button
                    type="button"
                    onClick={() => setShowCurrentPassword(!showCurrentPassword)}
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-[#4b5563] hover:text-[#1e3a8a]"
                  >
                    {showCurrentPassword ? (
                      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.736m0 0L21 21" />
                      </svg>
                    ) : (
                      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                      </svg>
                    )}
                  </button>
                </div>
              </div>

              {/* New Password */}
              <div>
                <label className="block text-base font-normal text-[#1e3a8a] mb-2">
                  Mật khẩu mới <span className="text-red-600">*</span>
                </label>
                <div className="relative">
                  <input
                    type={showNewPassword ? "text" : "password"}
                    value={newPassword}
                    onChange={(e) => setNewPassword(e.target.value)}
                    className="w-full px-4 py-3 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#00897b] focus:border-transparent pr-12"
                    placeholder="Nhập mật khẩu mới"
                  />
                  <button
                    type="button"
                    onClick={() => setShowNewPassword(!showNewPassword)}
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-[#4b5563] hover:text-[#1e3a8a]"
                  >
                    {showNewPassword ? (
                      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.736m0 0L21 21" />
                      </svg>
                    ) : (
                      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                      </svg>
                    )}
                  </button>
                </div>
                <p className="text-sm font-normal text-[#4b5563] mt-2">
                  Tối thiểu 8 ký tự, kết hợp chữ và số
                </p>
              </div>

              {/* Confirm Password */}
              <div>
                <label className="block text-base font-normal text-[#1e3a8a] mb-2">
                  Xác nhận mật khẩu mới <span className="text-red-600">*</span>
                </label>
                <div className="relative">
                  <input
                    type={showConfirmPassword ? "text" : "password"}
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                    className="w-full px-4 py-3 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#00897b] focus:border-transparent pr-12"
                    placeholder="Nhập lại mật khẩu mới"
                  />
                  <button
                    type="button"
                    onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-[#4b5563] hover:text-[#1e3a8a]"
                  >
                    {showConfirmPassword ? (
                      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.736m0 0L21 21" />
                      </svg>
                    ) : (
                      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                      </svg>
                    )}
                  </button>
                </div>
              </div>

              {/* Update Button */}
              <button
                onClick={handleUpdatePassword}
                className="px-6 py-3 bg-[#00897b] text-white rounded-lg hover:bg-[#007a6c] transition-colors font-bold italic text-base"
              >
                Cập nhật mật khẩu
              </button>
            </div>
          </div>

          {/* Footer */}
          <div className="text-center pt-4">
            <p className="text-xs font-normal text-[#9ca3af]">
              Phiên bản BizFlow Admin v1.0
            </p>
          </div>
        </div>
      </div>
    </>
  );
}
