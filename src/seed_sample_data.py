"""
Script de them du lieu mau:
- 1 Subscription Plan
- 1 Household
- 1 Subscription (active)
- 1 User Owner (co household_id)
- 1 User Employee (cung household voi Owner)
"""
import sys
import os
# Set encoding for Windows console
if sys.platform == 'win32':
    try:
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    except:
        pass  # Ignore if already set

from app import create_app
from infrastructure.databases.mssql import session
from infrastructure.models import (
    SubscriptionPlan, Household, Subscription, User, Role
)
from datetime import datetime, timedelta, timezone

def seed_sample_data():
    app = create_app()
    
    with app.app_context():
        try:
            # 1. Lấy Admin user (giả sử có user admin với id=1)
            admin_user = session.query(User).filter_by(user_name='admin').first()
            if not admin_user:
                print("[ERROR] Khong tim thay admin user. Vui long tao admin user truoc.")
                return
            
            # 2. Lấy Role IDs
            owner_role = session.query(Role).filter_by(role_name='Owner').first()
            employee_role = session.query(Role).filter_by(role_name='Employee').first()
            
            if not owner_role:
                print("[ERROR] Khong tim thay Owner role")
                return
            if not employee_role:
                print("[ERROR] Khong tim thay Employee role")
                return
            
            # 3. Tạo Subscription Plan
            plan = SubscriptionPlan(
                name="Gói Cơ Bản",
                user_id=admin_user.id,
                billing_cycle="monthly",
                price=500000.00,
                description="Gói cơ bản cho hộ kinh doanh nhỏ",
                status="ACTIVE",
                created_by="admin",
                updated_by="admin"
            )
            session.add(plan)
            session.flush()  # Để lấy plan.id
            print(f"[OK] Da tao Subscription Plan: {plan.name} (ID: {plan.id})")
            
            # 4. Tạo Household
            household = Household(
                tax_code="123456789012",
                name="Ho Kinh Doanh ABC",
                phone="0901234567",
                address="123 Duong ABC, Quan XYZ, TP.HCM",
                description="Ho kinh doanh mau",
                status="ACTIVE",
                created_by="admin",
                updated_by="admin"
            )
            session.add(household)
            session.flush()  # Để lấy household.id
            print(f"[OK] Da tao Household: {household.name} (ID: {household.id})")
            
            # 5. Tạo Subscription (active)
            start_date = datetime.now(timezone.utc)
            end_date = start_date + timedelta(days=30)  # 30 ngày
            
            subscription = Subscription(
                plan_id=plan.id,
                household_id=household.id,
                start_date=start_date,
                end_date=end_date,
                is_active=True
            )
            session.add(subscription)
            session.flush()
            print(f"[OK] Da tao Subscription: Active tu {start_date.date()} den {end_date.date()}")
            
            # 6. Tạo User Owner
            owner_user = User(
                household_id=household.id,
                role_id=owner_role.id,
                user_name="owner1",
                password="owner123",
                email="owner1@example.com",
                description="Owner cua ho kinh doanh ABC",
                status="ACTIVE",
                created_by="admin",
                updated_by="admin"
            )
            session.add(owner_user)
            session.flush()
            print(f"[OK] Da tao Owner User: {owner_user.user_name} (ID: {owner_user.id}, Household ID: {owner_user.household_id})")
            
            # 7. Tạo User Employee (cùng household)
            employee_user = User(
                household_id=household.id,
                role_id=employee_role.id,
                user_name="employee1",
                password="emp123",
                email="employee1@example.com",
                description="Employee cua ho kinh doanh ABC",
                status="ACTIVE",
                created_by="owner1",
                updated_by="owner1"
            )
            session.add(employee_user)
            session.flush()
            print(f"[OK] Da tao Employee User: {employee_user.user_name} (ID: {employee_user.id}, Household ID: {employee_user.household_id})")
            
            # Commit tất cả
            session.commit()
            print("\n[SUCCESS] Da them du lieu mau thanh cong!")
            print("\nTom tat:")
            print(f"   - Subscription Plan: {plan.name} (ID: {plan.id})")
            print(f"   - Household: {household.name} (ID: {household.id})")
            print(f"   - Subscription: Active (ID: {subscription.id})")
            print(f"   - Owner: {owner_user.user_name} / {owner_user.password}")
            print(f"   - Employee: {employee_user.user_name} / {employee_user.password}")
            
        except Exception as e:
            session.rollback()
            print(f"[ERROR] Loi: {str(e)}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    seed_sample_data()
