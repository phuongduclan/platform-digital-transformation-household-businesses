"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter, useSearchParams } from "next/navigation";
import LoadingOverlay from "@/components/ui/loading-overlay";
import { showToast } from "@/components/ui/toast";
import { ownerService, OwnerSeller } from "@/services/owner.service";
import AddressAutocomplete from "@/components/address-autocomplete";

export default function OwnerSellerDetailPage() {
  const params = useParams();
  const searchParams = useSearchParams();
  const router = useRouter();
  const idParam = params?.id;
  const sellerId =
    typeof idParam === "string" ? Number(idParam) : NaN;

  const [seller, setSeller] = useState<OwnerSeller | null>(null);
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
    if (!Number.isNaN(sellerId)) {
      const mode = searchParams.get("mode");
      setEditMode(mode === "edit");
      fetchSeller();
    } else {
      showToast("ID nhà cung cấp không hợp lệ", "error");
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [sellerId]);

  const fetchSeller = async () => {
    try {
      setLoading(true);
      const data = await ownerService.getSeller(sellerId);
      setSeller(data);
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
        "Lỗi khi tải nhà cung cấp";
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
      showToast("Tên nhà cung cấp không được để trống", "error");
      return;
    }
    if (!seller) return;
    try {
      setSaving(true);
      const updated = await ownerService.updateSeller(seller.id, {
        name: name.trim(),
        tax_code: taxCode.trim() || undefined,
        phone: phone.trim() || undefined,
        address: address.trim() || undefined,
        description: description.trim() || undefined,
        status,
      });
      setSeller(updated);
      setEditMode(false);
      showToast("Cập nhật nhà cung cấp thành công", "success");
    } catch (error: any) {
      showToast("Cập nhật nhà cung cấp thất bại", "error");
    } finally {
      setSaving(false);
    }
  };

  if (loading || !seller) {
    return (
      <LoadingOverlay
        isLoading={true}
        message="Đang tải nhà cung cấp..."
      />
    );
  }

  const isActive = (seller.status || "").toUpperCase() === "ACTIVE";

  return (
    <>
      <LoadingOverlay
        isLoading={saving}
        message="Đang lưu nhà cung cấp..."
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
            onClick={() => router.push("/owner/sellers")}
            className="text-[#00897b] hover:underline"
          >
            Nhà cung cấp
          </button>
          <span className="text-[#4b5563]">/</span>
          <span className="text-[#4b5563]">{seller.name}</span>
        </div>

        {/* Header */}
        <div className="mb-6 flex items-center justify-between">
          <div>
            <h1 className="text-[28px] font-bold italic text-[#1e3a8a] mb-1">
              {seller.name}
            </h1>
            <p className="text-xs text-[#6b7280]">
              Tạo ngày {formatDate(seller.created_at)}
            </p>
          </div>
          <div className="flex items-center gap-3">
            <span
              className={`px-3 py-1 text-xs font-bold italic rounded-full text-white ${isActive ? "bg-[#10b981]" : "bg-[#6b7280]"
                }`}
            >
              {seller.status}
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
          {/* Thông tin nhà cung cấp */}
          <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6">
            <h2 className="text-[18px] font-bold italic text-[#1e3a8a] mb-4">
              Thông tin nhà cung cấp
            </h2>
            <div className="space-y-4 text-sm">
              <div>
                <p className="text-xs text-[#6b7280] mb-1">Tên nhà cung cấp</p>
                {editMode ? (
                  <input
                    type="text"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#00897b] focus:border-transparent"
                  />
                ) : (
                  <p className="text-[#1e3a8a]">{seller.name}</p>
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
                      {seller.tax_code || "-"}
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
                      {seller.phone || "-"}
                    </p>
                  )}
                </div>
              </div>
              <div>
                <p className="text-xs text-[#6b7280] mb-1">Địa chỉ</p>
                {editMode ? (
                  <AddressAutocomplete
                    value={address}
                    onChange={setAddress}
                    placeholder="Nhập địa chỉ (có gợi ý tự động)..."
                    disabled={saving}
                  />
                ) : (
                  <p className="text-[#1e3a8a]">
                    {seller.address || "-"}
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
                    {seller.description || "-"}
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
                    className={`px-2 py-1 text-xs font-bold italic rounded text-white ${isActive ? "bg-[#10b981]" : "bg-[#6b7280]"
                      }`}
                  >
                    {seller.status}
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

          {/* Ghi chú sử dụng nhà cung cấp */}
          <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6">
            <h2 className="text-[18px] font-bold italic text-[#1e3a8a] mb-4">
              Ghi chú sử dụng
            </h2>
            <p className="text-sm text-[#6b7280]">
              Nhà cung cấp này sẽ xuất hiện trong các dropdown chọn **người bán /
              nhà cung cấp** ở màn Hóa đơn, Phiếu nhập, Thanh toán... Khi trạng
              thái chuyển sang Inactive, nhà cung cấp sẽ không còn xuất hiện ở
              các màn tạo mới nhưng dữ liệu chứng từ cũ vẫn được giữ nguyên.
            </p>
          </div>
        </div>
      </div>
    </>
  );
}

