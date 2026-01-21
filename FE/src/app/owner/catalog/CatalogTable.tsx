"use client";

import { useMemo, useState } from "react";

export type CatalogStatus = "ACTIVE" | "INACTIVE";

export interface CatalogBaseItem {
  id: number;
  name: string;
  code?: string | null; // dùng cho Product mã, nếu sau này có
  typeLabel?: string | null; // Loại (Category/Unit/Product,...)
  status: string;
  created_at: string;
}

interface CatalogTableProps<T extends CatalogBaseItem> {
  title: string;
  createLabel: string;
  items: T[];
  loading: boolean;
  onRefresh: () => void;
  onCreate: () => void;
  onView?: (item: T) => void;
  onEdit: (item: T) => void;
  onDelete: (item: T) => void;
}

export function CatalogTable<T extends CatalogBaseItem>({
  title,
  createLabel,
  items,
  loading,
  onRefresh,
  onCreate,
  onView,
  onEdit,
  onDelete,
}: CatalogTableProps<T>) {
  const [searchTerm, setSearchTerm] = useState("");
  const [statusFilter, setStatusFilter] = useState<"" | CatalogStatus>("");

  const filtered = useMemo(() => {
    const term = searchTerm.trim().toLowerCase();
    const normalizedFilter = (statusFilter || "").toLowerCase();
    return items.filter((item) => {
      const status = (item.status || "").toLowerCase();
      const matchStatus =
        !normalizedFilter || status === normalizedFilter.toLowerCase();
      const matchSearch =
        !term ||
        item.name.toLowerCase().includes(term) ||
        (item.code || "").toLowerCase().includes(term) ||
        (item.typeLabel || "").toLowerCase().includes(term);
      return matchStatus && matchSearch;
    });
  }, [items, searchTerm, statusFilter]);

  const formatDate = (value?: string) => {
    if (!value) return "-";
    const d = new Date(value);
    return d.toLocaleDateString("vi-VN", {
      day: "2-digit",
      month: "2-digit",
      year: "numeric",
    });
  };

  const getStatusBadge = (status: string) => {
    const isActive = status?.toUpperCase() === "ACTIVE";
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
    <div className="p-8">
      {/* Header */}
      <div className="mb-6 flex items-center justify-between">
        <h1 className="text-[28px] font-bold italic text-[#1e3a8a]">
          {title}
        </h1>
        <button
          type="button"
          onClick={onCreate}
          className="px-4 py-2 bg-[#00897b] text-white rounded-lg hover:bg-[#007a6c] transition-colors font-bold italic text-base flex items-center gap-2"
        >
          <span>+</span>
          <span>{createLabel}</span>
        </button>
      </div>

      {/* Filter card */}
      <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6 mb-6">
        {/* Search */}
        <div className="mb-4">
          <div className="flex gap-2">
            <input
              type="text"
              placeholder="Tìm theo tên, mã hoặc loại..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="flex-1 px-4 py-2.5 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#00897b] focus:border-transparent"
            />
            <button
              type="button"
              onClick={() => {
                setSearchTerm("");
                setStatusFilter("");
                onRefresh();
              }}
              className="px-4 py-2 bg-white border border-[#1e3a8a] text-[#1e3a8a] rounded-lg hover:bg-slate-50 transition-colors text-sm font-medium"
            >
              Làm mới
            </button>
          </div>
        </div>

        {/* Status filter */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label className="block text-sm font-normal text-[#1e3a8a] mb-1.5">
              Trạng thái
            </label>
            <select
              value={statusFilter}
              onChange={(e) =>
                setStatusFilter(e.target.value as "" | CatalogStatus)
              }
              className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#00897b] focus:border-transparent"
            >
              <option value="">Tất cả</option>
              <option value="ACTIVE">ACTIVE</option>
              <option value="INACTIVE">INACTIVE</option>
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
                  Tên
                </th>
                <th className="px-6 py-3 text-left text-xs font-bold italic text-[#4b5563] uppercase tracking-wider">
                  Mã
                </th>
                <th className="px-6 py-3 text-left text-xs font-bold italic text-[#4b5563] uppercase tracking-wider">
                  Loại
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
              {loading ? (
                <tr>
                  <td
                    colSpan={7}
                    className="px-6 py-12 text-center text-[#6b7280] text-sm"
                  >
                    Đang tải dữ liệu...
                  </td>
                </tr>
              ) : filtered.length === 0 ? (
                <tr>
                  <td
                    colSpan={7}
                    className="px-6 py-12 text-center text-[#6b7280] text-sm"
                  >
                    Không có dữ liệu
                  </td>
                </tr>
              ) : (
                filtered.map((item) => (
                  <tr
                    key={item.id}
                    className="hover:bg-slate-50 transition-colors"
                  >
                    <td className="px-6 py-4 text-sm font-normal text-[#1e3a8a]">
                      {item.id}
                    </td>
                    <td className="px-6 py-4 text-sm font-normal text-[#1e3a8a]">
                      {item.name}
                    </td>
                    <td className="px-6 py-4 text-sm font-normal text-[#1e3a8a]">
                      {item.code || "-"}
                    </td>
                    <td className="px-6 py-4 text-sm font-normal text-[#1e3a8a]">
                      {item.typeLabel || "-"}
                    </td>
                    <td className="px-6 py-4">{getStatusBadge(item.status)}</td>
                    <td className="px-6 py-4 text-sm font-normal text-[#1e3a8a]">
                      {formatDate(item.created_at)}
                    </td>
                    <td className="px-6 py-4">
                      <div className="flex items-center gap-3">
                        {onView && (
                          <button
                            type="button"
                            onClick={() => onView(item)}
                            className="px-3 py-1 text-sm text-[#1e3a8a] hover:text-[#00897b] transition-colors border border-[#1e3a8a] rounded hover:border-[#00897b]"
                          >
                            Xem
                          </button>
                        )}
                        <button
                          type="button"
                          onClick={() => onEdit(item)}
                          className="px-3 py-1 text-sm text-[#1e3a8a] hover:text-[#00897b] transition-colors border border-[#1e3a8a] rounded hover:border-[#00897b]"
                        >
                          Chỉnh sửa
                        </button>
                        <button
                          type="button"
                          onClick={() => onDelete(item)}
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
  );
}

