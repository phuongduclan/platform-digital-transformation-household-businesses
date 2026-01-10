"""
Subscription Service - Check household có subscription active không
"""
from datetime import datetime
from infrastructure.databases.mssql import session
from infrastructure.models import Subscription

class SubscriptionService:
    def __init__(self, db_session):
        self.session = db_session
    
    def check_household_subscription_active(self, household_id):
        """
        Check household có subscription active không
        
        Args:
            household_id: ID của household
            
        Returns:
            bool: True nếu có subscription active, False nếu không
        """
        if not household_id:
            # Admin không cần check subscription
            return True
        
        subscription = self.session.query(Subscription).filter_by(
            household_id=household_id,
            is_active=True
        ).first()
        
        if not subscription:
            return False
        
        # Check end_date > now()
        if subscription.end_date < datetime.utcnow():
            return False
        
        return True
    
    def get_active_subscription(self, household_id):
        """Lấy subscription active của household"""
        if not household_id:
            return None
        
        subscription = self.session.query(Subscription).filter_by(
            household_id=household_id,
            is_active=True
        ).first()
        
        if subscription and subscription.end_date >= datetime.utcnow():
            return subscription
        
        return None
