from src.infrastructure.databases.mssql import session
from src.infrastructure.repositories.auth_repository import AuthRepository
from src.services.auth_service import AuthService
from src.services.subscription_service import SubscriptionService
from src.app import create_app

def test_login_logic():
    app = create_app()
    with app.app_context():
        auth_repo = AuthRepository(session)
        sub_service = SubscriptionService(session)
        auth_service = AuthService(auth_repo, sub_service)

        print("Testing owner1 / owner123...")
        user = auth_service.login("owner1", "owner123")
        if user:
            print(f"SUCCESS: Logged in as {user.username}")
        else:
            print("FAILED: owner1 / owner123")

        print("Testing employee1 / emp123...")
        user = auth_service.login("employee1", "emp123")
        if user:
            print(f"SUCCESS: Logged in as {user.username}")
        else:
            print("FAILED: employee1 / emp123")

if __name__ == "__main__":
    test_login_logic()
