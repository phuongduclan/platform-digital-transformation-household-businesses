# src/infrastructure/repositories/subscription_plan_repository.py

from domain.models.isubscription_plan_repository import ISubscriptionPlanRepository
from domain.models.subscription_plan import SubscriptionPlan
from typing import List, Optional
from infrastructure.databases.mssql import session
from infrastructure.models.subscriptionplan_model import SubscriptionPlan as SubscriptionPlanModel
from sqlalchemy.orm import Session
from datetime import datetime

class SubscriptionPlanRepository(ISubscriptionPlanRepository):
    def __init__(self, session: Session = session):
        self._plans = []
        self._id_counter = 1
        self.session = session

    # ---------------- CREATE ----------------
    def add(self, plan: SubscriptionPlan) -> SubscriptionPlanModel:
        try:
            plan_model = SubscriptionPlanModel(
                name=plan.name,
                price=plan.price,
                user_id=plan.user_id,
                billing_cycle=plan.billing_cycle,
                description=plan.description,
                status=plan.status,
                created_by=plan.created_by,
                updated_by=plan.updated_by,
                created_at=plan.created_at,
                updated_at=plan.updated_at
            )
            self.session.add(plan_model)
            self.session.commit()
            self.session.refresh(plan_model)
            return plan_model
        except Exception as e:
            self.session.rollback()
            raise ValueError(f"Error creating subscription plan: {str(e)}")
        finally:
            self.session.close()

    # ---------------- READ ----------------
    def get_by_id(self, plan_id: int) -> Optional[SubscriptionPlanModel]:
        return self.session.query(SubscriptionPlanModel).filter_by(id=plan_id).first()

    def list(self) -> List[SubscriptionPlanModel]:
        self._plans = self.session.query(SubscriptionPlanModel).all()
        return self._plans

    def get_by_name(self, name: str) -> Optional[SubscriptionPlanModel]:
        return self.session.query(SubscriptionPlanModel).filter_by(name=name).first()

    # ---------------- UPDATE ----------------
    def update(self, plan: SubscriptionPlanModel) -> SubscriptionPlanModel:
        try:
            plan_model = SubscriptionPlanModel(
                id=plan.id,
                name=plan.name,
                price=plan.price,
                user_id=plan.user_id,
                billing_cycle=plan.billing_cycle,
                description=plan.description,
                status=plan.status,
                created_by=plan.created_by,
                updated_by=plan.updated_by,
                created_at=plan.created_at,
                updated_at=plan.updated_at
            )
            self.session.merge(plan_model)
            self.session.commit()
            self.session.refresh(plan_model)
            return plan_model
        except Exception as e:
            self.session.rollback()
            raise ValueError(f"Error updating subscription plan: {str(e)}")
        finally:
            self.session.close()

    # ---------------- DELETE ----------------
    def delete(self, plan_id: int) -> None:
        try:
            plan_model = self.session.query(SubscriptionPlanModel).filter_by(id=plan_id).first()
            if plan_model:
                self.session.delete(plan_model)
                self.session.commit()
            else:
                raise ValueError("Subscription plan not found")
        except Exception as e:
            self.session.rollback()
            raise ValueError(f"Error deleting subscription plan: {str(e)}")
        finally:
            self.session.close()
