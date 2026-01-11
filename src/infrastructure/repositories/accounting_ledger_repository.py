from domain.models.iaccounting_ledger_repository import IAccountingLedgerRepository
from domain.models.accounting_ledger import AccountingLedger
from typing import List, Optional
from infrastructure.models.accounting_ledger_model import AccountingLedger as AccountingLedgerModel
from infrastructure.models.invoice_model import Invoice as InvoiceModel
from infrastructure.databases.mssql import session
from datetime import datetime
from sqlalchemy import desc

class AccountingLedgerRepository(IAccountingLedgerRepository):
    def __init__(self, session=session):
        self.session = session

    def create(self, accounting_ledger: AccountingLedger) -> AccountingLedger:
        try:
            accounting_ledger_model = AccountingLedgerModel(
                invoice_id=accounting_ledger.invoice_id,
                transaction_date=accounting_ledger.transaction_date,
                description=accounting_ledger.description,
                debit_amount=accounting_ledger.debit_amount,
                credit_amount=accounting_ledger.credit_amount,
                balance=accounting_ledger.balance,
                document_number=accounting_ledger.document_number,
                movement_type=accounting_ledger.movement_type,
                status=accounting_ledger.status,
                created_at=accounting_ledger.created_at,
                updated_at=accounting_ledger.updated_at
            )
            self.session.add(accounting_ledger_model)
            self.session.flush()
            self.session.refresh(accounting_ledger_model)
            return self._to_domain(accounting_ledger_model)
        except Exception as e:
            self.session.rollback()
            raise ValueError(f'Error creating accounting ledger: {str(e)}')

    def get_by_id(self, accounting_ledger_id: int, household_id: int = None) -> Optional[AccountingLedger]:
        query = self.session.query(AccountingLedgerModel).filter_by(id=accounting_ledger_id)
        if household_id is not None:
            query = query.join(InvoiceModel).filter(InvoiceModel.household_id == household_id)
        accounting_ledger_model = query.first()
        return self._to_domain(accounting_ledger_model) if accounting_ledger_model else None

    def list(self, household_id: int, from_date: datetime = None, to_date: datetime = None,
             movement_type: str = None) -> List[AccountingLedger]:
        query = self.session.query(AccountingLedgerModel).join(InvoiceModel).filter(
            InvoiceModel.household_id == household_id
        )
        if from_date is not None:
            query = query.filter(AccountingLedgerModel.transaction_date >= from_date)
        if to_date is not None:
            query = query.filter(AccountingLedgerModel.transaction_date <= to_date)
        if movement_type is not None:
            query = query.filter(AccountingLedgerModel.movement_type == movement_type)
        query = query.order_by(desc(AccountingLedgerModel.transaction_date))
        accounting_ledger_models = query.all()
        return [self._to_domain(alm) for alm in accounting_ledger_models]

    def get_by_invoice_id(self, invoice_id: int, household_id: int = None) -> Optional[AccountingLedger]:
        """Lấy accounting ledger theo invoice_id"""
        query = self.session.query(AccountingLedgerModel).filter_by(invoice_id=invoice_id)
        if household_id is not None:
            query = query.join(InvoiceModel).filter(InvoiceModel.household_id == household_id)
        accounting_ledger_model = query.first()
        return self._to_domain(accounting_ledger_model) if accounting_ledger_model else None

    def _to_domain(self, accounting_ledger_model: AccountingLedgerModel) -> AccountingLedger:
        return AccountingLedger(
            id=accounting_ledger_model.id,
            invoice_id=accounting_ledger_model.invoice_id,
            transaction_date=accounting_ledger_model.transaction_date,
            description=accounting_ledger_model.description,
            debit_amount=accounting_ledger_model.debit_amount,
            credit_amount=accounting_ledger_model.credit_amount,
            balance=accounting_ledger_model.balance,
            document_number=accounting_ledger_model.document_number,
            movement_type=accounting_ledger_model.movement_type,
            status=accounting_ledger_model.status,
            created_at=accounting_ledger_model.created_at,
            updated_at=accounting_ledger_model.updated_at
        )
