"use client";

import { useEffect, useMemo, useState } from "react";
import Link from "next/link";
import LoadingOverlay from "@/components/ui/loading-overlay";
import { showToast } from "@/components/ui/toast";
import { ownerService, OwnerSeller } from "@/services/owner.service";

type StatusFilter = "" | "Active" | "Inactive";

export default function OwnerSellersPage() {
  const [sellers, setSellers] = useState<OwnerSeller[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState("");
  const [statusFilter, setStatusFilter] = useState<StatusFilter>("");

  useEffect(() => {
    fetchSellers();
  }, []);

  const fetchSellers = async () => {
    try {
      setLoading(true);
      const data = await ownerService.listSellers();
      setSellers(data || []);
    } catch (error: any) {
      const message =
        error?.response?.data?.error ||
        error?.message ||
        "Lỗi khi tải danh sách nhà cung cấp";
      showToast(message, "error");
    } finally {
      setLoading(false);
    }
  };

  const handleRefresh = () => {
    setSearchTerm("");
    setStatusFilter("");
    fetchSellers();
  };

  const handleDelete = async (id: number) => {
    if (!confirm("Bạn có chắc chắn muốn xóa nhà cung cấp này?")) return;
    try {
      await ownerService.deleteSeller(id);
      showToast("Xóa nhà cung cấp thành công", "success");
      fetchSellers();
    } catch (error: any) {
      const message =
        error?.response?.data?.error ||
        error?.message ||
        "Lỗi khi xóa nhà cung cấp";
      showToast(message, "error");
    }
  };

  const filteredSellers = useMemo(() => {
    const normalizedFilter = statusFilter.toLowerCase();
    return sellers.filter((s) => {
      const normalizedStatus = (s.status || "").toLowerCase();
      const matchStatus =
        !normalizedFilter || normalizedStatus === normalizedFilter;
      const term = searchTerm.trim().toLowerCase();
      const matchSearch =
        !term ||
        s.name.toLowerCase().includes(term) ||
        (s.phone || "").toLowerCase().includes(term) ||
        (s.tax_code || "").toLowerCase().includes(term);
      return matchStatus && matchSearch;
    });
  }, [sellers, statusFilter, searchTerm]);

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
        message="Đang tải danh sách nhà cung cấp..."
      />
      <div className="p-8">
        {/* Page Header */}
        <div className="mb-6 flex items-center justify-between">
          <h1 className="text-[28px] font-bold italic text-[#1e3a8a]">
            Nhà cung cấp
          </h1>
          <Link
            href="/owner/sellers/create"
            className="px-4 py-2 bg-[#00897b] text-white rounded-lg hover:bg-[#007a6c] transition-colors font-bold italic text-base flex items-center gap-2"
          >
            <span>+</span>
            <span>Tạo nhà cung cấp</span>
          </Link>
        </div>

        {/* Filter Card */}
        <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6 mb-6">
          <div className="mb-4">
            <div className="flex gap-2">
              <input
                type="text"
                placeholder="Tìm theo tên, SĐT hoặc mã số thuế..."
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
                    Tên nhà cung cấp
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-bold italic text-[#4b5563] uppercase tracking-wider">
                    Mã số thuế
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-bold italic text-[#4b5563] uppercase tracking-wider">
                    Số điện thoại
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-bold italic text-[#4b5563] uppercase tracking-wider">
                    Địa chỉ
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
                {filteredSellers.length === 0 ? (
                  <tr>
                    <td
                      colSpan={8}
                      className="px-6 py-12 text-center text-slate-500"
                    >
                      Không có nhà cung cấp
                    </td>
                  </tr>
                ) : (
                  filteredSellers.map((s) => (
                    <tr
                      key={s.id}
                      className="hover:bg-slate-50 transition-colors"
                    >
                      <td className="px-6 py-4 text-sm font-normal text-[#1e3a8a]">
                        {s.id}
                      </td>
                      <td className="px-6 py-4 text-sm font-normal text-[#1e3a8a]">
                        {s.name}
                      </td>
                      <td className="px-6 py-4 text-sm font-normal text-[#1e3a8a]">
                        {s.tax_code || "-"}
                      </td>
                      <td className="px-6 py-4 text-sm font-normal text-[#1e3a8a]">
                        {s.phone || "-"}
                      </td>
                      <td className="px-6 py-4 text-sm font-normal text-[#1e3a8a]">
                        {s.address || "-"}
                      </td>
                      <td className="px-6 py-4">{getStatusBadge(s.status)}</td>
                      <td className="px-6 py-4 text-sm font-normal text-[#1e3a8a]">
                        {formatDate(s.created_at)}
                      </td>
                      <td className="px-6 py-4">
                        <div className="flex items-center gap-3">
                          <Link
                            href={`/owner/sellers/${s.id}`}
                            className="px-3 py-1 text-sm text-[#1e3a8a] hover:text-[#00897b] transition-colors border border-[#1e3a8a] rounded hover:border-[#00897b]"
                          >
                            Xem
                          </Link>
                          <Link
                            href={`/owner/sellers/${s.id}?mode=edit`}
                            className="px-3 py-1 text-sm text-[#1e3a8a] hover:text-[#00897b] transition-colors border border-[#1e3a8a] rounded hover:border-[#00897b]"
                          >
                            Chỉnh sửa
                          </Link>
                          <button
                            type="button"
                            onClick={() => handleDelete(s.id)}
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

