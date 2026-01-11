from typing import Optional
from datetime import datetime

class SubscriptionPlan:
    def __init__(
        self,
        id: Optional[int],
        name: str,
        price: float,
        user_id: int,
        billing_cycle: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[str] = "active",
        created_by: Optional[str] = None,
        updated_by: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.name = name
        self.price = price
        self.user_id = user_id
        self.billing_cycle = billing_cycle
        self.description = description
        self.status = status
        self.created_by = created_by
        self.updated_by = updated_by
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()

    def update(
        self,
        name: Optional[str] = None,
        price: Optional[float] = None,
        billing_cycle: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[str] = None,
        updated_by: Optional[str] = None
    ):
        """Cập nhật thông tin plan"""
        if name is not None:
            self.name = name
        if price is not None:
            self.price = price
        if billing_cycle is not None:
            self.billing_cycle = billing_cycle
        if description is not None:
            self.description = description
        if status is not None:
            self.status = status
        if updated_by is not None:
            self.updated_by = updated_by
        self.updated_at = datetime.utcnow()
