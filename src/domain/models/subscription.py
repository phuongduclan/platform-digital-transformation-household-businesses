from datetime import datetime
from typing import Optional

class Subscription:
    def __init__(
        self,
        id: Optional[int],
        plan_id: int,
        household_id: int,
        start_date: Optional[datetime],
        end_date: Optional[datetime],
        is_active: bool,
        created_at: datetime,
        updated_at: datetime
    ):
        self.id = id
        self.plan_id = plan_id
        self.household_id = household_id
        self.start_date = start_date
        self.end_date = end_date
        self.is_active = is_active
        self.created_at = created_at
        self.updated_at = updated_at
