from app import create_app
from infrastructure.databases.mssql import session
from infrastructure.models import User, Role
from werkzeug.security import generate_password_hash

def bootstrap_admin():
    app = create_app()
    with app.app_context():
        try:
            # Create Roles if they don't exist
            roles = ['Admin', 'Owner', 'Employee']
            for r_name in roles:
                role = session.query(Role).filter_by(role_name=r_name).first()
                if not role:
                    role = Role(role_name=r_name, description=f"{r_name} role")
                    session.add(role)
                    print(f"Created role: {r_name}")
            session.flush()

            # Get Admin Role
            admin_role = session.query(Role).filter_by(role_name='Admin').first()
            
            # Create Admin User if doesn't exist
            admin = session.query(User).filter_by(username='admin').first()
            if not admin:
                admin = User(
                    username='admin',
                    password=generate_password_hash('admin_password'),
                    role_id=admin_role.id,
                    status='ACTIVE',
                    created_by='system'
                )
                session.add(admin)
                print("Created admin user.")
            
            session.commit()
            print("Bootstrap completed successfully.")
            
        except Exception as e:
            session.rollback()
            print(f"Error bootstrapping: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    bootstrap_admin()
