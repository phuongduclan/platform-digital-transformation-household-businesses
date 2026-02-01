import { renderToStaticMarkup } from 'react-dom/server';
import { InvoicePDFData } from '@/components/invoice-template';
import RetailInvoiceTemplate from '@/components/retail-invoice-template';
import { numberToVietnameseWords } from './number-to-words';

export const generateInvoicePDF = async (data: InvoicePDFData) => {
    // Dynamically import html2pdf
    const html2pdf = (await import('html2pdf.js')).default;

    // Map InvoicePDFData to RetailInvoiceTemplateProps
    const isPurchaseInvoice = !!data.invoice.seller_id;
    // For sales invoice: household is seller, customer is buyer
    // For purchase invoice: seller is seller, household is buyer

    // Note: RetailInvoiceTemplate expects "customer" info. 
    // In our context, the "customer" shown on invoice is the Buyer.
    const buyerInfo = isPurchaseInvoice ? data.household : data.customer;

    // The "Seller" info is hardcoded in RetailInvoiceTemplate (BizFlow) or should be passed?
    // RetailInvoiceTemplate currently has hardcoded "BizFlow" header. 
    // Ideally we should pass seller info too, but for now we map what we have.

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

    const templateProps = {
        invoiceNumber: String(data.invoice.id),
        serialNumber: data.invoice.invoice_type || '', // Or other field if available
        customerName: buyerInfo?.name || (isPurchaseInvoice ? '---' : 'Khách lẻ'),
        customerAddress: buyerInfo?.address || '---',
        customerPhone: buyerInfo?.phone || '---',
        items: items,
        totalAmount: totalAmount,
        totalInWords: totalInWords,
        date: { day, month, year }
    };

    // Generate HTML string from React Component
    const htmlContent = renderToStaticMarkup(<RetailInvoiceTemplate {...templateProps} />);

    // Create container for PDF content
    const container = document.createElement('div');
    container.style.position = 'fixed';
    container.style.top = '0';
    container.style.left = '0';
    container.style.width = '210mm'; // A4 width
    container.style.zIndex = '-9999';
    container.style.backgroundColor = '#ffffff';

    // Inject font link and HTML content
    // Note: Tailwind classes need the style to be present. 
    // Since we are not building CSS, we rely on html2pdf using computed styles 
    // OR we need to ensure the styles are available.
    // However, html2pdf renders in a hidden iframe/container usually?
    // Using `document.body.appendChild(container)` puts it in the main document, 
    // so it should inherit global styles if they apply.
    // BUT `RetailInvoiceTemplate` uses specific tailwind utility classes.
    // If we just dump HTML, those classes might rely on Tailwind stylesheet being present in the page.
    // Since this runs in the browser where the app is loaded, the Tailwind styles SHOULD be available.

    container.innerHTML = `
        <style>
            .invoice-container { background: white; width: 100%; min-height: 297mm; }
        </style>
        <div class="invoice-container">
            ${htmlContent}
        </div>
    `;

    document.body.appendChild(container);

    // Wait for fonts/images
    try {
        await document.fonts.ready;
    } catch (e) {
        console.warn('Font loading failed', e);
    }
    await new Promise(resolve => setTimeout(resolve, 1000));

    const options = {
        margin: 0,
        filename: `Hoa_don_${data.invoice.id}.pdf`,
        image: { type: 'jpeg', quality: 0.98 },
        html2canvas: {
            scale: 2,
            useCORS: true,
            logging: true,
            letterRendering: true,
            windowWidth: 794 // 210mm @ 96 DPI
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
        if (document.body.contains(container)) {
            document.body.removeChild(container);
        }
    }
};

