'use client';

import React, { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import { ownerService } from '@/services/owner.service';
import RetailInvoiceTemplate from '@/components/retail-invoice-template';
import { numberToVietnameseWords } from '@/lib/number-to-words';

export default function InvoicePrintPage() {
    const params = useParams();
    const id = params?.id ? parseInt(params.id as string) : null;
    const [templateProps, setTemplateProps] = useState<any>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        if (!id) return;

        const fetchData = async () => {
            try {
                const data = await ownerService.printInvoice(id);

                // Map data to template props
                const isPurchaseInvoice = !!data.invoice.seller_id;
                const buyerInfo = isPurchaseInvoice ? data.household : data.customer;

                const items = data.details.map((d: any, index: number) => ({
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
                    invoiceNumber: String(data.invoice.id),
                    serialNumber: data.invoice.invoice_type || '',
                    customerName: buyerInfo?.name || (isPurchaseInvoice ? '---' : 'Khách lẻ'),
                    customerAddress: buyerInfo?.address || '---',
                    customerPhone: buyerInfo?.phone || '---',
                    items: items,
                    totalAmount: totalAmount,
                    totalInWords: totalInWords,
                    date: { day, month, year }
                };

                setTemplateProps(props);
            } catch (err: any) {
                console.error(err);
                setError('Không thể tải thông tin hóa đơn.');
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, [id]);

    useEffect(() => {
        if (templateProps && !loading) {
            // Auto print when loaded
            setTimeout(() => {
                window.print();
            }, 500);
        }
    }, [templateProps, loading]);

    if (loading) return <div className="p-8 text-center">Đang tải bản in...</div>;
    if (error) return <div className="p-8 text-center text-red-600">{error}</div>;
    if (!templateProps) return null;

    return (
        <div className="print-page">
            <style jsx global>{`
                @media print {
                    @page {
                        margin: 0;
                        size: A4;
                    }
                    body {
                        margin: 0;
                        padding: 0;
                        background: white;
                    }
                    .no-print {
                        display: none !important;
                    }
                }
                .print-page {
                    background: white;
                    min-height: 100vh;
                    display: flex;
                    justify-content: center;
                    padding: 20px;
                }
                @media print {
                    .print-page {
                        padding: 0;
                        display: block;
                    }
                }
            `}</style>

            <div className="no-print fixed top-4 right-4 flex gap-2">
                <button
                    onClick={() => window.print()}
                    className="bg-blue-600 text-white px-4 py-2 rounded shadow hover:bg-blue-700"
                >
                    In Hóa Đơn
                </button>
            </div>

            <RetailInvoiceTemplate {...templateProps} />
        </div>
    );
}
