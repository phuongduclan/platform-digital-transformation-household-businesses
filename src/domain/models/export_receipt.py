from datetime import datetime, date
from typing import Optional

class ExportReceipt:
    def __init__(self, id: int = None, warehouse_id: int = None, invoice_id: int = None,
                 export_date: date = None, reason: str = None, status: str = 'Confirm',
                 created_at: datetime = None, updated_at: datetime = None):
        self.id = id
        self.warehouse_id = warehouse_id
        self.invoice_id = invoice_id
        self.export_date = export_date
        self.reason = reason
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at
