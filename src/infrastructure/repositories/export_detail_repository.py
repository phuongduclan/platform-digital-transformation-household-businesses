from domain.models.iexport_detail_repository import IExportDetailRepository
from domain.models.export_detail import ExportDetail
from typing import List, Optional
from infrastructure.models.export_detail_model import ExportDetail as ExportDetailModel
from infrastructure.models.export_receipt_model import ExportReceipt as ExportReceiptModel
from infrastructure.models.warehouse_model import Warehouse
from infrastructure.databases.mssql import session

class ExportDetailRepository(IExportDetailRepository):
    def __init__(self, session=session):
        self.session = session

    def add(self, export_detail: ExportDetail) -> ExportDetail:
        try:
            export_detail_model = ExportDetailModel(
                export_id=export_detail.export_id,
                product_id=export_detail.product_id,
                unit_id=export_detail.unit_id,
                quantity=export_detail.quantity
            )
            self.session.add(export_detail_model)
            self.session.flush()
            self.session.refresh(export_detail_model)
            return self._to_domain(export_detail_model)
        except Exception as e:
            self.session.rollback()
            raise ValueError(f'Error creating export detail: {str(e)}')

    def get_by_id(self, export_detail_id: int, household_id: int = None) -> Optional[ExportDetail]:
        query = self.session.query(ExportDetailModel).join(ExportReceiptModel).join(Warehouse).filter(
            ExportDetailModel.id == export_detail_id
        )
        if household_id is not None:
            query = query.filter(Warehouse.household_id == household_id)
        export_detail_model = query.first()
        return self._to_domain(export_detail_model) if export_detail_model else None

    def list_by_export_id(self, export_id: int, household_id: int = None) -> List[ExportDetail]:
        query = self.session.query(ExportDetailModel).join(ExportReceiptModel).join(Warehouse).filter(
            ExportDetailModel.export_id == export_id
        )
        if household_id is not None:
            query = query.filter(Warehouse.household_id == household_id)
        export_detail_models = query.all()
        return [self._to_domain(edm) for edm in export_detail_models]

    def update(self, export_detail: ExportDetail, household_id: int = None) -> ExportDetail:
        try:
            query = self.session.query(ExportDetailModel).join(ExportReceiptModel).join(Warehouse).filter(
                ExportDetailModel.id == export_detail.id
            )
            if household_id is not None:
                query = query.filter(Warehouse.household_id == household_id)
            export_detail_model = query.first()
            if not export_detail_model:
                raise ValueError('Export detail not found')

            if export_detail.product_id is not None:
                export_detail_model.product_id = export_detail.product_id
            if export_detail.unit_id is not None:
                export_detail_model.unit_id = export_detail.unit_id
            if export_detail.quantity is not None:
                export_detail_model.quantity = export_detail.quantity

            self.session.flush()
            self.session.refresh(export_detail_model)
            return self._to_domain(export_detail_model)
        except Exception as e:
            self.session.rollback()
            raise ValueError(f'Error updating export detail: {str(e)}')

    def _to_domain(self, export_detail_model: ExportDetailModel) -> ExportDetail:
        return ExportDetail(
            id=export_detail_model.id,
            export_id=export_detail_model.export_id,
            product_id=export_detail_model.product_id,
            unit_id=export_detail_model.unit_id,
            quantity=export_detail_model.quantity
        )
