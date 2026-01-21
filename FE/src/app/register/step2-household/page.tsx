"use client";

import { FormEvent, useState } from "react";
import { useRouter } from "next/navigation";
import { useRegistration } from "@/context/registration-context";
import { showToast } from "@/components/ui/toast";

export default function Step2HouseholdPage() {
  const router = useRouter();
  const { state, updateHousehold } = useRegistration();
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    setError(null);

    if (!state.household.name?.trim()) {
      setError("Vui lòng nhập tên hộ kinh doanh.");
      showToast("Vui lòng nhập tên hộ kinh doanh", "warning");
      return;
    }

    showToast("Thông tin hộ kinh doanh đã được lưu. Chuyển sang bước tiếp theo...", "success", 1500);
    setTimeout(() => {
      router.push("/register/step3-account");
    }, 1000);
  };

  return (
    <section>
      <div className="mb  -6">
        <h2 className="text-xl font-semibold text-slate-900">
          Thông tin hộ kinh doanh
        </h2>
        <p className="mt-1 text-sm text-slate-600">
          Thông tin này sẽ được dùng để in trên hóa đơn và báo cáo.
        </p>
      </div>

      {error && (
        <div className="mb-4 rounded-lg border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="grid gap-4 md:grid-cols-2">
          <div className="md:col-span-2">
            <label
              htmlFor="name"
              className="mb-1 block text-sm font-medium text-slate-700"
            >
              Tên hộ kinh doanh *
            </label>
            <input
              id="name"
              type="text"
              className="block w-full rounded-lg border border-slate-200 bg-slate-50 px-3 py-2 text-sm text-slate-900 outline-none transition focus:border-slate-900 focus:bg-white focus:ring-2 focus:ring-slate-900/10"
              placeholder="Hộ kinh doanh Hoa Mai"
              value={state.household.name ?? ""}
              onChange={e =>
                updateHousehold({
                  name: e.target.value
                })
              }
            />
          </div>

          <div>
            <label
              htmlFor="tax_code"
              className="mb-1 block text-sm font-medium text-slate-700"
            >
              Mã số thuế / CCCD người đại diện
            </label>
            <input
              id="tax_code"
              type="text"
              className="block w-full rounded-lg border border-slate-200 bg-slate-50 px-3 py-2 text-sm text-slate-900 outline-none transition focus:border-slate-900 focus:bg-white focus:ring-2 focus:ring-slate-900/10"
              placeholder="012345678901"
              value={state.household.tax_code ?? ""}
              onChange={e =>
                updateHousehold({
                  tax_code: e.target.value
                })
              }
            />
            <p className="mt-1 text-xs text-slate-500">
              Nếu có, hệ thống sẽ dùng để in trên hóa đơn.
            </p>
          </div>

          <div>
            <label
              htmlFor="phone"
              className="mb-1 block text-sm font-medium text-slate-700"
            >
              Số điện thoại liên hệ
            </label>
            <input
              id="phone"
              type="text"
              className="block w-full rounded-lg border border-slate-200 bg-slate-50 px-3 py-2 text-sm text-slate-900 outline-none transition focus:border-slate-900 focus:bg-white focus:ring-2 focus:ring-slate-900/10"
              placeholder="090 123 4567"
              value={state.household.phone ?? ""}
              onChange={e =>
                updateHousehold({
                  phone: e.target.value
                })
              }
            />
          </div>
        </div>

        <div>
          <label
            htmlFor="address"
            className="mb-1 block text-sm font-medium text-slate-700"
          >
            Địa chỉ kinh doanh
          </label>
          <textarea
            id="address"
            rows={3}
            className="block w-full resize-none rounded-lg border border-slate-200 bg-slate-50 px-3 py-2 text-sm text-slate-900 outline-none transition focus:border-slate-900 focus:bg-white focus:ring-2 focus:ring-slate-900/10"
            placeholder="Số nhà, đường, phường/xã, quận/huyện, tỉnh/thành phố"
            value={state.household.address ?? ""}
            onChange={e =>
              updateHousehold({
                address: e.target.value
              })
            }
          />
        </div>

        <div>
          <label
            htmlFor="description"
            className="mb-1 block text-sm font-medium text-slate-700"
          >
            Mô tả (tùy chọn)
          </label>
          <textarea
            id="description"
            rows={3}
            className="block w-full resize-none rounded-lg border border-slate-200 bg-slate-50 px-3 py-2 text-sm text-slate-900 outline-none transition focus:border-slate-900 focus:bg-white focus:ring-2 focus:ring-slate-900/10"
            placeholder="Mặt hàng chính, khu vực phục vụ, ghi chú nội bộ…"
            value={state.household.description ?? ""}
            onChange={e =>
              updateHousehold({
                description: e.target.value
              })
            }
          />
        </div>

        <div className="mt-6 flex items-center justify-between">
          <button
            type="button"
            onClick={() => router.push("/register/step1-plan")}
            className="text-sm font-medium text-slate-600 hover:text-slate-900"
          >
            Quay lại
          </button>
          <button
            type="submit"
            className="inline-flex items-center justify-center rounded-lg bg-slate-900 px-4 py-2.5 text-sm font-medium text-white"
          >
            Tiếp tục
          </button>
        </div>
      </form>
    </section>
  );
}

