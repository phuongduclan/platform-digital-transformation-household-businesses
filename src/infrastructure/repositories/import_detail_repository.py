from domain.models.iimport_detail_repository import IImportDetailRepository
from domain.models.import_detail import ImportDetail
from typing import List, Optional
from infrastructure.models.import_detail_model import ImportDetail as ImportDetailModel
from infrastructure.models.import_receipt_model import ImportReceipt as ImportReceiptModel
from infrastructure.models.warehouse_model import Warehouse
from infrastructure.databases.mssql import session

class ImportDetailRepository(IImportDetailRepository):
    def __init__(self, session=session):
        self.session = session

    def add(self, import_detail: ImportDetail) -> ImportDetail:
        try:
            import_detail_model = ImportDetailModel(
                import_id=import_detail.import_id,
                product_id=import_detail.product_id,
                unit_id=import_detail.unit_id,
                quantity=import_detail.quantity
            )
            self.session.add(import_detail_model)
            self.session.flush()
            self.session.refresh(import_detail_model)
            return self._to_domain(import_detail_model)
        except Exception as e:
            self.session.rollback()
            raise ValueError(f'Error creating import detail: {str(e)}')

    def get_by_id(self, import_detail_id: int, household_id: int = None) -> Optional[ImportDetail]:
        query = self.session.query(ImportDetailModel).join(ImportReceiptModel).join(Warehouse).filter(
            ImportDetailModel.id == import_detail_id
        )
        if household_id is not None:
            query = query.filter(Warehouse.household_id == household_id)
        import_detail_model = query.first()
        return self._to_domain(import_detail_model) if import_detail_model else None

    def list_by_import_id(self, import_id: int, household_id: int = None) -> List[ImportDetail]:
        query = self.session.query(ImportDetailModel).join(ImportReceiptModel).join(Warehouse).filter(
            ImportDetailModel.import_id == import_id
        )
        if household_id is not None:
            query = query.filter(Warehouse.household_id == household_id)
        import_detail_models = query.all()
        return [self._to_domain(idm) for idm in import_detail_models]

    def update(self, import_detail: ImportDetail, household_id: int = None) -> ImportDetail:
        try:
            query = self.session.query(ImportDetailModel).join(ImportReceiptModel).join(Warehouse).filter(
                ImportDetailModel.id == import_detail.id
            )
            if household_id is not None:
                query = query.filter(Warehouse.household_id == household_id)
            import_detail_model = query.first()
            if not import_detail_model:
                raise ValueError('Import detail not found')

            if import_detail.product_id is not None:
                import_detail_model.product_id = import_detail.product_id
            if import_detail.unit_id is not None:
                import_detail_model.unit_id = import_detail.unit_id
            if import_detail.quantity is not None:
                import_detail_model.quantity = import_detail.quantity

            self.session.flush()
            self.session.refresh(import_detail_model)
            return self._to_domain(import_detail_model)
        except Exception as e:
            self.session.rollback()
            raise ValueError(f'Error updating import detail: {str(e)}')

    def _to_domain(self, import_detail_model: ImportDetailModel) -> ImportDetail:
        return ImportDetail(
            id=import_detail_model.id,
            import_id=import_detail_model.import_id,
            product_id=import_detail_model.product_id,
            unit_id=import_detail_model.unit_id,
            quantity=import_detail_model.quantity
        )
