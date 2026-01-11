from domain.models.invoice import Invoice
from domain.models.iinvoice_repository import IInvoiceRepository
from domain.models.iinvoice_detail_repository import IInvoiceDetailRepository
from domain.models.invoice_detail import InvoiceDetail
from typing import List, Optional
from datetime import datetime
from decimal import Decimal

class InvoiceService:
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

        now = datetime.utcnow()
        
        # Convert 0 thành None để tránh Foreign Key constraint violation
        # Nếu seller_id hoặc customer_id = 0, thì set thành None (NULL)
        if seller_id == 0 or seller_id == '0':
            seller_id = None
        if customer_id == 0 or customer_id == '0':
            customer_id = None
        
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
            db_session.rollback()
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

        now = datetime.utcnow()
        
        # Convert 0 thành None để tránh Foreign Key constraint violation
        if seller_id == 0 or seller_id == '0':
            seller_id = None
        if customer_id == 0 or customer_id == '0':
            customer_id = None
        
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
        """
        invoice = self.repository.get_by_id(invoice_id, household_id)
        if not invoice:
            raise ValueError('Invoice not found')

        if invoice.status != 'Draft':
            raise ValueError('Only Draft invoices can be deleted')

        self.repository.delete(invoice_id, household_id)

    def confirm_invoice(self, invoice_id: int, household_id: int, updated_by: str = None) -> Invoice:
        """
        Confirm invoice: chuyển status từ 'Draft' → 'Confirm'
        Bất kỳ ai trong household đều có thể confirm, không cần là người tạo
        """
        invoice = self.repository.get_by_id(invoice_id, household_id)
        if not invoice:
            raise ValueError('Invoice not found')

        if invoice.status != 'Draft':
            raise ValueError('Only Draft invoices can be confirmed')

        invoice.updated_by = updated_by
        invoice.updated_at = datetime.utcnow()

        return self.repository.confirm(invoice_id, household_id, updated_by)
