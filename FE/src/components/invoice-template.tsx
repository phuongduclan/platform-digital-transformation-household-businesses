import React from 'react';
import { numberToVietnameseWords } from '@/lib/number-to-words';

// Re-define interface here to avoid circular dependency (or import if shared)
export interface InvoicePDFData {
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

export const InvoiceTemplate: React.FC<{ data: InvoicePDFData }> = ({ data }) => {
    const createdDate = new Date(data.invoice.created_at);
    const totalAmount = Number(data.invoice.total_amount);

    return (
        <div style={{
            fontFamily: "'Be Vietnam Pro', sans-serif",
            padding: '40px',
            color: '#000',
            background: 'white',
            width: '100%',
            maxWidth: '210mm',
            margin: '0 auto',
            boxSizing: 'border-box'
        }}>
            <style>{`
                @import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;600;700&display=swap');
            `}</style>

            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '30px' }}>
                <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#1e3a8a' }}>BizFlow</div>
                <div style={{ textAlign: 'right', fontSize: '12px' }}>
                    <div><strong>Số:</strong> #{data.invoice.id}</div>
                    <div><strong>Ngày:</strong> {createdDate.getDate()}/{createdDate.getMonth() + 1}/{createdDate.getFullYear()}</div>
                </div>
            </div>

            <div style={{
                textAlign: 'center',
                fontSize: '24px',
                fontWeight: 'bold',
                margin: '30px 0',
                textTransform: 'uppercase',
                letterSpacing: '1px'
            }}>
                HÓA ĐƠN BÁN LẺ
            </div>

            <div style={{ fontSize: '13px', lineHeight: '1.8', marginBottom: '30px' }}>
                <div style={{ display: 'grid', gridTemplateColumns: '130px 1fr', gap: '5px' }}>
                    <strong>Đơn vị bán hàng:</strong> <span>{data.household?.name || 'Hộ Kinh Doanh'}</span>
                    <strong>MST:</strong> <span>{data.household?.tax_code || '---'}</span>
                    <strong>Địa chỉ:</strong> <span>{data.household?.address || '---'}</span>
                    <strong>SĐT:</strong> <span>{data.household?.phone || '---'}</span>
                </div>

                <div style={{ borderTop: '1px dashed #ccc', margin: '15px 0' }}></div>

                <div style={{ display: 'grid', gridTemplateColumns: '130px 1fr', gap: '5px' }}>
                    <strong>Khách hàng:</strong> <span>{data.customer?.name || 'Khách lẻ'}</span>
                    <strong>Địa chỉ:</strong> <span>{data.customer?.address || '---'}</span>
                    <strong>SĐT:</strong> <span>{data.customer?.phone || '---'}</span>
                </div>
            </div>

            <table style={{
                width: '100%',
                borderCollapse: 'collapse',
                marginBottom: '30px',
                fontSize: '12px'
            }}>
                <thead>
                    <tr style={{ background: '#f8fafc' }}>
                        <th style={{ border: '1px solid #e2e8f0', padding: '12px 8px', width: '50px', textAlign: 'center' }}>STT</th>
                        <th style={{ border: '1px solid #e2e8f0', padding: '12px 8px', textAlign: 'left' }}>Tên sản phẩm</th>
                        <th style={{ border: '1px solid #e2e8f0', padding: '12px 8px', width: '80px', textAlign: 'center' }}>ĐVT</th>
                        <th style={{ border: '1px solid #e2e8f0', padding: '12px 8px', width: '80px', textAlign: 'right' }}>SL</th>
                        <th style={{ border: '1px solid #e2e8f0', padding: '12px 8px', width: '120px', textAlign: 'right' }}>Đơn giá</th>
                        <th style={{ border: '1px solid #e2e8f0', padding: '12px 8px', width: '140px', textAlign: 'right' }}>Thành tiền</th>
                    </tr>
                </thead>
                <tbody>
                    {data.details.map((item, index) => (
                        <tr key={index}>
                            <td style={{ border: '1px solid #e2e8f0', padding: '10px 8px', textAlign: 'center' }}>{index + 1}</td>
                            <td style={{ border: '1px solid #e2e8f0', padding: '10px 8px' }}>{item.product_name}</td>
                            <td style={{ border: '1px solid #e2e8f0', padding: '10px 8px', textAlign: 'center' }}>{item.unit_name}</td>
                            <td style={{ border: '1px solid #e2e8f0', padding: '10px 8px', textAlign: 'right' }}>{item.quantity}</td>
                            <td style={{ border: '1px solid #e2e8f0', padding: '10px 8px', textAlign: 'right' }}>{Number(item.price || 0).toLocaleString('vi-VN')}</td>
                            <td style={{ border: '1px solid #e2e8f0', padding: '10px 8px', textAlign: 'right', fontWeight: 'bold' }}>{Number(item.line_total).toLocaleString('vi-VN')}</td>
                        </tr>
                    ))}
                </tbody>
            </table>

            <div style={{ textAlign: 'right', marginBottom: '50px' }}>
                <div style={{ fontSize: '16px', fontWeight: 'bold', marginBottom: '8px' }}>
                    Tổng thanh toán: <span style={{ color: '#1e3a8a' }}>{totalAmount.toLocaleString('vi-VN')} đ</span>
                </div>
                <div style={{ fontSize: '13px', fontStyle: 'italic', color: '#666' }}>
                    (Bằng chữ: {numberToVietnameseWords(totalAmount)})
                </div>
            </div>

            <div style={{
                display: 'flex',
                justifyContent: 'space-between',
                textAlign: 'center',
                fontSize: '13px',
                marginTop: '60px'
            }}>
                <div style={{ width: '200px' }}>
                    <strong>Người mua hàng</strong>
                    <div style={{ fontSize: '11px', color: '#666', marginTop: '4px' }}>(Ký, ghi rõ họ tên)</div>
                </div>
                <div style={{ width: '200px' }}>
                    <strong>Người bán hàng</strong>
                    <div style={{ fontSize: '11px', color: '#666', marginTop: '4px' }}>(Ký, ghi rõ họ tên)</div>
                </div>
            </div>
        </div>
    );
};
