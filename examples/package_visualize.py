#!/usr/bin/env python3
"""
Script to visualize sample.js file with direct imports
"""

import os
import sys

# Add the src directory to the path
sys.path.insert(0, os.path.abspath('src'))

# Now import directly from modules without relative imports
from src.build_pdg import get_data_flow
from src.display_graph import draw_ast, draw_cfg, draw_pdg

def main():
    # Parse and build PDG
    print("Analyzing sample.js...")
    sample_file = os.path.join(os.path.dirname(__file__), 'sample.js')
    pdg = get_data_flow(sample_file, benchmarks=dict())
    
    if not pdg:
        print("Error: Failed to build PDG")
        return 1
    
    # Create output directory if it doesn't exist
    output_dir = os.path.join(os.path.dirname(__file__), 'output')
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate visualizations
    ast_output = os.path.join(output_dir, 'sample_ast')
    print(f"Generating AST visualization: {ast_output}.pdf")
    draw_ast(pdg, attributes=True, save_path=ast_output)
    
    cfg_output = os.path.join(output_dir, 'sample_cfg')
    print(f"Generating CFG visualization: {cfg_output}.pdf")
    draw_cfg(pdg, attributes=True, save_path=cfg_output)
    
    pdg_output = os.path.join(output_dir, 'sample_pdg')
    print(f"Generating PDG visualization: {pdg_output}.pdf")
    draw_pdg(pdg, attributes=True, save_path=pdg_output)
    
    print("Visualization complete!")
    return 0

if __name__ == "__main__":
    sys.exit(main()) 