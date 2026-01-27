"use client";

import { useEffect, useMemo, useState } from "react";
import { useRouter } from "next/navigation";
import LoadingOverlay from "@/components/ui/loading-overlay";
import { showToast } from "@/components/ui/toast";
import {
  ownerService,
  OwnerProduct,
  OwnerUnit,
  OwnerInvoice,
  OwnerCustomer,
  OwnerSeller,
} from "@/services/owner.service";

interface InvoiceLineForm {
  id?: number; // local id, BE detail id when editing
  product_id: number | "";
  unit_id: number | "";
  quantity: number | "";
  price: number | "";
  vat: number | "";
  discount: number | "";
  description: string;
}

export default function OwnerCreateInvoicePage() {
  const router = useRouter();
  const [products, setProducts] = useState<OwnerProduct[]>([]);
  const [units, setUnits] = useState<OwnerUnit[]>([]);
  const [customers, setCustomers] = useState<OwnerCustomer[]>([]);
  const [sellers, setSellers] = useState<OwnerSeller[]>([]);
  const [saving, setSaving] = useState(false);

  const [sellerId, setSellerId] = useState<number | "">("");
  const [customerId, setCustomerId] = useState<number | "">("");
  const [invoiceType, setInvoiceType] = useState<"PAID" | "UNPAID">("PAID");
  const [description, setDescription] = useState("");

  const [lines, setLines] = useState<InvoiceLineForm[]>([
    { product_id: "", unit_id: "", quantity: "", price: "", vat: "", discount: "", description: "" },
  ]);

  useEffect(() => {
    fetchMeta();
  }, []);

  const fetchMeta = async () => {
    try {
      const [prods, uns, custs, sels] = await Promise.all([
        ownerService.listProducts(),
        ownerService.listUnits(),
        ownerService.listCustomers({ status: "Active" }),
        ownerService.listSellers({ status: "Active" }),
      ]);
      setProducts(prods);
      setUnits(uns);
      setCustomers(custs);
      setSellers(sels);
    } catch (error: any) {
      showToast(
        error?.response?.data?.error ||
        error?.message ||
        "Lỗi khi tải dữ liệu sản phẩm/đơn vị",
        "error"
      );
    }
  };

  const addLine = () => {
    setLines((prev) => [
      ...prev,
      {
        product_id: "",
        unit_id: "",
        quantity: "",
        price: "",
        vat: "",
        discount: "",
        description: "",
      },
    ]);
  };

  const updateLine = (index: number, patch: Partial<InvoiceLineForm>) => {
    setLines((prev) =>
      prev.map((l, i) => (i === index ? { ...l, ...patch } : l))
    );
  };

  const removeLine = (index: number) => {
    setLines((prev) => prev.filter((_, i) => i !== index));
  };

  const totalAmount = useMemo(() => {
    return lines.reduce((sum, l) => {
      const qty = Number(l.quantity || 0);
      const price = Number(l.price || 0);
      const discount = Number(l.discount || 0);
      const vat = Number(l.vat || 0);
      const lineBase = qty * price;
      const lineDiscount = (lineBase * discount) / 100;
      const afterDiscount = lineBase - lineDiscount;
      const lineVat = (afterDiscount * vat) / 100;
      return sum + afterDiscount + lineVat;
    }, 0);
  }, [lines]);

  const handleSubmit = async () => {
    if (lines.length === 0) {
      showToast("Hóa đơn phải có ít nhất 1 dòng hàng", "error");
      return;
    }

    for (const l of lines) {
      if (!l.product_id || !l.unit_id || !l.quantity || !l.price) {
        showToast(
          "Mỗi dòng hàng cần chọn sản phẩm, đơn vị, số lượng và đơn giá",
          "error"
        );
        return;
      }
    }

    try {
      setSaving(true);
      const payload = {
        seller_id:
          sellerId === "" ? undefined : Number(sellerId) || null,
        customer_id:
          customerId === "" ? undefined : Number(customerId) || null,
        invoice_type: invoiceType,
        description: description.trim() || undefined,
        status: "Draft",
        details: lines.map((l) => ({
          product_id: Number(l.product_id),
          unit_id: Number(l.unit_id),
          quantity: Number(l.quantity),
          price: Number(l.price),
          vat: l.vat === "" ? 0 : Number(l.vat),
          discount: l.discount === "" ? 0 : Number(l.discount),
          description: l.description.trim() || undefined,
        })),
      };

      const created: OwnerInvoice = await ownerService.createInvoice(payload);
      showToast("Tạo hóa đơn nháp thành công", "success");
      // Sau khi lưu nháp, chuyển thẳng sang màn chi tiết hóa đơn như mong muốn
      router.push(`/owner/invoices/${created.id}`);
    } catch (error: any) {
      showToast("Tạo hóa đơn thất bại", "error");
    } finally {
      setSaving(false);
    }
  };

  const formatCurrency = (value: number) =>
    new Intl.NumberFormat("vi-VN", {
      maximumFractionDigits: 0,
    }).format(value);

  return (
    <>
      <LoadingOverlay
        isLoading={saving}
        message="Đang lưu hóa đơn..."
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
            onClick={() => router.push("/owner/invoices")}
            className="text-[#00897b] hover:underline"
          >
            Hóa đơn
          </button>
          <span className="text-[#4b5563]">/</span>
          <span className="text-[#4b5563]">Tạo mới</span>
        </div>

        {/* Header */}
        <div className="mb-6 flex items-center justify-between">
          <h1 className="text-[28px] font-bold italic text-[#1e3a8a]">
            Tạo hóa đơn
          </h1>
        </div>

        {/* Master + lines */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
          {/* Master */}
          <div className="lg:col-span-2 bg-white rounded-lg shadow-sm border border-slate-200 p-6">
            <h2 className="text-[18px] font-bold italic text-[#1e3a8a] mb-4">
              Thông tin chung
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-normal text-[#1e3a8a] mb-1.5">
                  Người bán
                </label>
                <select
                  value={sellerId}
                  onChange={(e) =>
                    setSellerId(
                      e.target.value === "" ? "" : Number(e.target.value)
                    )
                  }
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#00897b] focus:border-transparent"
                >
                  <option value="">Chọn người bán (hoặc để trống)</option>
                  {sellers.map((s) => (
                    <option key={s.id} value={s.id}>
                      {s.name} {s.tax_code ? `- MST: ${s.tax_code}` : ""}
                    </option>
                  ))}
                </select>
              </div>
              <div>
                <label className="block text-sm font-normal text-[#1e3a8a] mb-1.5">
                  Khách hàng
                </label>
                <select
                  value={customerId}
                  onChange={(e) => {
                    const val = e.target.value;
                    const next =
                      val === "" ? "" : (Number(val) as number | "");
                    setCustomerId(next);
                    if (next === "") {
                      setInvoiceType("PAID");
                    }
                  }}
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#00897b] focus:border-transparent"
                >
                  <option value="">Chọn khách hàng (hoặc để trống)</option>
                  {customers.map((c) => (
                    <option key={c.id} value={c.id}>
                      {c.name} {c.phone ? `- ${c.phone}` : ""}
                    </option>
                  ))}
                </select>
              </div>
              <div>
                <label className="block text-sm font-normal text-[#1e3a8a] mb-1.5">
                  Loại hóa đơn
                </label>
                <select
                  value={invoiceType}
                  onChange={(e) =>
                    setInvoiceType(e.target.value as "PAID" | "UNPAID")
                  }
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#00897b] focus:border-transparent"
                >
                  <option value="PAID">PAID</option>
                  <option value="UNPAID" disabled={!customerId}>
                    UNPAID
                  </option>
                </select>
              </div>
              <div className="md:col-span-2">
                <label className="block text-sm font-normal text-[#1e3a8a] mb-1.5">
                  Mô tả
                </label>
                <textarea
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  rows={3}
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-[#00897b] focus:border-transparent"
                />
              </div>
            </div>
          </div>

          {/* Summary */}
          <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6">
            <h2 className="text-[18px] font-bold italic text-[#1e3a8a] mb-4">
              Tạm tính
            </h2>
            <p className="text-sm text-[#4b5563] mb-2">
              Tổng tiền tạm tính (đã áp dụng VAT & chiết khấu):
            </p>
            <p className="text-2xl font-bold italic text-[#00897b]">
              {formatCurrency(totalAmount)}
            </p>
          </div>
        </div>

        {/* Lines table */}
        <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6 mb-6">
          <div className="mb-4 flex items-center justify-between">
            <h2 className="text-[18px] font-bold italic text-[#1e3a8a]">
              Dòng hàng
            </h2>
            <button
              type="button"
              onClick={addLine}
              className="px-3 py-1.5 text-xs bg-[#00897b] text-white rounded-lg hover:bg-[#007a6c] transition-colors font-bold"
            >
              + Thêm dòng
            </button>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-slate-50 border-b border-slate-200">
                <tr>
                  <th className="px-3 py-2 text-left text-xs font-bold italic text-[#4b5563] uppercase">
                    Sản phẩm
                  </th>
                  <th className="px-3 py-2 text-left text-xs font-bold italic text-[#4b5563] uppercase">
                    Đơn vị
                  </th>
                  <th className="px-3 py-2 text-right text-xs font-bold italic text-[#4b5563] uppercase">
                    SL
                  </th>
                  <th className="px-3 py-2 text-right text-xs font-bold italic text-[#4b5563] uppercase">
                    Đơn giá
                  </th>
                  <th className="px-3 py-2 text-right text-xs font-bold italic text-[#4b5563] uppercase">
                    VAT %
                  </th>
                  <th className="px-3 py-2 text-right text-xs font-bold italic text-[#4b5563] uppercase">
                    CK %
                  </th>
                  <th className="px-3 py-2 text-right text-xs font-bold italic text-[#4b5563] uppercase">
                    Thành tiền
                  </th>
                  <th className="px-3 py-2 text-left text-xs font-bold italic text-[#4b5563] uppercase">
                    Ghi chú
                  </th>
                  <th className="px-3 py-2" />
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-200">
                {lines.map((l, idx) => {
                  const qty = Number(l.quantity || 0);
                  const price = Number(l.price || 0);
                  const vat = Number(l.vat || 0);
                  const discount = Number(l.discount || 0);
                  const base = qty * price;
                  const discountAmount = (base * discount) / 100;
                  const afterDiscount = base - discountAmount;
                  const lineTotal = afterDiscount + (afterDiscount * vat) / 100;
                  return (
                    <tr key={idx}>
                      <td className="px-3 py-1.5">
                        <select
                          value={l.product_id}
                          onChange={(e) =>
                            updateLine(idx, {
                              product_id: e.target.value
                                ? Number(e.target.value)
                                : "",
                            })
                          }
                          className="w-full px-2 py-1 border border-slate-300 rounded text-xs focus:outline-none focus:ring-1 focus:ring-[#00897b]"
                        >
                          <option value="">Chọn sản phẩm</option>
                          {products
                            .filter(
                              (p) =>
                                (p.status || "").toUpperCase() === "ACTIVE"
                            )
                            .map((p) => (
                              <option key={p.id} value={p.id}>
                                {p.name}
                              </option>
                            ))}
                        </select>
                      </td>
                      <td className="px-3 py-1.5">
                        <select
                          value={l.unit_id}
                          onChange={(e) =>
                            updateLine(idx, {
                              unit_id: e.target.value
                                ? Number(e.target.value)
                                : "",
                            })
                          }
                          className="w-full px-2 py-1 border border-slate-300 rounded text-xs focus:outline-none focus:ring-1 focus:ring-[#00897b]"
                        >
                          <option value="">Chọn đơn vị</option>
                          {units
                            .filter(
                              (u) =>
                                (u.status || "").toUpperCase() === "ACTIVE"
                            )
                            .map((u) => (
                              <option key={u.id} value={u.id}>
                                {u.name}
                              </option>
                            ))}
                        </select>
                      </td>
                      <td className="px-3 py-1.5">
                        <input
                          type="number"
                          value={l.quantity}
                          onChange={(e) =>
                            updateLine(idx, {
                              quantity:
                                e.target.value === ""
                                  ? ""
                                  : Number(e.target.value),
                            })
                          }
                          className="w-full px-2 py-1 border border-slate-300 rounded text-xs text-right focus:outline-none focus:ring-1 focus:ring-[#00897b]"
                        />
                      </td>
                      <td className="px-3 py-1.5">
                        <input
                          type="number"
                          value={l.price}
                          onChange={(e) =>
                            updateLine(idx, {
                              price:
                                e.target.value === ""
                                  ? ""
                                  : Number(e.target.value),
                            })
                          }
                          className="w-full px-2 py-1 border border-slate-300 rounded text-xs text-right focus:outline-none focus:ring-1 focus:ring-[#00897b]"
                        />
                      </td>
                      <td className="px-3 py-1.5">
                        <input
                          type="number"
                          value={l.vat}
                          onChange={(e) =>
                            updateLine(idx, {
                              vat:
                                e.target.value === ""
                                  ? ""
                                  : Number(e.target.value),
                            })
                          }
                          className="w-full px-2 py-1 border border-slate-300 rounded text-xs text-right focus:outline-none focus:ring-1 focus:ring-[#00897b]"
                        />
                      </td>
                      <td className="px-3 py-1.5">
                        <input
                          type="number"
                          value={l.discount}
                          onChange={(e) =>
                            updateLine(idx, {
                              discount:
                                e.target.value === ""
                                  ? ""
                                  : Number(e.target.value),
                            })
                          }
                          className="w-full px-2 py-1 border border-slate-300 rounded text-xs text-right focus:outline-none focus:ring-1 focus:ring-[#00897b]"
                        />
                      </td>
                      <td className="px-3 py-1.5 text-right text-xs text-[#1e3a8a]">
                        {formatCurrency(lineTotal || 0)}
                      </td>
                      <td className="px-3 py-1.5">
                        <input
                          type="text"
                          value={l.description}
                          onChange={(e) =>
                            updateLine(idx, { description: e.target.value })
                          }
                          className="w-full px-2 py-1 border border-slate-300 rounded text-xs focus:outline-none focus:ring-1 focus:ring-[#00897b]"
                        />
                      </td>
                      <td className="px-3 py-1.5">
                        <button
                          type="button"
                          onClick={() => removeLine(idx)}
                          className="px-2 py-1 text-xs text-red-600 hover:text-red-700"
                        >
                          Xóa
                        </button>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>

        {/* Actions */}
        <div className="flex items-center justify-end gap-3">
          <button
            type="button"
            onClick={() => router.push("/owner/invoices")}
            className="px-5 py-2 bg-white border border-slate-300 text-sm rounded-lg hover:bg-slate-50 transition-colors"
          >
            Hủy
          </button>
          <button
            type="button"
            onClick={handleSubmit}
            disabled={saving}
            className="px-5 py-2 bg-slate-500 text-white rounded-lg text-sm font-bold hover:bg-slate-600 transition-colors disabled:bg-slate-400 disabled:cursor-not-allowed"
          >
            {saving ? "Đang lưu..." : "Lưu nháp"}
          </button>
        </div>
      </div>
    </>
  );
}

