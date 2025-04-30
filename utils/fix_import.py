#!/usr/bin/env python3
"""
Fix imports in Python files to make them work as standalone applications.
This script replaces relative imports with absolute imports.
"""

import os
import re
import sys

def fix_imports(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Replace relative imports with absolute ones
    modified_content = re.sub(
        r'from \. import ([a-zA-Z_]+) as ([a-zA-Z_]+)',
        r'import src.\1 as \2',
        content
    )
    
    with open(file_path, 'w') as file:
        file.write(modified_content)
    
    print(f"Fixed imports in {file_path}")

def main():
    # Fix imports in key files
    fix_imports('src/build_pdg.py')
    fix_imports('src/build_ast.py')
    fix_imports('src/data_flow.py')
    fix_imports('src/control_flow.py')
    
    print("Import fixes complete. Now try running your script again.")

if __name__ == "__main__":
    main() 