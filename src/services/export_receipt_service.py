from domain.models.export_receipt import ExportReceipt
from domain.models.iexport_receipt_repository import IExportReceiptRepository
from domain.models.iexport_detail_repository import IExportDetailRepository
from domain.models.export_detail import ExportDetail
from typing import List, Optional
from datetime import datetime, date

class ExportReceiptService:
    def __init__(self, repository: IExportReceiptRepository, export_detail_repository: IExportDetailRepository):
        self.repository = repository
        self.export_detail_repository = export_detail_repository

    def create_export_receipt_with_details(self, warehouse_id: int, invoice_id: int = None,
                                           export_date: date = None, reason: str = None,
                                           details: List[dict] = None) -> ExportReceipt:
        """
        Tạo export receipt với details trong 1 transaction.
        Được gọi tự động từ InvoiceService khi invoice confirm (có customer_id).
        """
        if not details or len(details) == 0:
            raise ValueError("Export receipt must have at least 1 detail")

        if export_date is None:
            export_date = date.today()

        if reason is None:
            reason = "Xuất bán hàng"

        now = datetime.utcnow()

        # Tạo export receipt
        export_receipt = ExportReceipt(
            id=None,
            warehouse_id=warehouse_id,
            invoice_id=invoice_id,
            export_date=export_date,
            reason=reason,
            status='Confirm',
            created_at=now,
            updated_at=now
        )

        # Lấy session từ repository để quản lý transaction
        db_session = getattr(self.repository, 'session', None)
        if not db_session:
            raise ValueError("Repository must have a session attribute")

        # Đảm bảo export_detail_repository dùng cùng session
        if hasattr(self.export_detail_repository, 'session'):
            self.export_detail_repository.session = db_session

        try:
            # Tạo export receipt (flush để lấy ID)
            export_receipt = self.repository.create(export_receipt)
            export_id = export_receipt.id

            # Tạo details
            for detail_data in details:
                product_id = detail_data.get('product_id')
                unit_id = detail_data.get('unit_id')
                quantity = detail_data.get('quantity', 0)

                export_detail = ExportDetail(
                    id=None,
                    export_id=export_id,
                    product_id=product_id,
                    unit_id=unit_id,
                    quantity=quantity
                )
                self.export_detail_repository.add(export_detail)

            # Commit transaction
            db_session.commit()
            return export_receipt

        except Exception as e:
            db_session.rollback()
            raise ValueError(f'Error creating export receipt with details: {str(e)}')

    def get_export_receipt(self, export_receipt_id: int, household_id: int) -> Optional[ExportReceipt]:
        return self.repository.get_by_id(export_receipt_id, household_id)

    def list_export_receipts(self, household_id: int) -> List[ExportReceipt]:
        return self.repository.list(household_id)

    def update_export_receipt(self, export_receipt_id: int, household_id: int,
                             warehouse_id: int = None, export_date: date = None,
                             reason: str = None) -> ExportReceipt:
        """
        Owner chỉ được điều chỉnh (update warehouse_id, export_date, reason)
        """
        export_receipt = self.repository.get_by_id(export_receipt_id, household_id)
        if not export_receipt:
            raise ValueError('Export receipt not found')

        if warehouse_id is not None:
            export_receipt.warehouse_id = warehouse_id
        if export_date is not None:
            export_receipt.export_date = export_date
        if reason is not None:
            export_receipt.reason = reason
        
        export_receipt.updated_at = datetime.utcnow()

        return self.repository.update(export_receipt)
