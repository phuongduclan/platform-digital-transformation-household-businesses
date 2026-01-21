"use client";

import { useEffect, useState } from "react";
import { useRouter, useParams } from "next/navigation";
import { adminService, User } from "@/services/admin.service";
import { showToast } from "@/components/ui/toast";
import LoadingOverlay from "@/components/ui/loading-overlay";
import Link from "next/link";

interface Household {
  id: number;
  name: string;
}

export default function UserDetailPage() {
  const router = useRouter();
  const params = useParams();
  const userId = Number(params.id);
  const [user, setUser] = useState<User | null>(null);
  const [household, setHousehold] = useState<Household | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (userId) {
      fetchUserData();
    }
  }, [userId]);

  const fetchUserData = async () => {
    try {
      setLoading(true);
      const userData = await adminService.getUser(userId);
      setUser(userData);
      
      // REMOVED: Admin không có quyền xem household details
      // Chỉ lưu household_id để hiển thị
      if (userData.household_id) {
        setHousehold({
          id: userData.household_id,
          name: `ID: ${userData.household_id}` // Chỉ hiển thị ID
        });
      }
    } catch (error: any) {
      showToast(error.message || "Lỗi khi tải thông tin người dùng", "error");
      router.push("/admin/users");
    } finally {
      setLoading(false);
    }
  };

  const getRoleName = (roleId: number) => {
    switch (roleId) {
      case 1: return "Admin";
      case 2: return "Owner";
      case 3: return "Employee";
      default: return "Unknown";
    }
  };

  const getRoleBadge = (roleId: number) => {
    const roleName = getRoleName(roleId);
    const isAdmin = roleId === 1;
    return (
      <span className={`px-3 py-1 text-sm font-bold italic rounded text-white ${
        isAdmin ? "bg-[#10b981]" : "bg-[#3b82f6]"
      }`}>
        {roleName}
      </span>
    );
  };

  const getStatusBadge = (status: string) => {
    const isActive = status === "Active";
    return (
      <span className={`px-3 py-1 text-sm font-bold italic rounded text-white ${
        isActive ? "bg-[#10b981]" : "bg-[#6b7280]"
      }`}>
        {status}
      </span>
    );
  };

  const formatDate = (dateString: string) => {
    if (!dateString) return "-";
    const date = new Date(dateString);
    return date.toLocaleDateString("vi-VN", {
      day: "2-digit",
      month: "2-digit",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  };

  const handleToggleStatus = async (newStatus: string) => {
    if (!user) return;
    
    try {
      const currentUserStr = localStorage.getItem("user_info");
      const currentUser = currentUserStr ? JSON.parse(currentUserStr) : null;
      
      const updateData: any = {
        status: newStatus,
      };
      
      if (currentUser?.user_name) {
        updateData.updated_by = currentUser.user_name;
      }

      await adminService.updateUser(userId, updateData);
      showToast(`Đã ${newStatus === "Active" ? "kích hoạt" : "vô hiệu hóa"} tài khoản thành công`, "success");
      fetchUserData(); // Refresh user data
    } catch (error: any) {
      showToast(error.message || "Lỗi khi cập nhật trạng thái tài khoản", "error");
    }
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
    <div className="p-8">
      {/* Page Header */}
      <div className="mb-6 flex items-center justify-between">
        <div>
          <h1 className="text-[28px] font-bold italic text-[#1e3a8a] mb-2">
            Chi tiết Người dùng
          </h1>
          <div className="flex items-center gap-2">
            <Link href="/admin/users" className="text-[#00897b] hover:underline text-sm">
              Quản lý Người dùng
            </Link>
            <span className="text-[#4b5563]">/</span>
            <span className="text-sm text-[#4b5563]">Chi tiết</span>
          </div>
        </div>
        <div className="flex items-center gap-3">
          {/* Chỉ hiển thị Active/Deactivate cho Owner (role_id = 2) */}
          {user.role_id === 2 && (
            <button
              onClick={() => handleToggleStatus(user.status === "Active" ? "Inactive" : "Active")}
              className={`px-4 py-2 rounded-lg hover:opacity-90 transition-colors font-bold italic text-base ${
                user.status === "Active"
                  ? "bg-red-600 text-white hover:bg-red-700"
                  : "bg-[#10b981] text-white hover:bg-[#059669]"
              }`}
            >
              {user.status === "Active" ? "Deactivate" : "Active"}
            </button>
          )}
        </div>
      </div>

      {/* User Info Card */}
      <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6 mb-6">
        <h2 className="text-[20px] font-bold italic text-[#1e3a8a] mb-6">
          Thông tin cơ bản
        </h2>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-normal text-[#4b5563] mb-1">
              ID
            </label>
            <p className="text-base font-normal text-[#1e3a8a]">{user.id}</p>
          </div>

          <div>
            <label className="block text-sm font-normal text-[#4b5563] mb-1">
              Tên đăng nhập
            </label>
            <p className="text-base font-normal text-[#1e3a8a]">{user.user_name}</p>
          </div>

          <div>
            <label className="block text-sm font-normal text-[#4b5563] mb-1">
              Email
            </label>
            <p className="text-base font-normal text-[#1e3a8a]">{user.email || "-"}</p>
          </div>

          <div>
            <label className="block text-sm font-normal text-[#4b5563] mb-1">
              Vai trò
            </label>
            <div className="mt-1">
              {getRoleBadge(user.role_id)}
            </div>
          </div>

          <div>
            <label className="block text-sm font-normal text-[#4b5563] mb-1">
              Trạng thái
            </label>
            <div className="mt-1">
              {getStatusBadge(user.status)}
            </div>
          </div>

          <div>
            <label className="block text-sm font-normal text-[#4b5563] mb-1">
              Hộ kinh doanh
            </label>
            {household ? (
              <p className="text-base font-normal text-[#1e3a8a]">{household.name}</p>
            ) : user.household_id ? (
              <p className="text-base font-normal text-[#1e3a8a]">ID: {user.household_id}</p>
            ) : (
              <p className="text-base font-normal text-[#1e3a8a]">-</p>
            )}
          </div>

          {user.description && (
            <div className="md:col-span-2">
              <label className="block text-sm font-normal text-[#4b5563] mb-1">
                Mô tả
              </label>
              <p className="text-base font-normal text-[#1e3a8a]">{user.description}</p>
            </div>
          )}

          <div>
            <label className="block text-sm font-normal text-[#4b5563] mb-1">
              Ngày tạo
            </label>
            <p className="text-base font-normal text-[#1e3a8a]">{formatDate(user.created_at)}</p>
          </div>

          <div>
            <label className="block text-sm font-normal text-[#4b5563] mb-1">
              Ngày cập nhật
            </label>
            <p className="text-base font-normal text-[#1e3a8a]">{formatDate(user.updated_at)}</p>
          </div>

          {user.created_by && (
            <div>
              <label className="block text-sm font-normal text-[#4b5563] mb-1">
                Tạo bởi
              </label>
              <p className="text-base font-normal text-[#1e3a8a]">{user.created_by}</p>
            </div>
          )}

          {user.updated_by && (
            <div>
              <label className="block text-sm font-normal text-[#4b5563] mb-1">
                Cập nhật bởi
              </label>
              <p className="text-base font-normal text-[#1e3a8a]">{user.updated_by}</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
