import { pdf } from '@react-pdf/renderer';
import { InvoicePDFData } from '@/components/invoice-template';
import { numberToVietnameseWords } from './number-to-words';
import InvoicePDFDocument from '@/components/pdf/InvoicePDFDocument';

// Note: You might need to install file-saver: npm install file-saver @types/file-saver

export const generateInvoicePDF = async (data: InvoicePDFData) => {
    try {
        // Map data
        const isPurchaseInvoice = !!data.invoice.seller_id;
        const buyerInfo = isPurchaseInvoice ? data.household : data.customer;

        const items = data.details.map((d, index) => ({
            stt: index + 1,
            productName: d.product_name,
            unit: d.unit_name,
            quantity: d.quantity,
            unitPrice: Number(d.price || 0),
            total: Number(d.line_total || 0)
        }));

        const date = new Date(data.invoice.created_at);
        const day = date.getDate().toString().padStart(2, '0');
        const month = (date.getMonth() + 1).toString().padStart(2, '0');
        const year = date.getFullYear().toString();

        const totalAmount = Number(data.invoice.total_amount || 0);
        const totalInWords = numberToVietnameseWords(totalAmount);

        const props = {
            data: data,
            invoiceNumber: String(data.invoice.id),
            customerName: buyerInfo?.name || (isPurchaseInvoice ? '---' : 'Khách lẻ'),
            customerAddress: buyerInfo?.address || '---',
            customerPhone: buyerInfo?.phone || '---',
            items: items,
            totalAmount: totalAmount,
            totalInWords: totalInWords,
            day, month, year
        };

        // Generate PDF blob
        const blob = await pdf(<InvoicePDFDocument {...props} />).toBlob();

        // Save file
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `Hoa_don_${data.invoice.id}.pdf`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);

    } catch (error) {
        console.error('PDF Generation Error:', error);
        alert('Có lỗi xảy ra khi xuất PDF. Vui lòng thử lại.');
    }
};
