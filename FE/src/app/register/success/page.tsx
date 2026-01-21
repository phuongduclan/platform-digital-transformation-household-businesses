"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { showToast } from "@/components/ui/toast";

type Summary = {
  household_name?: string;
  user_name?: string;
  household_id?: number;
  user_id?: number;
};

export default function RegisterSuccessPage() {
  const router = useRouter();
  const [summary, setSummary] = useState<Summary | null>(null);

  useEffect(() => {
    if (typeof window === "undefined") return;
    const raw = window.sessionStorage.getItem("register_summary");
    if (raw) {
      try {
        const data = JSON.parse(raw);
        setSummary(data);
        showToast(
          `Đăng ký thành công! Chào mừng ${data.household_name || ""} đến với BizFlow!`,
          "success",
          5000
        );
      } catch {
        setSummary(null);
      }
    } else {
      // Nếu không có summary, có thể user truy cập trực tiếp URL này
      showToast("Không tìm thấy thông tin đăng ký. Vui lòng đăng ký lại.", "warning");
      setTimeout(() => {
        router.push("/register/step1-plan");
      }, 2000);
    }
  }, [router]);

  return (
    <section className="text-center">
      <div className="mx-auto mb-4 flex h-12 w-12 items-center justify-center rounded-full bg-emerald-100">
        <span className="text-xl">✓</span>
      </div>
      <h2 className="mb-2 text-xl font-semibold text-slate-900">
        Đăng ký thành công!
      </h2>
      <p className="mb-4 text-sm text-slate-600">
        Hệ thống đã tạo tài khoản chủ hộ và kích hoạt gói dịch vụ cho hộ kinh
        doanh của bạn.
      </p>

      {summary && (
        <div className="mx-auto mb-6 max-w-md rounded-xl bg-slate-50 px-4 py-3 text-left text-sm text-slate-700">
          {summary.household_name && (
            <div className="mb-1">
              <span className="font-medium">Hộ kinh doanh: </span>
              <span>{summary.household_name}</span>
            </div>
          )}
          {summary.user_name && (
            <div className="mb-1">
              <span className="font-medium">Tài khoản đăng nhập: </span>
              <span>{summary.user_name}</span>
            </div>
          )}
          {summary.household_id && (
            <div className="mb-1 text-xs text-slate-500">
              ID hộ kinh doanh: {summary.household_id}
            </div>
          )}
          {summary.user_id && (
            <div className="text-xs text-slate-500">
              ID tài khoản: {summary.user_id}
            </div>
          )}
        </div>
      )}

      <div className="flex justify-center gap-3">
        <button
          type="button"
          onClick={() => {
            showToast("Chuyển đến trang đăng nhập...", "info", 1000);
            setTimeout(() => {
              router.push("/login");
            }, 500);
          }}
          className="inline-flex items-center justify-center rounded-lg bg-slate-900 px-4 py-2.5 text-sm font-medium text-white"
        >
          Đăng nhập ngay
        </button>
        <button
          type="button"
          onClick={() => {
            showToast("Chuyển về trang chủ...", "info", 1000);
            setTimeout(() => {
              router.push("/");
            }, 500);
          }}
          className="inline-flex items-center justify-center rounded-lg border border-slate-200 px-4 py-2.5 text-sm font-medium text-slate-700 hover:bg-slate-50"
        >
          Về trang chủ
        </button>
      </div>
    </section>
  );
}

