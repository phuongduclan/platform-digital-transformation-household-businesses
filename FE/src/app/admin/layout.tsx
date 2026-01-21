"use client";

import { useEffect, useState } from "react";
import { useRouter, usePathname } from "next/navigation";
import Link from "next/link";

import { showToast } from "@/components/ui/toast";


interface AdminLayoutProps {
  children: React.ReactNode;
}

export default function AdminLayout({ children }: AdminLayoutProps) {
  const router = useRouter();
  const pathname = usePathname();
  const [user, setUser] = useState<any>(null);
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
    // Check authentication
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
          // Check if user is Admin (role_id = 1)
          if (userData.role_id !== 1) {
            showToast("Bạn không có quyền truy cập trang Admin", "error");
            router.push("/");
            return;
          }
          setUser(userData);
        } catch (e) {
          router.push("/login");
        }
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
    { href: "/admin", label: "Dashboard" },
    { href: "/admin/users", label: "Quản lý Người dùng", code: "F005" },
    { href: "/admin/subscription-plans", label: "Quản lý Gói đăng ký", code: "F002" },
    { href: "/admin/subscriptions", label: "Quản lý Đăng ký", code: "F003" },
    { href: "/admin/payment-methods", label: "Phương thức Thanh toán", code: "F006" },
    { href: "/admin/analytics", label: "Phân tích Nền tảng", code: "F004" },
    { href: "/admin/config", label: "Cài đặt Hệ thống", code: "F006" },
    { href: "/admin/settings", label: "Cài đặt" },
  ];

  return (
    <div className="flex h-screen bg-slate-50">
      {/* Sidebar */}
      <aside className="w-64 bg-white border-r border-slate-200 flex flex-col">
        {/* Logo */}

        <div className="p-6 border-b border-slate-200 flex flex-col items-start gap-1">
          <h1 className="text-2xl font-bold italic text-[#1e3a8a]">BizFlow</h1>
          <p className="text-xs text-[#4b5563] mt-1">Quản trị hệ thống</p>
        </div>

        {/* Navigation */}
        <nav className="flex-1 overflow-y-auto p-4">
          <ul className="space-y-1">
            {menuItems.map((item) => {
              const isActive = pathname === item.href || pathname?.startsWith(item.href + "/");
              return (
                <li key={item.href}>
                  <Link
                    href={item.href}
                    className={`flex items-center px-4 py-2.5 rounded-lg text-sm font-normal transition-colors ${isActive
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
            <p className="text-sm font-medium text-slate-900">{user?.user_name || "Admin"}</p>
            <p className="text-xs text-slate-500">Quản trị viên</p>
          </div>
          <button
            onClick={handleLogout}
            className="w-full px-4 py-2 text-sm font-medium text-red-600 hover:bg-red-50 rounded-lg transition-colors"
          >
            Đăng xuất
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 overflow-y-auto">
        {/* Top Header with Breadcrumb - only show on non-dashboard pages */}
        {pathname !== "/admin" && (
          <div className="bg-white border-b border-slate-200 px-8 py-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2 text-sm">
                <Link href="/admin" className="text-[#00897b] hover:underline">
                  Dashboard
                </Link>
                {pathname !== "/admin" && (
                  <span className="text-[#4b5563]">
                    {pathname.includes("/users") && " > Quản lý Người dùng"}
                    {pathname.includes("/subscription-plans") && " > Quản lý Gói đăng ký"}
                    {pathname.includes("/subscriptions") && " > Quản lý Đăng ký"}
                    {pathname.includes("/analytics") && " > Phân tích Nền tảng"}
                    {pathname.includes("/config") && " > Cài đặt Hệ thống"}
                    {pathname.includes("/settings") && " > Cài đặt"}
                  </span>
                )}
              </div>
              <div className="flex items-center gap-4">
                <span className="text-sm text-[#1e3a8a]">
                  Xin chào, {user?.user_name || "Admin"}
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
