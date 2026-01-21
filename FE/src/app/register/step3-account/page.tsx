"use client";

import { FormEvent, useState } from "react";
import { useRouter } from "next/navigation";
import { useRegistration } from "@/context/registration-context";
import { registerOwner } from "@/services/registration.service";
import { showToast } from "@/components/ui/toast";
import LoadingOverlay from "@/components/ui/loading-overlay";

export default function Step3AccountPage() {
  const router = useRouter();
  const { state, updateOwner, reset } = useRegistration();
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);
  const [showPassword, setShowPassword] = useState(false);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError(null);

    if (!state.planId) {
      setError("Vui lòng chọn gói đăng ký trước.");
      return;
    }
    if (!state.household.name?.trim()) {
      setError("Vui lòng nhập tên hộ kinh doanh.");
      return;
    }
    if (!state.owner.user_name?.trim()) {
      setError("Vui lòng nhập tên đăng nhập.");
      return;
    }
    if (!state.owner.password) {
      setError("Vui lòng nhập mật khẩu.");
      return;
    }
    if (state.owner.password !== state.owner.confirmPassword) {
      setError("Mật khẩu xác nhận không khớp.");
      return;
    }

    try {
      setSubmitting(true);
      const payload = {
        plan_id: state.planId,
        household: {
          tax_code: state.household.tax_code || undefined,
          name: state.household.name,
          phone: state.household.phone || undefined,
          address: state.household.address || undefined,
          description: state.household.description || undefined
        },
        owner_account: {
          user_name: state.owner.user_name,
          password: state.owner.password,
          email: state.owner.email || undefined,
          description: state.owner.description || undefined
        }
      };

      const res = await registerOwner(payload);

      // Hiển thị thông báo thành công
      showToast(
        "Đăng ký thành công! Đang chuyển đến trang xác nhận...",
        "success",
        2000
      );

      // Lưu một chút thông tin để hiển thị ở trang success (client only)
      if (typeof window !== "undefined") {
        window.sessionStorage.setItem(
          "register_summary",
          JSON.stringify({
            household_name: state.household.name,
            user_name: state.owner.user_name,
            household_id: res.household_id,
            user_id: res.user_id
          })
        );
      }

      reset();
      setTimeout(() => {
        router.push("/register/success");
      }, 1500);
    } catch (err: any) {
      const message =
        err?.response?.data?.error ||
        err?.response?.data?.message ||
        err?.message ||
        "Đăng ký thất bại. Vui lòng thử lại.";
      setError(message);
      showToast(message, "error", 5000);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <>
      <LoadingOverlay isLoading={submitting} message="Đang đăng ký tài khoản..." />
      <section>
      <div className="mb-6">
        <h2 className="text-xl font-semibold text-slate-900">
          Tài khoản chủ hộ (Owner)
        </h2>
        <p className="mt-1 text-sm text-slate-600">
          Tài khoản này dùng để đăng nhập và quản lý toàn bộ hệ thống.
        </p>
      </div>

      {error && (
        <div className="mb-4 rounded-lg border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="grid gap-4 md:grid-cols-2">
          <div>
            <label
              htmlFor="user_name"
              className="mb-1 block text-sm font-medium text-slate-700"
            >
              Tên đăng nhập *
            </label>
            <input
              id="user_name"
              type="text"
              className="block w-full rounded-lg border border-slate-200 bg-slate-50 px-3 py-2 text-sm text-slate-900 outline-none transition focus:border-slate-900 focus:bg-white focus:ring-2 focus:ring-slate-900/10"
              placeholder="vd: hoakh_hoa_mai"
              value={state.owner.user_name ?? ""}
              onChange={e => updateOwner({ user_name: e.target.value })}
            />
          </div>

          <div>
            <label
              htmlFor="email"
              className="mb-1 block text-sm font-medium text-slate-700"
            >
              Email
            </label>
            <input
              id="email"
              type="email"
              className="block w-full rounded-lg border border-slate-200 bg-slate-50 px-3 py-2 text-sm text-slate-900 outline-none transition focus:border-slate-900 focus:bg-white focus:ring-2 focus:ring-slate-900/10"
              placeholder="owner@example.com"
              value={state.owner.email ?? ""}
              onChange={e => updateOwner({ email: e.target.value })}
            />
          </div>
        </div>

        <div className="grid gap-4 md:grid-cols-2">
          <div>
            <label
              htmlFor="password"
              className="mb-1 block text-sm font-medium text-slate-700"
            >
              Mật khẩu *
            </label>
            <div className="relative">
              <input
                id="password"
                type={showPassword ? "text" : "password"}
                className="block w-full rounded-lg border border-slate-200 bg-slate-50 px-3 py-2 pr-10 text-sm text-slate-900 outline-none transition focus:border-slate-900 focus:bg-white focus:ring-2 focus:ring-slate-900/10"
                placeholder="••••••••"
                value={state.owner.password ?? ""}
                onChange={e => updateOwner({ password: e.target.value })}
              />
              <button
                type="button"
                onClick={() => setShowPassword(prev => !prev)}
                className="absolute inset-y-0 right-0 flex items-center px-3 text-xs font-medium text-slate-500 hover:text-slate-700"
              >
                {showPassword ? "Ẩn" : "Hiện"}
              </button>
            </div>
            <p className="mt-1 text-xs text-slate-500">
              Nên dài từ 8 ký tự trở lên, kết hợp chữ và số.
            </p>
          </div>

          <div>
            <label
              htmlFor="confirm_password"
              className="mb-1 block text-sm font-medium text-slate-700"
            >
              Xác nhận mật khẩu *
            </label>
            <input
              id="confirm_password"
              type={showPassword ? "text" : "password"}
              className="block w-full rounded-lg border border-slate-200 bg-slate-50 px-3 py-2 text-sm text-slate-900 outline-none transition focus:border-slate-900 focus:bg-white focus:ring-2 focus:ring-slate-900/10"
              placeholder="Nhập lại mật khẩu"
              value={state.owner.confirmPassword ?? ""}
              onChange={e =>
                updateOwner({
                  confirmPassword: e.target.value
                })
              }
            />
          </div>
        </div>

        <div>
          <label
            htmlFor="description"
            className="mb-1 block text-sm font-medium text-slate-700"
          >
            Mô tả tài khoản (tùy chọn)
          </label>
          <textarea
            id="description"
            rows={3}
            className="block w-full resize-none rounded-lg border border-slate-200 bg-slate-50 px-3 py-2 text-sm text-slate-900 outline-none transition focus:border-slate-900 focus:bg-white focus:ring-2 focus:ring-slate-900/10"
            placeholder="Chủ hộ kinh doanh, quản lý chính hệ thống…"
            value={state.owner.description ?? ""}
            onChange={e => updateOwner({ description: e.target.value })}
          />
        </div>

        <div className="mt-6 flex items-center justify-between">
          <button
            type="button"
            onClick={() => router.push("/register/step2-household")}
            className="text-sm font-medium text-slate-600 hover:text-slate-900"
          >
            Quay lại
          </button>
          <button
            type="submit"
            disabled={submitting}
            className="inline-flex items-center justify-center rounded-lg bg-slate-900 px-4 py-2.5 text-sm font-medium text-white disabled:cursor-not-allowed disabled:bg-slate-400"
          >
            {submitting ? "Đang đăng ký..." : "Đăng ký"}
          </button>
        </div>
      </form>
    </section>
    </>
  );
}

