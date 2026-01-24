from domain.models.import_receipt import ImportReceipt
from domain.models.iimport_receipt_repository import IImportReceiptRepository
from domain.models.iimport_detail_repository import IImportDetailRepository
from domain.models.iimport_receipt_service import IImportReceiptService
from domain.models.import_detail import ImportDetail
from typing import List, Optional
from datetime import datetime, date
from infrastructure.utils.datetime_utils import vietnam_now

class ImportReceiptService(IImportReceiptService):
    def __init__(self, repository: IImportReceiptRepository, import_detail_repository: IImportDetailRepository):
        self.repository = repository
        self.import_detail_repository = import_detail_repository

    def create_import_receipt_with_details(self, warehouse_id: int, invoice_id: int = None,
                                           import_date: date = None, details: List[dict] = None) -> ImportReceipt:
        """
        Tạo import receipt với details trong 1 transaction.
        Được gọi tự động từ InvoiceService khi invoice confirm (có seller_id).
        """
        if not details or len(details) == 0:
            raise ValueError("Import receipt must have at least 1 detail")

        if import_date is None:
            import_date = date.today()

        now = vietnam_now()

        # Tạo import receipt
        import_receipt = ImportReceipt(
            id=None,
            warehouse_id=warehouse_id,
            invoice_id=invoice_id,
            import_date=import_date,
            status='Confirm',
            created_at=now,
            updated_at=now
        )

        # Lấy session từ repository để quản lý transaction
        db_session = getattr(self.repository, 'session', None)
        if not db_session:
            raise ValueError("Repository must have a session attribute")

        # Đảm bảo import_detail_repository dùng cùng session
        if hasattr(self.import_detail_repository, 'session'):
            self.import_detail_repository.session = db_session

        try:
            # Tạo import receipt (flush để lấy ID)
            import_receipt = self.repository.create(import_receipt)
            import_id = import_receipt.id

            # Tạo details
            for detail_data in details:
                product_id = detail_data.get('product_id')
                unit_id = detail_data.get('unit_id')
                quantity = detail_data.get('quantity', 0)

                import_detail = ImportDetail(
                    id=None,
                    import_id=import_id,
                    product_id=product_id,
                    unit_id=unit_id,
                    quantity=quantity
                )
                self.import_detail_repository.add(import_detail)

            # Commit transaction
            db_session.commit()
            return import_receipt

        except Exception as e:
            from infrastructure.databases.session_utils import safe_rollback
            safe_rollback(db_session)
            raise ValueError(f'Error creating import receipt with details: {str(e)}')

    def get_import_receipt(self, import_receipt_id: int, household_id: int) -> Optional[ImportReceipt]:
        return self.repository.get_by_id(import_receipt_id, household_id)

    def list_import_receipts(self, household_id: int) -> List[ImportReceipt]:
        return self.repository.list(household_id)

    def update_import_receipt(self, import_receipt_id: int, household_id: int,
                              warehouse_id: int = None, import_date: date = None) -> ImportReceipt:
        """
        Owner chỉ được điều chỉnh (update warehouse_id, import_date)
        """
        import_receipt = self.repository.get_by_id(import_receipt_id, household_id)
        if not import_receipt:
            raise ValueError('Import receipt not found')

        if warehouse_id is not None:
            import_receipt.warehouse_id = warehouse_id
        if import_date is not None:
            import_receipt.import_date = import_date
        
        import_receipt.updated_at = vietnam_now()

        return self.repository.update(import_receipt)
