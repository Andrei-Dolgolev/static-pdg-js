# Phase 1: Semantic Concept Grouping

"""
Module to detect high-level semantic concepts on AST nodes.
"""

from typing import Dict
import src.node as _node

# Concept categories for AST node types
CONCEPT_GROUPS: Dict[str, str] = {
    'FunctionDeclaration': 'Function',
    'FunctionExpression': 'Function',
    'ArrowFunctionExpression': 'Function',
    'VariableDeclaration': 'Declaration',
    'VariableDeclarator': 'Declaration',
    'IfStatement': 'Conditional',
    'SwitchStatement': 'Conditional',
    'ForStatement': 'Loop',
    'WhileStatement': 'Loop',
    'DoWhileStatement': 'Loop',
    'ReturnStatement': 'Return',
    'CallExpression': 'Call',
    'MemberExpression': 'Access',
    'BinaryExpression': 'Operation',
    'LogicalExpression': 'Operation',
    # Add more mappings as needed
}


def detect_concepts(node: _node.Node, groups: Dict[str, str] = CONCEPT_GROUPS) -> _node.Node:
    """
    Recursively traverse the AST node tree and attach a .concept attribute
    to each node, defaulting to 'Other' if the node type is unmapped.

    Parameters:
    - node: Node -- the AST node to process
    - groups: dict -- mapping from node.name to concept label

    Returns:
    - The root node with .concept attributes set on all descendants.
    """
    # Assign concept based on node type
    setattr(node, 'concept', groups.get(node.name, 'Other'))
    # Traverse children
    for child in getattr(node, 'children', []):
        detect_concepts(child, groups)
    return node 