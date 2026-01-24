"""
Script to check for indentation errors related to vietnam_now import
"""
import os

# List of directories to check
directories = [
    'src/services',
    'src/infrastructure/repositories',
    'src/api/controllers'
]

base_path = 'd:/platform-digital-transformation-household-businesses'

print("Checking for indentation errors...")

for directory in directories:
    dir_path = os.path.join(base_path, directory)
    if not os.path.exists(dir_path):
        continue
        
    for filename in os.listdir(dir_path):
        if not filename.endswith('.py'):
            continue
            
        filepath = os.path.join(dir_path, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        for i, line in enumerate(lines):
            if 'from infrastructure.utils.datetime_utils import vietnam_now' in line:
                # Check indentation of this line
                current_indent = len(line) - len(line.lstrip())
                
                # Check indentation of previous non-empty line
                prev_line_idx = i - 1
                while prev_line_idx >= 0 and not lines[prev_line_idx].strip():
                    prev_line_idx -= 1
                
                if prev_line_idx >= 0:
                    prev_line = lines[prev_line_idx]
                    prev_indent = len(prev_line) - len(prev_line.lstrip())
                    
                    # If previous line is an import and has indentation, this line should match
                    if 'import' in prev_line and prev_indent > 0 and current_indent == 0:
                        print(f"Potential error in {filepath} at line {i+1}")
                        print(f"  Prev: {prev_line.rstrip()}")
                        print(f"  Curr: {line.rstrip()}")

print("Check complete.")
