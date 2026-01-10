from fastapi import APIRouter, Depends
from services.import_receipt_service import ImportReceiptService
from api.schemas.import_receipt import ImportReceiptCreate
from domain.models.import_receipt import ImportReceiptDTO
from infrastructure.repositories.import_receipt_repository import ImportReceiptRepository

router = APIRouter(prefix="/api/owner/import-receipts", tags=["ImportReceipt"])

@router.post("")
def create_import_receipt(body: ImportReceiptCreate):
    service = ImportReceiptService(ImportReceiptRepository())
    dto = ImportReceiptDTO(**body.dict(), status="DRAFT", created_by=1)
    return service.create(dto)

@router.put("/{id}/confirm")
def confirm_import_receipt(id: int):
    service = ImportReceiptService(ImportReceiptRepository())
    return service.confirm(id)
