#!/usr/bin/env python3
"""
A comprehensive script to fix import issues in static-pdg-js
"""

import os
import re
import sys
import glob

def fix_file_imports(file_path):
    print(f"Processing {file_path}...")
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Fix relative imports
    modified_content = re.sub(
        r'from \. import ([a-zA-Z_]+) as ([a-zA-Z_]+)',
        r'import src.\1 as \2',
        content
    )
    
    # Fix other types of relative imports
    modified_content = re.sub(
        r'from \.(.*) import (.*)',
        r'from src.\1 import \2',
        modified_content
    )
    
    # Fix standalone imports from the same package
    modified_content = re.sub(
        r'import ([a-zA-Z_]+) as ([a-zA-Z_]+)',
        lambda m: f'import src.{m.group(1)} as {m.group(2)}' if m.group(1) in ['node', 'extended_ast', 'scope', 'utility_df', 'control_flow', 'data_flow', 'build_ast', 'display_graph', 'pointer_analysis', 'value_filters'] else m.group(0),
        modified_content
    )
    
    if content != modified_content:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(modified_content)
        print(f"  Fixed imports in {file_path}")
    else:
        print(f"  No changes needed in {file_path}")

def main():
    # Get all Python files in src directory
    python_files = glob.glob('src/**/*.py', recursive=True)
    
    # Fix imports in each file
    for file_path in python_files:
        fix_file_imports(file_path)
    
    # Also fix specific scripts that need imports
    scripts = glob.glob('scripts/**/*.py', recursive=True)
    for script in scripts:
        fix_file_imports(script)
    
    print("\nImport fixes complete.")
    print("Now try running your visualization script again.")
    print("For example: python3 direct_visualize.py")

if __name__ == "__main__":
    main() 