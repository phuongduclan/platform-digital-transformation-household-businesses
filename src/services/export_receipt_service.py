from domain.models.export_receipt import ExportReceiptDTO
from domain.models.iexport_receipt_repository import IExportReceiptRepository

class ExportReceiptService:

    def __init__(self, repo: IExportReceiptRepository):
        self.repo = repo

    def create(self, dto: ExportReceiptDTO):
        return self.repo.create(dto)

    def confirm(self, receipt_id: int):
        return self.repo.confirm(receipt_id)
