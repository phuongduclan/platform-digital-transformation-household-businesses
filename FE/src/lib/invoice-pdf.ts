import jsPDF from 'jspdf';
import { EmployeeInvoice } from '@/services/employee.service';

interface InvoicePDFData {
    invoice: EmployeeInvoice & { total_amount: string };
    household: {
        name: string | null;
        tax_code: string | null;
        address: string | null;
        phone: string | null;
        description: string | null;
    } | null;
    customer: {
        name: string | null;
        tax_code: string | null;
        address: string | null;
        phone: string | null;
    } | null;
    seller: {
        name: string | null;
        tax_code: string | null;
        address: string | null;
        phone: string | null;
    } | null;
    details: Array<{
        id: number;
        product_name: string;
        unit_name: string;
        quantity: number;
        price: string | null;
        discount: string | null;
        vat: number;
        line_total: string;
    }>;
}

export const generateInvoicePDF = async (data: InvoicePDFData) => {
    const doc = new jsPDF();

    // Note: Default jsPDF fonts do not support Vietnamese characters well.
    // For a production app, we should load a custom font that supports Vietnamese.

    doc.setFontSize(20);
    doc.text('HOA DON / INVOICE', 105, 20, { align: 'center' });

    doc.setFontSize(10);
    doc.text(`Ma hoa don: ${data.invoice.id}`, 150, 30);
    doc.text(`Ngay: ${new Date(data.invoice.created_at).toLocaleDateString()}`, 150, 35);

    let y = 50;

    // Household info (Left side)
    if (data.household) {
        doc.setFontSize(12);
        doc.text(data.household.name || 'Household Business', 20, y);
        y += 5;
        doc.setFontSize(10);
        doc.text(`MST: ${data.household.tax_code || ''}`, 20, y);
        y += 5;
        doc.text(`Dia chi: ${data.household.address || ''}`, 20, y);
        y += 5;
        doc.text(`SDT: ${data.household.phone || ''}`, 20, y);
        y += 10;
    }

    // Customer info (Right side - roughly)
    // Reset y for customer if needed or just place below
    // For simplicity, placing below household for now
    if (data.customer) {
        y += 5;
        doc.setFontSize(11);
        doc.text('Khach hang:', 20, y);
        y += 5;
        doc.setFontSize(10);
        doc.text(data.customer.name || 'Guest', 30, y);
        y += 5;
        if (data.customer.tax_code) {
            doc.text(`MST: ${data.customer.tax_code}`, 30, y);
            y += 5;
        }
        if (data.customer.address) {
            doc.text(`Dia chi: ${data.customer.address}`, 30, y);
            y += 5;
        }
        y += 5;
    }

    // Table Header
    y += 5;
    doc.line(20, y, 190, y);
    y += 5;
    doc.setFontSize(10);
    doc.text('San pham', 20, y);
    doc.text('DVT', 80, y);
    doc.text('SL', 100, y);
    doc.text('Don gia', 120, y);
    doc.text('Thanh tien', 160, y);
    y += 3;
    doc.line(20, y, 190, y);
    y += 7;

    // Table Rows
    data.details.forEach((item) => {
        doc.text(item.product_name, 20, y);
        doc.text(item.unit_name, 80, y);
        doc.text(String(item.quantity), 100, y);
        doc.text(String(item.price), 120, y);
        doc.text(item.line_total, 160, y);
        y += 7;
    });

    doc.line(20, y, 190, y);
    y += 10;

    doc.setFontSize(12);
    doc.text(`Tong cong: ${data.invoice.total_amount}`, 140, y);

    doc.save(`invoice-${data.invoice.id}.pdf`);
};
