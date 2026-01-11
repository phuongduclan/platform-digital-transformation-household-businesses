from src.infrastructure.databases.mssql import session
from src.infrastructure.models import User, Role
import sys

def check_users():
    try:
        print("Checking users in database...")
        users = session.query(User).all()
        if not users:
            print("No users found in database.")
            return

        for u in users:
            role = session.query(Role).filter_by(id=u.role_id).first()
            role_name = role.role_name if role else "Unknown"
            print(f"ID: {u.id} | Username: {u.username} | Role: {role_name} | Status: {u.status} | Household: {u.household_id}")
            # print(f"Password Hash: {u.password}") # Be careful with printing hashes, but for local debugging it might help
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_users()
