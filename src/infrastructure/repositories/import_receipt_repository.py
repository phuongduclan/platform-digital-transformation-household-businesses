from domain.models.iimport_receipt_repository import IImportReceiptRepository
from domain.models.import_receipt import ImportReceiptDTO
from infrastructure.models.import_receipt import ImportReceipt
from infrastructure.db import db

class ImportReceiptRepository(IImportReceiptRepository):

    def create(self, dto: ImportReceiptDTO):
        receipt = ImportReceipt(**dto.__dict__)
        db.session.add(receipt)
        db.session.commit()
        return receipt

    def confirm(self, receipt_id: int):
        receipt = ImportReceipt.query.get(receipt_id)
        receipt.status = "CONFIRMED"
        db.session.commit()
        return receipt
