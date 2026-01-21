"use client";

import { useEffect, useMemo, useState } from "react";
import Link from "next/link";
import LoadingOverlay from "@/components/ui/loading-overlay";
import { showToast } from "@/components/ui/toast";
import { ownerService, OwnerEmployee } from "@/services/owner.service";

type StatusFilter = "" | "Active" | "Inactive";

export default function OwnerEmployeesPage() {
  const [employees, setEmployees] = useState<OwnerEmployee[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState("");
  const [statusFilter, setStatusFilter] = useState<StatusFilter>("");

  useEffect(() => {
    fetchEmployees();
  }, []);

  const fetchEmployees = async () => {
    try {
      setLoading(true);
      const data = await ownerService.listEmployees();
      setEmployees(data);
    } catch (error: any) {
      const message =
        error?.response?.data?.error ||
        error?.message ||
        "Lỗi khi tải danh sách nhân viên";
      showToast(message, "error");
    } finally {
      setLoading(false);
    }
  };

  const handleRefresh = () => {
    setSearchTerm("");
    setStatusFilter("");
    fetchEmployees();
  };

  const handleDelete = async (id: number) => {
    if (!confirm("Bạn có chắc chắn muốn xóa nhân viên này?")) return;
    try {
      await ownerService.deleteEmployee(id);
      showToast("Xóa nhân viên thành công", "success");
      fetchEmployees();
    } catch (error: any) {
      const message =
        error?.response?.data?.error ||
        error?.message ||
        "Lỗi khi xóa nhân viên";
      showToast(message, "error");
    }
  };

  const filteredEmployees = useMemo(() => {
    const normalizedFilter = statusFilter.toLowerCase();
    return employees.filter((e) => {
      const normalizedStatus = (e.status || "").toLowerCase();
      const matchStatus =
        !normalizedFilter || normalizedStatus === normalizedFilter;
      const term = searchTerm.trim().toLowerCase();
      const matchSearch =
        !term ||
        e.user_name.toLowerCase().includes(term) ||
        (e.email || "").toLowerCase().includes(term) ||
        (e.description || "").toLowerCase().includes(term);
      return matchStatus && matchSearch;
    });
  }, [employees, statusFilter, searchTerm]);

  const formatDate = (dateString: string) => {
    if (!dateString) return "-";
    const date = new Date(dateString);
    return date.toLocaleDateString("vi-VN", {
      day: "2-digit",
      month: "2-digit",
      year: "numeric",
    });
  };

  const getStatusBadge = (status: string) => {
    const isActive = status === "Active";
    return (
      <span
        className={`px-2 py-1 text-xs font-bold italic rounded text-white ${
          isActive ? "bg-[#10b981]" : "bg-[#6b7280]"
        }`}
      >
        {status}
      </span>
    );
  };

  return (
    <>
      <LoadingOverlay
        isLoading={loading}
        message="Đang tải danh sách nhân viên..."
      />
      <div className="p-8">
        {/* Page Header */}
        <div className="mb-6 flex items-center justify-between">
          <h1 className="text-[28px] font-bold italic text-[#1e3a8a]">
            Quản lý Nhân viên
          </h1>
          <Link
            href="/owner/employees/create"
            className="px-4 py-2 bg-[#00897b] text-white rounded-lg hover:bg-[#007a6c] transition-colors font-bold italic text-base flex items-center gap-2"
          >
            <span>+</span>
            <span>Tạo nhân viên</span>
          </Link>
        </div>

        {/* Filter Card */}
        <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6 mb-6">
          {/* Search Bar */}
          <div className="mb-4">
            <div className="flex gap-2">
              <input
                type="text"
                placeholder="Tìm theo tên đăng nhập, email hoặc mô tả..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="flex-1 px-4 py-2.5 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#00897b] focus:border-transparent"
              />
              <button
                onClick={handleRefresh}
                className="px-4 py-2 bg-white border border-[#1e3a8a] text-[#1e3a8a] rounded-lg hover:bg-slate-50 transition-colors text-sm font-medium"
              >
                Làm mới
              </button>
            </div>
          </div>

          {/* Status Filter */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-normal text-[#1e3a8a] mb-1.5">
                Trạng thái
              </label>
              <select
                value={statusFilter}
                onChange={(e) => setStatusFilter(e.target.value as StatusFilter)}
                className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#00897b] focus:border-transparent"
              >
                <option value="">Tất cả</option>
                <option value="Active">Active</option>
                <option value="Inactive">Inactive</option>
              </select>
            </div>
          </div>
        </div>

        {/* Table */}
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
                    Họ tên / Mô tả
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-bold italic text-[#4b5563] uppercase tracking-wider">
                    Email
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
                {filteredEmployees.length === 0 ? (
                  <tr>
                    <td
                      colSpan={7}
                      className="px-6 py-12 text-center text-slate-500"
                    >
                      Không có nhân viên
                    </td>
                  </tr>
                ) : (
                  filteredEmployees.map((emp) => (
                    <tr
                      key={emp.id}
                      className="hover:bg-slate-50 transition-colors"
                    >
                      <td className="px-6 py-4 text-sm font-normal text-[#1e3a8a]">
                        {emp.id}
                      </td>
                      <td className="px-6 py-4 text-sm font-normal text-[#1e3a8a]">
                        {emp.user_name}
                      </td>
                      <td className="px-6 py-4 text-sm font-normal text-[#1e3a8a]">
                        {emp.description || "-"}
                      </td>
                      <td className="px-6 py-4 text-sm font-normal text-[#1e3a8a]">
                        {emp.email || "-"}
                      </td>
                      <td className="px-6 py-4">
                        {getStatusBadge(emp.status)}
                      </td>
                      <td className="px-6 py-4 text-sm font-normal text-[#1e3a8a]">
                        {formatDate(emp.created_at)}
                      </td>
                      <td className="px-6 py-4">
                        <div className="flex items-center gap-3">
                          <Link
                            href={`/owner/employees/${emp.id}`}
                            className="px-3 py-1 text-sm text-[#1e3a8a] hover:text-[#00897b] transition-colors border border-[#1e3a8a] rounded hover:border-[#00897b]"
                          >
                            Xem
                          </Link>
                          <button
                            onClick={() => handleDelete(emp.id)}
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
        </div>
      </div>
    </>
  );
}

