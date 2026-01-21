"use client";

import { useEffect, useMemo, useState } from "react";
import { ownerService, OwnerWarehouse, OwnerInventory } from "@/services/owner.service";
import LoadingOverlay from "@/components/ui/loading-overlay";
import { showToast } from "@/components/ui/toast";

interface WarehouseFormState {
  id?: number;
  name: string;
  address: string;
  description: string;
  status: "ACTIVE" | "INACTIVE";
}

export default function OwnerWarehousesPage() {
  const [warehouses, setWarehouses] = useState<OwnerWarehouse[]>([]);
  const [inventory, setInventory] = useState<OwnerInventory[]>([]);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [modalOpen, setModalOpen] = useState(false);
  const [form, setForm] = useState<WarehouseFormState>({
    name: "",
    address: "",
    description: "",
    status: "ACTIVE",
  });

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [whs, inv] = await Promise.all([
        ownerService.listWarehouses(),
        ownerService.listInventory(),
      ]);
      setWarehouses(whs);
      setInventory(inv);
    } catch (error: any) {
      showToast(
        error?.response?.data?.error ||
          error?.message ||
          "Lỗi khi tải danh sách kho",
        "error"
      );
    } finally {
      setLoading(false);
    }
  };

  const productCountByWarehouse = useMemo(() => {
    const map = new Map<number, number>();
    inventory.forEach((inv) => {
      const setKey = `${inv.warehouse_id}-${inv.product_id}`;
      // tạm dùng Set logic bằng Map<string,boolean> để đếm distinct
      const current = map.get(inv.warehouse_id) || 0;
      map.set(inv.warehouse_id, current + 1);
    });
    return map;
  }, [inventory]);

  const openCreate = () => {
    setForm({
      id: undefined,
      name: "",
      address: "",
      description: "",
      status: "ACTIVE",
    });
    setModalOpen(true);
  };

  const openEdit = (w: OwnerWarehouse) => {
    setForm({
      id: w.id,
      name: w.name,
      address: w.address,
      description: w.description || "",
      status: (w.status as "ACTIVE" | "INACTIVE") || "ACTIVE",
    });
    setModalOpen(true);
  };

  const handleDelete = async (w: OwnerWarehouse) => {
    if (!confirm("Bạn có chắc chắn muốn xóa kho này?")) return;
    try {
      await ownerService.deleteWarehouse(w.id);
      showToast("Xóa kho hàng thành công", "success");
      fetchData();
    } catch (error: any) {
      showToast(
        error?.response?.data?.error ||
          error?.message ||
          "Lỗi khi xóa kho hàng",
        "error"
      );
    }
  };

  const handleSave = async () => {
    if (!form.name.trim()) {
      showToast("Tên kho không được để trống", "error");
      return;
    }
    if (!form.address.trim()) {
      showToast("Địa chỉ kho không được để trống", "error");
      return;
    }

    try {
      setSaving(true);
      const payload = {
        name: form.name.trim(),
        address: form.address.trim(),
        description: form.description.trim() || undefined,
        status: form.status,
      };
      if (form.id) {
        await ownerService.updateWarehouse(form.id, payload);
        showToast("Cập nhật kho hàng thành công", "success");
      } else {
        await ownerService.createWarehouse(payload);
        showToast("Tạo kho hàng mới thành công", "success");
      }
      setModalOpen(false);
      fetchData();
    } catch (error: any) {
      showToast(
        error?.response?.data?.error ||
          error?.message ||
          "Lỗi khi lưu kho hàng",
        "error"
      );
    } finally {
      setSaving(false);
    }
  };

  return (
    <>
      <LoadingOverlay
        isLoading={saving}
        message="Đang lưu kho hàng..."
      />
      <div className="p-8">
        <div className="mb-6 flex items-center justify-between">
          <h1 className="text-[28px] font-bold italic text-[#1e3a8a]">
            Kho hàng
          </h1>
          <button
            type="button"
            onClick={openCreate}
            className="px-4 py-2 bg-[#00897b] text-white rounded-lg hover:bg-[#007a6c] transition-colors font-bold italic text-base flex items-center gap-2"
          >
            <span>+</span>
            <span>Tạo kho mới</span>
          </button>
        </div>

        {/* Warehouse cards / table */}
        <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6">
          {loading ? (
            <p className="text-sm text-[#6b7280]">Đang tải dữ liệu...</p>
          ) : warehouses.length === 0 ? (
            <p className="text-sm text-[#6b7280]">Chưa có kho hàng nào.</p>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
              {warehouses.map((w) => {
                const productCount = productCountByWarehouse.get(w.id) || 0;
                const isActive = (w.status || "").toUpperCase() === "ACTIVE";
                return (
                  <div
                    key={w.id}
                    className="rounded-xl border border-slate-200 bg-slate-50 hover:bg-slate-100 transition-colors shadow-sm p-4 flex flex-col justify-between"
                  >
                    <div>
                      <div className="flex items-center justify-between mb-2">
                        <h2 className="text-[18px] font-bold italic text-[#1e3a8a]">
                          {w.name}
                        </h2>
                        <span
                          className={`px-2 py-1 text-xs font-bold italic rounded-full text-white ${
                            isActive ? "bg-[#10b981]" : "bg-[#6b7280]"
                          }`}
                        >
                          {w.status}
                        </span>
                      </div>
                      <p className="text-xs text-[#6b7280] mb-1">
                        ID kho: {w.id}
                      </p>
                      <p className="text-sm text-[#1f2933] mb-2">
                        {w.address}
                      </p>
                      {w.description && (
                        <p className="text-xs text-[#4b5563]">
                          {w.description}
                        </p>
                      )}
                    </div>
                    <div className="mt-4 flex items-center justify-between">
                      <p className="text-xs text-[#6b7280]">
                        Số sản phẩm đang quản lý:
                        <span className="ml-1 font-bold text-[#1e3a8a]">
                          {productCount}
                        </span>
                      </p>
                      <div className="flex items-center gap-2">
                        <button
                          type="button"
                          onClick={() => openEdit(w)}
                          className="px-3 py-1 text-xs text-[#1e3a8a] hover:text-[#00897b] transition-colors border border-[#1e3a8a] rounded hover:border-[#00897b]"
                        >
                          Chỉnh sửa
                        </button>
                        <button
                          type="button"
                          onClick={() => handleDelete(w)}
                          className="px-3 py-1 text-xs text-red-600 hover:text-red-700 transition-colors border border-red-600 rounded hover:border-red-700"
                        >
                          Xóa
                        </button>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>
      </div>

      {/* Modal create/edit */}
      {modalOpen && (
        <div className="fixed inset-0 z-40 flex items-center justify-center bg-black/30">
          <div className="bg-white rounded-2xl shadow-xl border border-slate-200 w-full max-w-lg p-6">
            <h2 className="text-[20px] font-bold italic text-[#1e3a8a] mb-4">
              {form.id ? "Chỉnh sửa kho hàng" : "Tạo kho hàng mới"}
            </h2>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-normal text-[#1e3a8a] mb-1.5">
                  Tên kho <span className="text-red-600">*</span>
                </label>
                <input
                  type="text"
                  value={form.name}
                  onChange={(e) =>
                    setForm((prev) => ({ ...prev, name: e.target.value }))
                  }
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#00897b] focus:border-transparent"
                />
              </div>
              <div>
                <label className="block text-sm font-normal text-[#1e3a8a] mb-1.5">
                  Địa chỉ <span className="text-red-600">*</span>
                </label>
                <input
                  type="text"
                  value={form.address}
                  onChange={(e) =>
                    setForm((prev) => ({ ...prev, address: e.target.value }))
                  }
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#00897b] focus:border-transparent"
                />
              </div>
              <div>
                <label className="block text-sm font-normal text-[#1e3a8a] mb-1.5">
                  Mô tả
                </label>
                <textarea
                  value={form.description}
                  onChange={(e) =>
                    setForm((prev) => ({
                      ...prev,
                      description: e.target.value,
                    }))
                  }
                  rows={3}
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#00897b] focus:border-transparent"
                />
              </div>
              <div>
                <label className="block text-sm font-normal text-[#1e3a8a] mb-1.5">
                  Trạng thái
                </label>
                <select
                  value={form.status}
                  onChange={(e) =>
                    setForm((prev) => ({
                      ...prev,
                      status: e.target.value as "ACTIVE" | "INACTIVE",
                    }))
                  }
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#00897b] focus:border-transparent"
                >
                  <option value="ACTIVE">ACTIVE</option>
                  <option value="INACTIVE">INACTIVE</option>
                </select>
              </div>
            </div>

            <div className="mt-6 flex items-center justify-end gap-3">
              <button
                type="button"
                onClick={() => setModalOpen(false)}
                className="px-4 py-2 bg-white border border-slate-300 text-sm rounded-lg hover:bg-slate-50 transition-colors"
              >
                Hủy
              </button>
              <button
                type="button"
                onClick={handleSave}
                disabled={saving}
                className="px-6 py-2 bg-[#00897b] text-white rounded-lg text-sm font-bold hover:bg-[#007a6c] transition-colors disabled:bg-slate-400 disabled:cursor-not-allowed"
              >
                {saving ? "Đang lưu..." : "Lưu"}
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}

