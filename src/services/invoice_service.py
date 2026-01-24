from domain.models.invoice import Invoice
from domain.models.iinvoice_repository import IInvoiceRepository
from domain.models.iinvoice_detail_repository import IInvoiceDetailRepository
from domain.models.iinvoice_service import IInvoiceService
from domain.models.invoice_detail import InvoiceDetail
from typing import List, Optional
from datetime import datetime
from decimal import Decimal
from infrastructure.utils.datetime_utils import vietnam_now

class InvoiceService(IInvoiceService):
    def __init__(self, repository: IInvoiceRepository, invoice_detail_repository: IInvoiceDetailRepository):
        self.repository = repository
        self.invoice_detail_repository = invoice_detail_repository

    def create_invoice_with_details(self, household_id: int, seller_id: int = None, customer_id: int = None,
                                    invoice_type: str = 'PAID', description: str = None, status: str = 'Draft',
                                    created_by: str = None, details: List[dict] = None) -> Invoice:
        """
        Tạo invoice cùng với details trong 1 transaction.
        Phải có ít nhất 1 detail.
        Tính toán total_amount, vat_total, discount_total từ details.
        """
        if not details or len(details) == 0:
            raise ValueError("Invoice must have at least 1 detail")

        now = vietnam_now()
        
        # Convert 0 thành None để tránh Foreign Key constraint violation
        # Nếu seller_id hoặc customer_id = 0, thì set thành None (NULL)
        if seller_id == 0 or seller_id == '0':
            seller_id = None
        if customer_id == 0 or customer_id == '0':
            customer_id = None

        # Validation: Invoice không được gắn đồng thời seller_id và customer_id
        # Hóa đơn mua: chỉ có seller_id, không có customer_id
        # Hóa đơn bán: có hoặc không có customer_id, nhưng không có seller_id
        if seller_id is not None and customer_id is not None:
            raise ValueError('Invoice không được có đồng thời seller_id và customer_id. Vui lòng chọn 1 loại hóa đơn (mua hoặc bán).')
        
        # Validation: Hóa đơn không gắn khách hàng (customer_id = None) không được ghi nhận công nợ
        if customer_id is None and invoice_type != 'PAID':
            raise ValueError('Hóa đơn không gắn khách hàng phải có invoice_type = PAID (thanh toán đủ ngay)')
        
        # Tính toán tổng từ details
        total_amount = Decimal('0')
        vat_total = Decimal('0')
        discount_total = Decimal('0')

        # Tạo invoice trước (chưa commit)
        invoice = Invoice(
            id=None,
            household_id=household_id,
            seller_id=seller_id,
            customer_id=customer_id,
            invoice_type=invoice_type,
            discount_total=Decimal('0'),
            vat_total=Decimal('0'),
            total_amount=Decimal('0'),
            description=description,
            status=status,
            created_by=created_by,
            updated_by=created_by,
            created_at=now,
            updated_at=now
        )

        # Lấy session từ repository để quản lý transaction
        db_session = getattr(self.repository, 'session', None)
        if not db_session:
            raise ValueError("Repository must have a session attribute")

        # Đảm bảo invoice_detail_repository dùng cùng session
        if hasattr(self.invoice_detail_repository, 'session'):
            self.invoice_detail_repository.session = db_session

        try:
            # Tạo invoice (flush để lấy ID)
            invoice = self.repository.create(invoice)
            invoice_id = invoice.id

            # Tạo details và tính toán tổng
            for detail_data in details:
                product_id = detail_data.get('product_id')
                unit_id = detail_data.get('unit_id')
                quantity = detail_data.get('quantity', 1)
                price = Decimal(str(detail_data.get('price', 0)))
                vat_percent = detail_data.get('vat', 0)
                discount_percent = detail_data.get('discount', 0)
                detail_description = detail_data.get('description')

                # Tính subtotal
                subtotal = price * Decimal(quantity)
                
                # Tính discount amount
                discount_amount = subtotal * Decimal(discount_percent) / Decimal('100')
                discount_total += discount_amount
                
                # Tính sau discount
                after_discount = subtotal - discount_amount
                
                # Tính VAT amount
                vat_amount = after_discount * Decimal(vat_percent) / Decimal('100')
                vat_total += vat_amount
                
                # Tính total cho detail này
                detail_total = after_discount + vat_amount
                total_amount += detail_total

                # Tạo invoice detail
                invoice_detail = InvoiceDetail(
                    id=None,
                    invoice_id=invoice_id,
                    product_id=product_id,
                    unit_id=unit_id,
                    vat=vat_percent,
                    discount=discount_percent,
                    price=price,
                    description=detail_description,
                    quantity=quantity,
                    status=status,
                    created_at=now,
                    updated_at=now
                )
                self.invoice_detail_repository.add(invoice_detail)

            # Cập nhật tổng vào invoice
            invoice.discount_total = discount_total
            invoice.vat_total = vat_total
            invoice.total_amount = total_amount
            invoice = self.repository.update(invoice)

            # Commit transaction
            db_session.commit()
            return invoice

        except Exception as e:
            from infrastructure.databases.session_utils import safe_rollback
            safe_rollback(db_session)
            raise ValueError(f'Error creating invoice with details: {str(e)}')

    def get_invoice(self, invoice_id: int, household_id: int) -> Optional[Invoice]:
        return self.repository.get_by_id(invoice_id, household_id)

    def list_invoices(self, household_id: int, status: Optional[str] = None) -> List[Invoice]:
        return self.repository.list(household_id, status)

    def update_invoice(self, invoice_id: int, household_id: int, seller_id: int = None,
                       customer_id: int = None, invoice_type: str = None, description: str = None,
                       updated_by: str = None) -> Invoice:
        """
        Chỉ được update khi status='Draft'
        """
        invoice = self.repository.get_by_id(invoice_id, household_id)
        if not invoice:
            raise ValueError('Invoice not found')

        if invoice.status != 'Draft':
            raise ValueError('Only Draft invoices can be updated')

        now = vietnam_now()
        
        # Convert 0 thành None để tránh Foreign Key constraint violation
        if seller_id == 0 or seller_id == '0':
            seller_id = None
        if customer_id == 0 or customer_id == '0':
            customer_id = None

        # Validation: Invoice không được gắn đồng thời seller_id và customer_id
        # Kiểm tra dựa trên giá trị sau khi update (nếu field không truyền lên thì giữ nguyên)
        new_seller_id = seller_id if seller_id is not None else invoice.seller_id
        new_customer_id = customer_id if customer_id is not None else invoice.customer_id
        if new_seller_id is not None and new_customer_id is not None:
            raise ValueError('Invoice không được có đồng thời seller_id và customer_id. Vui lòng chọn 1 loại hóa đơn (mua hoặc bán).')
        
        # Validation: Nếu đang update customer_id thành None thì không được để invoice_type khác PAID
        if customer_id is None and invoice_type is not None and invoice_type != 'PAID':
            raise ValueError('Hóa đơn không gắn khách hàng phải có invoice_type = PAID (thanh toán đủ ngay)')
        # Nếu đang update invoice_type thành UNPAID nhưng customer_id = None
        if invoice_type == 'UNPAID' and (customer_id is None or invoice.customer_id is None):
            raise ValueError('Hóa đơn bán chịu (UNPAID) phải có khách hàng trong bảng customer')
        
        # Cập nhật các field nếu có
        if seller_id is not None:
            invoice.seller_id = seller_id
        if customer_id is not None:
            invoice.customer_id = customer_id
        if invoice_type is not None:
            invoice.invoice_type = invoice_type
        if description is not None:
            invoice.description = description
        if updated_by is not None:
            invoice.updated_by = updated_by
        
        invoice.updated_at = now

        return self.repository.update(invoice)

    def delete_invoice(self, invoice_id: int, household_id: int) -> None:
        """
        Chỉ được delete khi status='Draft'
        Xóa invoice details trước, sau đó mới xóa invoice để tránh lỗi foreign key constraint
        """
        invoice = self.repository.get_by_id(invoice_id, household_id)
        if not invoice:
            raise ValueError('Invoice not found')

        if invoice.status != 'Draft':
            raise ValueError('Only Draft invoices can be deleted')

        # Lấy session từ repository để quản lý transaction
        db_session = getattr(self.repository, 'session', None)
        if not db_session:
            raise ValueError("Repository must have a session attribute")

        try:
            # Xóa tất cả invoice details trước
            invoice_details = self.invoice_detail_repository.list_by_invoice_id(invoice_id, household_id)
            for detail in invoice_details:
                self.invoice_detail_repository.delete(detail.id, household_id)
            
            # Sau đó mới xóa invoice
            self.repository.delete(invoice_id, household_id)
            
            # Commit transaction
            db_session.commit()
        except Exception as e:
            from infrastructure.databases.session_utils import safe_rollback
            safe_rollback(db_session)
            raise ValueError(f'Error deleting invoice: {str(e)}')

    def confirm_invoice(self, invoice_id: int, household_id: int, updated_by: str = None,
                       import_receipt_service=None, export_receipt_service=None,
                       inventory_service=None, warehouse_repository=None,
                       debt_record_service=None, accounting_ledger_service=None,
                       seller_repository=None, customer_repository=None) -> Invoice:
        """
        Confirm invoice: chuyển status từ 'Draft' → 'Confirm'
        Bất kỳ ai trong household đều có thể confirm, không cần là người tạo
        
        Tự động tạo ImportReceipt/ExportReceipt và cập nhật inventory:
        - Nếu invoice có seller_id (hóa đơn mua) → Tự động tạo ImportReceipt + tăng inventory
        - Nếu invoice KHÔNG có seller_id (hóa đơn bán, dù có customer_id hay không - kể cả khách vãng lai) 
          → Tự động tạo ExportReceipt + giảm inventory
        """
        invoice = self.repository.get_by_id(invoice_id, household_id)
        if not invoice:
            raise ValueError('Invoice not found')

        if invoice.status != 'Draft':
            raise ValueError('Only Draft invoices can be confirmed')

        # Lấy session từ repository để quản lý transaction
        db_session = getattr(self.repository, 'session', None)
        if not db_session:
            raise ValueError("Repository must have a session attribute")

        try:
            # Confirm invoice (chuyển status sang 'Confirm')
            invoice.updated_by = updated_by
            invoice.updated_at = vietnam_now()
            invoice = self.repository.confirm(invoice_id, household_id, updated_by)

            # Lấy invoice details
            invoice_details = self.invoice_detail_repository.list_by_invoice_id(invoice_id, household_id)
            
            # Lấy warehouse đầu tiên của household (hoặc có thể truyền warehouse_id từ invoice nếu có)
            warehouse_id = None
            if warehouse_repository:
                warehouses = warehouse_repository.list(household_id)
                if warehouses and len(warehouses) > 0:
                    warehouse_id = warehouses[0].id
                else:
                    raise ValueError(f'No warehouse found for household_id={household_id}')

            if warehouse_id:
                # Chuẩn bị details cho import/export receipt
                details = []
                for detail in invoice_details:
                    details.append({
                        'product_id': detail.product_id,
                        'unit_id': detail.unit_id,
                        'quantity': detail.quantity
                    })

                # Tự động tạo ImportReceipt nếu có seller_id (hóa đơn mua)
                if invoice.seller_id:
                    if import_receipt_service and inventory_service:
                        # Đảm bảo repositories dùng cùng session
                        import_receipt_service.repository.session = db_session
                        if hasattr(import_receipt_service, 'import_detail_repository'):
                            import_receipt_service.import_detail_repository.session = db_session
                        inventory_service.repository.session = db_session
                        
                        # Tạo ImportReceipt
                        import_receipt = import_receipt_service.create_import_receipt_with_details(
                            warehouse_id=warehouse_id,
                            invoice_id=invoice_id,
                            details=details
                        )
                        
                        # Tự động tăng inventory cho từng product
                        for detail in invoice_details:
                            inventory_service.increase_inventory(
                                product_id=detail.product_id,
                                unit_id=detail.unit_id,
                                warehouse_id=warehouse_id,
                                quantity=detail.quantity,
                                household_id=household_id
                            )

                # Tự động tạo ExportReceipt nếu KHÔNG có seller_id (hóa đơn bán)
                # Bao gồm cả trường hợp customer_id = null (bán cho khách vãng lai)
                if not invoice.seller_id:
                    if export_receipt_service and inventory_service:
                        # Đảm bảo repositories dùng cùng session
                        export_receipt_service.repository.session = db_session
                        if hasattr(export_receipt_service, 'export_detail_repository'):
                            export_receipt_service.export_detail_repository.session = db_session
                        inventory_service.repository.session = db_session
                        
                        # Kiểm tra inventory đủ số lượng trước khi tạo ExportReceipt
                        for detail in invoice_details:
                            existing_inventory = inventory_service.get_inventory(
                                product_id=detail.product_id,
                                warehouse_id=warehouse_id,
                                household_id=household_id,
                                unit_id=detail.unit_id
                            )
                            if not existing_inventory or existing_inventory.quantity < detail.quantity:
                                raise ValueError(
                                    f'Insufficient inventory for product_id={detail.product_id}. '
                                    f'Available: {existing_inventory.quantity if existing_inventory else 0}, '
                                    f'Required: {detail.quantity}'
                                )
                        
                        # Tạo ExportReceipt
                        export_receipt = export_receipt_service.create_export_receipt_with_details(
                            warehouse_id=warehouse_id,
                            invoice_id=invoice_id,
                            reason="Xuất bán hàng",
                            details=details
                        )
                        
                        # Tự động giảm inventory cho từng product
                        for detail in invoice_details:
                            inventory_service.decrease_inventory(
                                product_id=detail.product_id,
                                unit_id=detail.unit_id,
                                warehouse_id=warehouse_id,
                                quantity=detail.quantity,
                                household_id=household_id
                            )

            # Tự động tạo DebtRecord (nếu invoice có customer_id != null và invoice_type = 'UNPAID')
            if debt_record_service and invoice.customer_id and invoice.invoice_type == 'UNPAID':
                # Đảm bảo debt_record_service dùng cùng session
                if hasattr(debt_record_service.repository, 'session'):
                    debt_record_service.repository.session = db_session
                
                # Lấy balance hiện tại của customer
                previous_balance = debt_record_service.get_customer_balance(invoice.customer_id, household_id)
                new_balance = previous_balance + invoice.total_amount  # Nợ tăng balance
                
                debt_record = debt_record_service.create_debt_record(
                    customer_id=invoice.customer_id,
                    invoice_id=invoice_id,
                    debit_amount=invoice.total_amount,
                    description=invoice.description or f"Hóa đơn #{invoice_id}",
                    household_id=household_id
                )

            # Tự động tạo AccountingLedger
            if accounting_ledger_service:
                # Đảm bảo accounting_ledger_service dùng cùng session
                if hasattr(accounting_ledger_service.repository, 'session'):
                    accounting_ledger_service.repository.session = db_session
                
                now = vietnam_now()
                
                # Hóa đơn mua (seller_id != null)
                if invoice.seller_id:
                    # Lấy seller name
                    seller_name = "Nhà cung cấp"
                    if seller_repository:
                        seller = seller_repository.get_by_id(invoice.seller_id, household_id)
                        if seller:
                            seller_name = seller.name or "Nhà cung cấp"
                    
                    # Lấy balance hiện tại
                    previous_balance = accounting_ledger_service._get_last_balance(household_id)
                    new_balance = previous_balance - invoice.total_amount  # Chi giảm balance
                    
                    accounting_ledger = accounting_ledger_service.create_accounting_ledger(
                        invoice_id=invoice_id,
                        transaction_date=now,
                        debit_amount=invoice.total_amount,
                        description=f"Mua hàng từ {seller_name} - HĐ #{invoice_id}",
                        movement_type='Chi',
                        household_id=household_id
                    )
                
                # Hóa đơn bán
                elif not invoice.seller_id:
                    # Trường hợp 1: Khách vãng lai (customer_id = None) - luôn PAID
                    if invoice.customer_id is None:
                        # Tạo AccountingLedger Thu cho khách vãng lai
                        accounting_ledger = accounting_ledger_service.create_accounting_ledger(
                            invoice_id=invoice_id,
                            transaction_date=now,
                            credit_amount=invoice.total_amount,
                            description=f"Bán hàng cho khách vãng lai - HĐ #{invoice_id}",
                            movement_type='Thu',
                            household_id=household_id
                        )
                    
                    # Trường hợp 2: Khách có trong customer + PAID (thu đủ ngay)
                    elif invoice.customer_id and invoice.invoice_type == 'PAID':
                        # Lấy customer name
                        customer_name = "Khách hàng"
                        if customer_repository:
                            customer = customer_repository.get_by_id(invoice.customer_id, household_id)
                            if customer:
                                customer_name = customer.name or "Khách hàng"
                        
                        # Tạo AccountingLedger Thu
                        accounting_ledger = accounting_ledger_service.create_accounting_ledger(
                            invoice_id=invoice_id,
                            transaction_date=now,
                            credit_amount=invoice.total_amount,
                            description=f"Bán hàng cho {customer_name} - Đã thanh toán - HĐ #{invoice_id}",
                            movement_type='Thu',
                            household_id=household_id
                        )
                    
                    # Trường hợp 3: Khách có trong customer + UNPAID (ghi nợ)
                    # → KHÔNG tạo AccountingLedger ở đây (chưa có thu)
                    # → Chỉ tạo DebtRecord, AccountingLedger sẽ được tạo khi có Payment

            # Commit transaction
            db_session.commit()
            return invoice

        except Exception as e:
            from infrastructure.databases.session_utils import safe_rollback
            safe_rollback(db_session)
            raise ValueError(f'Error confirming invoice: {str(e)}')
