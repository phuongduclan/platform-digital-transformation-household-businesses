"use client";

import { useEffect, useMemo, useState } from "react";
import { CatalogBaseItem, CatalogTable } from "../CatalogTable";
import {
  ownerService,
  OwnerCategory,
  OwnerProduct,
} from "@/services/owner.service";
import { showToast } from "@/components/ui/toast";
import LoadingOverlay from "@/components/ui/loading-overlay";

interface ProductFormState {
  id?: number;
  category_id: number | "";
  name: string;
  image_url: string;
  description: string;
  status: "ACTIVE" | "INACTIVE";
}

export default function OwnerProductsPage() {
  const [products, setProducts] = useState<OwnerProduct[]>([]);
  const [categories, setCategories] = useState<OwnerCategory[]>([]);
  const [loading, setLoading] = useState(true);
  const [modalOpen, setModalOpen] = useState(false);
  const [saving, setSaving] = useState(false);
  const [viewProduct, setViewProduct] = useState<OwnerProduct | null>(null);
  const [form, setForm] = useState<ProductFormState>({
    category_id: "",
    name: "",
    image_url: "",
    description: "",
    status: "ACTIVE",
  });

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [cats, prods] = await Promise.all([
        ownerService.listCategories(),
        ownerService.listProducts(),
      ]);
      setCategories(cats);
      setProducts(prods);
    } catch (error: any) {
      showToast(
        error?.response?.data?.error ||
          error?.message ||
          "Lỗi khi tải sản phẩm",
        "error"
      );
    } finally {
      setLoading(false);
    }
  };

  const categoryMap = useMemo(() => {
    const m = new Map<number, string>();
    categories.forEach((c) => m.set(c.id, c.name));
    return m;
  }, [categories]);

  const mappedItems: CatalogBaseItem[] = products.map((p) => ({
    id: p.id,
    name: p.name,
    code: undefined,
    typeLabel: categoryMap.get(p.category_id) || "Không có danh mục",
    status: p.status,
    created_at: p.created_at,
  }));

  const openCreate = () => {
    setForm({
      id: undefined,
      category_id: "",
      name: "",
      image_url: "",
      description: "",
      status: "ACTIVE",
    });
    setModalOpen(true);
  };

  const openEdit = (item: CatalogBaseItem) => {
    const found = products.find((p) => p.id === item.id);
    if (!found) return;
    setForm({
      id: found.id,
      category_id: found.category_id,
      name: found.name,
      image_url: found.image_url || "",
      description: found.description || "",
      status: (found.status as "ACTIVE" | "INACTIVE") || "ACTIVE",
    });
    setModalOpen(true);
  };

  const openView = (item: CatalogBaseItem) => {
    const found = products.find((p) => p.id === item.id);
    if (!found) return;
    setViewProduct(found);
  };

  const handleDelete = async (item: CatalogBaseItem) => {
    if (!confirm("Bạn có chắc chắn muốn xóa sản phẩm này?")) return;
    try {
      await ownerService.deleteProduct(item.id);
      showToast("Xóa sản phẩm thành công", "success");
      fetchData();
    } catch (error: any) {
      showToast(
        error?.response?.data?.error ||
          error?.message ||
          "Lỗi khi xóa sản phẩm",
        "error"
      );
    }
  };

  const handleSave = async () => {
    if (!form.category_id) {
      showToast("Vui lòng chọn danh mục", "error");
      return;
    }
    if (!form.name.trim()) {
      showToast("Tên sản phẩm không được để trống", "error");
      return;
    }

    try {
      setSaving(true);
      const payload = {
        category_id:
          typeof form.category_id === "string"
            ? Number(form.category_id)
            : form.category_id,
        name: form.name.trim(),
        image_url: form.image_url.trim() || undefined,
        description: form.description.trim() || undefined,
        status: form.status,
      };

      if (form.id) {
        await ownerService.updateProduct(form.id, payload);
        showToast("Cập nhật sản phẩm thành công", "success");
      } else {
        await ownerService.createProduct(payload);
        showToast("Tạo sản phẩm mới thành công", "success");
      }
      setModalOpen(false);
      fetchData();
    } catch (error: any) {
      showToast(
        error?.response?.data?.error ||
          error?.message ||
          "Lỗi khi lưu sản phẩm",
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
        message="Đang lưu sản phẩm..."
      />
      <CatalogTable
        title="Sản phẩm"
        createLabel="Tạo sản phẩm"
        items={mappedItems}
        loading={loading}
        onRefresh={fetchData}
        onCreate={openCreate}
        onView={openView}
        onEdit={openEdit}
        onDelete={handleDelete}
      />

      {modalOpen && (
        <div className="fixed inset-0 z-40 flex items-center justify-center bg-black/30">
          <div className="bg-white rounded-2xl shadow-xl border border-slate-200 w-full max-w-2xl p-6">
            <h2 className="text-[20px] font-bold italic text-[#1e3a8a] mb-4">
              {form.id ? "Chỉnh sửa sản phẩm" : "Tạo sản phẩm mới"}
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="md:col-span-2">
                <label className="block text-sm font-normal text-[#1e3a8a] mb-1.5">
                  Danh mục <span className="text-red-600">*</span>
                </label>
                <select
                  value={form.category_id}
                  onChange={(e) =>
                    setForm((prev) => ({
                      ...prev,
                      category_id: e.target.value
                        ? Number(e.target.value)
                        : "",
                    }))
                  }
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#00897b] focus:border-transparent"
                >
                  <option value="">Chọn danh mục</option>
                  {categories
                    .filter(
                      (c) => (c.status || "").toUpperCase() === "ACTIVE"
                    )
                    .map((c) => (
                    <option key={c.id} value={c.id}>
                      {c.name}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-normal text-[#1e3a8a] mb-1.5">
                  Tên sản phẩm <span className="text-red-600">*</span>
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
                  Ảnh (URL)
                </label>
                <input
                  type="text"
                  value={form.image_url}
                  onChange={(e) =>
                    setForm((prev) => ({
                      ...prev,
                      image_url: e.target.value,
                    }))
                  }
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#00897b] focus:border-transparent"
                  placeholder="Nhập đường dẫn ảnh (tùy chọn)"
                />
              </div>

              <div className="md:col-span-2">
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

      {/* View product modal */}
      {viewProduct && (
        <div className="fixed inset-0 z-30 flex items-center justify-center bg-black/40">
          <div className="bg-gradient-to-br from-slate-50 via-white to-slate-100 rounded-2xl shadow-2xl border border-slate-200 w-full max-w-3xl p-7">
            <div className="flex items-center justify-between mb-5">
              <div>
                <h2 className="text-[24px] font-bold italic text-[#1e3a8a]">
                  Thông tin sản phẩm
                </h2>
                <p className="mt-1 text-xs text-[#6b7280]">
                  Xem nhanh hình ảnh, danh mục và mô tả chi tiết của sản phẩm.
                </p>
              </div>
              <span className="px-3 py-1 rounded-full bg-[#e0f2f1] text-xs font-bold italic text-[#00897b]">
                ID: {viewProduct.id}
              </span>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="flex items-center justify-center bg-white rounded-xl p-4 shadow-inner border border-slate-200">
                {viewProduct.image_url ? (
                  // eslint-disable-next-line @next/next/no-img-element
                  <img
                    src={viewProduct.image_url}
                    alt={viewProduct.name}
                    className="max-h-72 w-auto object-contain rounded-md shadow-md"
                  />
                ) : (
                  <p className="text-sm text-[#9ca3af] text-center">
                    Chưa có hình ảnh sản phẩm
                  </p>
                )}
              </div>

              <div className="space-y-4">
                <div>
                  <p className="text-xs text-[#6b7280] mb-1 uppercase tracking-wide">
                    Tên sản phẩm
                  </p>
                  <p className="text-lg font-bold italic text-[#1e3a8a]">
                    {viewProduct.name}
                  </p>
                </div>
                <div>
                  <p className="text-xs text-[#6b7280] mb-1 uppercase tracking-wide">
                    Danh mục
                  </p>
                  <p className="text-sm text-[#1e3a8a]">
                    {categoryMap.get(viewProduct.category_id) ||
                      `ID: ${viewProduct.category_id}`}
                  </p>
                </div>
                <div>
                  <p className="text-xs text-[#6b7280] mb-1 uppercase tracking-wide">
                    Trạng thái
                  </p>
                  <span
                    className={`inline-flex px-3 py-1 text-xs font-bold italic rounded-full text-white ${
                      (viewProduct.status || "").toUpperCase() === "ACTIVE"
                        ? "bg-[#10b981]"
                        : "bg-[#6b7280]"
                    }`}
                  >
                    {viewProduct.status}
                  </span>
                </div>
              </div>
              <div className="md:col-span-2">
                <p className="text-xs text-[#6b7280] mb-1 uppercase tracking-wide">
                  Mô tả
                </p>
                <p className="text-sm text-[#1f2933] whitespace-pre-line bg-white rounded-xl border border-slate-200 p-4 shadow-sm min-h-[72px]">
                  {viewProduct.description || "Chưa có mô tả cho sản phẩm này."}
                </p>
              </div>
            </div>

            <div className="mt-6 flex items-center justify-end">
              <button
                type="button"
                onClick={() => setViewProduct(null)}
                className="px-6 py-2 bg-[#00897b] text-white rounded-lg text-sm font-bold hover:bg-[#007a6c] transition-colors shadow-md"
              >
                Đóng
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}

