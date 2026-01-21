"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { adminService } from "@/services/admin.service";
import { showToast } from "@/components/ui/toast";
import LoadingOverlay from "@/components/ui/loading-overlay";

interface PaymentMethod {
  id: number;
  name: string;
  status: string;
  created_at: string;
  updated_at: string;
}

export default function AdminPaymentMethodsPage() {
  const router = useRouter();
  const [paymentMethods, setPaymentMethods] = useState<PaymentMethod[]>([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState<{ status?: string }>({});

  useEffect(() => {
    fetchPaymentMethods();
  }, [filters]);

  const fetchPaymentMethods = async () => {
    try {
      setLoading(true);
      const params: any = {};
      if (filters.status) {
        params.status = filters.status;
      }
      const data = await adminService.listPaymentMethods(params);
      setPaymentMethods(data);
    } catch (error: any) {
      showToast(error.message || "Lỗi khi tải danh sách phương thức thanh toán", "error");
    } finally {
      setLoading(false);
    }
  };

  const handleRefresh = () => {
    setFilters({});
    fetchPaymentMethods();
  };

  const handleDelete = async (id: number) => {
    if (!confirm("Bạn có chắc chắn muốn xóa phương thức thanh toán này?")) return;
    try {
      await adminService.deletePaymentMethod(id);
      showToast("Xóa phương thức thanh toán thành công", "success");
      fetchPaymentMethods();
    } catch (error: any) {
      showToast(error.message || "Lỗi khi xóa phương thức thanh toán", "error");
    }
  };

  const formatDate = (dateString: string) => {
    if (!dateString) return "-";
    const date = new Date(dateString);
    return date.toLocaleDateString("vi-VN", { day: "2-digit", month: "2-digit", year: "numeric" });
  };

  const getStatusBadge = (status: string) => {
    const isActive = status === "Active";
    return (
      <span className={`px-2 py-1 text-xs font-bold italic rounded ${
        isActive ? "bg-[#10b981] text-white" : "bg-[#6b7280] text-white"
      }`}>
        {isActive ? "Active" : "Inactive"}
      </span>
    );
  };

  // Mock description based on payment method name (since BE doesn't have description field)
  const getDescription = (name: string) => {
    const nameLower = name.toLowerCase();
    if (nameLower.includes("chuyển khoản") || nameLower.includes("ngân hàng")) {
      return "Thanh toán qua chuyển khoản ngân hàng trực tiếp";
    } else if (nameLower.includes("tiền mặt") || nameLower.includes("cash")) {
      return "Thanh toán trực tiếp bằng tiền mặt";
    } else if (nameLower.includes("ví điện tử") || nameLower.includes("momo") || nameLower.includes("zalopay") || nameLower.includes("vnpay")) {
      return "Thanh toán qua Momo, ZaloPay, VNPay và các ví điện tử khác";
    } else if (nameLower.includes("thẻ tín dụng") || nameLower.includes("visa") || nameLower.includes("mastercard")) {
      return "Thanh toán qua thẻ Visa, Mastercard, JCB";
    }
    return `Phương thức thanh toán: ${name}`;
  };

  return (
    <>
      <LoadingOverlay isLoading={loading} message="Đang tải danh sách phương thức thanh toán..." />
      
      <div className="p-8">
        {/* Page Header */}
        <div className="mb-6 flex items-center justify-between">
          <h1 className="text-[28px] font-bold italic text-[#1e3a8a]">
            Phương thức Thanh toán
          </h1>
          <button
            type="button"
            onClick={() => router.push("/admin/payment-methods/create")}
            className="px-4 py-2 bg-[#00897b] text-white rounded-lg hover:bg-[#007a6c] transition-colors font-bold italic text-base"
          >
            + Tạo phương thức mới
          </button>
        </div>

        {/* Filter Section */}
        <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6 mb-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-normal text-[#1e3a8a] mb-1.5">
                Trạng thái
              </label>
              <select
                value={filters.status || ""}
                onChange={(e) => setFilters(prev => ({ ...prev, status: e.target.value || undefined }))}
                className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#00897b] focus:border-transparent"
              >
                <option value="">Tất cả</option>
                <option value="Active">Active</option>
                <option value="Inactive">Inactive</option>
              </select>
            </div>
            <div className="flex items-end">
              <button
                onClick={handleRefresh}
                className="w-full px-4 py-2 bg-white border border-[#1e3a8a] text-[#1e3a8a] rounded-lg hover:bg-slate-50 transition-colors font-bold italic text-base"
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
                  <th className="px-6 py-3 text-left text-xs font-bold italic text-[#1e3a8a] uppercase tracking-wider">
                    ID
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-bold italic text-[#1e3a8a] uppercase tracking-wider">
                    TÊN PHƯƠNG THỨC
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-bold italic text-[#1e3a8a] uppercase tracking-wider">
                    MÔ TẢ
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-bold italic text-[#1e3a8a] uppercase tracking-wider">
                    TRẠNG THÁI
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-bold italic text-[#1e3a8a] uppercase tracking-wider">
                    NGÀY TẠO
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-bold italic text-[#1e3a8a] uppercase tracking-wider">
                    THAO TÁC
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-slate-200">
                {paymentMethods.length === 0 ? (
                  <tr>
                    <td colSpan={6} className="px-6 py-12 text-center text-slate-500">
                      Không có dữ liệu
                    </td>
                  </tr>
                ) : (
                  paymentMethods.map((pm) => (
                    <tr key={pm.id} className="hover:bg-slate-50 transition-colors">
                      <td className="px-6 py-4 text-sm font-normal text-[#4b5563]">
                        {pm.id}
                      </td>
                      <td className="px-6 py-4">
                        <p className="text-sm font-bold italic text-[#4b5563]">
                          {pm.name}
                        </p>
                      </td>
                      <td className="px-6 py-4 text-sm font-normal text-[#4b5563]">
                        {getDescription(pm.name)}
                      </td>
                      <td className="px-6 py-4">
                        {getStatusBadge(pm.status)}
                      </td>
                      <td className="px-6 py-4 text-sm font-normal text-[#4b5563]">
                        {formatDate(pm.created_at)}
                      </td>
                      <td className="px-6 py-4">
                        <div className="flex items-center gap-3">
                          <button
                            type="button"
                            onClick={() =>
                              router.push(`/admin/payment-methods/${pm.id}/edit`)
                            }
                            className="px-3 py-1 text-sm text-[#1e3a8a] hover:text-[#00897b] transition-colors border border-[#1e3a8a] rounded hover:border-[#00897b]"
                          >
                            Sửa
                          </button>
                          <button
                            onClick={() => handleDelete(pm.id)}
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
