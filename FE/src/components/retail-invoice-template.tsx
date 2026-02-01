import React from 'react';

interface RetailInvoiceTemplateProps {
    invoiceNumber?: string;
    serialNumber?: string;
    customerName?: string;
    customerAddress?: string;
    customerPhone?: string;
    items?: Array<{
        stt: number;
        productName: string;
        unit: string;
        quantity: number;
        unitPrice: number;
        total: number;
    }>;
    totalAmount?: number;
    totalInWords?: string;
    date?: {
        day: string;
        month: string;
        year: string;
    };
}

const RetailInvoiceTemplate: React.FC<RetailInvoiceTemplateProps> = ({
    invoiceNumber = '',
    serialNumber = '',
    customerName = '',
    customerAddress = '',
    customerPhone = '',
    items = [],
    totalAmount = 0,
    totalInWords = '',
    date = { day: '__', month: '__', year: '20__' },
}) => {
    // Ensure we always have 12 rows
    const paddedItems = [...items];
    while (paddedItems.length < 12) {
        paddedItems.push({
            stt: paddedItems.length + 1,
            productName: '',
            unit: '',
            quantity: 0,
            unitPrice: 0,
            total: 0,
        });
    }

    return (
        <div
            className="w-[210mm] min-h-[297mm] mx-auto bg-white p-[40px] text-sm leading-relaxed"
            style={{ fontFamily: '"Be Vietnam Pro", sans-serif' }}
        >
            {/* Header Section */}
            <div className="flex justify-between items-start mb-8">
                {/* Left: BizFlow Logo & Info */}
                <div className="w-1/2">
                    <h1 className="text-[#1e3a8a] font-bold text-3xl mb-2 tracking-tight">BizFlow</h1>
                    <div className="text-gray-600 text-[11px] space-y-1">
                        <p>Đ/C: ...</p>
                        <p>SĐT: ...</p>
                    </div>
                </div>

                {/* Right: Circular and Serial */}
                <div className="w-1/2 text-right">
                    <div className="text-[10px] text-gray-500 italic mb-2 leading-tight">
                        <p>Ban hành kèm theo thông tư số</p>
                        <p>88/2021/TT-BTC</p>
                    </div>
                    <div className="mt-2">
                        <div className="text-[#dc2626] font-bold text-base">
                            SỐ: {invoiceNumber}
                        </div>
                    </div>
                </div>
            </div>

            {/* Title */}
            <div className="text-center mb-8 relative">
                <h2 className="text-2xl font-bold text-gray-900 uppercase tracking-wide">HÓA ĐƠN BÁN LẺ</h2>
                <div className="absolute w-32 h-1 bg-[#1e3a8a] bottom-[-10px] left-1/2 transform -translate-x-1/2 opacity-20"></div>
            </div>

            {/* Customer Info */}
            <div className="mb-8 space-y-3 px-2">
                <div className="flex items-end">
                    <span className="font-semibold min-w-[120px] text-gray-700">Tên khách hàng:</span>
                    <div className="flex-1 border-b border-gray-300 pb-1 font-medium text-gray-900 ml-2">
                        {customerName}
                    </div>
                </div>
                <div className="flex items-end">
                    <span className="font-semibold min-w-[120px] text-gray-700">Địa chỉ:</span>
                    <div className="flex-1 border-b border-gray-300 pb-1 text-gray-900 ml-2">
                        {customerAddress}
                    </div>
                </div>
                <div className="flex items-end">
                    <span className="font-semibold min-w-[120px] text-gray-700">Điện thoại:</span>
                    <div className="flex-1 border-b border-gray-300 pb-1 text-gray-900 ml-2">
                        {customerPhone}
                    </div>
                </div>
            </div>

            {/* Product Table */}
            <div className="mb-6">
                <table className="w-full border-collapse border border-black">
                    <thead>
                        <tr className="bg-[#f1f5f9] text-gray-900">
                            <th className="border border-black px-3 py-2 text-xs font-bold w-[50px] text-center">STT</th>
                            <th className="border border-black px-3 py-2 text-xs font-bold text-left">TÊN SẢN PHẨM</th>
                            <th className="border border-black px-3 py-2 text-xs font-bold w-[60px] text-center">ĐVT</th>
                            <th className="border border-black px-3 py-2 text-xs font-bold w-[60px] text-center">SL</th>
                            <th className="border border-black px-3 py-2 text-xs font-bold w-[120px] text-right">ĐƠN GIÁ</th>
                            <th className="border border-black px-3 py-2 text-xs font-bold w-[120px] text-right">THÀNH TIỀN</th>
                        </tr>
                    </thead>
                    <tbody>
                        {paddedItems.map((item, index) => (
                            <tr key={index} className="h-[32px]">
                                <td className="border border-black px-2 py-1 text-xs text-center text-gray-600">
                                    {item.productName ? index + 1 : ''}
                                </td>
                                <td className="border border-black px-2 py-1 text-xs text-gray-900 font-medium">
                                    {item.productName}
                                </td>
                                <td className="border border-black px-2 py-1 text-xs text-center text-gray-600">
                                    {item.unit}
                                </td>
                                <td className="border border-black px-2 py-1 text-xs text-center text-gray-900">
                                    {item.quantity > 0 ? item.quantity : ''}
                                </td>
                                <td className="border border-black px-2 py-1 text-xs text-right text-gray-900">
                                    {item.unitPrice > 0 ? item.unitPrice.toLocaleString('vi-VN') : ''}
                                </td>
                                <td className="border border-black px-2 py-1 text-xs text-right text-gray-900 font-semibold">
                                    {item.total > 0 ? item.total.toLocaleString('vi-VN') : ''}
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>

            {/* Total Section */}
            <div className="mb-10 px-2">
                <div className="flex justify-end items-end mb-3">
                    <span className="font-bold text-gray-900 mr-4 text-base">Tổng cộng:</span>
                    <div className="min-w-[150px] border-b-2 border-gray-400 pb-1 text-right font-bold text-lg text-[#1e3a8a]">
                        {totalAmount > 0 ? totalAmount.toLocaleString('vi-VN') : '0'}
                        <span className="text-sm font-normal text-gray-500 ml-1">đ</span>
                    </div>
                </div>
                <div className="flex items-start">
                    <span className="font-semibold text-gray-700 italic mr-2 whitespace-nowrap">Số tiền bằng chữ:</span>
                    <div className="flex-1 font-medium text-gray-900 italic">
                        {totalInWords} đồng.
                    </div>
                </div>
            </div>

            {/* Footer Section */}
            <div className="grid grid-cols-2 gap-8 text-center text-xs">
                <div>
                    <div className="mb-2 italic text-gray-500">Người mua hàng</div>
                    <div className="font-semibold text-gray-400 mt-10">(Ký, ghi rõ họ tên)</div>
                </div>
                <div>
                    <div className="italic text-gray-600 mb-2">
                        Ngày <span className="font-bold">{date.day}</span> tháng <span className="font-bold">{date.month}</span> năm <span className="font-bold">{date.year}</span>
                    </div>
                    <div className="font-bold text-gray-900 uppercase">Người bán hàng</div>
                    <div className="font-semibold text-gray-400 mt-10">(Ký, ghi rõ họ tên)</div>
                </div>
            </div>

            <div className="mt-12 text-[10px] text-gray-400 text-center italic border-t border-gray-100 pt-4">
                Sản phẩm được bảo hành theo chính sách tiêu chuẩn của nhà sản xuất.
            </div>
        </div >
    );
};

export default RetailInvoiceTemplate;
