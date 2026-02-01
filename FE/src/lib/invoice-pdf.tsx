import { InvoicePDFData } from '@/components/invoice-template';
import { numberToVietnameseWords } from './number-to-words';

export const generateInvoicePDF = async (data: InvoicePDFData) => {
    // Open the print page in a new tab
    // We construct the URL manually or use a router push if we were in a component, 
    // but helper functions don't have access to router.
    // Assuming the URL structure is /owner/invoices/[id]/print
    const url = `/owner/invoices/${data.invoice.id}/print`;
    window.open(url, '_blank');
};
