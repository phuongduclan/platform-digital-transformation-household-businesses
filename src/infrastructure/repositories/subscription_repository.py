from domain.models.isubscription_repository import ISubscriptionRepository
from domain.models.subscription import Subscription
from typing import List, Optional
from infrastructure.databases.mssql import session
from infrastructure.models.subscription_model import Subscription as SubscriptionModel
from sqlalchemy.orm import Session
from datetime import datetime, timezone

class SubscriptionRepository(ISubscriptionRepository):
    def __init__(self, session: Session = session):
        self.session = session

    def add(self, subscription: Subscription) -> SubscriptionModel:
        """
        Add subscription to session (NO COMMIT - let controller manage transaction)
        Transaction management: Controller phải commit/rollback
        """
        try:
            sub_model = SubscriptionModel(
                plan_id=subscription.plan_id,
                household_id=subscription.household_id,
                start_date=subscription.start_date,
                end_date=subscription.end_date,
                is_active=subscription.is_active,
                created_at=subscription.created_at,
                updated_at=subscription.updated_at
            )
            self.session.add(sub_model)
            # KHÔNG commit ở đây - để controller quản lý transaction
            # self.session.commit()
            self.session.flush()  # Flush để lấy ID, nhưng không commit
            return sub_model
        except Exception as e:
            # KHÔNG rollback ở đây - để controller quản lý transaction
            # self.session.rollback()
            raise ValueError(f"Error creating subscription: {str(e)}")

    def get_by_id(self, subscription_id: int) -> Optional[SubscriptionModel]:
        """
        Lấy subscription theo ID
        """
        return self.session.query(SubscriptionModel).filter_by(id=subscription_id).first()

    def list(self) -> List[SubscriptionModel]:
        """
        Lấy tất cả subscription
        """
        return self.session.query(SubscriptionModel).all()

    def update(self, subscription: SubscriptionModel) -> SubscriptionModel:
        """
        Update subscription in session (NO COMMIT - let controller manage transaction)
        """
        sub_model = self.get_by_id(subscription.id)
        if not sub_model:
            raise ValueError("Subscription not found")

        sub_model.plan_id = subscription.plan_id
        sub_model.household_id = subscription.household_id
        sub_model.start_date = subscription.start_date
        sub_model.end_date = subscription.end_date
        sub_model.is_active = subscription.is_active
        sub_model.updated_at = subscription.updated_at or datetime.now(timezone.utc)

        # KHÔNG commit ở đây - để controller quản lý transaction
        # self.session.commit()
        self.session.flush()  # Flush để refresh, nhưng không commit
        return sub_model

    def delete(self, subscription_id: int) -> None:
        """
        Delete subscription from session (NO COMMIT - let controller manage transaction)
        """
        sub_model = self.get_by_id(subscription_id)
        if not sub_model:
            raise ValueError("Subscription not found")
        self.session.delete(sub_model)
        # KHÔNG commit ở đây - để controller quản lý transaction
        # self.session.commit()

    def get_by_household_id(self, household_id: int) -> Optional[SubscriptionModel]:
        """
        Lấy subscription active theo household_id
        """
        now = datetime.now(timezone.utc).replace(tzinfo=None)
        return self.session.query(SubscriptionModel).filter(
            SubscriptionModel.household_id == household_id,
            SubscriptionModel.is_active == True,
            SubscriptionModel.end_date >= now
        ).first()
