#!/usr/bin/env python3
"""
Test script for the LLM-based summarizer.
"""

import os
import sys
import logging

# Add the parent directory to the path so we can import the src modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.build_pdg import get_data_flow
from src.semantic_concepts import detect_concepts
from src.summarizer import summarize_concepts

# Configure logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(levelname)s - %(message)s')

def print_node_info(node, depth=0, max_depth=2):
    """Print information about a node and its children up to max_depth."""
    indent = "  " * depth
    
    # Get node attributes
    node_name = node.name
    node_concept = getattr(node, 'concept', 'None')
    node_summary = getattr(node, 'summary', 'None')
    
    # Print node information
    print(f"{indent}Node: {node_name} (ID: {node.id})")
    print(f"{indent}Concept: {node_concept}")
    print(f"{indent}Summary: {node_summary}")
    print(f"{indent}{'=' * 40}")
    
    # Recursively print children up to max_depth
    if depth < max_depth:
        for child in getattr(node, 'children', []):
            print_node_info(child, depth + 1, max_depth)

def main():
    """Main function to test the summarizer."""
    # Check if an API key is set
    if not os.environ.get("OPENAI_API_KEY"):
        logging.warning("OPENAI_API_KEY environment variable not set. Summaries will be basic.")
    
    # Get the sample JavaScript file
    sample_js = os.path.join(os.path.dirname(__file__), 'sample.js')
    if not os.path.exists(sample_js):
        logging.error(f"Sample file not found: {sample_js}")
        return 1
    
    logging.info(f"Analyzing {sample_js}...")
    
    # Parse and build PDG
    pdg_root = get_data_flow(sample_js, benchmarks=dict())
    if not pdg_root:
        logging.error("Failed to build PDG")
        return 1
    
    # Phase 1: Concept detection
    logging.info("Detecting concepts...")
    detect_concepts(pdg_root)
    
    # Phase 2: Generate summaries
    logging.info("Generating summaries...")
    summarize_concepts(pdg_root)
    
    # Print the results
    logging.info("Summary results:")
    print_node_info(pdg_root)
    
    logging.info("Test complete!")
    return 0

if __name__ == "__main__":
    sys.exit(main())