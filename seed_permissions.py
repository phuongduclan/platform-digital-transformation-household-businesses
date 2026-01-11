import sys
import os

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))

try:
    from infrastructure.databases.mssql import session
    from infrastructure.models import Function, Role, RoleFunction
except ImportError:
    # Fallback to absolute imports if running from root
    sys.path.append(os.getcwd())
    from src.infrastructure.databases.mssql import session
    from src.infrastructure.models import Function, Role, RoleFunction

from src.app import create_app

def seed_permissions():
    app = create_app()
    with app.app_context():
        try:
            # 1. Define Functions
            functions_data = [
                ('F111', 'Owner Invoice Management', '/api/owner/invoices/*', 'C,R,U,D'),
                ('F207', 'Employee Create Draft Invoice', '/api/employee/invoices/', 'C'),
                ('F208', 'Employee Update Draft Invoice', '/api/employee/invoices/*', 'U'),
                ('F209', 'Employee Read Own Invoices', '/api/employee/invoices/', 'R'),
                ('F210', 'Employee Confirm Invoice', '/api/employee/invoices/*/confirm', 'U'),
                ('F213', 'Employee Read AI Draft Orders', '/api/employee/draft-orders/', 'R'),
                ('F214', 'Employee Confirm AI Draft Order', '/api/employee/draft-orders/*/confirm', 'U'),
            ]

            for code, name, pattern, methods in functions_data:
                func = session.query(Function).filter_by(function_code=code).first()
                if not func:
                    func = Function(
                        function_code=code, 
                        function_name=name,
                        url_pattern=pattern,
                        http_methods=methods
                    )
                    session.add(func)
            session.flush()

            # 2. Get Roles
            owner_role = session.query(Role).filter_by(role_name='Owner').first()
            employee_role = session.query(Role).filter_by(role_name='Employee').first()

            if not owner_role or not employee_role:
                print("Roles not found. Please run bootstrap_admin first.")
                return

            # 3. Assign Permissions
            # Owner (F111)
            f111 = session.query(Function).filter_by(function_code='F111').first()
            if not session.query(RoleFunction).filter_by(role_id=owner_role.id, function_id=f111.id).first():
                session.add(RoleFunction(role_id=owner_role.id, function_id=f111.id))

            # Employee & Owner (Employee features)
            permission_codes = ['F207', 'F208', 'F209', 'F210', 'F213', 'F214']

            for code in permission_codes:
                func = session.query(Function).filter_by(function_code=code).first()
                if func:
                    # Give to Employee
                    if not session.query(RoleFunction).filter_by(role_id=employee_role.id, function_id=func.id).first():
                        session.add(RoleFunction(role_id=employee_role.id, function_id=func.id))
                    # Give to Owner too
                    if not session.query(RoleFunction).filter_by(role_id=owner_role.id, function_id=func.id).first():
                        session.add(RoleFunction(role_id=owner_role.id, function_id=func.id))

            session.commit()
            print("Permissions seeded successfully!")

        except Exception as e:
            session.rollback()
            print(f"Error seeding permissions: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    seed_permissions()
