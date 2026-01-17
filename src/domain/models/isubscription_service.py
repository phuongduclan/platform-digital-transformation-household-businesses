from abc import ABC, abstractmethod
from typing import Optional, List
from datetime import datetime

class ISubscriptionService(ABC):
    @abstractmethod
    def check_household_subscription_active(self, household_id: int) -> bool:
        pass

    @abstractmethod
    def get_active_subscription(self, household_id: int):
        pass

    @abstractmethod
    def create_subscription(
        self,
        household_id: int,
        plan_id: int,
        start_date: datetime,
        end_date: datetime,
        is_active: bool = True,
        allow_multiple: bool = False
    ):
        pass

    @abstractmethod
    def list_subscriptions(self) -> List:
        pass

    @abstractmethod
    def get_subscription(self, subscription_id: int):
        pass

    @abstractmethod
    def update_subscription(
        self,
        subscription_id: int,
        household_id: int = None,
        plan_id: int = None,
        start_date: datetime = None,
        end_date: datetime = None,
        is_active: bool = None
    ):
        pass

    @abstractmethod
    def delete_subscription(self, subscription_id: int) -> None:
        pass

    @abstractmethod
    def get_own_subscription(self, household_id: int):
        pass

    @abstractmethod
    def update_own_subscription(
        self,
        household_id: int,
        plan_id: int,
        start_date: datetime = None,
        end_date: datetime = None
    ):
        pass
