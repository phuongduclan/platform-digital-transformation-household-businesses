import { numberToVietnameseWords } from './number-to-words';

interface InvoicePDFData {
    invoice: {
        id: number;
        created_at: string;
        total_amount: string | number;
    };
    household: {
        name: string | null;
        tax_code: string | null;
        address: string | null;
        phone: string | null;
    } | null;
    customer: {
        name: string | null;
        address: string | null;
        phone: string | null;
    } | null;
    details: Array<{
        product_name: string;
        unit_name: string;
        quantity: number;
        price: string | null;
        line_total: string;
    }>;
}

export const generateInvoicePDF = async (data: InvoicePDFData) => {
    // Dynamically import html2pdf
    const html2pdf = (await import('html2pdf.js')).default;

    const createdDate = new Date(data.invoice.created_at);
    const totalAmount = Number(data.invoice.total_amount);

    // Create container for PDF content
    const container = document.createElement('div');
    container.style.position = 'fixed';
    container.style.top = '-9999px';
    container.style.left = '0';
    container.style.width = '210mm'; // A4 width
    container.style.backgroundColor = 'white';
    container.style.zIndex = '-1';

    // Inject HTML content directly
    container.innerHTML = `
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;600;700&display=swap');
            .invoice-content { 
                font-family: 'Be Vietnam Pro', sans-serif; 
                padding: 20px; 
                color: #000;
                background: white;
            }
            .invoice-box { max-width: 100%; margin: 0 auto; }
            .header { display: flex; justify-content: space-between; margin-bottom: 20px; }
            .logo { font-size: 24px; font-weight: bold; color: #1e3a8a; }
            .title { text-align: center; font-size: 20px; font-weight: bold; margin: 20px 0; text-transform: uppercase; }
            .customer-info { margin: 20px 0; font-size: 13px; line-height: 1.6; }
            table { width: 100%; border-collapse: collapse; margin: 20px 0; font-size: 12px; }
            th, td { border: 1px solid #ccc; padding: 10px; text-align: left; }
            th { background: #f5f5f5; font-weight: 700; text-align: center; }
            .text-right { text-align: right; }
            .total-section { text-align: right; margin-top: 30px; font-size: 14px; }
            .total-amount { font-weight: bold; font-size: 16px; margin-bottom: 5px; }
            .total-words { font-style: italic; font-size: 13px; color: #555; }
        </style>

        <div class="invoice-content">
            <div class="invoice-box">
                <div class="header">
                    <div class="logo">BizFlow</div>
                    <div style="text-align: right; font-size: 12px;">
                        <div><strong>Số:</strong> #${data.invoice.id}</div>
                        <div><strong>Ngày:</strong> ${createdDate.getDate()}/${createdDate.getMonth() + 1}/${createdDate.getFullYear()}</div>
                    </div>
                </div>
                
                <div class="title">HÓA ĐƠN BÁN LẺ</div>
                
                <div class="customer-info">
                    <div><strong>Đơn vị bán hàng:</strong> ${data.household?.name || 'Hộ Kinh Doanh'}</div>
                    <div><strong>MST:</strong> ${data.household?.tax_code || '---'}</div>
                    <div><strong>Địa chỉ:</strong> ${data.household?.address || '---'}</div>
                    <div><strong>SĐT:</strong> ${data.household?.phone || '---'}</div>
                    <hr style="margin: 10px 0; border: 0; border-top: 1px dashed #ccc;">
                    <div><strong>Khách hàng:</strong> ${data.customer?.name || 'Khách lẻ'}</div>
                    <div><strong>Địa chỉ:</strong> ${data.customer?.address || '---'}</div>
                    <div><strong>SĐT:</strong> ${data.customer?.phone || '---'}</div>
                </div>
                
                <table>
                    <thead>
                        <tr>
                            <th style="width: 5%">STT</th>
                            <th style="width: 40%">Tên sản phẩm</th>
                            <th style="width: 10%">ĐVT</th>
                            <th style="width: 10%">SL</th>
                            <th style="width: 15%">Đơn giá</th>
                            <th style="width: 20%">Thành tiền</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${data.details.map((item, index) => `
                            <tr>
                                <td style="text-align: center;">${index + 1}</td>
                                <td>${item.product_name}</td>
                                <td style="text-align: center;">${item.unit_name}</td>
                                <td class="text-right">${item.quantity}</td>
                                <td class="text-right">${Number(item.price || 0).toLocaleString('vi-VN')}</td>
                                <td class="text-right">${Number(item.line_total).toLocaleString('vi-VN')}</td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
                
                <div class="total-section">
                    <div class="total-amount">Tổng thanh toán: ${totalAmount.toLocaleString('vi-VN')} đ</div>
                    <div class="total-words">(Bằng chữ: ${numberToVietnameseWords(totalAmount)})</div>
                </div>
                
                <div style="display: flex; justify-content: space-between; margin-top: 50px; text-align: center; font-size: 12px;">
                    <div style="width: 40%">
                        <strong>Người mua hàng</strong><br>
                        (Ký, ghi rõ họ tên)
                    </div>
                    <div style="width: 40%">
                        <strong>Người bán hàng</strong><br>
                        (Ký, ghi rõ họ tên)
                    </div>
                </div>
            </div>
        </div>
    `;

    document.body.appendChild(container);

    // Wait for fonts to load
    await document.fonts.ready;

    // Additional small delay to ensure rendering
    await new Promise(resolve => setTimeout(resolve, 500));

    const options = {
        margin: [10, 10, 10, 10], // top, right, bottom, left
        filename: `Hoa_don_${data.invoice.id}.pdf`,
        image: { type: 'jpeg', quality: 0.98 },
        html2canvas: {
            scale: 2,
            useCORS: true,
            logging: false,
            letterRendering: true
        },
        jsPDF: {
            unit: 'mm',
            format: 'a4',
            orientation: 'portrait'
        }
    };

    try {
        await html2pdf().set(options).from(container).save();
    } catch (error) {
        console.error('PDF Generation Error:', error);
        alert('Có lỗi xảy ra khi xuất PDF. Vui lòng thử lại.');
    } finally {
        document.body.removeChild(container);
    }
};
