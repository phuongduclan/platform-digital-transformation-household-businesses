# src/domain/models/isubscription_repository.py

from abc import ABC, abstractmethod
from typing import List, Optional
from .subscription import Subscription

class ISubscriptionRepository(ABC):
    @abstractmethod
    def add(self, subscription: Subscription) -> Subscription:
        pass

    @abstractmethod
    def get_by_id(self, subscription_id: int) -> Optional[Subscription]:
        pass

    @abstractmethod
    def list(self) -> List[Subscription]:
        pass

    @abstractmethod
    def update(self, subscription: Subscription) -> Subscription:
        pass

    @abstractmethod
    def delete(self, subscription_id: int) -> None:
        pass

    @abstractmethod
    def get_by_household_id(self, household_id: int) -> Optional[Subscription]:
        pass
