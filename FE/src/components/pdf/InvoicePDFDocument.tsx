import React from 'react';
import { Page, Text, View, Document, StyleSheet, Font } from '@react-pdf/renderer';
import { InvoicePDFData } from '@/components/invoice-template';

// Register font for Vietnamese support
Font.register({
    family: 'BeVietnamPro',
    fonts: [
        { src: 'https://cdn.jsdelivr.net/fontsource/fonts/be-vietnam-pro@latest/vietnamese-400-normal.woff' },
        { src: 'https://cdn.jsdelivr.net/fontsource/fonts/be-vietnam-pro@latest/vietnamese-700-normal.woff', fontWeight: 700 },
        { src: 'https://cdn.jsdelivr.net/fontsource/fonts/be-vietnam-pro@latest/vietnamese-500-normal.woff', fontWeight: 500 },
        { src: 'https://cdn.jsdelivr.net/fontsource/fonts/be-vietnam-pro@latest/vietnamese-600-normal.woff', fontWeight: 600 },
    ]
});

// Styles
const styles = StyleSheet.create({
    page: {
        fontFamily: 'BeVietnamPro',
        padding: 40,
        fontSize: 10,
        lineHeight: 1.5,
    },
    header: {
        flexDirection: 'row',
        marginBottom: 20,
    },
    headerLeft: {
        flexGrow: 1,
    },
    headerRight: {
        alignItems: 'flex-end',
    },
    companyName: {
        fontSize: 18,
        fontWeight: 'bold',
        color: '#1e3a8a',
        marginBottom: 4,
    },
    smallText: {
        fontSize: 9,
        color: '#4b5563',
        marginBottom: 2,
    },
    circularInfo: {
        fontSize: 8,
        color: '#374151',
        textAlign: 'right',
        marginBottom: 1,
    },
    invoiceNumber: {
        fontSize: 11,
        color: '#dc2626',
        fontWeight: 'bold',
        marginTop: 4,
    },
    title: {
        fontSize: 16,
        fontWeight: 'bold',
        textAlign: 'center',
        textTransform: 'uppercase',
        marginBottom: 20,
        marginTop: 10,
    },
    customerSection: {
        marginBottom: 20,
    },
    row: {
        flexDirection: 'row',
        marginBottom: 6,
        alignItems: 'flex-end',
    },
    label: {
        width: 100,
        fontSize: 10,
        fontWeight: 'bold',
    },
    value: {
        flex: 1,
        borderBottomWidth: 1,
        borderBottomColor: '#9ca3af',
        paddingBottom: 2,
        fontSize: 10,
    },
    table: {
        width: '100%',
        borderStyle: 'solid',
        borderWidth: 1,
        borderColor: '#000',
        marginBottom: 20,
    },
    tableRow: {
        flexDirection: 'row',
        borderBottomWidth: 1,
        borderBottomColor: '#000',
        minHeight: 25,
        alignItems: 'center',
    },
    tableHeader: {
        backgroundColor: '#f1f5f9',
        fontWeight: 'bold',
    },
    col1: { width: '8%', borderRightWidth: 1, borderRightColor: '#000', textAlign: 'center', padding: 4, fontSize: 9 },
    col2: { width: '42%', borderRightWidth: 1, borderRightColor: '#000', padding: 4, fontSize: 9 },
    col3: { width: '10%', borderRightWidth: 1, borderRightColor: '#000', textAlign: 'center', padding: 4, fontSize: 9 },
    col4: { width: '10%', borderRightWidth: 1, borderRightColor: '#000', textAlign: 'center', padding: 4, fontSize: 9 },
    col5: { width: '15%', borderRightWidth: 1, borderRightColor: '#000', textAlign: 'right', padding: 4, fontSize: 9 },
    col6: { width: '15%', textAlign: 'right', padding: 4, fontSize: 9 },

    totalSection: {
        marginBottom: 20,
    },
    totalRow: {
        flexDirection: 'row',
        alignItems: 'center',
        marginBottom: 5,
        justifyContent: 'flex-end'
    },
    totalLabel: {
        width: 100,
        fontWeight: 'bold',
        textAlign: 'right',
        marginRight: 10,
    },
    totalValue: {
        width: 150,
        textAlign: 'right',
        fontWeight: 'bold',
        borderBottomWidth: 1,
        borderBottomColor: '#9ca3af',
        fontSize: 12,
    },
    footer: {
        marginTop: 30,
    },
    dateSection: {
        marginTop: 20,
        textAlign: 'right',
        fontStyle: 'italic',
    }
});

export interface InvoicePDFDocumentProps {
    data: InvoicePDFData;
    invoiceNumber: string;
    customerName: string;
    customerAddress: string;
    customerPhone: string;
    items: any[];
    totalAmount: number;
    totalInWords: string;
    day: string;
    month: string;
    year: string;
}

const InvoicePDFDocument: React.FC<InvoicePDFDocumentProps> = ({
    invoiceNumber,
    customerName,
    customerAddress,
    customerPhone,
    items,
    totalAmount,
    totalInWords,
    day,
    month,
    year
}) => {
    // Fill to 12 rows
    const filledItems = [...items];
    while (filledItems.length < 12) {
        filledItems.push({
            stt: filledItems.length + 1,
            productName: '',
            unit: '',
            quantity: 0,
            unitPrice: 0,
            total: 0
        });
    }

    return (
        <Document>
            <Page size="A4" style={styles.page}>
                {/* Header */}
                <View style={styles.header}>
                    <View style={styles.headerLeft}>
                        <Text style={styles.companyName}>BizFlow</Text>
                        <Text style={styles.smallText}>Đ/C: ...</Text>
                        <Text style={styles.smallText}>SĐT: ...</Text>
                    </View>
                    <View style={styles.headerRight}>
                        <Text style={styles.circularInfo}>Ban hành kèm theo</Text>
                        <Text style={styles.circularInfo}>thông tư số</Text>
                        <Text style={styles.circularInfo}>88/2021/TT-BTC</Text>
                        <Text style={styles.invoiceNumber}>SỐ: {invoiceNumber}</Text>
                    </View>
                </View>

                {/* Title */}
                <Text style={styles.title}>HÓA ĐƠN BÁN LẺ</Text>

                {/* Customer Info */}
                <View style={styles.customerSection}>
                    <View style={styles.row}>
                        <Text style={styles.label}>Tên khách hàng:</Text>
                        <Text style={styles.value}>{customerName}</Text>
                    </View>
                    <View style={styles.row}>
                        <Text style={styles.label}>Địa chỉ:</Text>
                        <Text style={styles.value}>{customerAddress}</Text>
                    </View>
                    <View style={styles.row}>
                        <Text style={styles.label}>Điện thoại:</Text>
                        <Text style={styles.value}>{customerPhone}</Text>
                    </View>
                </View>

                {/* Table */}
                <View style={styles.table}>
                    {/* Header */}
                    <View style={[styles.tableRow, styles.tableHeader]}>
                        <Text style={styles.col1}>STT</Text>
                        <Text style={styles.col2}>TÊN SẢN PHẨM</Text>
                        <Text style={styles.col3}>ĐVT</Text>
                        <Text style={styles.col4}>SL</Text>
                        <Text style={styles.col5}>ĐƠN GIÁ</Text>
                        <Text style={styles.col6}>THÀNH TIỀN</Text>
                    </View>

                    {/* Rows */}
                    {filledItems.map((item, index) => (
                        <View key={index} style={styles.tableRow}>
                            <Text style={styles.col1}>{item.productName ? index + 1 : ''}</Text>
                            <Text style={styles.col2}>{item.productName}</Text>
                            <Text style={styles.col3}>{item.productName ? item.unit : ''}</Text>
                            <Text style={styles.col4}>{item.quantity > 0 ? item.quantity : ''}</Text>
                            <Text style={styles.col5}>{item.unitPrice > 0 ? item.unitPrice.toLocaleString('vi-VN') : ''}</Text>
                            <Text style={styles.col6}>{item.total > 0 ? item.total.toLocaleString('vi-VN') : ''}</Text>
                        </View>
                    ))}
                </View>

                {/* Total */}
                <View style={styles.totalSection}>
                    <View style={styles.totalRow}>
                        <Text style={styles.totalLabel}>Tổng cộng:</Text>
                        <Text style={styles.totalValue}>{totalAmount.toLocaleString('vi-VN')}</Text>
                    </View>
                    <View style={styles.row}>
                        <Text style={styles.label}>Số tiền bằng chữ:</Text>
                        <Text style={styles.value}>{totalInWords}</Text>
                    </View>
                </View>

                {/* Footer */}
                <View style={styles.footer}>
                    <View style={styles.row}>
                        <Text style={{ fontSize: 10, fontStyle: 'italic' }}>
                            Sản phẩm được bảo hành ________ tháng kể từ ngày mua.
                        </Text>
                    </View>
                    <View style={styles.dateSection}>
                        <Text>ngày {day} tháng {month} năm {year}</Text>
                    </View>
                </View>
            </Page>
        </Document>
    );
};

export default InvoicePDFDocument;
