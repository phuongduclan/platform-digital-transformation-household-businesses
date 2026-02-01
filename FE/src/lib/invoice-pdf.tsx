import { renderToStaticMarkup } from 'react-dom/server';
import { InvoicePDFData, InvoiceTemplate } from '@/components/invoice-template';

export const generateInvoicePDF = async (data: InvoicePDFData) => {
    // Dynamically import html2pdf
    const html2pdf = (await import('html2pdf.js')).default;

    // Generate HTML string from React Component
    const htmlContent = renderToStaticMarkup(<InvoiceTemplate data={data} />);

    // Create container for PDF content
    const container = document.createElement('div');
    container.style.position = 'absolute';
    container.style.top = '0';
    container.style.left = '0';
    container.style.width = '210mm'; // A4 width
    container.style.opacity = '0';
    container.style.pointerEvents = 'none';
    container.style.zIndex = '-1000';
    container.style.backgroundColor = 'white';

    // Inject font link and HTML content
    // We add the link tag here to ensure it's in the DOM during capture
    container.innerHTML = `
        <link href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;600;700&display=swap" rel="stylesheet">
        <div style="background: white;">
            ${htmlContent}
        </div>
    `;

    document.body.appendChild(container);

    // Wait for fonts to load
    try {
        await document.fonts.ready;
    } catch (e) {
        console.warn('Font loading failed or timed out', e);
    }

    // Additional delay to ensure layout is calculated and rendered
    await new Promise(resolve => setTimeout(resolve, 1500));

    const options = {
        margin: [10, 10, 10, 10], // top, right, bottom, left
        filename: `Hoa_don_${data.invoice.id}.pdf`,
        image: { type: 'jpeg', quality: 0.98 },
        html2canvas: {
            scale: 2,
            useCORS: true,
            logging: true,
            letterRendering: true,
            scrollX: 0,
            scrollY: 0,
            windowWidth: 794, // Standard A4 width in px
            backgroundColor: '#ffffff'
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
