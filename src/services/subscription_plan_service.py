from domain.models.subscription_plan import SubscriptionPlan
from domain.models.isubscription_plan_repository import ISubscriptionPlanRepository
from domain.models.isubscription_plan_service import ISubscriptionPlanService
from typing import List, Optional
from datetime import datetime
from infrastructure.utils.datetime_utils import vietnam_now

class SubscriptionPlanService(ISubscriptionPlanService):
    def __init__(self, repository: ISubscriptionPlanRepository):
        self.repository = repository

    def create_plan(
        self,
        name: str,
        price: float,
        billing_cycle: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[str] = "active",
        created_by: Optional[str] = None,
        updated_by: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ) -> SubscriptionPlan:
        plan = SubscriptionPlan(
            id=None,
            name=name,
            price=price,
            billing_cycle=billing_cycle,
            description=description,
            status=status,
            created_by=created_by,
            updated_by=updated_by,
            created_at=created_at or vietnam_now(),
            updated_at=updated_at or vietnam_now()
        )
        return self.repository.add(plan)

    def get_plan(self, plan_id: int) -> Optional[SubscriptionPlan]:
        return self.repository.get_by_id(plan_id)

    def list_plans(self) -> List[SubscriptionPlan]:
        return self.repository.list()

    def get_plan_by_name(self, name: str) -> Optional[SubscriptionPlan]:
        return self.repository.get_by_name(name)

    def update_plan(
        self,
        plan_id: int,
        name: Optional[str] = None,
        price: Optional[float] = None,
        billing_cycle: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[str] = None,
        updated_by: Optional[str] = None,
        updated_at: Optional[datetime] = None
    ) -> SubscriptionPlan:
        plan = self.repository.get_by_id(plan_id)
        if not plan:
            raise ValueError("Subscription plan not found")

        # Update ORM model attributes directly (không gọi plan.update() vì đây là ORM model)
        if name is not None:
            plan.name = name
        if price is not None:
            plan.price = price
        if billing_cycle is not None:
            plan.billing_cycle = billing_cycle
        if description is not None:
            plan.description = description
        if status is not None:
            plan.status = status
        if updated_by is not None:
            plan.updated_by = updated_by
        plan.updated_at = updated_at or vietnam_now()

        return self.repository.update(plan)

    def delete_plan(self, plan_id: int) -> None:
        self.repository.delete(plan_id)