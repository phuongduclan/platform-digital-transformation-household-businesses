from domain.models.iimport_receipt_repository import IImportReceiptRepository
from domain.models.import_receipt import ImportReceipt
from typing import List, Optional
from infrastructure.models.import_receipt_model import ImportReceipt as ImportReceiptModel
from infrastructure.models.warehouse_model import Warehouse
from infrastructure.databases.mssql import session

class ImportReceiptRepository(IImportReceiptRepository):
    def __init__(self, session=session):
        self.session = session

    def create(self, import_receipt: ImportReceipt) -> ImportReceipt:
        try:
            import_receipt_model = ImportReceiptModel(
                warehouse_id=import_receipt.warehouse_id,
                invoice_id=import_receipt.invoice_id,
                import_date=import_receipt.import_date,
                created_at=import_receipt.created_at,
                updated_at=import_receipt.updated_at
            )
            self.session.add(import_receipt_model)
            self.session.flush()
            self.session.refresh(import_receipt_model)
            return self._to_domain(import_receipt_model)
        except Exception as e:
            self.session.rollback()
            raise ValueError(f'Error creating import receipt: {str(e)}')

    def get_by_id(self, import_receipt_id: int, household_id: int = None) -> Optional[ImportReceipt]:
        query = self.session.query(ImportReceiptModel).join(Warehouse).filter(ImportReceiptModel.id == import_receipt_id)
        if household_id is not None:
            query = query.filter(Warehouse.household_id == household_id)
        import_receipt_model = query.first()
        return self._to_domain(import_receipt_model) if import_receipt_model else None

    def list(self, household_id: int) -> List[ImportReceipt]:
        query = self.session.query(ImportReceiptModel).join(Warehouse).filter(Warehouse.household_id == household_id)
        import_receipt_models = query.all()
        return [self._to_domain(im) for im in import_receipt_models]

    def update(self, import_receipt: ImportReceipt) -> ImportReceipt:
        try:
            query = self.session.query(ImportReceiptModel).join(Warehouse).filter(ImportReceiptModel.id == import_receipt.id)
            if import_receipt.warehouse_id:
                # Verify household_id through warehouse
                query = query.filter(Warehouse.household_id == self._get_household_id_from_warehouse(import_receipt.warehouse_id))
            import_receipt_model = query.first()
            if not import_receipt_model:
                raise ValueError('Import receipt not found')

            if import_receipt.warehouse_id is not None:
                import_receipt_model.warehouse_id = import_receipt.warehouse_id
            if import_receipt.import_date is not None:
                import_receipt_model.import_date = import_receipt.import_date
            if import_receipt.updated_at is not None:
                import_receipt_model.updated_at = import_receipt.updated_at

            self.session.flush()
            self.session.refresh(import_receipt_model)
            return self._to_domain(import_receipt_model)
        except Exception as e:
            self.session.rollback()
            raise ValueError(f'Error updating import receipt: {str(e)}')

    def _get_household_id_from_warehouse(self, warehouse_id: int) -> int:
        warehouse = self.session.query(Warehouse).filter_by(id=warehouse_id).first()
        return warehouse.household_id if warehouse else None

    def _to_domain(self, import_receipt_model: ImportReceiptModel) -> ImportReceipt:
        return ImportReceipt(
            id=import_receipt_model.id,
            warehouse_id=import_receipt_model.warehouse_id,
            invoice_id=import_receipt_model.invoice_id,
            import_date=import_receipt_model.import_date,
            status='Confirm',  # Default status
            created_at=import_receipt_model.created_at,
            updated_at=import_receipt_model.updated_at
        )
