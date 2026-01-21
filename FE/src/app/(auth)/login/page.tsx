"use client";

import { FormEvent, useState } from "react";
import { login } from "@/services/auth.service";
import Link from "next/link";
import { showToast } from "@/components/ui/toast";

import LoadingOverlay from "@/components/ui/loading-overlay";

type LoginFormState = {
  user_name: string;
  password: string;
};

export default function LoginPage() {
  const [form, setForm] = useState<LoginFormState>({
    user_name: "",
    password: ""
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showPassword, setShowPassword] = useState(false);
  const [rememberMe, setRememberMe] = useState(false);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError(null);

    if (!form.user_name || !form.password) {
      setError("Vui lòng nhập đầy đủ tài khoản và mật khẩu.");
      return;
    }

    try {
      setIsSubmitting(true);
      const loginResponse = await login(form.user_name, form.password);
      // Hiển thị thông báo thành công
      showToast("Đăng nhập thành công! Đang chuyển hướng...", "success", 2000);

      // Redirect theo role_id
      setTimeout(() => {
        const roleId = loginResponse.role_id;
        if (roleId === 1) {
          // Admin
          window.location.href = "/admin";
        } else if (roleId === 2) {
          // Owner
          window.location.href = "/owner";
        } else if (roleId === 3) {
          // Employee
          window.location.href = "/employee";
        } else {
          window.location.href = "/";
        }
      }, 1500);
    } catch (err: any) {
      // Ưu tiên hiển thị message từ backend
      let message =
        err?.response?.data?.error ||
        err?.response?.data?.message ||
        err?.message ||
        "Đăng nhập không thành công. Vui lòng thử lại.";

      // Nếu là network error, hiển thị message rõ ràng hơn
      if (
        err?.code === "ECONNREFUSED" ||
        err?.message?.includes("Network Error") ||
        err?.message?.includes("kết nối đến máy chủ")
      ) {
        message =
          "Không thể kết nối đến máy chủ. Vui lòng đảm bảo backend đang chạy tại http://localhost:6868";
      }

      setError(message);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <>
      <LoadingOverlay isLoading={isSubmitting} message="Đang đăng nhập..." />
      <main
        className="relative flex min-h-screen overflow-hidden"
        style={{
          backgroundPosition: "center center",
          background:
            "conic-gradient(from 0deg at 68.4% 85.35%, #fff0 0 60deg, #38bba7 0 120deg, #159380 0 202.5deg, #fff0 0 360deg) 50%/20vmin 25vmin, " +
            "conic-gradient(from 0deg at 31.6% 85.35%, #fff0 0 157.5deg, #17a18c 0 240deg, #38bba7 0 300deg, #fff0 0 360deg) 50%/20vmin 25vmin, " +
            "conic-gradient(from 0deg at 81.35% 35.5%, #fff0 0 22.75deg, #128070 0 157.25deg, #fff0 0 360deg) 50%/20vmin 25vmin, " +
            "conic-gradient(from 0deg at 18.65% 35.5%, #fff0 0 202.75deg, #01685b 0 337.25deg, #fff0 0 360deg) 50%/20vmin 25vmin, " +
            "conic-gradient(from 0deg at 50% 50%, #fff0 0 60deg, #17a18c 0 157.5deg, #01685b 0 180.1deg, #128070 0 202.5deg, #159380 0 300deg, #fff0 0 360deg) 50%/20vmin 25vmin, " +
            "conic-gradient(from 0deg at 50% 21.15%, #fff0 0 22.5deg, #159380 0 120deg, #38bba7 0 240deg, #17a18c 0 337.5deg, #fff0 0 360deg) 50%/20vmin 25vmin, " +
            "linear-gradient(90deg, #128070 0 50%, #01685b 0 100%) 50%/20vmin 25vmin",
          backgroundColor: "#f8fafc", // gần với bg-slate-50
        }}
      >
        {/* Left Section - Hero */}
        <div className="hidden lg:flex lg:w-2/3 flex-col px-12 py-16 relative">
          {/* White overlay panel for readability */}
          <div className="relative z-10 max-w-3xl rounded-2xl bg-white/85 backdrop-blur-sm border border-white/60 shadow-sm p-8">
            <div className="mb-8">
              <div className="mb-2">
                <h1 className="text-[40px] font-bold italic text-[#1e3a8a]">BizFlow</h1>
              </div>
              <p className="text-2xl text-[#1e3a8a]">
                Nền tảng quản lý hộ kinh doanh
              </p>
            </div>

            <div className="mb-8">
              <h2 className="text-[36px] font-bold italic text-[#1e3a8a] leading-tight mb-6">
                Quản lý doanh nghiệp nhỏ, phát triển lớn mạnh.
              </h2>
            </div>

            <div className="space-y-4">
              <div className="flex items-center gap-3">
                <div className="w-5 h-5 flex-shrink-0">
                  <svg
                    viewBox="0 0 20 20"
                    fill="none"
                    xmlns="http://www.w3.org/2000/svg"
                    className="w-full h-full text-[#00897b]"
                  >
                    <path
                      d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                      fill="currentColor"
                    />
                  </svg>
                </div>
                <p className="text-base text-[#4b5563]">
                  Quản lý hóa đơn hiệu quả.
                </p>
              </div>
              <div className="flex items-center gap-3">
                <div className="w-5 h-5 flex-shrink-0">
                  <svg
                    viewBox="0 0 20 20"
                    fill="none"
                    xmlns="http://www.w3.org/2000/svg"
                    className="w-full h-full text-[#00897b]"
                  >
                    <path
                      d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                      fill="currentColor"
                    />
                  </svg>
                </div>
                <p className="text-base text-[#4b5563]">
                  Theo dõi kho hàng tức thời.
                </p>
              </div>
              <div className="flex items-center gap-3">
                <div className="w-5 h-5 flex-shrink-0">
                  <svg
                    viewBox="0 0 20 20"
                    fill="none"
                    xmlns="http://www.w3.org/2000/svg"
                    className="w-full h-full text-[#00897b]"
                  >
                    <path
                      d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                      fill="currentColor"
                    />
                  </svg>
                </div>
                <p className="text-base text-[#4b5563]">
                  Báo cáo tài chính minh bạch.
                </p>
              </div>
              <div className="flex items-center gap-3">
                <div className="w-5 h-5 flex-shrink-0">
                  <svg
                    viewBox="0 0 20 20"
                    fill="none"
                    xmlns="http://www.w3.org/2000/svg"
                    className="w-full h-full text-[#00897b]"
                  >
                    <path
                      d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                      fill="currentColor"
                    />
                  </svg>
                </div>
                <p className="text-base text-[#4b5563]">
                  Tiết kiệm thời gian, tối ưu lợi nhuận.
                </p>
              </div>
            </div>
          </div>

          {/* System notice: removed (no usable feature yet) */}
        </div>

        {/* Right Section - Login Form */}
        <div className="w-full lg:w-1/3 flex items-center justify-center px-6 py-12">
          <div className="w-full max-w-md">
            <div className="bg-white rounded-2xl shadow-xl p-8">
              {/* Form Header */}
              <div className="mb-8">
                <h1 className="text-[32px] font-bold italic text-[#1e3a8a] mb-3">
                  Đăng nhập vào
                </h1>
                <p className="text-base text-[#4b5563] leading-relaxed">
                  Chào mừng trở lại! Hãy đăng nhập để tiếp tục quản lý.
                </p>
              </div>

              {error && (
                <div className="mb-4 rounded-lg border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700">
                  {error}
                </div>
              )}

              <form onSubmit={handleSubmit} className="space-y-5">
                {/* Username Field */}
                <div>
                  <label
                    htmlFor="user_name"
                    className="mb-1.5 block text-base font-normal text-[#4b5563]"
                  >
                    Tên đăng nhập
                  </label>
                  <input
                    id="user_name"
                    name="user_name"
                    type="text"
                    autoComplete="username"
                    className="block w-full h-11 rounded-lg border border-slate-200 bg-sky-50 px-3 py-2 text-base text-slate-900 outline-none transition focus:border-slate-400 focus:bg-white focus:ring-2 focus:ring-slate-300"
                    placeholder=""
                    value={form.user_name}
                    onChange={e =>
                      setForm(prev => ({ ...prev, user_name: e.target.value }))
                    }
                  />
                </div>

                {/* Password Field */}
                <div>
                  <label
                    htmlFor="password"
                    className="mb-1.5 block text-base font-normal text-[#4b5563]"
                  >
                    Mật khẩu
                  </label>
                  <div className="relative">
                    <input
                      id="password"
                      name="password"
                      type={showPassword ? "text" : "password"}
                      autoComplete="current-password"
                      className="block w-full h-11 rounded-lg border border-slate-200 bg-sky-50 px-3 py-2 pr-12 text-base text-slate-900 outline-none transition focus:border-slate-400 focus:bg-white focus:ring-2 focus:ring-slate-300"
                      placeholder=""
                      value={form.password}
                      onChange={e =>
                        setForm(prev => ({ ...prev, password: e.target.value }))
                      }
                    />
                    <button
                      type="button"
                      onClick={() => setShowPassword(prev => !prev)}
                      className="absolute inset-y-0 right-0 flex items-center px-3 text-sm font-medium text-[#4b5563] hover:text-slate-700"
                    >
                      {showPassword ? "Ẩn" : "Hiện"}
                    </button>
                  </div>
                </div>

                {/* Remember Me Checkbox */}
                <div className="flex items-center gap-2">
                  <input
                    type="checkbox"
                    id="remember_me"
                    checked={rememberMe}
                    onChange={e => setRememberMe(e.target.checked)}
                    className="h-4 w-4 rounded border-slate-300 text-[#00897b] focus:ring-[#00897b]"
                  />
                  <label
                    htmlFor="remember_me"
                    className="text-base font-normal text-[#4b5563] cursor-pointer"
                  >
                    Ghi nhớ đăng nhập trên thiết bị này
                  </label>
                </div>

                {/* Login Button */}
                <button
                  type="submit"
                  disabled={isSubmitting}
                  className="w-full h-11 rounded-lg bg-[#00897b] px-4 py-2.5 text-base font-bold text-white shadow-sm transition hover:bg-[#007a6c] disabled:cursor-not-allowed disabled:bg-slate-400"
                >
                  {isSubmitting ? "Đang đăng nhập..." : "Đăng nhập"}
                </button>
              </form>

              {/* Footer Links */}
              <div className="mt-8 text-center">
                <p className="text-base text-[#4b5563] mb-1">
                  Chưa có tài khoản hộ kinh doanh?
                </p>
                <Link
                  href="/register/step1-plan"
                  className="text-sm font-bold italic text-[#00897b] hover:underline"
                >
                  Đăng ký ngay
                </Link>
              </div>
            </div>
          </div>
        </div>
      </main>
    </>
  );
}
