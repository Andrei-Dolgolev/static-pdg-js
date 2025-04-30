#!/usr/bin/env python3
"""
Script to visualize sample.js file
"""

import os
import sys
from src.build_pdg import get_data_flow
from src.display_graph import draw_ast, draw_cfg, draw_pdg

def main():
    # Parse and build PDG
    print("Analyzing sample.js...")
    pdg = get_data_flow('sample.js', benchmarks=dict())
    
    if not pdg:
        print("Error: Failed to build PDG")
        return 1
    
    # Generate visualizations
    print("Generating AST visualization: sample_ast.pdf")
    draw_ast(pdg, attributes=True, save_path="sample_ast")
    
    print("Generating CFG visualization: sample_cfg.pdf")
    draw_cfg(pdg, attributes=True, save_path="sample_cfg")
    
    print("Generating PDG visualization: sample_pdg.pdf")
    draw_pdg(pdg, attributes=True, save_path="sample_pdg")
    
    print("Visualization complete!")
    return 0

if __name__ == "__main__":
    sys.exit(main()) 