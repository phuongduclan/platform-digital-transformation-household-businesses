"""
Seed Data Script - Authentication & Authorization
Tạo Roles, Functions, và RoleFunction mappings

Usage:
    python src/scripts/seed_auth_data.py              # Clean RoleFunctions + F001 only (default)
    python src/scripts/seed_auth_data.py --clean-all  # Clean all Functions + RoleFunctions
"""
import sys
import os
import argparse
from datetime import datetime, timezone
from infrastructure.utils.datetime_utils import vietnam_now

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from infrastructure.databases.mssql import session
from infrastructure.models import Role, Function, RoleFunction

def clean_old_data(clean_all_functions=False):
    """
    Xóa dữ liệu cũ để seed lại từ đầu
    
    Args:
        clean_all_functions: True nếu muốn xóa tất cả Functions (seed lại từ đầu)
                           False nếu chỉ xóa RoleFunction mappings và F001
    """
    print("Cleaning old data...")
    print(f"  Mode: {'Clean all (Functions + RoleFunctions)' if clean_all_functions else 'Clean RoleFunctions + F001 only'}")
    
    try:
        # Bat buoc: Xoa tat ca RoleFunction mappings (de tranh mapping cu nhu F001 vao Admin)
        deleted_rf_count = session.query(RoleFunction).delete()
        session.commit()
        print(f"  Deleted {deleted_rf_count} RoleFunction mappings")
        
        # Bat buoc: Xoa F001 function neu ton tai (Admin khong co F001 nua)
        f001_function = session.query(Function).filter_by(function_code='F001').first()
        if f001_function:
            session.delete(f001_function)
            session.commit()
            print("  Deleted F001 function (Admin no longer has F001 manage_households)")
        else:
            print("  F001 function not found (already cleaned or never existed)")
        
        # Optional: Xoa tat ca Functions neu clean_all_functions=True
        if clean_all_functions:
            deleted_functions = session.query(Function).delete()
            session.commit()
            print(f"  Deleted {deleted_functions} Functions (seed lai tu dau)")
        
        # KHONG xoa Roles (giu lai Admin, Owner, Employee roles)
        # Vi co the da co Users su dung cac roles nay
        
        print("Old data cleaned successfully!\n")
        
    except Exception as e:
        session.rollback()
        print(f"  WARNING: Error cleaning old data: {str(e)}")
        print("  Continuing with seed...\n")

def seed_roles():
    """Tạo Roles: Admin, Owner, Employee"""
    print("Creating Roles...")
    
    roles_data = [
        {'role_name': 'Admin', 'description': 'Administrator - Manages platform'},
        {'role_name': 'Owner', 'description': 'Household Owner - Manages own household'},
        {'role_name': 'Employee', 'description': 'Employee - Works for household'}
    ]
    
    for role_data in roles_data:
        existing = session.query(Role).filter_by(role_name=role_data['role_name']).first()
        if not existing:
            role = Role(**role_data, created_at=vietnam_now(), updated_at=vietnam_now())
            session.add(role)
            print(f"  Created role: {role_data['role_name']}")
        else:
            print(f"  Role already exists: {role_data['role_name']}")
    
    session.commit()
    print("Roles created successfully!\n")

def seed_functions():
    """Tạo Functions: F0xx (Admin), F1xx (Owner), F2xx (Employee)"""
    print("Creating Functions...")
    
    functions_data = [
        # Admin Functions (F0xx) - KHÔNG có F001 manage_households
        {'function_code': 'F002', 'function_name': 'manage_subscription_plans', 'url_pattern': '/api/admin/subscription-plans', 'http_methods': 'C,R,U,D', 'description': 'Manage subscription plans', 'resource_type': 'SubscriptionPlan'},
        {'function_code': 'F003', 'function_name': 'manage_subscriptions', 'url_pattern': '/api/admin/subscriptions', 'http_methods': 'R,U', 'description': 'List all subscriptions and deactivate (CHỈ list và deactivate, KHÔNG create/update plan_id/delete)', 'resource_type': 'Subscription'},
        {'function_code': 'F004', 'function_name': 'view_platform_analytics', 'url_pattern': '/api/admin/analytics', 'http_methods': 'R', 'description': 'View platform analytics', 'resource_type': 'Analytics'},
        {'function_code': 'F005', 'function_name': 'manage_admin_users', 'url_pattern': '/api/admin/users', 'http_methods': 'C,R,U,D', 'description': 'Manage admin and owner users (not employee)', 'resource_type': 'User'},
        {'function_code': 'F006', 'function_name': 'manage_system_config', 'url_pattern': '/api/admin/system-config', 'http_methods': 'R,U', 'description': 'Manage system configuration', 'resource_type': 'SystemConfig'},
        {'function_code': 'F007', 'function_name': 'view_all_accounting_ledgers', 'url_pattern': '/api/admin/accounting-ledgers', 'http_methods': 'R', 'description': 'View all accounting ledgers', 'resource_type': 'AccountingLedger'},
        
        # Owner Functions (F1xx)
        {'function_code': 'F101', 'function_name': 'manage_employees', 'url_pattern': '/api/owner/employees', 'http_methods': 'C,R,U,D', 'description': 'Manage employees of household', 'resource_type': 'User'},
        {'function_code': 'F102', 'function_name': 'view_own_household', 'url_pattern': '/api/owner/household', 'http_methods': 'R,U', 'description': 'View and update own household', 'resource_type': 'Household'},
        {'function_code': 'F103', 'function_name': 'manage_categories', 'url_pattern': '/api/owner/categories', 'http_methods': 'C,R,U,D', 'description': 'Manage categories', 'resource_type': 'Category'},
        {'function_code': 'F104', 'function_name': 'manage_products', 'url_pattern': '/api/owner/products', 'http_methods': 'C,R,U,D', 'description': 'Manage products', 'resource_type': 'Product'},
        {'function_code': 'F105', 'function_name': 'manage_units', 'url_pattern': '/api/owner/units', 'http_methods': 'C,R,U,D', 'description': 'Manage units', 'resource_type': 'Unit'},
        {'function_code': 'F106', 'function_name': 'manage_inventory', 'url_pattern': '/api/owner/inventory', 'http_methods': 'R,U', 'description': 'View and adjust inventory (auto-updated from import/export receipts, no manual create/delete)', 'resource_type': 'Inventory'},
        {'function_code': 'F107', 'function_name': 'manage_warehouses', 'url_pattern': '/api/owner/warehouses', 'http_methods': 'C,R,U,D', 'description': 'Manage warehouses', 'resource_type': 'Warehouse'},
        {'function_code': 'F108', 'function_name': 'manage_import_receipts', 'url_pattern': '/api/owner/import-receipts', 'http_methods': 'R,U', 'description': 'View and adjust import receipts (auto-created from invoice confirm, no manual create)', 'resource_type': 'ImportReceipt'},
        {'function_code': 'F109', 'function_name': 'manage_customers', 'url_pattern': '/api/owner/customers', 'http_methods': 'C,R,U,D', 'description': 'Manage customers', 'resource_type': 'Customer'},
        {'function_code': 'F110', 'function_name': 'manage_sellers', 'url_pattern': '/api/owner/sellers', 'http_methods': 'C,R,U,D', 'description': 'Manage sellers', 'resource_type': 'Seller'},
        {'function_code': 'F111', 'function_name': 'manage_all_invoices', 'url_pattern': '/api/owner/invoices', 'http_methods': 'C,R,U,D', 'description': 'Manage all invoices', 'resource_type': 'Invoice'},
        {'function_code': 'F112', 'function_name': 'manage_payments', 'url_pattern': '/api/owner/payments', 'http_methods': 'C,R,U,D', 'description': 'Manage payments', 'resource_type': 'Payment'},
        {'function_code': 'F113', 'function_name': 'manage_payment_methods', 'url_pattern': '/api/owner/payment-methods', 'http_methods': 'C,R,U,D', 'description': 'Manage payment methods', 'resource_type': 'PaymentMethod'},
        {'function_code': 'F114', 'function_name': 'manage_debt_records', 'url_pattern': '/api/owner/debt-records', 'http_methods': 'C,R,U,D', 'description': 'Manage debt records', 'resource_type': 'DebtRecord'},
        {'function_code': 'F115', 'function_name': 'view_household_reports', 'url_pattern': '/api/owner/reports', 'http_methods': 'R', 'description': 'View household reports', 'resource_type': 'Report'},
        {'function_code': 'F116', 'function_name': 'view_accounting_ledgers', 'url_pattern': '/api/owner/accounting-ledgers', 'http_methods': 'R', 'description': 'View accounting ledgers', 'resource_type': 'AccountingLedger'},
        {'function_code': 'F117', 'function_name': 'export_reports', 'url_pattern': '/api/owner/reports/export', 'http_methods': 'R', 'description': 'Export reports', 'resource_type': 'Report'},
        {'function_code': 'F118', 'function_name': 'manage_export_receipts', 'url_pattern': '/api/owner/export-receipts', 'http_methods': 'R,U', 'description': 'View and adjust export receipts (auto-created from invoice confirm, no manual create)', 'resource_type': 'ExportReceipt'},
        
        # Employee Functions (F2xx)
        {'function_code': 'F201', 'function_name': 'view_products', 'url_pattern': '/api/employee/products', 'http_methods': 'R', 'description': 'View products (read-only)', 'resource_type': 'Product'},
        {'function_code': 'F202', 'function_name': 'view_categories', 'url_pattern': '/api/employee/categories', 'http_methods': 'R', 'description': 'View categories (read-only)', 'resource_type': 'Category'},
        {'function_code': 'F203', 'function_name': 'view_inventory', 'url_pattern': '/api/employee/inventory', 'http_methods': 'R', 'description': 'View inventory (read-only)', 'resource_type': 'Inventory'},
        {'function_code': 'F204', 'function_name': 'view_units', 'url_pattern': '/api/employee/units', 'http_methods': 'R', 'description': 'View units (read-only)', 'resource_type': 'Unit'},
        {'function_code': 'F205', 'function_name': 'view_customers', 'url_pattern': '/api/employee/customers', 'http_methods': 'R', 'description': 'View customers (read-only)', 'resource_type': 'Customer'},
        {'function_code': 'F216', 'function_name': 'view_warehouses', 'url_pattern': '/api/employee/warehouses', 'http_methods': 'R', 'description': 'View warehouses (read-only) - Check warehouse before creating invoice', 'resource_type': 'Warehouse'},
        {'function_code': 'F206', 'function_name': 'view_customer_debt', 'url_pattern': '/api/employee/customers/*/debt', 'http_methods': 'R', 'description': 'View customer debt', 'resource_type': 'DebtRecord'},
        {'function_code': 'F207', 'function_name': 'create_sales_invoice', 'url_pattern': '/api/employee/invoices', 'http_methods': 'C', 'description': 'Create draft invoice with details (transaction)', 'resource_type': 'Invoice'},
        {'function_code': 'F208', 'function_name': 'view_invoices', 'url_pattern': '/api/employee/invoices', 'http_methods': 'R', 'description': 'View all invoices of household (filter by status to see draft orders)', 'resource_type': 'Invoice'},
        {'function_code': 'F209', 'function_name': 'update_draft_invoice', 'url_pattern': '/api/employee/invoices/*', 'http_methods': 'U', 'description': 'Update draft invoice (only when status=Draft)', 'resource_type': 'Invoice'},
        {'function_code': 'F210', 'function_name': 'confirm_invoice', 'url_pattern': '/api/employee/invoices/*/confirm', 'http_methods': 'U', 'description': 'Confirm invoice (Draft → Confirm, anyone in household can confirm)', 'resource_type': 'Invoice'},
        {'function_code': 'F211', 'function_name': 'record_payment', 'url_pattern': '/api/employee/payments', 'http_methods': 'C,R', 'description': 'Record payment', 'resource_type': 'Payment'},
        {'function_code': 'F212', 'function_name': 'record_debt', 'url_pattern': '/api/employee/debt-records', 'http_methods': 'C,R', 'description': 'Record debt', 'resource_type': 'DebtRecord'},
        {'function_code': 'F213', 'function_name': 'delete_draft_invoice', 'url_pattern': '/api/employee/invoices/*', 'http_methods': 'D', 'description': 'Delete draft invoice (only when status=Draft)', 'resource_type': 'Invoice'},
        {'function_code': 'F215', 'function_name': 'receive_notifications', 'url_pattern': '/api/employee/notifications', 'http_methods': 'R', 'description': 'Receive notifications', 'resource_type': 'Notification'},
    ]
    
    for func_data in functions_data:
        existing = session.query(Function).filter_by(function_code=func_data['function_code']).first()
        if not existing:
            func = Function(**func_data, created_at=vietnam_now(), updated_at=vietnam_now())
            session.add(func)
            print(f"  Created function: {func_data['function_code']} - {func_data['function_name']}")
        else:
            # Update function nếu đã tồn tại (để đảm bảo thông tin đúng)
            existing.function_name = func_data['function_name']
            existing.url_pattern = func_data['url_pattern']
            existing.http_methods = func_data['http_methods']
            existing.description = func_data['description']
            existing.resource_type = func_data['resource_type']
            existing.updated_at = vietnam_now()
            print(f"  Updated function: {func_data['function_code']} - {func_data['function_name']}")
    
    session.commit()
    print("Functions created/updated successfully!\n")

def seed_role_functions():
    """Map Functions to Roles"""
    print("Creating RoleFunction mappings...")
    
    # Get roles
    admin_role = session.query(Role).filter_by(role_name='Admin').first()
    owner_role = session.query(Role).filter_by(role_name='Owner').first()
    employee_role = session.query(Role).filter_by(role_name='Employee').first()
    
    if not admin_role or not owner_role or not employee_role:
        print("ERROR: Roles not found. Please run seed_roles() first.")
        return
    
    # Admin Functions - KHÔNG có F001 manage_households
    admin_functions = ['F002', 'F003', 'F004', 'F005', 'F006', 'F007']
    
    # Owner Functions
    owner_functions = ['F101', 'F102', 'F103', 'F104', 'F105', 'F106', 'F107', 'F108', 'F109', 'F110', 'F111', 'F112', 'F113', 'F114', 'F115', 'F116', 'F117', 'F118']
    
    # Employee Functions
    employee_functions = ['F201', 'F202', 'F203', 'F204', 'F205', 'F206', 'F207', 'F208', 'F209', 'F210', 'F211', 'F212', 'F213', 'F215', 'F216']
    
    # Map Admin Functions
    print("  Mapping Admin functions...")
    for func_code in admin_functions:
        func = session.query(Function).filter_by(function_code=func_code).first()
        if func:
            existing = session.query(RoleFunction).filter_by(role_id=admin_role.id, function_id=func.id).first()
            if not existing:
                role_func = RoleFunction(role_id=admin_role.id, function_id=func.id, created_at=vietnam_now())
                session.add(role_func)
                print(f"    Mapped {func_code} to Admin")
            else:
                print(f"    {func_code} already mapped to Admin")
        else:
            print(f"    WARNING: Function {func_code} not found")
    
    # Map Owner Functions
    print("  Mapping Owner functions...")
    for func_code in owner_functions:
        func = session.query(Function).filter_by(function_code=func_code).first()
        if func:
            existing = session.query(RoleFunction).filter_by(role_id=owner_role.id, function_id=func.id).first()
            if not existing:
                role_func = RoleFunction(role_id=owner_role.id, function_id=func.id, created_at=vietnam_now())
                session.add(role_func)
                print(f"    Mapped {func_code} to Owner")
            else:
                print(f"    {func_code} already mapped to Owner")
        else:
            print(f"    WARNING: Function {func_code} not found")
    
    # Map Employee Functions
    print("  Mapping Employee functions...")
    for func_code in employee_functions:
        func = session.query(Function).filter_by(function_code=func_code).first()
        if func:
            existing = session.query(RoleFunction).filter_by(role_id=employee_role.id, function_id=func.id).first()
            if not existing:
                role_func = RoleFunction(role_id=employee_role.id, function_id=func.id, created_at=vietnam_now())
                session.add(role_func)
                print(f"    Mapped {func_code} to Employee")
            else:
                print(f"    {func_code} already mapped to Employee")
        else:
            print(f"    WARNING: Function {func_code} not found")
    
    session.commit()
    print("RoleFunction mappings created successfully!\n")

def main():
    """
    Main function to seed all data
    """
    parser = argparse.ArgumentParser(description='Seed Authentication & Authorization Data')
    parser.add_argument(
        '--clean-all',
        action='store_true',
        help='Clean all Functions and RoleFunctions (default: only clean RoleFunctions and F001)'
    )
    args = parser.parse_args()
    
    print("=" * 60)
    print("SEED DATA: Authentication & Authorization")
    print("=" * 60)
    print()
    
    if args.clean_all:
        print("WARNING: --clean-all flag enabled. All Functions will be deleted and recreated.")
        print()
    
    try:
        # Bước 0: Xóa dữ liệu cũ (RoleFunction mappings, F001 function)
        # Để đảm bảo seed lại từ đầu với phân quyền mới (Admin không có F001)
        clean_old_data(clean_all_functions=args.clean_all)
        
        # Bước 1: Tạo Roles (nếu chưa có)
        seed_roles()
        
        # Bước 2: Tạo Functions (nếu chưa có, update nếu đã có)
        seed_functions()
        
        # Bước 3: Map Functions to Roles (tạo mới RoleFunction mappings)
        seed_role_functions()
        
        print("=" * 60)
        print("SEED DATA COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print()
        print("Summary:")
        print("- Roles: Admin, Owner, Employee")
        print("- Admin Functions: F002, F003 (R,U - ONLY list and deactivate), F004, F005, F006, F007 (NO F001)")
        print("- Owner Functions: F101-F118 (includes F102 manage_own_household and subscription)")
        print("- Employee Functions: F201-F216 (includes F216 view_warehouses)")
        print()
        print("IMPORTANT:")
        print("  - Admin does NOT have F001 manage_households.")
        print("  - Only Owner has F102 view_own_household (R, U) to manage household and subscription.")
        print("  - Admin F003: ONLY list all subscriptions and deactivate (NO create/update plan_id/delete).")
        print("  - F108, F118: Only R,U (view and adjust import/export receipts, auto-created from invoice confirm).")
        print("  - F106: Only R,U (view and adjust inventory, auto-updated from import/export receipts).")
        
    except Exception as e:
        session.rollback()
        print(f"ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        session.close()

if __name__ == '__main__':
    main()
