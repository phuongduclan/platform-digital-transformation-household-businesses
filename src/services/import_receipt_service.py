from domain.models.import_receipt import ImportReceiptDTO
from domain.models.iimport_receipt_repository import IImportReceiptRepository

class ImportReceiptService:

    def __init__(self, repo: IImportReceiptRepository):
        self.repo = repo

    def create(self, dto: ImportReceiptDTO):
        return self.repo.create(dto)

    def confirm(self, receipt_id: int):
        return self.repo.confirm(receipt_id)
