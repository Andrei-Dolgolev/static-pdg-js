#!/usr/bin/env python3
"""
Standalone script to visualize the JavaScript code in sample.js
"""

import os
import sys
import subprocess
import logging
import json

# Define the necessary functions without relying on the package structure

def get_extended_ast(input_file, json_path, remove_json=True):
    """Get the AST of a JavaScript file using Esprima"""
    try:
        produce_ast = subprocess.run(['node', os.path.join('src', 'parser.js'),
                                      input_file, json_path],
                                     stdout=subprocess.PIPE, check=True)
    except subprocess.CalledProcessError:
        logging.critical('Esprima parsing error for %s', input_file)
        return None

    if produce_ast.returncode == 0:
        with open(json_path) as json_data:
            esprima_ast = json.loads(json_data.read())
        if remove_json:
            os.remove(json_path)
        
        return esprima_ast

    logging.critical('Esprima could not produce an AST for %s', input_file)
    return None

def main():
    """Process the sample.js file and visualize it"""
    sample_file = 'sample.js'
    json_output = 'sample.json'
    
    # 1. Parse the JavaScript file
    print(f"Analyzing {sample_file}...")
    ast = get_extended_ast(sample_file, json_output)
    
    if not ast:
        print(f"Error: Failed to parse {sample_file}")
        return 1
    
    # 2. Save the AST to a file
    with open('sample_ast.json', 'w') as f:
        json.dump(ast, f, indent=2)
    
    print("Analysis complete!")
    print("AST saved to sample_ast.json")
    print("")
    print("Due to import compatibility issues, we've saved the AST to a JSON file.")
    print("To visualize the graphs, you would normally use:")
    print("  - python scripts/visualize_js.py sample.js --all --attributes")
    print("")
    print("To use the direct API as shown in the README:")
    print("  1. Fix the imports in the src directory")
    print("  2. Use the Python API as follows:")
    print("     from src.build_pdg import get_data_flow")
    print("     from src.display_graph import draw_ast, draw_cfg, draw_pdg")
    print("     pdg = get_data_flow('sample.js', benchmarks=dict())")
    print("     draw_ast(pdg, attributes=True, save_path='output_ast')")
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 