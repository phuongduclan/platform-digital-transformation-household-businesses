"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter, useSearchParams } from "next/navigation";
import LoadingOverlay from "@/components/ui/loading-overlay";
import { showToast } from "@/components/ui/toast";
import { ownerService, OwnerCustomer } from "@/services/owner.service";

export default function OwnerCustomerDetailPage() {
  const params = useParams();
  const searchParams = useSearchParams();
  const router = useRouter();
  const idParam = params?.id;
  const customerId =
    typeof idParam === "string" ? Number(idParam) : NaN;

  const [customer, setCustomer] = useState<OwnerCustomer | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [editMode, setEditMode] = useState(false);

  const [name, setName] = useState("");
  const [taxCode, setTaxCode] = useState("");
  const [phone, setPhone] = useState("");
  const [address, setAddress] = useState("");
  const [description, setDescription] = useState("");
  const [status, setStatus] = useState<"Active" | "Inactive">("Active");

  useEffect(() => {
    if (!Number.isNaN(customerId)) {
      const mode = searchParams.get("mode");
      setEditMode(mode === "edit");
      fetchCustomer();
    } else {
      showToast("ID khách hàng không hợp lệ", "error");
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [customerId]);

  const fetchCustomer = async () => {
    try {
      setLoading(true);
      const data = await ownerService.getCustomer(customerId);
      setCustomer(data);
      setName(data.name);
      setTaxCode(data.tax_code || "");
      setPhone(data.phone || "");
      setAddress(data.address || "");
      setDescription(data.description || "");
      setStatus((data.status as "Active" | "Inactive") || "Active");
    } catch (error: any) {
      const message =
        error?.response?.data?.error ||
        error?.message ||
        "Lỗi khi tải khách hàng";
      showToast(message, "error");
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (value?: string) => {
    if (!value) return "-";
    const d = new Date(value);
    return d.toLocaleDateString("vi-VN", {
      day: "2-digit",
      month: "2-digit",
      year: "numeric",
    });
  };

  const handleSave = async () => {
    if (!name.trim()) {
      showToast("Tên khách hàng không được để trống", "error");
      return;
    }
    if (!customer) return;
    try {
      setSaving(true);
      const updated = await ownerService.updateCustomer(customer.id, {
        name: name.trim(),
        tax_code: taxCode.trim() || undefined,
        phone: phone.trim() || undefined,
        address: address.trim() || undefined,
        description: description.trim() || undefined,
        status,
      });
      setCustomer(updated);
      setEditMode(false);
      showToast("Cập nhật khách hàng thành công", "success");
    } catch (error: any) {
      showToast("Cập nhật khách hàng thất bại", "error");
    } finally {
      setSaving(false);
    }
  };

  if (loading || !customer) {
    return (
      <LoadingOverlay
        isLoading={true}
        message="Đang tải khách hàng..."
      />
    );
  }

  const isActive = (customer.status || "").toUpperCase() === "ACTIVE";

  return (
    <>
      <LoadingOverlay
        isLoading={saving}
        message="Đang lưu khách hàng..."
      />
      <div className="p-8">
        {/* Breadcrumb */}
        <div className="mb-4 flex items-center gap-2 text-sm">
          <button
            type="button"
            onClick={() => router.push("/owner")}
            className="text-[#00897b] hover:underline"
          >
            Tổng quan
          </button>
          <span className="text-[#4b5563]">/</span>
          <button
            type="button"
            onClick={() => router.push("/owner/customers")}
            className="text-[#00897b] hover:underline"
          >
            Khách hàng
          </button>
          <span className="text-[#4b5563]">/</span>
          <span className="text-[#4b5563]">{customer.name}</span>
        </div>

        {/* Header */}
        <div className="mb-6 flex items-center justify-between">
          <div>
            <h1 className="text-[28px] font-bold italic text-[#1e3a8a] mb-1">
              {customer.name}
            </h1>
            <p className="text-xs text-[#6b7280]">
              Tạo ngày {formatDate(customer.created_at)}
            </p>
          </div>
          <div className="flex items-center gap-3">
            <span
              className={`px-3 py-1 text-xs font-bold italic rounded-full text-white ${
                isActive ? "bg-[#10b981]" : "bg-[#6b7280]"
              }`}
            >
              {customer.status}
            </span>
            <button
              type="button"
              onClick={() => setEditMode((prev) => !prev)}
              className="px-4 py-2 bg-white border border-[#1e3a8a] text-[#1e3a8a] rounded-lg hover:bg-slate-50 transition-colors text-sm font-medium"
            >
              {editMode ? "Hủy chỉnh sửa" : "Chỉnh sửa"}
            </button>
          </div>
        </div>

        {/* Content */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Thông tin khách hàng */}
          <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6">
            <h2 className="text-[18px] font-bold italic text-[#1e3a8a] mb-4">
              Thông tin khách hàng
            </h2>
            <div className="space-y-4 text-sm">
              <div>
                <p className="text-xs text-[#6b7280] mb-1">Tên khách hàng</p>
                {editMode ? (
                  <input
                    type="text"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#00897b] focus:border-transparent"
                  />
                ) : (
                  <p className="text-[#1e3a8a]">{customer.name}</p>
                )}
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <p className="text-xs text-[#6b7280] mb-1">Mã số thuế</p>
                  {editMode ? (
                    <input
                      type="text"
                      value={taxCode}
                      onChange={(e) => setTaxCode(e.target.value)}
                      className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#00897b] focus:border-transparent"
                    />
                  ) : (
                    <p className="text-[#1e3a8a]">
                      {customer.tax_code || "-"}
                    </p>
                  )}
                </div>
                <div>
                  <p className="text-xs text-[#6b7280] mb-1">Số điện thoại</p>
                  {editMode ? (
                    <input
                      type="text"
                      value={phone}
                      onChange={(e) => setPhone(e.target.value)}
                      className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#00897b] focus:border-transparent"
                    />
                  ) : (
                    <p className="text-[#1e3a8a]">
                      {customer.phone || "-"}
                    </p>
                  )}
                </div>
              </div>
              <div>
                <p className="text-xs text-[#6b7280] mb-1">Địa chỉ</p>
                {editMode ? (
                  <input
                    type="text"
                    value={address}
                    onChange={(e) => setAddress(e.target.value)}
                    className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#00897b] focus:border-transparent"
                  />
                ) : (
                  <p className="text-[#1e3a8a]">
                    {customer.address || "-"}
                  </p>
                )}
              </div>
              <div>
                <p className="text-xs text-[#6b7280] mb-1">Ghi chú</p>
                {editMode ? (
                  <textarea
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                    rows={3}
                    className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#00897b] focus:border-transparent"
                  />
                ) : (
                  <p className="text-[#1e3a8a]">
                    {customer.description || "-"}
                  </p>
                )}
              </div>
              <div>
                <p className="text-xs text-[#6b7280] mb-1">Trạng thái</p>
                {editMode ? (
                  <select
                    value={status}
                    onChange={(e) =>
                      setStatus(e.target.value as "Active" | "Inactive")
                    }
                    className="w-full max-w-xs px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#00897b] focus:border-transparent"
                  >
                    <option value="Active">Active</option>
                    <option value="Inactive">Inactive</option>
                  </select>
                ) : (
                  <span
                    className={`px-2 py-1 text-xs font-bold italic rounded text-white ${
                      isActive ? "bg-[#10b981]" : "bg-[#6b7280]"
                    }`}
                  >
                    {customer.status}
                  </span>
                )}
              </div>
              {editMode && (
                <div className="pt-2 flex items-center justify-end">
                  <button
                    type="button"
                    onClick={handleSave}
                    disabled={saving}
                    className="px-5 py-2 bg-[#00897b] text-white rounded-lg text-sm font-bold hover:bg-[#007a6c] transition-colors disabled:bg-slate-400 disabled:cursor-not-allowed"
                  >
                    {saving ? "Đang lưu..." : "Lưu thay đổi"}
                  </button>
                </div>
              )}
            </div>
          </div>

          {/* Công nợ & lịch sử mua hàng - placeholder text vì FE hiện tại chưa map API chi tiết */}
          <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6">
            <h2 className="text-[18px] font-bold italic text-[#1e3a8a] mb-4">
              Công nợ & lịch sử
            </h2>
            <p className="text-sm text-[#6b7280]">
              Thông tin tổng quan công nợ và lịch sử mua hàng sẽ được hiển thị
              tại đây khi tích hợp thêm API chi tiết (customer debt & purchase
              history). Hiện tại, bạn có thể theo dõi công nợ ở các báo cáo và
              danh sách chứng từ.
            </p>
          </div>
        </div>
      </div>
    </>
  );
}

