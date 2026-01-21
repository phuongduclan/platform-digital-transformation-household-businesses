"use client";

import { useEffect, useState } from "react";
import { adminService, User, UserListParams } from "@/services/admin.service";
import { showToast } from "@/components/ui/toast";
import LoadingOverlay from "@/components/ui/loading-overlay";
import Link from "next/link";

interface Household {
  id: number;
  name: string;
}

export default function AdminUsersPage() {
  const [users, setUsers] = useState<User[]>([]);
  const [households, setHouseholds] = useState<Household[]>([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState<UserListParams>({});
  const [searchTerm, setSearchTerm] = useState("");
  const [currentPage, setCurrentPage] = useState(1);
  const [totalUsers, setTotalUsers] = useState(0);
  const itemsPerPage = 5;

  useEffect(() => {
    fetchHouseholds();
  }, []);

  useEffect(() => {
    // Chỉ fetch khi filters hoặc currentPage thay đổi (không fetch khi searchTerm thay đổi)
    // Search chỉ fetch khi user bấm nút "Tìm kiếm"
    fetchUsers();
  }, [filters, currentPage]);

  const handleSearch = () => {
    // Reset về trang 1 khi search
    if (currentPage !== 1) {
      setCurrentPage(1);
    } else {
      // Fetch với search term
      fetchUsers();
    }
  };

  const fetchHouseholds = async () => {
    // REMOVED: Admin không có quyền quản lý Household
    // Không fetch households vì không có API Admin cho households
    setHouseholds([]);
  };

  const fetchUsers = async () => {
    try {
      setLoading(true);
      const params = { ...filters };
      if (searchTerm) params.search = searchTerm;
      const data = await adminService.listUsers(params);
      setUsers(data);
      setTotalUsers(data.length);
    } catch (error: any) {
      showToast(error.message || "Lỗi khi tải danh sách người dùng", "error");
    } finally {
      setLoading(false);
    }
  };

  const handleToggleStatus = async (userId: number, newStatus: string) => {
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
      fetchUsers(); // Refresh list
    } catch (error: any) {
      showToast(error.message || "Lỗi khi cập nhật trạng thái tài khoản", "error");
    }
  };

  const handleRefresh = () => {
    setSearchTerm("");
    setFilters({});
    setCurrentPage(1);
    fetchUsers();
  };

  const handleFilterChange = (key: keyof UserListParams, value: any) => {
    setFilters(prev => ({ ...prev, [key]: value || undefined }));
    setCurrentPage(1);
  };

  const handleDelete = async (id: number) => {
    if (!confirm("Bạn có chắc chắn muốn xóa người dùng này?")) return;
    try {
      await adminService.deleteUser(id);
      showToast("Xóa người dùng thành công", "success");
      fetchUsers();
    } catch (error: any) {
      showToast(error.message || "Lỗi khi xóa người dùng", "error");
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
      <span className={`px-2 py-1 text-xs font-bold italic rounded text-white ${
        isAdmin ? "bg-[#10b981]" : "bg-[#3b82f6]"
      }`}>
        {roleName}
      </span>
    );
  };

  const getStatusBadge = (status: string) => {
    const isActive = status === "Active";
    return (
      <span className={`px-2 py-1 text-xs font-bold italic rounded text-white ${
        isActive ? "bg-[#10b981]" : "bg-[#6b7280]"
      }`}>
        {status}
      </span>
    );
  };

  const getHouseholdName = (householdId: number | null) => {
    // Chỉ hiển thị household_id vì Admin không có quyền xem household details
    if (!householdId) return "-";
    return `ID: ${householdId}`;
  };

  const formatDate = (dateString: string) => {
    if (!dateString) return "-";
    const date = new Date(dateString);
    return date.toLocaleDateString("vi-VN", { day: "2-digit", month: "2-digit", year: "numeric" });
  };

  // Pagination
  const totalPages = Math.ceil(totalUsers / itemsPerPage);
  const startIndex = (currentPage - 1) * itemsPerPage;
  const endIndex = startIndex + itemsPerPage;
  const paginatedUsers = users.slice(startIndex, endIndex);

  return (
    <>
      <LoadingOverlay isLoading={loading} message="Đang tải danh sách người dùng..." />
      
      <div className="p-8">
        {/* Page Header */}
        <div className="mb-6 flex items-center justify-between">
          <h1 className="text-[28px] font-bold italic text-[#1e3a8a]">
            Quản lý Người dùng
          </h1>
          <Link
            href="/admin/users/create"
            className="px-4 py-2 bg-[#00897b] text-white rounded-lg hover:bg-[#007a6c] transition-colors font-bold italic text-base flex items-center gap-2"
          >
            <span>+</span>
            <span>Tạo người dùng mới</span>
          </Link>
        </div>

        {/* Filter Card */}
        <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6 mb-6">
          {/* Search Bar */}
          <div className="mb-4">
            <div className="flex gap-2">
              <input
                type="text"
                placeholder="Tìm kiếm..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === "Enter") {
                    handleSearch();
                  }
                }}
                className="flex-1 px-4 py-2.5 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#00897b] focus:border-transparent"
              />
              <button
                onClick={handleSearch}
                className="px-6 py-2.5 bg-[#00897b] text-white rounded-lg text-sm font-medium hover:bg-[#007a6e] transition-colors"
              >
                Tìm kiếm
              </button>
            </div>
          </div>

          {/* Filter Row */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div>
              <label className="block text-sm font-normal text-[#1e3a8a] mb-1.5">
                Vai trò
              </label>
              <select
                value={filters.role_id || ""}
                onChange={(e) => handleFilterChange("role_id", e.target.value ? Number(e.target.value) : null)}
                className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#00897b] focus:border-transparent"
              >
                <option value="">Tất cả</option>
                <option value="1">Admin</option>
                <option value="2">Owner</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-normal text-[#1e3a8a] mb-1.5">
                Trạng thái
              </label>
              <select
                value={filters.status || ""}
                onChange={(e) => handleFilterChange("status", e.target.value || null)}
                className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#00897b] focus:border-transparent"
              >
                <option value="">Tất cả</option>
                <option value="Active">Active</option>
                <option value="Inactive">Inactive</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-normal text-[#1e3a8a] mb-1.5">
                Hộ kinh doanh
              </label>
              <select
                value={filters.household_id || ""}
                onChange={(e) => handleFilterChange("household_id", e.target.value ? Number(e.target.value) : null)}
                className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#00897b] focus:border-transparent"
              >
                <option value="">Tất cả</option>
                {households.map((h) => (
                  <option key={h.id} value={h.id}>
                    {h.name}
                  </option>
                ))}
              </select>
            </div>
            <div className="flex items-end">
              <button
                onClick={handleRefresh}
                className="w-full px-4 py-2 bg-white border border-[#1e3a8a] text-[#1e3a8a] rounded-lg hover:bg-slate-50 transition-colors font-normal text-base"
              >
                Làm mới
              </button>
            </div>
          </div>
        </div>

        {/* Table Card */}
        <div className="bg-white rounded-lg shadow-sm border border-slate-200 overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-slate-50 border-b border-slate-200">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-bold italic text-[#4b5563] uppercase tracking-wider">
                    ID
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-bold italic text-[#4b5563] uppercase tracking-wider">
                    Tên đăng nhập
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-bold italic text-[#4b5563] uppercase tracking-wider">
                    Email
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-bold italic text-[#4b5563] uppercase tracking-wider">
                    Vai trò
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-bold italic text-[#4b5563] uppercase tracking-wider">
                    Hộ kinh doanh
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-bold italic text-[#4b5563] uppercase tracking-wider">
                    Trạng thái
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-bold italic text-[#4b5563] uppercase tracking-wider">
                    Ngày tạo
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-bold italic text-[#4b5563] uppercase tracking-wider">
                    Thao tác
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-slate-200">
                {paginatedUsers.length === 0 ? (
                  <tr>
                    <td colSpan={8} className="px-6 py-12 text-center text-slate-500">
                      Không có dữ liệu
                    </td>
                  </tr>
                ) : (
                  paginatedUsers.map((user) => (
                    <tr key={user.id} className="hover:bg-slate-50 transition-colors">
                      <td className="px-6 py-4 text-base font-normal text-[#1e3a8a]">
                        {user.id}
                      </td>
                      <td className="px-6 py-4 text-base font-normal text-[#1e3a8a]">
                        {user.user_name}
                      </td>
                      <td className="px-6 py-4 text-base font-normal text-[#1e3a8a]">
                        {user.email || "-"}
                      </td>
                      <td className="px-6 py-4">
                        {getRoleBadge(user.role_id)}
                      </td>
                      <td className="px-6 py-4 text-base font-normal text-[#1e3a8a]">
                        {getHouseholdName(user.household_id)}
                      </td>
                      <td className="px-6 py-4">
                        {getStatusBadge(user.status)}
                      </td>
                      <td className="px-6 py-4 text-base font-normal text-[#1e3a8a]">
                        {formatDate(user.created_at)}
                      </td>
                      <td className="px-6 py-4">
                        <div className="flex items-center gap-3">
                          <button
                            onClick={() => window.location.href = `/admin/users/${user.id}`}
                            className="px-3 py-1 text-sm text-[#1e3a8a] hover:text-[#00897b] transition-colors border border-[#1e3a8a] rounded hover:border-[#00897b]"
                          >
                            Xem
                          </button>
                          {/* Chỉ hiển thị Active/Deactivate cho Owner (role_id = 2) */}
                          {user.role_id === 2 && (
                            <button
                              onClick={() => handleToggleStatus(user.id, user.status === "Active" ? "Inactive" : "Active")}
                              className={`px-3 py-1 text-sm rounded transition-colors border ${
                                user.status === "Active"
                                  ? "text-red-600 hover:text-red-700 border-red-600 hover:border-red-700"
                                  : "text-[#10b981] hover:text-[#059669] border-[#10b981] hover:border-[#059669]"
                              }`}
                            >
                              {user.status === "Active" ? "Deactivate" : "Active"}
                            </button>
                          )}
                          <button
                            onClick={() => handleDelete(user.id)}
                            className="px-3 py-1 text-sm text-red-600 hover:text-red-700 transition-colors border border-red-600 rounded hover:border-red-700"
                          >
                            Xóa
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>

          {/* Pagination */}
          {totalUsers > 0 && (
            <div className="px-6 py-4 border-t border-slate-200 flex items-center justify-between">
              <p className="text-sm text-[#4b5563]">
                Hiển thị {startIndex + 1}-{Math.min(endIndex, totalUsers)} của {totalUsers} người dùng
              </p>
              <div className="flex items-center gap-2">
                <button
                  onClick={() => setCurrentPage(prev => Math.max(1, prev - 1))}
                  disabled={currentPage === 1}
                  className={`px-3 py-1.5 rounded text-sm ${
                    currentPage === 1
                      ? "text-slate-300 cursor-not-allowed"
                      : "text-[#4b5563] hover:bg-slate-100"
                  }`}
                >
                  Trước
                </button>
                {Array.from({ length: totalPages }, (_, i) => i + 1).map((page) => (
                  <button
                    key={page}
                    onClick={() => setCurrentPage(page)}
                    className={`px-3 py-1.5 rounded text-sm font-normal ${
                      currentPage === page
                        ? "bg-[#00897b] text-white"
                        : "text-[#4b5563] hover:bg-slate-100"
                    }`}
                  >
                    {page}
                  </button>
                ))}
                <button
                  onClick={() => setCurrentPage(prev => Math.min(totalPages, prev + 1))}
                  disabled={currentPage === totalPages}
                  className={`px-3 py-1.5 rounded text-sm ${
                    currentPage === totalPages
                      ? "text-slate-300 cursor-not-allowed"
                      : "text-[#4b5563] hover:bg-slate-100"
                  }`}
                >
                  Sau
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </>
  );
}
