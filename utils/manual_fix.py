#!/usr/bin/env python3
"""
Script to fix imports in the static-pdg-js package to ensure it works properly
when installed and used in notebooks or extensions.
"""

import os
import re
import glob

def fix_imports_in_file(filepath):
    """Fix imports in a file to be consistent with proper Python packaging."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Collect original content for comparison
    original_content = content
    
    # Fix the problematic imports
    # 1. Change "from . import X as Y" to "from src import X as Y"
    content = re.sub(r'from \. import ([a-zA-Z_]+) as ([a-zA-Z_]+)', 
                    r'from src import \1 as \2', 
                    content)
    
    # 2. Fix standalone relative imports
    content = re.sub(r'from \.(.*) import (.*)', 
                    r'from src\1 import \2', 
                    content)
    
    # Only write if changes were made
    if content != original_content:
        print(f"Fixing imports in {filepath}")
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
    else:
        print(f"No changes needed in {filepath}")

def main():
    # Process all Python files in the src directory
    src_files = glob.glob('src/**/*.py', recursive=True)
    for filepath in src_files:
        fix_imports_in_file(filepath)
    
    # Fix scripts directory
    script_files = glob.glob('scripts/**/*.py', recursive=True)
    for filepath in script_files:
        fix_imports_in_file(filepath)
        
    print("\nCreate an __init__.py file to make the package importable")
    if not os.path.exists('src/__init__.py'):
        with open('src/__init__.py', 'w', encoding='utf-8') as f:
            f.write('# Make package importable\n')
    
    print("\nImport fixes complete. Now install the package with:")
    print("pip install -e .")
    print("\nExample usage in a notebook or script:")
    print("from src.build_pdg import get_data_flow")
    print("from src.display_graph import draw_ast, draw_cfg, draw_pdg")
    print("\npdg = get_data_flow('example.js', benchmarks=dict())")
    print("draw_ast(pdg, attributes=True, save_path='output_ast')")

if __name__ == "__main__":
    main() 