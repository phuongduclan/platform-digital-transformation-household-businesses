"use client";

import { useEffect, useState } from "react";
import { CatalogBaseItem, CatalogTable } from "../CatalogTable";
import { ownerService, OwnerCategory } from "@/services/owner.service";
import { showToast } from "@/components/ui/toast";
import LoadingOverlay from "@/components/ui/loading-overlay";

interface CategoryFormState {
  id?: number;
  name: string;
  description: string;
  status: "ACTIVE" | "INACTIVE";
}

export default function OwnerCategoriesPage() {
  const [categories, setCategories] = useState<OwnerCategory[]>([]);
  const [loading, setLoading] = useState(true);
  const [modalOpen, setModalOpen] = useState(false);
  const [saving, setSaving] = useState(false);
  const [form, setForm] = useState<CategoryFormState>({
    name: "",
    description: "",
    status: "ACTIVE",
  });

  useEffect(() => {
    fetchCategories();
  }, []);

  const fetchCategories = async () => {
    try {
      setLoading(true);
      const data = await ownerService.listCategories();
      setCategories(data);
    } catch (error: any) {
      showToast(
        error?.response?.data?.error ||
          error?.message ||
          "Lỗi khi tải danh mục hàng",
        "error"
      );
    } finally {
      setLoading(false);
    }
  };

  const mappedItems: CatalogBaseItem[] = categories.map((c) => ({
    id: c.id,
    name: c.name,
    code: undefined,
    typeLabel: "Danh mục",
    status: c.status,
    created_at: c.created_at,
  }));

  const openCreate = () => {
    setForm({
      id: undefined,
      name: "",
      description: "",
      status: "ACTIVE",
    });
    setModalOpen(true);
  };

  const openEdit = (item: CatalogBaseItem) => {
    const found = categories.find((c) => c.id === item.id);
    if (!found) return;
    setForm({
      id: found.id,
      name: found.name,
      description: found.description || "",
      status: (found.status as "ACTIVE" | "INACTIVE") || "ACTIVE",
    });
    setModalOpen(true);
  };

  const handleDelete = async (item: CatalogBaseItem) => {
    if (!confirm("Bạn có chắc chắn muốn xóa danh mục này?")) return;
    try {
      await ownerService.deleteCategory(item.id);
      showToast("Xóa danh mục thành công", "success");
      fetchCategories();
    } catch (error: any) {
      showToast(
        error?.response?.data?.error ||
          error?.message ||
          "Lỗi khi xóa danh mục",
        "error"
      );
    }
  };

  const handleSave = async () => {
    if (!form.name.trim()) {
      showToast("Tên danh mục không được để trống", "error");
      return;
    }

    try {
      setSaving(true);
      if (form.id) {
        await ownerService.updateCategory(form.id, {
          name: form.name.trim(),
          description: form.description.trim() || undefined,
          status: form.status,
        });
        showToast("Cập nhật danh mục thành công", "success");
      } else {
        await ownerService.createCategory({
          name: form.name.trim(),
          description: form.description.trim() || undefined,
          status: form.status,
        });
        showToast("Tạo danh mục mới thành công", "success");
      }
      setModalOpen(false);
      fetchCategories();
    } catch (error: any) {
      showToast(
        error?.response?.data?.error ||
          error?.message ||
          "Lỗi khi lưu danh mục",
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
        message="Đang lưu danh mục..."
      />
      <CatalogTable
        title="Danh mục hàng"
        createLabel="Tạo danh mục"
        items={mappedItems}
        loading={loading}
        onRefresh={fetchCategories}
        onCreate={openCreate}
        onEdit={openEdit}
        onDelete={handleDelete}
      />

      {/* Slide-over / modal đơn giản */}
      {modalOpen && (
        <div className="fixed inset-0 z-40 flex items-center justify-center bg-black/30">
          <div className="bg-white rounded-2xl shadow-xl border border-slate-200 w-full max-w-lg p-6">
            <h2 className="text-[20px] font-bold italic text-[#1e3a8a] mb-4">
              {form.id ? "Chỉnh sửa danh mục" : "Tạo danh mục mới"}
            </h2>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-normal text-[#1e3a8a] mb-1.5">
                  Tên danh mục <span className="text-red-600">*</span>
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

