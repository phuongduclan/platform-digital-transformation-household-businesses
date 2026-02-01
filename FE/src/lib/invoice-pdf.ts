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

    // Create HTML string with Vietnamese font
    const htmlContent = `
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <link rel="preconnect" href="https://fonts.googleapis.com">
            <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
            <link href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;600;700&display=swap" rel="stylesheet">
            <style>
                * { margin: 0; padding: 0; box-sizing: border-box; }
                body { font-family: 'Be Vietnam Pro', sans-serif; padding: 20px; }
                .invoice { max-width: 800px; margin: 0 auto; }
                .header { display: flex; justify-content: space-between; margin-bottom: 20px; }
                .logo { font-size: 24px; font-weight: bold; color: #1e3a8a; }
                .title { text-align: center; font-size: 20px; font-weight: bold; margin: 20px 0; }
                .customer { margin: 20px 0; font-size: 12px; }
                table { width: 100%; border-collapse: collapse; margin: 20px 0; font-size: 11px; }
                th, td { border: 1px solid #ccc; padding: 8px; text-align: left; }
                th { background: #f5f5f5; font-weight: 600; }
                .total { text-align: right; margin: 20px 0; font-size: 14px; font-weight: bold; }
            </style>
        </head>
        <body>
            <div class="invoice">
                <div class="header">
                    <div class="logo">BizFlow</div>
                    <div style="text-align: right; font-size: 11px;">
                        <div>Mã hóa đơn: ${data.invoice.id}</div>
                        <div>Ngày: ${createdDate.getDate()}/${createdDate.getMonth() + 1}/${createdDate.getFullYear()}</div>
                    </div>
                </div>
                
                <div class="title">HÓA ĐƠN BÁN LẺ / INVOICE</div>
                
                <div class="customer">
                    <div><strong>MST:</strong> ${data.household?.tax_code || ''}</div>
                    <div><strong>Địa chỉ:</strong> ${data.household?.address || ''}</div>
                    <div><strong>SĐT:</strong> ${data.household?.phone || ''}</div>
                    <br>
                    <div><strong>Khách hàng:</strong> ${data.customer?.name || 'Khách lẻ'}</div>
                    <div><strong>Địa chỉ:</strong> ${data.customer?.address || ''}</div>
                    <div><strong>Điện thoại:</strong> ${data.customer?.phone || ''}</div>
                </div>
                
                <table>
                    <thead>
                        <tr>
                            <th>Sản phẩm</th>
                            <th>ĐVT</th>
                            <th style="text-align: right;">SL</th>
                            <th style="text-align: right;">Đơn giá</th>
                            <th style="text-align: right;">Thành tiền</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${data.details.map((item) => `
                            <tr>
                                <td>${item.product_name}</td>
                                <td>${item.unit_name}</td>
                                <td style="text-align: right;">${item.quantity}</td>
                                <td style="text-align: right;">${Number(item.price || 0).toLocaleString('vi-VN')}</td>
                                <td style="text-align: right;">${Number(item.line_total).toLocaleString('vi-VN')}</td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
                
                <div class="total">
                    <div>Tổng cộng: ${totalAmount.toLocaleString('vi-VN')} đồng</div>
                    <div style="font-size: 11px; font-weight: normal; margin-top: 5px;">
                        Bằng chữ: ${numberToVietnameseWords(totalAmount)}
                    </div>
                </div>
            </div>
        </body>
        </html>
    `;

    // Create temporary element
    const tempDiv = document.createElement('div');
    tempDiv.innerHTML = htmlContent;
    tempDiv.style.position = 'absolute';
    tempDiv.style.left = '-9999px';
    document.body.appendChild(tempDiv);

    // Wait for fonts to load
    await document.fonts.ready;

    const options = {
        margin: 10,
        filename: `hoa-don-${data.invoice.id}.pdf`,
        image: { type: 'jpeg', quality: 0.98 },
        html2canvas: {
            scale: 2,
            useCORS: true,
            logging: false
        },
        jsPDF: {
            unit: 'mm',
            format: 'a4',
            orientation: 'portrait'
        }
    };

    try {
        await html2pdf().set(options).from(tempDiv).save();
    } finally {
        document.body.removeChild(tempDiv);
    }
};
