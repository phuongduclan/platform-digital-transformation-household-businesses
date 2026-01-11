from abc import ABC, abstractmethod
from typing import List, Optional
from .subscription_plan import SubscriptionPlan

class ISubscriptionPlanRepository(ABC):
    @abstractmethod
    def add(self, plan: SubscriptionPlan) -> SubscriptionPlan:
        pass

    @abstractmethod
    def get_by_id(self, plan_id: int) -> Optional[SubscriptionPlan]:
        pass

    @abstractmethod
    def list(self) -> List[SubscriptionPlan]:
        pass

    @abstractmethod
    def update(self, plan: SubscriptionPlan) -> SubscriptionPlan:
        pass

    @abstractmethod
    def delete(self, plan_id: int) -> None:
        pass

    @abstractmethod
    def get_by_name(self, name: str) -> Optional[SubscriptionPlan]:
        pass
