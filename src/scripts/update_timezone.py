"""
Script to replace datetime.utcnow() with vietnam_now() across all service files
"""
import os
import re

# List of service files to update
service_files = [
    'customer_service.py',
    'seller_service.py',
    'product_service.py',
    'category_service.py',
    'unit_service.py',
    'warehouse_service.py',
    'payment_service.py',
    'payment_method_service.py',
    'debt_record_service.py',
    'invoice_detail_service.py',
    'import_receipt_service.py',
    'export_receipt_service.py',
    'function_service.py',
    'role_service.py',
    'role_function_service.py',
    'subscription_service.py',
    'subscription_plan_service.py',
    'household_service.py',
    'auth_service.py'
]

base_path = 'd:/platform-digital-transformation-household-businesses/src/services'

for filename in service_files:
    filepath = os.path.join(base_path, filename)
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        continue
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if already has import
    if 'from infrastructure.utils.datetime_utils import vietnam_now' in content:
        print(f"Already updated: {filename}")
        continue
    
    # Add import after datetime import
    if 'from datetime import' in content:
        content = re.sub(
            r'(from datetime import [^\n]+)',
            r'\1\nfrom infrastructure.utils.datetime_utils import vietnam_now',
            content,
            count=1
        )
    
    # Replace datetime.utcnow() with vietnam_now()
    content = content.replace('datetime.utcnow()', 'vietnam_now()')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Updated: {filename}")

print("\nDone!")
