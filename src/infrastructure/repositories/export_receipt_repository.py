from domain.models.iexport_receipt_repository import IExportReceiptRepository
from domain.models.export_receipt import ExportReceipt
from typing import List, Optional
from infrastructure.models.export_receipt_model import ExportReceipt as ExportReceiptModel
from infrastructure.models.warehouse_model import Warehouse
from infrastructure.databases.mssql import session

class ExportReceiptRepository(IExportReceiptRepository):
    def __init__(self, session=session):
        self.session = session

    def create(self, export_receipt: ExportReceipt) -> ExportReceipt:
        try:
            export_receipt_model = ExportReceiptModel(
                warehouse_id=export_receipt.warehouse_id,
                invoice_id=export_receipt.invoice_id,
                export_date=export_receipt.export_date,
                reason=export_receipt.reason,
                created_at=export_receipt.created_at,
                updated_at=export_receipt.updated_at
            )
            self.session.add(export_receipt_model)
            self.session.flush()
            self.session.refresh(export_receipt_model)
            return self._to_domain(export_receipt_model)
        except Exception as e:
            self.session.rollback()
            raise ValueError(f'Error creating export receipt: {str(e)}')

    def get_by_id(self, export_receipt_id: int, household_id: int = None) -> Optional[ExportReceipt]:
        query = self.session.query(ExportReceiptModel).join(Warehouse).filter(ExportReceiptModel.id == export_receipt_id)
        if household_id is not None:
            query = query.filter(Warehouse.household_id == household_id)
        export_receipt_model = query.first()
        return self._to_domain(export_receipt_model) if export_receipt_model else None

    def list(self, household_id: int) -> List[ExportReceipt]:
        query = self.session.query(ExportReceiptModel).join(Warehouse).filter(Warehouse.household_id == household_id)
        export_receipt_models = query.all()
        return [self._to_domain(em) for em in export_receipt_models]

    def update(self, export_receipt: ExportReceipt) -> ExportReceipt:
        try:
            query = self.session.query(ExportReceiptModel).join(Warehouse).filter(ExportReceiptModel.id == export_receipt.id)
            if export_receipt.warehouse_id:
                # Verify household_id through warehouse
                query = query.filter(Warehouse.household_id == self._get_household_id_from_warehouse(export_receipt.warehouse_id))
            export_receipt_model = query.first()
            if not export_receipt_model:
                raise ValueError('Export receipt not found')

            if export_receipt.warehouse_id is not None:
                export_receipt_model.warehouse_id = export_receipt.warehouse_id
            if export_receipt.export_date is not None:
                export_receipt_model.export_date = export_receipt.export_date
            if export_receipt.reason is not None:
                export_receipt_model.reason = export_receipt.reason
            if export_receipt.updated_at is not None:
                export_receipt_model.updated_at = export_receipt.updated_at

            self.session.flush()
            self.session.refresh(export_receipt_model)
            return self._to_domain(export_receipt_model)
        except Exception as e:
            self.session.rollback()
            raise ValueError(f'Error updating export receipt: {str(e)}')

    def _get_household_id_from_warehouse(self, warehouse_id: int) -> int:
        warehouse = self.session.query(Warehouse).filter_by(id=warehouse_id).first()
        return warehouse.household_id if warehouse else None

    def _to_domain(self, export_receipt_model: ExportReceiptModel) -> ExportReceipt:
        return ExportReceipt(
            id=export_receipt_model.id,
            warehouse_id=export_receipt_model.warehouse_id,
            invoice_id=export_receipt_model.invoice_id,
            export_date=export_receipt_model.export_date,
            reason=export_receipt_model.reason,
            status='Confirm',  # Default status
            created_at=export_receipt_model.created_at,
            updated_at=export_receipt_model.updated_at
        )
