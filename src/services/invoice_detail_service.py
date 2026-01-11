from domain.models.invoice_detail import InvoiceDetail
from domain.models.iinvoice_detail_repository import IInvoiceDetailRepository
from domain.models.iinvoice_repository import IInvoiceRepository
from typing import List, Optional
from datetime import datetime
from decimal import Decimal

class InvoiceDetailService:
    def __init__(self, repository: IInvoiceDetailRepository, invoice_repository: IInvoiceRepository):
        self.repository = repository
        self.invoice_repository = invoice_repository

    def create_invoice_detail(self, invoice_id: int, product_id: int, unit_id: int,
                              quantity: int, price: Decimal, vat: int = 0, discount: int = 0,
                              description: str = None, status: str = 'Draft',
                              household_id: int = None) -> InvoiceDetail:
        """
        Tạo invoice detail.
        Chỉ được tạo khi invoice status='Draft'
        """
        # Kiểm tra invoice tồn tại và status='Draft'
        invoice = self.invoice_repository.get_by_id(invoice_id, household_id)
        if not invoice:
            raise ValueError('Invoice not found')

        if invoice.status != 'Draft':
            raise ValueError('Can only add details to Draft invoices')

        now = datetime.utcnow()
        invoice_detail = InvoiceDetail(
            id=None,
            invoice_id=invoice_id,
            product_id=product_id,
            unit_id=unit_id,
            vat=vat,
            discount=discount,
            price=price,
            description=description,
            quantity=quantity,
            status=status,
            created_at=now,
            updated_at=now
        )
        return self.repository.add(invoice_detail)

    def get_invoice_detail(self, invoice_detail_id: int, household_id: int = None) -> Optional[InvoiceDetail]:
        return self.repository.get_by_id(invoice_detail_id, household_id)

    def list_invoice_details(self, invoice_id: int, household_id: int = None) -> List[InvoiceDetail]:
        return self.repository.list_by_invoice_id(invoice_id, household_id)

    def update_invoice_detail(self, invoice_detail_id: int, household_id: int = None,
                              product_id: int = None, unit_id: int = None, quantity: int = None,
                              price: Decimal = None, vat: int = None, discount: int = None,
                              description: str = None) -> InvoiceDetail:
        """
        Update invoice detail.
        Chỉ được update khi invoice status='Draft'
        """
        invoice_detail = self.repository.get_by_id(invoice_detail_id, household_id)
        if not invoice_detail:
            raise ValueError('Invoice detail not found')

        # Kiểm tra invoice status
        invoice = self.invoice_repository.get_by_id(invoice_detail.invoice_id, household_id)
        if not invoice:
            raise ValueError('Invoice not found')

        if invoice.status != 'Draft':
            raise ValueError('Can only update details of Draft invoices')

        now = datetime.utcnow()
        
        # Cập nhật các field nếu có
        if product_id is not None:
            invoice_detail.product_id = product_id
        if unit_id is not None:
            invoice_detail.unit_id = unit_id
        if quantity is not None:
            invoice_detail.quantity = quantity
        if price is not None:
            invoice_detail.price = price
        if vat is not None:
            invoice_detail.vat = vat
        if discount is not None:
            invoice_detail.discount = discount
        if description is not None:
            invoice_detail.description = description
        
        invoice_detail.updated_at = now

        return self.repository.update(invoice_detail)

    def delete_invoice_detail(self, invoice_detail_id: int, household_id: int = None) -> None:
        """
        Delete invoice detail.
        Chỉ được delete khi invoice status='Draft'
        """
        invoice_detail = self.repository.get_by_id(invoice_detail_id, household_id)
        if not invoice_detail:
            raise ValueError('Invoice detail not found')

        # Kiểm tra invoice status
        invoice = self.invoice_repository.get_by_id(invoice_detail.invoice_id, household_id)
        if not invoice:
            raise ValueError('Invoice not found')

        if invoice.status != 'Draft':
            raise ValueError('Can only delete details of Draft invoices')

        self.repository.delete(invoice_detail_id, household_id)
