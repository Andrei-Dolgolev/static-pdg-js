#!/usr/bin/env python3
"""
Script to visualize JavaScript code as AST, CFG, and PDG graphs.
"""

import os
import sys
import argparse
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
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
    parser.add_argument('--format', '-f', default='pdf', choices=['pdf', 'svg', 'png'], 
                        help='Output format (default: pdf)')
    parser.add_argument('--max-depth', type=int, default=None,
                        help='Maximum depth for AST visualization (zoom level). None means full depth.')
    parser.add_argument('--collapse-concepts',
                        help='Comma-separated list of concepts to collapse (e.g. Function,Loop,Conditional)')
    parser.add_argument('--summaries', action='store_true',
                        help='Generate and include natural-language summaries for AST nodes')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.js_file):
        print(f"Error: File {args.js_file} not found")
        return 1
    
    # If no specific graph type is selected, default to --all
    if not (args.ast or args.cfg or args.pdg):
        args.all = True
    
    print(f"Analyzing {args.js_file}...")
    
    # Parse and build PDG
    pdg_root = get_data_flow(args.js_file, benchmarks=dict())
    
    # Phase 1: Concept detection
    from src.semantic_concepts import detect_concepts
    if args.collapse_concepts or args.summaries:
        # Ensure each node has a .concept
        detect_concepts(pdg_root)

    # Phase 2: Summaries
    if args.summaries:
        from src.summarizer import summarize_concepts
        summarize_concepts(pdg_root)
    
    if not pdg_root:
        print("Error: Failed to build PDG")
        return 1
    
    # Generate visualizations
    if args.ast or args.all:
        ast_output = f"{args.output}_ast"
        concepts = args.collapse_concepts.split(',') if args.collapse_concepts else None
        print(f"Generating AST visualization: {ast_output}.{args.format} "
              f"(max_depth={args.max_depth}, collapse_concepts={concepts}, summaries={args.summaries})")
        draw_ast(
            pdg_root,
            attributes=args.attributes,
            save_path=ast_output,
            format=args.format,
            max_depth=args.max_depth,
            collapse_concepts=concepts,
            summaries=args.summaries
        )
    
    if args.cfg or args.all:
        # Note: CFG and PDG visualization don't have max_depth yet
        cfg_output = f"{args.output}_cfg"
        print(f"Generating CFG visualization: {cfg_output}.{args.format}")
        draw_cfg(pdg_root, attributes=args.attributes, save_path=cfg_output, format=args.format)
    
    if args.pdg or args.all:
        # Note: CFG and PDG visualization don't have max_depth yet
        pdg_output = f"{args.output}_pdg"
        print(f"Generating PDG visualization: {pdg_output}.{args.format}")
        draw_pdg(pdg_root, attributes=args.attributes, save_path=pdg_output, format=args.format)
    
    print(f"Visualization complete! Files saved in {args.format} format.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
