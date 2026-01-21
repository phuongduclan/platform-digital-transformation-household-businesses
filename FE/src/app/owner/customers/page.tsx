"use client";

import { useEffect, useMemo, useState } from "react";
import Link from "next/link";
import LoadingOverlay from "@/components/ui/loading-overlay";
import { showToast } from "@/components/ui/toast";
import { ownerService, OwnerCustomer } from "@/services/owner.service";

type StatusFilter = "" | "Active" | "Inactive";

export default function OwnerCustomersPage() {
  const [customers, setCustomers] = useState<OwnerCustomer[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState("");
  const [statusFilter, setStatusFilter] = useState<StatusFilter>("");

  useEffect(() => {
    fetchCustomers();
  }, []);

  const fetchCustomers = async () => {
    try {
      setLoading(true);
      const data = await ownerService.listCustomers();
      setCustomers(data || []);
    } catch (error: any) {
      const message =
        error?.response?.data?.error ||
        error?.message ||
        "Lỗi khi tải danh sách khách hàng";
      showToast(message, "error");
    } finally {
      setLoading(false);
    }
  };

  const handleRefresh = () => {
    setSearchTerm("");
    setStatusFilter("");
    fetchCustomers();
  };

  const handleDelete = async (id: number) => {
    if (!confirm("Bạn có chắc chắn muốn xóa khách hàng này?")) return;
    try {
      await ownerService.deleteCustomer(id);
      showToast("Xóa khách hàng thành công", "success");
      fetchCustomers();
    } catch (error: any) {
      const message =
        error?.response?.data?.error ||
        error?.message ||
        "Lỗi khi xóa khách hàng";
      showToast(message, "error");
    }
  };

  const filteredCustomers = useMemo(() => {
    const normalizedFilter = statusFilter.toLowerCase();
    return customers.filter((c) => {
      const normalizedStatus = (c.status || "").toLowerCase();
      const matchStatus =
        !normalizedFilter || normalizedStatus === normalizedFilter;
      const term = searchTerm.trim().toLowerCase();
      const matchSearch =
        !term ||
        c.name.toLowerCase().includes(term) ||
        (c.phone || "").toLowerCase().includes(term) ||
        (c.tax_code || "").toLowerCase().includes(term);
      return matchStatus && matchSearch;
    });
  }, [customers, statusFilter, searchTerm]);

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
        message="Đang tải danh sách khách hàng..."
      />
      <div className="p-8">
        {/* Page Header */}
        <div className="mb-6 flex items-center justify-between">
          <h1 className="text-[28px] font-bold italic text-[#1e3a8a]">
            Khách hàng
          </h1>
          <Link
            href="/owner/customers/create"
            className="px-4 py-2 bg-[#00897b] text-white rounded-lg hover:bg-[#007a6c] transition-colors font-bold italic text-base flex items-center gap-2"
          >
            <span>+</span>
            <span>Tạo khách hàng</span>
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
                    Tên khách hàng
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
                {filteredCustomers.length === 0 ? (
                  <tr>
                    <td
                      colSpan={8}
                      className="px-6 py-12 text-center text-slate-500"
                    >
                      Không có khách hàng
                    </td>
                  </tr>
                ) : (
                  filteredCustomers.map((c) => (
                    <tr
                      key={c.id}
                      className="hover:bg-slate-50 transition-colors"
                    >
                      <td className="px-6 py-4 text-sm font-normal text-[#1e3a8a]">
                        {c.id}
                      </td>
                      <td className="px-6 py-4 text-sm font-normal text-[#1e3a8a]">
                        {c.name}
                      </td>
                      <td className="px-6 py-4 text-sm font-normal text-[#1e3a8a]">
                        {c.tax_code || "-"}
                      </td>
                      <td className="px-6 py-4 text-sm font-normal text-[#1e3a8a]">
                        {c.phone || "-"}
                      </td>
                      <td className="px-6 py-4 text-sm font-normal text-[#1e3a8a]">
                        {c.address || "-"}
                      </td>
                      <td className="px-6 py-4">{getStatusBadge(c.status)}</td>
                      <td className="px-6 py-4 text-sm font-normal text-[#1e3a8a]">
                        {formatDate(c.created_at)}
                      </td>
                      <td className="px-6 py-4">
                        <div className="flex items-center gap-3">
                          <Link
                            href={`/owner/customers/${c.id}`}
                            className="px-3 py-1 text-sm text-[#1e3a8a] hover:text-[#00897b] transition-colors border border-[#1e3a8a] rounded hover:border-[#00897b]"
                          >
                            Xem
                          </Link>
                          <Link
                            href={`/owner/customers/${c.id}?mode=edit`}
                            className="px-3 py-1 text-sm text-[#1e3a8a] hover:text-[#00897b] transition-colors border border-[#1e3a8a] rounded hover:border-[#00897b]"
                          >
                            Chỉnh sửa
                          </Link>
                          <button
                            type="button"
                            onClick={() => handleDelete(c.id)}
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

