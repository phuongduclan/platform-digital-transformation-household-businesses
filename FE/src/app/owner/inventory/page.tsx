"use client";

import { useEffect, useMemo, useState } from "react";
import {
  ownerService,
  OwnerInventory,
  OwnerProduct,
  OwnerUnit,
  OwnerWarehouse,
} from "@/services/owner.service";
import LoadingOverlay from "@/components/ui/loading-overlay";
import { showToast } from "@/components/ui/toast";

interface InventoryDetailState {
  inventory: OwnerInventory;
  product?: OwnerProduct;
  unit?: OwnerUnit;
  warehouse?: OwnerWarehouse;
}

export default function OwnerInventoryPage() {
  const [inventory, setInventory] = useState<OwnerInventory[]>([]);
  const [products, setProducts] = useState<OwnerProduct[]>([]);
  const [units, setUnits] = useState<OwnerUnit[]>([]);
  const [warehouses, setWarehouses] = useState<OwnerWarehouse[]>([]);
  const [loading, setLoading] = useState(true);
  const [detail, setDetail] = useState<InventoryDetailState | null>(null);

  const [selectedWarehouse, setSelectedWarehouse] = useState<number | "">("");
  const [selectedCategory, setSelectedCategory] = useState<number | "">("");
  const [searchTerm, setSearchTerm] = useState("");

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [inv, prods, uns, whs] = await Promise.all([
        ownerService.listInventory(),
        ownerService.listProducts(), // dùng cho mapping + filter, dữ liệu đã isolated theo household
        ownerService.listUnits(),
        ownerService.listWarehouses(),
      ]);
      setInventory(inv);
      setProducts(prods);
      setUnits(uns);
      setWarehouses(whs);
    } catch (error: any) {
      showToast(
        error?.response?.data?.error ||
          error?.message ||
          "Lỗi khi tải tồn kho",
        "error"
      );
    } finally {
      setLoading(false);
    }
  };

  const productMap = useMemo(() => {
    const m = new Map<number, OwnerProduct>();
    products.forEach((p) => m.set(p.id, p));
    return m;
  }, [products]);

  const unitMap = useMemo(() => {
    const m = new Map<number, OwnerUnit>();
    units.forEach((u) => m.set(u.id, u));
    return m;
  }, [units]);

  const warehouseMap = useMemo(() => {
    const m = new Map<number, OwnerWarehouse>();
    warehouses.forEach((w) => m.set(w.id, w));
    return m;
  }, [warehouses]);

  const categoryMap = useMemo(() => {
    const m = new Map<number, number | null>(); // product_id -> category_id
    products.forEach((p) => m.set(p.id, (p as any).category_id ?? null));
    return m;
  }, [products]);

  const filteredInventory = useMemo(() => {
    const term = searchTerm.trim().toLowerCase();
    return inventory.filter((item) => {
      const prod = productMap.get(item.product_id);
      const wh = warehouseMap.get(item.warehouse_id);
      const catId = categoryMap.get(item.product_id) ?? null;

      if (selectedWarehouse && item.warehouse_id !== selectedWarehouse)
        return false;
      if (selectedCategory && catId !== selectedCategory) return false;

      if (!term) return true;
      const name = prod?.name?.toLowerCase() || "";
      const whName = wh?.name?.toLowerCase() || "";
      return name.includes(term) || whName.includes(term);
    });
  }, [
    inventory,
    productMap,
    warehouseMap,
    categoryMap,
    selectedWarehouse,
    selectedCategory,
    searchTerm,
  ]);

  const handleRowClick = async (row: OwnerInventory) => {
    try {
      const invDetail = await ownerService.getInventoryDetail(
        row.product_id,
        row.warehouse_id,
        { unit_id: row.unit_id }
      );
      setDetail({
        inventory: invDetail,
        product: productMap.get(invDetail.product_id),
        unit: unitMap.get(invDetail.unit_id),
        warehouse: warehouseMap.get(invDetail.warehouse_id),
      });
    } catch (error: any) {
      showToast(
        error?.response?.data?.error ||
          error?.message ||
          "Lỗi khi tải chi tiết tồn kho",
        "error"
      );
    }
  };

  const formatNumber = (value: number) =>
    new Intl.NumberFormat("vi-VN").format(value);

  return (
    <>
      <LoadingOverlay
        isLoading={loading}
        message="Đang tải tồn kho..."
      />
      <div className="p-8">
        <h1 className="text-[28px] font-bold italic text-[#1e3a8a] mb-4">
          Tồn kho
        </h1>

        {/* Filters */}
        <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6 mb-6">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="md:col-span-2">
              <label className="block text-sm font-normal text-[#1e3a8a] mb-1.5">
                Tìm theo tên sản phẩm hoặc kho
              </label>
              <input
                type="text"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#00897b] focus:border-transparent"
                placeholder="Nhập từ khóa tìm kiếm..."
              />
            </div>
            <div>
              <label className="block text-sm font-normal text-[#1e3a8a] mb-1.5">
                Kho
              </label>
              <select
                value={selectedWarehouse}
                onChange={(e) =>
                  setSelectedWarehouse(
                    e.target.value ? Number(e.target.value) : ""
                  )
                }
                className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#00897b] focus:border-transparent"
              >
                <option value="">Tất cả kho</option>
                {warehouses
                  .filter(
                    (w) => (w.status || "").toUpperCase() === "ACTIVE"
                  )
                  .map((w) => (
                  <option key={w.id} value={w.id}>
                    {w.name}
                  </option>
                ))}
              </select>
            </div>
            <div>
              <label className="block text-sm font-normal text-[#1e3a8a] mb-1.5">
                Danh mục
              </label>
              <select
                value={selectedCategory}
                onChange={(e) =>
                  setSelectedCategory(
                    e.target.value ? Number(e.target.value) : ""
                  )
                }
                className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#00897b] focus:border-transparent"
              >
                <option value="">Tất cả danh mục</option>
                {Array.from(
                  new Map(
                    products.map((p) => [
                      (p as any).category_id,
                      (p as any).category_id,
                    ])
                  ).entries()
                )
                  .filter(([id]) => id)
                  .map(([id]) => (
                    <option key={id} value={id as number}>
                      Danh mục #{id}
                    </option>
                  ))}
              </select>
            </div>
          </div>
        </div>

        {/* Inventory table + detail panel */}
        <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
          {/* Table */}
          <div className="xl:col-span-2 bg-white rounded-lg shadow-sm border border-slate-200 overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-slate-50 border-b border-slate-200">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-bold italic text-[#4b5563] uppercase tracking-wider">
                      Sản phẩm
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-bold italic text-[#4b5563] uppercase tracking-wider">
                      Kho
                    </th>
                    <th className="px-6 py-3 text-right text-xs font-bold italic text-[#4b5563] uppercase tracking-wider">
                      Số lượng tồn
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-bold italic text-[#4b5563] uppercase tracking-wider">
                      Đơn vị
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-slate-200">
                  {filteredInventory.length === 0 ? (
                    <tr>
                      <td
                        colSpan={4}
                        className="px-6 py-8 text-center text-sm text-[#6b7280]"
                      >
                        Không có dữ liệu tồn kho
                      </td>
                    </tr>
                  ) : (
                    filteredInventory.map((row) => {
                      const prod = productMap.get(row.product_id);
                      const wh = warehouseMap.get(row.warehouse_id);
                      const unit = unitMap.get(row.unit_id);
                      return (
                        <tr
                          key={row.id}
                          className="hover:bg-slate-50 cursor-pointer"
                          onClick={() => handleRowClick(row)}
                        >
                          <td className="px-6 py-3 text-sm text-[#1e3a8a]">
                            {prod?.name || `SP #${row.product_id}`}
                          </td>
                          <td className="px-6 py-3 text-sm text-[#1e3a8a]">
                            {wh?.name || `Kho #${row.warehouse_id}`}
                          </td>
                          <td className="px-6 py-3 text-sm text-right text-[#1e3a8a]">
                            {formatNumber(row.quantity)}
                          </td>
                          <td className="px-6 py-3 text-sm text-[#1e3a8a]">
                            {unit?.name || "-"}
                          </td>
                        </tr>
                      );
                    })
                  )}
                </tbody>
              </table>
            </div>
          </div>

          {/* Detail panel */}
          <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6 min-h-[220px]">
            <h2 className="text-[18px] font-bold italic text-[#1e3a8a] mb-4">
              Chi tiết tồn kho
            </h2>
            {!detail ? (
              <p className="text-sm text-[#6b7280]">
                Chọn một dòng trong bảng để xem chi tiết tồn kho sản phẩm theo
                kho.
              </p>
            ) : (
              <div className="space-y-3 text-sm">
                <div>
                  <p className="text-xs text-[#6b7280] mb-1">Sản phẩm</p>
                  <p className="text-base font-bold text-[#1e3a8a]">
                    {detail.product?.name || `SP #${detail.inventory.product_id}`}
                  </p>
                </div>
                <div>
                  <p className="text-xs text-[#6b7280] mb-1">Kho</p>
                  <p className="text-sm text-[#1e3a8a]">
                    {detail.warehouse?.name ||
                      `Kho #${detail.inventory.warehouse_id}`}
                  </p>
                </div>
                <div>
                  <p className="text-xs text-[#6b7280] mb-1">Đơn vị</p>
                  <p className="text-sm text-[#1e3a8a]">
                    {detail.unit?.name || `Đơn vị #${detail.inventory.unit_id}`}
                  </p>
                </div>
                <div>
                  <p className="text-xs text-[#6b7280] mb-1">Số lượng tồn</p>
                  <p className="text-base font-bold text-[#1e3a8a]">
                    {formatNumber(detail.inventory.quantity)}
                  </p>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </>
  );
}

