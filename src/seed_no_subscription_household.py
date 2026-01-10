"""
Script de them du lieu mau:
- 1 Household CHUA co subscription (de test subscription check)
- 1 User Owner cua household do
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
    Household, User, Role
)

def seed_no_subscription_household():
    app = create_app()
    
    with app.app_context():
        try:
            # 1. Lấy Admin user (de tao household)
            admin_user = session.query(User).filter_by(user_name='admin').first()
            if not admin_user:
                print("[ERROR] Khong tim thay admin user. Vui long tao admin user truoc.")
                return
            
            # 2. Lấy Owner role
            owner_role = session.query(Role).filter_by(role_name='Owner').first()
            if not owner_role:
                print("[ERROR] Khong tim thay Owner role")
                return
            
            # 3. Tạo Household CHUA co subscription
            household = Household(
                tax_code="987654321098",
                name="Ho Kinh Doanh XYZ - Chua dang ky",
                phone="0987654321",
                address="456 Duong XYZ, Quan ABC, TP.HCM",
                description="Ho kinh doanh chua dang ky subscription - de test",
                status="ACTIVE",
                created_by="admin",
                updated_by="admin"
            )
            session.add(household)
            session.flush()  # De lay household.id
            print(f"[OK] Da tao Household CHUA co subscription: {household.name} (ID: {household.id})")
            
            # 4. Tạo User Owner cua household do (CHUA co subscription)
            owner_user = User(
                household_id=household.id,
                role_id=owner_role.id,
                user_name="owner_no_sub",
                password="owner123",
                email="owner_no_sub@example.com",
                description="Owner cua ho kinh doanh chua dang ky subscription",
                status="ACTIVE",
                created_by="admin",
                updated_by="admin"
            )
            session.add(owner_user)
            session.flush()
            print(f"[OK] Da tao Owner User: {owner_user.user_name} (ID: {owner_user.id}, Household ID: {owner_user.household_id})")
            print(f"[INFO] Household {household.id} CHUA co subscription - se bi block khi test API")
            
            # Commit tat ca
            session.commit()
            print("\n[SUCCESS] Da them du lieu mau thanh cong!")
            print("\nTom tat:")
            print(f"   - Household: {household.name} (ID: {household.id}) - CHUA CO SUBSCRIPTION")
            print(f"   - Owner: {owner_user.user_name} / {owner_user.password}")
            print(f"\n[TEST] Login voi owner_no_sub/owner123 se bi block boi subscription check!")
            
        except Exception as e:
            session.rollback()
            print(f"[ERROR] Loi: {str(e)}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    seed_no_subscription_household()
