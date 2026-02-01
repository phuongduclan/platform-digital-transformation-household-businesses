import React from 'react';
import { numberToVietnameseWords } from '@/lib/number-to-words';

// Re-define interface here to avoid circular dependency (or import if shared)
// Re-define interface here to avoid circular dependency (or import if shared)
// Re-define interface here to avoid circular dependency (or import if shared)
export interface InvoicePDFData {
    invoice: {
        id: number;
        created_at: string;
        total_amount: string | number;
        seller_id?: number | null; // To distinguish Purchase vs Sales
        invoice_type?: string;
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
    seller: { // External Supplier for Purchase Invoices
        name: string | null;
        tax_code?: string | null;
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

export const InvoiceTemplate: React.FC<{ data: InvoicePDFData }> = ({ data }) => {
    const createdDate = new Date(data.invoice.created_at);
    const totalAmount = Number(data.invoice.total_amount);

    // Determine if it's a Purchase Invoice or Sales Invoice
    const isPurchaseInvoice = !!data.invoice.seller_id;
    const sellerInfo = isPurchaseInvoice ? data.seller : data.household;
    const buyerInfo = isPurchaseInvoice ? data.household : data.customer;

    // Fill rows to ensure exactly 12 lines
    const ROWS_COUNT = 12;
    const filledDetails = [...data.details];
    while (filledDetails.length < ROWS_COUNT) {
        filledDetails.push({
            product_name: '',
            unit_name: '',
            quantity: 0,
            price: null,
            line_total: ''
        });
    }

    return (
        <div style={{
            fontFamily: "'Be Vietnam Pro', sans-serif",
            padding: '40px 50px', // Adjusted padding matches A4 margins visually
            color: '#1e293b', // slate-800
            background: 'white',
            width: '210mm',
            minHeight: '297mm', // Force A4 height
            margin: '0 auto',
            boxSizing: 'border-box',
            fontSize: '13px',
            lineHeight: '1.4',
            position: 'relative'
        }}>
            <style>{`
                @import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;700&display=swap');
                
                /* Reset & Base */
                * { box-sizing: border-box; }
                
                /* Layout Classes */
                .header-flex { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 30px; }
                .logo-section { width: 60%; }
                .meta-box { 
                    background-color: #f1f5f9; 
                    padding: 8px 12px; 
                    font-size: 11px; 
                    font-weight: 600; 
                    text-align: center;
                    border: 1px solid #e2e8f0;
                    width: 200px;
                }
                
                /* Title */
                .invoice-title { 
                    text-align: center; 
                    font-size: 24px; 
                    font-weight: 700; 
                    text-transform: uppercase; 
                    margin: 20px 0 30px 0;
                    color: #1e293b;
                }
                
                /* Info Lines */
                .info-row { display: flex; margin-bottom: 8px; align-items: flex-end; }
                .info-label { font-weight: 700; min-width: 120px; font-size: 13px; }
                .info-content { 
                    flex-grow: 1; 
                    border-bottom: 1px solid #94a3b8; 
                    padding-left: 10px; 
                    padding-bottom: 2px;
                    min-height: 20px;
                    font-size: 13px;
                }
                
                /* Table */
                table { width: 100%; border-collapse: collapse; margin-top: 20px; margin-bottom: 20px; }
                th { 
                    background-color: #f1f5f9; 
                    font-weight: 700; 
                    text-transform: uppercase; 
                    font-size: 11px; 
                    padding: 8px; 
                    border: 1px solid #64748b; 
                    text-align: center;
                }
                td { 
                    border: 1px solid #64748b; 
                    padding: 6px 8px; 
                    vertical-align: middle;
                    height: 32px; /* Ensure consistent row height */
                }
                
                /* Footer */
                .footer-flex { display: flex; justify-content: flex-end; margin-top: 10px; }
                .total-row { display: flex; align-items: center; width: 100%; margin-bottom: 10px; }
                .total-label { font-weight: 700; width: 150px; text-align: right; padding-right: 15px; }
                .total-value { 
                    flex-grow: 1; 
                    border-bottom: 1px solid #94a3b8; 
                    text-align: right; 
                    font-weight: 700;
                    font-size: 15px;
                    padding-bottom: 2px;
                }
                
                .words-row { display: flex; width: 100%; margin-bottom: 30px; }
                .words-label { font-weight: 700; white-space: nowrap; margin-right: 10px; font-size: 12px; }
                .words-value { 
                    flex-grow: 1; 
                    border-bottom: 1px solid #94a3b8; 
                    font-style: italic; 
                    font-size: 12px;
                }

                .warranty-text { font-size: 11px; font-style: italic; margin-top: 10px; text-align: left; }
                
                .signature-section { 
                    margin-top: 40px; 
                    text-align: right; 
                    font-size: 12px;
                    display: flex;
                    justify-content: flex-end;
                }
                .date-line { font-style: italic; margin-bottom: 5px; margin-right: 20px; }
            `}</style>

            {/* Header */}
            <div className="header-flex">
                <div className="logo-section">
                    <div style={{ fontSize: '28px', fontWeight: '800', color: '#1e3a8a', marginBottom: '8px' }}>BizFlow</div>
                    <div style={{ fontSize: '12px', marginBottom: '4px' }}>
                        <span style={{ fontWeight: '600' }}>Đ/C:</span> {sellerInfo?.address || '---'}
                    </div>
                    <div style={{ fontSize: '12px' }}>
                        <span style={{ fontWeight: '600' }}>SĐT:</span> {sellerInfo?.phone || '---'}
                    </div>
                </div>
                <div>
                    <div className="meta-box">
                        Ban hành kèm theo<br />
                        thông tư số 88/2021/<br />
                        TT-BTC
                    </div>
                    <div style={{ textAlign: 'center', marginTop: '10px', fontSize: '12px', color: '#cc3333', fontWeight: '700' }}>
                        SỐ: <span style={{ color: '#000' }}>#{data.invoice.id}</span>
                    </div>
                </div>
            </div>

            {/* Title */}
            <div className="invoice-title">HÓA ĐƠN BÁN LẺ</div>

            {/* Buyer Info */}
            <div>
                <div className="info-row">
                    <span className="info-label">Tên khách hàng:</span>
                    <span className="info-content">{buyerInfo?.name || (isPurchaseInvoice ? '---' : 'Khách lẻ')}</span>
                </div>
                <div className="info-row">
                    <span className="info-label">Địa chỉ:</span>
                    <span className="info-content">{buyerInfo?.address || '---'}</span>
                </div>
                <div className="info-row">
                    <span className="info-label">Điện thoại:</span>
                    <span className="info-content">{buyerInfo?.phone || '---'}</span>
                </div>
            </div>

            {/* Table */}
            <table>
                <colgroup>
                    <col style={{ width: '50px' }} />
                    <col style={{ width: 'auto' }} />
                    <col style={{ width: '80px' }} />
                    <col style={{ width: '60px' }} />
                    <col style={{ width: '110px' }} />
                    <col style={{ width: '110px' }} />
                </colgroup>
                <thead>
                    <tr>
                        <th>STT</th>
                        <th>TÊN SẢN PHẨM</th>
                        <th>ĐVT</th>
                        <th>SL</th>
                        <th>ĐƠN GIÁ</th>
                        <th>THÀNH TIỀN</th>
                    </tr>
                </thead>
                <tbody>
                    {filledDetails.map((item, index) => {
                        const hasData = !!item.product_name;
                        return (
                            <tr key={index}>
                                <td style={{ textAlign: 'center' }}>{hasData ? index + 1 : ''}</td>
                                <td>{item.product_name}</td>
                                <td style={{ textAlign: 'center' }}>{item.unit_name}</td>
                                <td style={{ textAlign: 'center' }}>{hasData ? item.quantity : ''}</td>
                                <td style={{ textAlign: 'right' }}>{hasData ? Number(item.price || 0).toLocaleString('vi-VN') : ''}</td>
                                <td style={{ textAlign: 'right' }}>{hasData ? Number(item.line_total).toLocaleString('vi-VN') : ''}</td>
                            </tr>
                        );
                    })}
                </tbody>
            </table>

            {/* Footer Totals */}
            <div className="footer-flex" style={{ flexDirection: 'column', alignItems: 'flex-end' }}>
                <div className="total-row" style={{ width: '60%' }}>
                    <span className="total-label">Tổng cộng:</span>
                    <span className="total-value">{totalAmount.toLocaleString('vi-VN')}</span>
                </div>
            </div>

            <div className="words-row">
                <span className="words-label">Số tiền bằng chữ:</span>
                <span className="words-value">{numberToVietnameseWords(totalAmount)}</span>
            </div>

            <div className="warranty-text">
                Sản phẩm được bảo hành ________ tháng theo quy định của nhà sản xuất.
            </div>

            {/* Signature */}
            <div className="signature-section">
                <div>
                    <div className="date-line">
                        ngày ____, tháng ____, năm 20__
                    </div>
                </div>
            </div>
        </div>
    );
};
