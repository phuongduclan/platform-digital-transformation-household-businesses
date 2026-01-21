"use client";

import { useEffect, useState } from "react";
import { useRouter, usePathname } from "next/navigation";
import Link from "next/link";


import { showToast } from "@/components/ui/toast";

interface EmployeeLayoutProps {
  children: React.ReactNode;
}

export default function EmployeeLayout({ children }: EmployeeLayoutProps) {
  const router = useRouter();
  const pathname = usePathname();
  const [user, setUser] = useState<any>(null);
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
    if (typeof window !== "undefined") {
      const token = localStorage.getItem("auth_token");
      const userStr = localStorage.getItem("user_info");

      if (!token) {
        router.push("/login");
        return;
      }

      if (userStr) {
        try {
          const userData = JSON.parse(userStr);
          // Employee role_id = 3
          if (userData.role_id !== 3) {
            showToast("Bạn không có quyền truy cập trang Nhân viên", "error");
            if (userData.role_id === 1) {
              router.push("/admin");
            } else if (userData.role_id === 2) {
              router.push("/owner");
            } else {
              router.push("/");
            }
            return;
          }
          setUser(userData);
        } catch {
          router.push("/login");
        }
      } else {
        router.push("/login");
      }
    }
  }, [router]);

  const handleLogout = () => {
    if (typeof window !== "undefined") {
      localStorage.removeItem("auth_token");
      localStorage.removeItem("user_info");
      showToast("Đã đăng xuất", "success");
      router.push("/login");
    }
  };

  if (!mounted) return null;

  const menuItems = [
    { href: "/employee", label: "Tổng quan" },
    { href: "/employee/customers", label: "Khách hàng" },
    { href: "/employee/inventory", label: "Tồn kho" },
    { href: "/employee/invoices", label: "Hóa đơn" },
    { href: "/employee/debt-records", label: "Công nợ" },
    { href: "/employee/settings", label: "Cài đặt" },
  ];

  const isDashboard = pathname === "/employee";

  return (
    <div className="flex h-screen bg-slate-50">
      {/* Sidebar */}
      <aside className="w-64 bg-white border-r border-slate-200 flex flex-col">
        {/* Logo */}

        <div className="p-6 border-b border-slate-200 flex flex-col items-start gap-1">
          <h1 className="text-2xl font-bold italic text-[#1e3a8a]">BizFlow</h1>
          <p className="text-xs text-[#4b5563] mt-1">Nhân viên bán hàng</p>
        </div>

        {/* Navigation */}
        <nav className="flex-1 overflow-y-auto p-4">
          <ul className="space-y-1">
            {menuItems.map((item) => {
              const active =
                pathname === item.href || pathname?.startsWith(item.href + "/");
              return (
                <li key={item.href}>
                  <Link
                    href={item.href}
                    className={`flex items-center px-4 py-2.5 rounded-lg text-sm font-normal transition-colors ${active
                      ? "bg-[#e0f2f1] text-[#00897b]"
                      : "text-[#4b5563] hover:bg-slate-100"
                      }`}
                  >
                    <span>{item.label}</span>
                  </Link>
                </li>
              );
            })}
          </ul>
        </nav>

        {/* User Info & Logout */}
        <div className="p-4 border-t border-slate-200">
          <div className="mb-3">
            <p className="text-sm font-medium text-slate-900">
              {user?.user_name || "Employee"}
            </p>
            <p className="text-xs text-slate-500">Nhân viên</p>
          </div>
          <button
            onClick={handleLogout}
            className="w-full px-4 py-2 text-sm font-medium text-red-600 hover:bg-red-50 rounded-lg transition-colors"
          >
            Đăng xuất
          </button>
        </div>
      </aside>

      {/* Main content */}
      <main className="flex-1 overflow-y-auto">
        {/* Top Header, ẩn trên dashboard chính */}
        {!isDashboard && (
          <div className="bg-white border-b border-slate-200 px-8 py-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2 text-sm">
                <Link
                  href="/employee"
                  className="text-[#00897b] hover:underline"
                >
                  Tổng quan
                </Link>
              </div>
              <div className="flex items-center gap-4">
                <span className="text-sm text-[#1e3a8a]">
                  Xin chào, {user?.user_name || "Employee"}
                </span>
                <button
                  onClick={handleLogout}
                  className="text-sm text-[#4b5563] hover:text-slate-900"
                >
                  Đăng xuất
                </button>
              </div>
            </div>
          </div>
        )}

        {children}
      </main>
    </div>
  );
}

