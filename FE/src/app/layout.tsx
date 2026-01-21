import type { Metadata } from "next";
import "./globals.css";
import "./bizflow-loader.css";
import { ToastContainer } from "@/components/ui/toast";

export const metadata: Metadata = {
  title: "BizFlow - Quản lý hộ kinh doanh",
  description: "Nền tảng quản lý hộ kinh doanh, hóa đơn, kho hàng"
};

export default function RootLayout({
  children
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="vi">
      <body className="min-h-screen bg-slate-50 text-slate-900">
        {children}
        <ToastContainer />
      </body>
    </html>
  );
}

