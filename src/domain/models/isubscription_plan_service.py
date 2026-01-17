from abc import ABC, abstractmethod
from domain.models.subscription_plan import SubscriptionPlan
from typing import List, Optional
from datetime import datetime

class ISubscriptionPlanService(ABC):
    @abstractmethod
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
        pass

    @abstractmethod
    def get_plan(self, plan_id: int) -> Optional[SubscriptionPlan]:
        pass

    @abstractmethod
    def list_plans(self) -> List[SubscriptionPlan]:
        pass

    @abstractmethod
    def get_plan_by_name(self, name: str) -> Optional[SubscriptionPlan]:
        pass

    @abstractmethod
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
        pass

    @abstractmethod
    def delete_plan(self, plan_id: int) -> None:
        pass
