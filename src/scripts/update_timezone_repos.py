"""
Script to replace datetime.utcnow() with vietnam_now() across all repository files
"""
import os
import re

# List of repository files to update
repository_files = [
    'invoice_repository.py',
    'inventory_repository.py',
    'household_repository.py',
    'subscription_repository.py'
]

base_path = 'd:/platform-digital-transformation-household-businesses/src/infrastructure/repositories'

for filename in repository_files:
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
