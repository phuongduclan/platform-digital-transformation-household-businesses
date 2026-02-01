"use client";

import RetailInvoiceTemplate from "@/components/retail-invoice-template";

export default function TestDesignPage() {
    // Sample data for testing
    const sampleData = {
        invoiceNumber: "001",
        serialNumber: "AA/26E-0001",
        customerName: "Nguyễn Văn A",
        customerAddress: "123 Đường ABC, Phường XYZ, Quận 1, TP.HCM",
        customerPhone: "0901234567",
        items: [
            {
                stt: 1,
                productName: "Sản phẩm A",
                unit: "Cái",
                quantity: 2,
                unitPrice: 150000,
                total: 300000,
            },
            {
                stt: 2,
                productName: "Sản phẩm B với tên dài để kiểm tra xuống dòng",
                unit: "Hộp",
                quantity: 5,
                unitPrice: 75000,
                total: 375000,
            },
            {
                stt: 3,
                productName: "Sản phẩm C",
                unit: "Kg",
                quantity: 3,
                unitPrice: 200000,
                total: 600000,
            },
        ],
        totalAmount: 1275000,
        totalInWords: "Một triệu hai trăm bảy mươi lăm nghìn đồng chẵn",
        date: {
            day: "01",
            month: "02",
            year: "2026",
        },
    };

    return (
        <div className="min-h-screen bg-slate-100 py-8">
            <div className="max-w-7xl mx-auto px-4">
                <div className="mb-6 text-center">
                    <h1 className="text-2xl font-bold text-slate-900 mb-2">
                        Preview: Hóa Đơn Bán Lẻ
                    </h1>
                    <p className="text-sm text-slate-600">
                        Thiết kế mới từ Figma với hỗ trợ font tiếng Việt đầy đủ
                    </p>
                </div>

                <div className="bg-white shadow-lg rounded-lg overflow-hidden">
                    <RetailInvoiceTemplate {...sampleData} />
                </div>

                <div className="mt-6 bg-white rounded-lg shadow p-6">
                    <h2 className="text-lg font-bold text-slate-900 mb-4">
                        Hướng dẫn kiểm tra:
                    </h2>
                    <ul className="list-disc list-inside space-y-2 text-sm text-slate-700">
                        <li>
                            Kiểm tra font chữ tiếng Việt: ê, á, đ, ư, ơ, â, ô không bị lỗi
                            hiển thị
                        </li>
                        <li>Bảng có đủ 12 dòng (3 dòng có dữ liệu, 9 dòng trống)</li>
                        <li>Logo "BizFlow" màu xanh dương (#1e3a8a)</li>
                        <li>Serial number màu đỏ ở góc phải</li>
                        <li>Căn lề và khoảng cách đều đặn</li>
                        <li>Tổng tiền được định dạng chuẩn Việt Nam (dấu phẩy)</li>
                    </ul>
                </div>
            </div>
        </div>
    );
}
