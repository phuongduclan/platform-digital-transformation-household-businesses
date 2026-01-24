from domain.models.customer import Customer
from domain.models.icustomer_repository import ICustomerRepository
from domain.models.iinvoice_repository import IInvoiceRepository
from domain.models.idebt_record_repository import IDebtRecordRepository
from domain.models.icustomer_service import ICustomerService
from typing import List, Optional
from datetime import datetime
from infrastructure.utils.datetime_utils import vietnam_now
from decimal import Decimal

class CustomerService(ICustomerService):
    def __init__(self, repository: ICustomerRepository,
                 invoice_repository: IInvoiceRepository = None,
                 debt_record_repository: IDebtRecordRepository = None):
        self.repository = repository
        self.invoice_repository = invoice_repository
        self.debt_record_repository = debt_record_repository

    def create_customer(self, household_id: int, tax_code: str = None, name: str = None,
                      phone: str = None, address: str = None, description: str = None,
                      status: str = 'Active', created_by: str = None) -> Customer:
        now = vietnam_now()
        customer = Customer(
            id=None,
            household_id=household_id,
            tax_code=tax_code,
            name=name,
            phone=phone,
            address=address,
            description=description,
            status=status,
            created_by=created_by,
            updated_by=created_by,
            created_at=now,
            updated_at=now
        )
        return self.repository.create(customer)

    def get_customer(self, customer_id: int, household_id: int) -> Optional[Customer]:
        return self.repository.get_by_id(customer_id, household_id)

    def list_customers(self, household_id: int, status: str = None) -> List[Customer]:
        return self.repository.list(household_id, status)

    def update_customer(self, customer_id: int, household_id: int, tax_code: str = None,
                       name: str = None, phone: str = None, address: str = None,
                       description: str = None, status: str = None,
                       updated_by: str = None) -> Customer:
        now = vietnam_now()
        customer = Customer(
            id=customer_id,
            household_id=household_id,
            tax_code=tax_code,
            name=name,
            phone=phone,
            address=address,
            description=description,
            status=status,
            updated_by=updated_by,
            updated_at=now
        )
        return self.repository.update(customer)

    def delete_customer(self, customer_id: int, household_id: int) -> None:
        self.repository.delete(customer_id, household_id)

    def get_customer_purchase_history(self, customer_id: int, household_id: int) -> List[dict]:
        """Lấy lịch sử mua hàng của customer (tất cả invoices có customer_id)"""
        if not self.invoice_repository:
            return []
        
        invoices = self.invoice_repository.list(household_id)
        customer_invoices = [inv for inv in invoices if inv.customer_id == customer_id]
        
        history = []
        for invoice in customer_invoices:
            history.append({
                "invoice_id": invoice.id,
                "invoice_type": invoice.invoice_type,
                "total_amount": str(invoice.total_amount) if invoice.total_amount else None,
                "status": invoice.status,
                "created_at": invoice.created_at.isoformat() if invoice.created_at else None
            })
        
        return history

    def get_customer_debt(self, customer_id: int, household_id: int) -> dict:
        """Lấy thông tin nợ của customer"""
        if not self.debt_record_repository:
            return {
                "customer_id": customer_id,
                "current_balance": "0",
                "debt_records": []
            }
        
        debt_records = self.debt_record_repository.get_by_customer_id(customer_id, household_id)
        last_record = self.debt_record_repository.get_customer_balance(customer_id, household_id)
        current_balance = last_record.balance if last_record else Decimal('0')
        
        return {
            "customer_id": customer_id,
            "current_balance": str(current_balance),
            "debt_records": [
                {
                    "id": dr.id,
                    "invoice_id": dr.invoice_id,
                    "payment_id": dr.payment_id,
                    "debit_amount": str(dr.debit_amount) if dr.debit_amount else None,
                    "credit_amount": str(dr.credit_amount) if dr.credit_amount else None,
                    "balance": str(dr.balance) if dr.balance else None,
                    "description": dr.description,
                    "record_at": dr.record_at.isoformat() if dr.record_at else None
                }
                for dr in debt_records
            ]
        }
