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
    <div className="max-w-[210mm] mx-auto bg-white p-8 font-sans" style={{ fontFamily: '"Inter", "Be Vietnam Pro", system-ui, sans-serif' }}>
      {/* Header Section */}
      <div className="flex justify-between items-start mb-6">
        {/* Left: BizFlow Logo */}
        <div>
          <div className="text-[#1e3a8a] font-bold text-2xl">BizFlow</div>
          <div className="text-xs text-gray-600 mt-1">Đ/C:</div>
          <div className="text-xs text-gray-600">SĐT:</div>
        </div>

        {/* Right: Circular and Serial */}
        <div className="text-right text-xs">
          <div className="text-gray-700 mb-1">Ban hành kèm theo</div>
          <div className="text-gray-700 mb-1">thông tư số</div>
          <div className="text-gray-700 mb-3">số/2017/TT-BTC</div>
          <div className="text-red-600 font-bold">
            SỐ: <span className="ml-2">{serialNumber}</span>
          </div>
        </div>
      </div>

      {/* Title */}
      <div className="text-center mb-6">
        <h1 className="text-xl font-bold uppercase">HÓA ĐƠN BÁN LẺ</h1>
      </div>

      {/* Customer Info */}
      <div className="mb-6 space-y-2">
        <div className="flex items-center text-sm">
          <span className="font-medium mr-2">Tên khách hàng:</span>
          <div className="flex-1 border-b border-gray-400 pb-1">{customerName}</div>
        </div>
        <div className="flex items-center text-sm">
          <span className="font-medium mr-2">Địa chỉ:</span>
          <div className="flex-1 border-b border-gray-400 pb-1">{customerAddress}</div>
        </div>
        <div className="flex items-center text-sm">
          <span className="font-medium mr-2">Điện thoại:</span>
          <div className="flex-1 border-b border-gray-400 pb-1">{customerPhone}</div>
        </div>
      </div>

      {/* Product Table */}
      <div className="mb-6">
        <table className="w-full border-collapse border border-gray-900">
          <thead>
            <tr className="bg-white">
              <th className="border border-gray-900 px-2 py-2 text-sm font-bold text-center">STT</th>
              <th className="border border-gray-900 px-2 py-2 text-sm font-bold text-center">TÊN SẢN PHẨM</th>
              <th className="border border-gray-900 px-2 py-2 text-sm font-bold text-center">ĐVT</th>
              <th className="border border-gray-900 px-2 py-2 text-sm font-bold text-center">SL</th>
              <th className="border border-gray-900 px-2 py-2 text-sm font-bold text-center">ĐƠN GIÁ</th>
              <th className="border border-gray-900 px-2 py-2 text-sm font-bold text-center">THÀNH TIỀN</th>
            </tr>
          </thead>
          <tbody>
            {paddedItems.map((item, index) => (
              <tr key={index}>
                <td className="border border-gray-900 px-2 py-2 text-sm text-center">
                  {item.productName ? item.stt : ''}
                </td>
                <td className="border border-gray-900 px-2 py-2 text-sm">{item.productName}</td>
                <td className="border border-gray-900 px-2 py-2 text-sm text-center">{item.unit}</td>
                <td className="border border-gray-900 px-2 py-2 text-sm text-center">
                  {item.quantity > 0 ? item.quantity : ''}
                </td>
                <td className="border border-gray-900 px-2 py-2 text-sm text-right">
                  {item.unitPrice > 0 ? item.unitPrice.toLocaleString('vi-VN') : ''}
                </td>
                <td className="border border-gray-900 px-2 py-2 text-sm text-right">
                  {item.total > 0 ? item.total.toLocaleString('vi-VN') : ''}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Total Section */}
      <div className="mb-8 space-y-2">
        <div className="flex items-center text-sm">
          <span className="font-medium mr-2">Tổng cộng:</span>
          <div className="flex-1 border-b border-gray-400 pb-1 text-right font-bold">
            {totalAmount > 0 ? totalAmount.toLocaleString('vi-VN') : ''}
          </div>
        </div>
        <div className="flex items-start text-sm">
          <span className="font-medium mr-2">Số tiền bằng chữ:</span>
          <div className="flex-1 border-b border-gray-400 pb-1">{totalInWords}</div>
        </div>
      </div>

      {/* Footer Section */}
      <div className="text-sm text-gray-700 space-y-1">
        <div className="flex items-center">
          <span>Sản phẩm được bảo hành</span>
          <div className="flex-1 border-b border-gray-400 mx-2"></div>
          <span>tháng kể từ ngày mua sản xuất.</span>
        </div>
        <div className="text-right mt-6">
          <span>
            ngày <span className="inline-block border-b border-gray-400 px-2">{date.day}</span> tháng{' '}
            <span className="inline-block border-b border-gray-400 px-2">{date.month}</span> năm{' '}
            <span className="inline-block border-b border-gray-400 px-2">{date.year}</span>
          </span>
        </div>
      </div>
    </div>
  );
};

export default RetailInvoiceTemplate;
