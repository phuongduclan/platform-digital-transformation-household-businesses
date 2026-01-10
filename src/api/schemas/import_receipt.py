from pydantic import BaseModel

class ImportReceiptCreate(BaseModel):
    household_id: int
    supplier_id: int | None
    total_amount: float
