"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

export default function HomePage() {
  const router = useRouter();

  useEffect(() => {
    // Check if user is logged in and redirect accordingly
    if (typeof window !== "undefined") {
      const token = localStorage.getItem("auth_token");
      const roleId = localStorage.getItem("role_id");

      if (token && roleId) {
        // User is logged in, redirect based on role
        const role = parseInt(roleId);
        if (role === 1) {
          router.push("/admin");
        } else if (role === 2) {
          router.push("/owner");
        } else if (role === 3) {
          router.push("/employee");
        }
      }
    }
  }, [router]);

  return (
    <main className="flex min-h-screen items-center justify-center">
      <div className="rounded-2xl bg-white px-8 py-10 shadow-lg">
        <h1 className="mb-2 text-4xl font-bold italic text-[#1e3a8a]">
          BizFlow
        </h1>
        <p className="mb-4 text-slate-600">
          Nền tảng quản lý hộ kinh doanh
        </p>
        <a
          href="/login"
          className="inline-flex items-center justify-center rounded-lg bg-slate-900 px-4 py-2 text-sm font-medium text-white hover:bg-slate-800"
        >
          Đến trang đăng nhập
        </a>
      </div>
    </main>
  );
}

