"""
Script to replace datetime.now(timezone.utc) with vietnam_now()
"""
import os
import re

# List of files to update
files_to_update = [
    'src/infrastructure/repositories/household_repository.py',
    'src/api/controllers/subscription_plan_controller.py',
    'src/api/controllers/registration_controller.py',
    'src/api/controllers/household_controller.py',
    'src/infrastructure/repositories/subscription_repository.py',
    'src/services/household_service.py',
    'src/services/subscription_service.py',
    'src/services/user_service.py'
]

base_path = 'd:/platform-digital-transformation-household-businesses'

for relative_path in files_to_update:
    filepath = os.path.join(base_path, relative_path)
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        continue
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if already has import
    if 'from infrastructure.utils.datetime_utils import vietnam_now' not in content:
        # Add import after datetime import
        if 'from datetime import' in content:
            content = re.sub(
                r'(from datetime import [^\n]+)',
                r'\1\nfrom infrastructure.utils.datetime_utils import vietnam_now',
                content,
                count=1
            )
    
    # Replace datetime.now(timezone.utc).replace(tzinfo=None) first (longer match)
    content = content.replace('datetime.now(timezone.utc).replace(tzinfo=None)', 'vietnam_now()')
    
    # Replace datetime.now(timezone.utc)
    content = content.replace('datetime.now(timezone.utc)', 'vietnam_now()')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Updated: {relative_path}")

print("\nDone!")
