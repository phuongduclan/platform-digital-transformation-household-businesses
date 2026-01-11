"""
Subscription Service - Check household có subscription active và CRUD subscription
"""
from datetime import datetime, timezone
from infrastructure.databases.mssql import session
from infrastructure.models import Subscription  # path đúng với project

class SubscriptionService:
    def __init__(self, db_session=None):
        # Nếu không truyền session thì dùng mặc định
        self.session = db_session or session

    # ---------------- CHECK ----------------
    def check_household_subscription_active(self, household_id: int) -> bool:
        """
        Check household có subscription active không
        
        Business Rule:
        - Một household chỉ được có 1 subscription active tại một thời điểm
        - Subscription active: is_active=True và end_date > now()
        """
        if not household_id:
            # Admin không cần check subscription
            return True
        
        subscription = self.get_active_subscription(household_id)
        return subscription is not None

    def get_active_subscription(self, household_id: int):
        """
        Lấy subscription active của household
        
        Business Rule:
        - Một household chỉ có 1 subscription active tại một thời điểm
        - Subscription active: is_active=True và end_date > now()
        
        Returns:
            Subscription object nếu có subscription active
            None nếu không có subscription active
        """
        if not household_id:
            return None
        
        subscription = self.session.query(Subscription).filter_by(
            household_id=household_id,
            is_active=True
        ).first()
        
        if subscription:
            # Check end_date với timezone-aware datetime
            now = datetime.now(timezone.utc)
            # Nếu subscription.end_date không có timezone, so sánh trực tiếp
            if hasattr(subscription.end_date, 'tzinfo') and subscription.end_date.tzinfo:
                if subscription.end_date >= now:
                    return subscription
            else:
                # Subscription.end_date không có timezone, so sánh với datetime.utcnow() (không timezone)
                if subscription.end_date >= datetime.utcnow():
                    return subscription
        
        return None

    # ---------------- CREATE ----------------
    def create_subscription(
        self,
        household_id: int,
        plan_id: int,
        start_date: datetime,
        end_date: datetime,
        is_active: bool = True,
        allow_multiple: bool = False  # Business rule: chỉ cho phép nhiều subscription nếu allow_multiple=True (Admin deactivate cũ rồi tạo mới)
    ):
        """
        Tạo subscription mới với business rules
        
        Business Rule:
        - KHÔNG được đăng ký Plan B khi đã có Plan A active (is_active=True và end_date > now())
        - Chỉ được upgrade: Admin phải deactivate subscription cũ rồi tạo mới, hoặc update subscription hiện tại
        - Trường hợp đặc biệt: Registration flow (allow_multiple=True) - tạo household mới nên không có subscription cũ
        
        Args:
            allow_multiple: True nếu cho phép tạo nhiều subscription (chỉ dùng cho registration flow)
        """
        # Business rule: Check duplicate active subscription
        if not allow_multiple:
            existing_active = self.get_active_subscription(household_id)
            if existing_active:
                raise ValueError(
                    f"Household {household_id} already has an active subscription (ID: {existing_active.id}). "
                    f"Cannot create new subscription. Please upgrade by deactivating the current subscription first, "
                    f"or update the existing subscription to change the plan."
                )
        
        subscription = Subscription(
            household_id=household_id,
            plan_id=plan_id,
            start_date=start_date,
            end_date=end_date,
            is_active=is_active,
            created_at=datetime.now(timezone.utc).replace(tzinfo=None),  # SQL Server không support timezone
            updated_at=datetime.now(timezone.utc).replace(tzinfo=None)  # SQL Server không support timezone
        )
        self.session.add(subscription)
        self.session.commit()
        self.session.refresh(subscription)
        return subscription

    # ---------------- LIST ----------------
    def list_subscriptions(self):
        """Lấy tất cả subscription"""
        return self.session.query(Subscription).all()

    # ---------------- GET BY ID ----------------
    def get_subscription(self, subscription_id: int):
        """Lấy subscription theo ID"""
        return self.session.query(Subscription).filter_by(id=subscription_id).first()

    # ---------------- UPDATE ----------------
    def update_subscription(
        self,
        subscription_id: int,
        household_id: int = None,
        plan_id: int = None,
        start_date: datetime = None,
        end_date: datetime = None,
        is_active: bool = None
    ):
        """Cập nhật subscription theo ID"""
        subscription = self.get_subscription(subscription_id)
        if not subscription:
            raise ValueError("Subscription not found")
        if household_id is not None:
            subscription.household_id = household_id
        if plan_id is not None:
            subscription.plan_id = plan_id
        if start_date is not None:
            subscription.start_date = start_date
        if end_date is not None:
            subscription.end_date = end_date
        if is_active is not None:
            subscription.is_active = is_active
        subscription.updated_at = datetime.now(timezone.utc).replace(tzinfo=None)  # SQL Server không support timezone
        self.session.commit()
        return subscription

    # ---------------- DELETE ----------------
    def delete_subscription(self, subscription_id: int):
        """Xóa subscription theo ID"""
        subscription = self.get_subscription(subscription_id)
        if not subscription:
            raise ValueError("Subscription not found")
        self.session.delete(subscription)
        self.session.commit()
    
    # ---------------- OWNER METHODS (Data Isolation) ----------------
    def get_own_subscription(self, household_id: int):
        """
        Lấy subscription active của household (Owner chỉ xem subscription của mình)
        
        Business Rule:
        - Owner chỉ được xem subscription của household mình (household_id từ JWT)
        - Data isolation enforced
        - Trả về subscription active (is_active=True và end_date > now())
        
        Returns:
            Subscription object nếu có subscription active
            None nếu không có subscription active
        """
        if not household_id:
            raise ValueError("Household ID is required")
        
        subscription = self.get_active_subscription(household_id)
        return subscription
    
    def update_own_subscription(
        self,
        household_id: int,
        plan_id: int,
        start_date: datetime = None,
        end_date: datetime = None
    ):
        """
        Owner upgrade subscription plan (update subscription của household mình)
        
        Business Rule:
        - Owner chỉ được update subscription của household mình (household_id từ JWT)
        - Data isolation enforced
        - Upgrade plan: Update plan_id và tính lại end_date dựa trên billing_cycle của plan mới
        - Nếu không có subscription active → Raise ValueError
        
        Args:
            household_id: Household ID từ JWT token (Owner không thể fake)
            plan_id: Plan ID mới (upgrade)
            start_date: Start date mới (optional, default: today)
            end_date: End date mới (optional, sẽ tính tự động dựa trên billing_cycle nếu không có)
        """
        if not household_id:
            raise ValueError("Household ID is required")
        
        # Lấy subscription active của household
        subscription = self.get_active_subscription(household_id)
        if not subscription:
            raise ValueError(f"Household {household_id} does not have an active subscription. Please contact administrator.")
        
        # Lấy plan mới để tính end_date
        from infrastructure.models import SubscriptionPlan
        new_plan = self.session.query(SubscriptionPlan).filter_by(id=plan_id).first()
        if not new_plan:
            raise ValueError(f"Subscription plan with ID {plan_id} not found")
        
        if hasattr(new_plan, 'status') and getattr(new_plan, 'status', '').lower() != 'active':
            raise ValueError(f"Subscription plan with ID {plan_id} is not active")
        
        # Tính start_date và end_date
        now = datetime.now(timezone.utc).replace(tzinfo=None)  # SQL Server không support timezone
        new_start_date = start_date if start_date else now
        
        # Tính end_date dựa trên billing_cycle của plan mới
        if not end_date:
            billing_cycle = getattr(new_plan, 'billing_cycle', 'monthly') if hasattr(new_plan, 'billing_cycle') else 'monthly'
            from datetime import timedelta
            if billing_cycle.lower() == 'monthly':
                new_end_date = new_start_date + timedelta(days=30)
            elif billing_cycle.lower() == 'yearly':
                new_end_date = new_start_date + timedelta(days=365)
            else:
                # Default: 30 days
                new_end_date = new_start_date + timedelta(days=30)
        else:
            new_end_date = end_date
        
        # Update subscription
        subscription.plan_id = plan_id
        subscription.start_date = new_start_date
        subscription.end_date = new_end_date
        subscription.updated_at = datetime.now(timezone.utc).replace(tzinfo=None)
        
        self.session.commit()
        self.session.refresh(subscription)
        return subscription