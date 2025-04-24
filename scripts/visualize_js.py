#!/usr/bin/env python3
"""
Script to visualize JavaScript code as AST, CFG, and PDG graphs.
"""

import os
import sys
import argparse
from src.build_pdg import get_data_flow
from src.display_graph import draw_ast, draw_cfg, draw_pdg

def main():
    parser = argparse.ArgumentParser(description='Visualize JavaScript code as AST, CFG, and PDG graphs')
    parser.add_argument('js_file', help='JavaScript file to analyze')
    parser.add_argument('--output', '-o', default='output', help='Output file prefix (default: output)')
    parser.add_argument('--ast', action='store_true', help='Generate AST visualization')
    parser.add_argument('--cfg', action='store_true', help='Generate CFG visualization')
    parser.add_argument('--pdg', action='store_true', help='Generate PDG visualization')
    parser.add_argument('--all', action='store_true', help='Generate all visualizations')
    parser.add_argument('--attributes', '-a', action='store_true', help='Include node attributes in visualizations')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.js_file):
        print(f"Error: File {args.js_file} not found")
        return 1
    
    # If no specific graph type is selected, default to --all
    if not (args.ast or args.cfg or args.pdg):
        args.all = True
    
    print(f"Analyzing {args.js_file}...")
    
    # Parse and build PDG
    pdg = get_data_flow(args.js_file, benchmarks=dict())
    
    if not pdg:
        print("Error: Failed to build PDG")
        return 1
    
    # Generate visualizations
    if args.ast or args.all:
        ast_output = f"{args.output}_ast"
        print(f"Generating AST visualization: {ast_output}.pdf")
        draw_ast(pdg, attributes=args.attributes, save_path=ast_output)
    
    if args.cfg or args.all:
        cfg_output = f"{args.output}_cfg"
        print(f"Generating CFG visualization: {cfg_output}.pdf")
        draw_cfg(pdg, attributes=args.attributes, save_path=cfg_output)
    
    if args.pdg or args.all:
        pdg_output = f"{args.output}_pdg"
        print(f"Generating PDG visualization: {pdg_output}.pdf")
        draw_pdg(pdg, attributes=args.attributes, save_path=pdg_output)
    
    print("Visualization complete!")
    return 0

if __name__ == "__main__":
    sys.exit(main())
