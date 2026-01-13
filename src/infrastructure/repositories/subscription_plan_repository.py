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
            # Query existing plan from database
            plan_model = self.session.query(SubscriptionPlanModel).filter_by(id=plan.id).first()
            if not plan_model:
                raise ValueError("Subscription plan not found")
            
            # Update only provided fields
            if plan.name is not None:
                plan_model.name = plan.name
            if plan.price is not None:
                plan_model.price = plan.price
            if plan.billing_cycle is not None:
                plan_model.billing_cycle = plan.billing_cycle
            if plan.description is not None:
                plan_model.description = plan.description
            if plan.status is not None:
                plan_model.status = plan.status
            if plan.updated_by is not None:
                plan_model.updated_by = plan.updated_by
            if plan.updated_at is not None:
                plan_model.updated_at = plan.updated_at
            
            self.session.commit()
            self.session.refresh(plan_model)
            return plan_model
        except Exception as e:
            self.session.rollback()
            raise ValueError(f"Error updating subscription plan: {str(e)}")

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
