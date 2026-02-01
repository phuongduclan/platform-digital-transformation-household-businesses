import { renderToStaticMarkup } from 'react-dom/server';
import { InvoicePDFData, InvoiceTemplate } from '@/components/invoice-template';

export const generateInvoicePDF = async (data: InvoicePDFData) => {
    // Dynamically import html2pdf
    const html2pdf = (await import('html2pdf.js')).default;

    // Generate HTML string from React Component
    const htmlContent = renderToStaticMarkup(<InvoiceTemplate data={ data } />);

    // Create container for PDF content
    const container = document.createElement('div');
    container.style.position = 'fixed';
    container.style.top = '-9999px';
    container.style.left = '0';
    container.style.width = '210mm'; // A4 width

    // IMPORTANT: Inject HTML
    container.innerHTML = htmlContent;

    document.body.appendChild(container);

    // Wait for fonts to load
    await document.fonts.ready;

    // Additional delay to ensure layout is calculated
    await new Promise(resolve => setTimeout(resolve, 800));

    const options = {
        margin: [10, 10, 10, 10], // top, right, bottom, left
        filename: `Hoa_don_${data.invoice.id}.pdf`,
        image: { type: 'jpeg', quality: 0.98 },
        html2canvas: {
            scale: 2,
            useCORS: true,
            logging: true, // Enable logging to debug
            letterRendering: true,
            windowWidth: 794 // A4 width in px at 96 DPI
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
