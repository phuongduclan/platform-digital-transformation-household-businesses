import sys
import os

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))

try:
    from infrastructure.databases.mssql import session
    from infrastructure.models import Role, Function, RoleFunction
except ImportError:
    # If that fails, try adding current directory and using src. prefix
    sys.path.append(os.getcwd())
    from src.infrastructure.databases.mssql import session
    from src.infrastructure.models import Role, Function, RoleFunction

def check_permissions():
    try:
        print("--- Roles ---")
        roles = session.query(Role).all()
        for r in roles:
            print(f"ID: {r.id} | Name: {r.role_name}")

        print("\n--- Functions ---")
        funcs = session.query(Function).all()
        for f in funcs:
            print(f"ID: {f.id} | Code: {f.function_code} | Name: {f.function_name} | Methods: {f.http_methods}")

        print("\n--- Role-Function Mappings ---")
        mappings = session.query(RoleFunction).all()
        for m in mappings:
            role = session.query(Role).get(m.role_id)
            func = session.query(Function).get(m.function_id)
            role_name = role.role_name if role else "Unknown"
            func_code = func.function_code if func else m.function_id
            print(f"Role ID: {m.role_id} ({role_name}) -> Function Code: {func_code}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_permissions()
