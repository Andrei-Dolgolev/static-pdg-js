# Copyright (C) 2021 Aurore Fass
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# Additional permission under GNU GPL version 3 section 7
#
# If you modify this Program, or any covered work, by linking or combining it with
# graphviz (or a modified version of that library), containing parts covered by the
# terms of The Common Public License, the licensors of this Program grant you
# additional permission to convey the resulting work.


"""
    Display graphs (AST, CFG, PDG) using the graphviz library.
"""

import graphviz

import src.node as _node


def append_leaf_attr(node, graph):
    """
        Append the leaf's attribute to the graph in graphviz format.

        -------
        Parameters:
        - node: Node
            Node.
        - graph: Digraph/Graph
            Graph object. Be careful it is mutable.
    """

    if node.is_leaf():
        leaf_id = str(node.id) + 'leaf_'
        graph.attr('node', style='filled', color='lightgoldenrodyellow',
                   fillcolor='lightgoldenrodyellow')
        graph.attr('edge', color='orange')
        got_attr, node_attributes = node.get_node_attributes()
        if got_attr:  # Got attributes
            leaf_attr = str(node_attributes)
            graph.node(leaf_id, leaf_attr)
            graph.edge(str(node.id), leaf_id)


def produce_ast(ast_nodes, attributes, graph=graphviz.Graph(comment='AST representation')):
    """
        Produce an AST in graphviz format.

        -------
        Parameters:
        - ast_nodes: Node
            Output of ast_to_ast_nodes(<ast>, ast_nodes=Node('Program')).
        - graph: Graph
            Graph object. Be careful it is mutable.
        - attributes: bool
            Whether to display the leaf attributes or not.

        -------
        Returns:
        - graph
            graphviz formatted graph.
    """

    graph.attr('node', color='black', style='filled', fillcolor='white')
    graph.attr('edge', color='black')
    graph.node(str(ast_nodes.id), ast_nodes.name)
    for child in ast_nodes.children:
        graph.attr('node', color='black', style='filled', fillcolor='white')
        graph.attr('edge', color='black')
        graph.edge(str(ast_nodes.id), str(child.id))
        produce_ast(child, attributes, graph)
        if attributes:
            append_leaf_attr(child, graph)
    return graph


def _produce_ast_limited(ast_nodes, attributes, max_depth, current_depth, graph):
    """Internal helper to produce AST limited to a certain depth."""
    graph.attr('node', color='black', style='filled', fillcolor='white')
    graph.node(str(ast_nodes.id), ast_nodes.name)

    # Stop recursion if we've reached the maximum depth
    if max_depth is not None and current_depth >= max_depth:
        if attributes and ast_nodes.children:
            # Indicate collapsed subtree
            collapse_id = f"{ast_nodes.id}_collapsed"
            graph.attr('node', shape='ellipse', style='filled', color='gray', fillcolor='lightgray')
            graph.node(collapse_id, '...')
            graph.edge(str(ast_nodes.id), collapse_id)
        return graph

    # Recurse into children
    for child in ast_nodes.children:
        graph.edge(str(ast_nodes.id), str(child.id))
        _produce_ast_limited(child, attributes, max_depth, current_depth + 1, graph)
        if attributes:
            append_leaf_attr(child, graph)
    return graph


def _produce_ast_semantic(node, attributes, graph, collapse_concepts, include_summaries=False):
    """Produce AST with semantic node collapse and optional summaries."""
    graph.attr('node', color='black', style='filled', fillcolor='white')
    # Build label with name, concept, and optional summary
    concept = getattr(node, 'concept', None)
    parts = [node.name + (f" ({concept})" if concept else "")]
    if include_summaries:
        summary = getattr(node, 'summary', None)
        if summary:
            parts.append(summary)
    label = "\n".join(parts)
    graph.node(str(node.id), label)

    for child in getattr(node, 'children', []):
        # If child's concept is in the collapse list, replace subtree with placeholder
        child_concept = getattr(child, 'concept', None)
        if collapse_concepts and child_concept in collapse_concepts:
            placeholder_id = f"{child.id}_placeholder"
            graph.attr('node', shape='ellipse', style='filled', fillcolor='lightgray', color='gray')
            graph.node(placeholder_id, '...')
            graph.edge(str(node.id), placeholder_id)
            continue

        graph.attr('node', color='black', style='filled', fillcolor='white')
        graph.attr('edge', color='black')
        graph.edge(str(node.id), str(child.id))
        _produce_ast_semantic(child, attributes, graph, collapse_concepts, include_summaries)
        if attributes:
            append_leaf_attr(child, graph)
    return graph


# Backward-compatible wrapper with new zoom capability

def draw_ast(ast_nodes, attributes=False, save_path=None, format='pdf', max_depth=None, collapse_concepts=None, summaries=False):
    """
    Plot an AST with optional zoom-level (depth limitation).

    Parameters
    ----------
    ast_nodes : Node
        Output of ast_to_ast_nodes(<ast>, ast_nodes=Node('Program')).
    attributes : bool, optional
        Whether to display the leaf attributes or not, by default False.
    save_path : str, optional
        File path prefix for the rendered output. If None, will open a viewer window.
    format : str, optional
        Output format passed to Graphviz (pdf, svg, png, ...). Default 'pdf'.
    max_depth : int, optional
        Maximum depth to traverse. None means full depth (no zoom).
    collapse_concepts : list, optional
        List of concepts to collapse.
    summaries : bool, optional
        Whether to include summaries in the AST.
    """

    # Semantic collapse by concept + optional summaries
    if collapse_concepts:
        dot = graphviz.Graph(comment='AST (semantic collapse)')
        _produce_ast_semantic(ast_nodes, attributes, dot, collapse_concepts, include_summaries=summaries)
    elif max_depth is not None:
        dot = graphviz.Graph(comment='AST (zoomed)')
        _produce_ast_limited(ast_nodes, attributes, max_depth, 0, dot)
    else:
        # Full AST, optionally include summaries
        if summaries:
            # reuse semantic printer without collapse
            dot = graphviz.Graph(comment='AST (with summaries)')
            _produce_ast_semantic(ast_nodes, attributes, dot, collapse_concepts=[], include_summaries=True)
        else:
            dot = produce_ast(ast_nodes, attributes)

    if save_path is None:
        dot.view()
    else:
        dot.render(save_path, view=False, format=format)
        if format != 'eps':
            dot.render(save_path, view=False, format='eps')
    dot.clear()


def cfg_type_node(child):
    """ Different form according to statement node or not. """

    if isinstance(child, _node.Statement) or child.is_comment():
        return ['box', 'red', 'lightpink']
    return ['ellipse', 'blue', 'lightblue2']


def produce_cfg_one_child(child, data_flow, attributes,
                          graph=graphviz.Digraph(comment='Control flow representation')):
    """
        Produce a CFG in graphviz format.

        -------
        Parameters:
        - child: Node
            Node to begin with.
        - data_flow: bool
            Whether to display the data flow or not. Default: False.
        - attributes: bool
            Whether to display the leaf attributes or not.
        - graph: Digraph
            Graph object. Be careful it is mutable.

        -------
        Returns:
        - graph
            graphviz formatted graph.
    """

    type_node = cfg_type_node(child)
    graph.attr('node', shape=type_node[0], style='filled', color=type_node[2],
               fillcolor=type_node[2])
    graph.attr('edge', color=type_node[1])
    graph.node(str(child.id), child.name)

    for child_statement_dep in child.statement_dep_children:
        child_statement = child_statement_dep.extremity
        type_node = cfg_type_node(child_statement)
        graph.attr('node', shape=type_node[0], color=type_node[2], fillcolor=type_node[2])
        graph.attr('edge', color=type_node[1])
        graph.edge(str(child.id), str(child_statement.id), label=child_statement_dep.label)
        produce_cfg_one_child(child_statement, data_flow=data_flow, attributes=attributes,
                              graph=graph)
        if attributes:
            append_leaf_attr(child_statement, graph)

    if isinstance(child, _node.Statement):
        for child_cf_dep in child.control_dep_children:
            child_cf = child_cf_dep.extremity
            type_node = cfg_type_node(child_cf)
            graph.attr('node', shape=type_node[0], color=type_node[2], fillcolor=type_node[2])
            graph.attr('edge', color=type_node[1])
            graph.edge(str(child.id), str(child_cf.id), label=str(child_cf_dep.label))
            produce_cfg_one_child(child_cf, data_flow=data_flow, attributes=attributes, graph=graph)
            if attributes:
                append_leaf_attr(child_cf, graph)

    if data_flow:
        graph.attr('edge', color='green')
        if isinstance(child, _node.Identifier):
            for child_data_dep in child.data_dep_children:
                child_data = child_data_dep.extremity
                type_node = cfg_type_node(child)
                graph.attr('node', shape=type_node[0], color=type_node[2], fillcolor=type_node[2])
                graph.edge(str(child.id), str(child_data.id), label=child_data_dep.label)
                # No call to the func as already recursive for data/statmt dep on the same nodes
                # logging.info("Data dependency on the variable " + child_data.attributes['name'])
        graph.attr('edge', color='seagreen')
        if hasattr(child, 'fun_param_parents'):  # Function parameters flow
            for child_param in child.fun_param_parents:
                type_node = cfg_type_node(child)
                graph.attr('node', shape=type_node[0], color=type_node[2], fillcolor=type_node[2])
                graph.edge(str(child.id), str(child_param.id), label='param')

    return graph


def draw_cfg(cfg_nodes, attributes=False, save_path=None, format='pdf'):
    """
        Plot a CFG.

        -------
        Parameters:
        - cfg_nodes: Node
            Output of produce_cfg(ast_to_ast_nodes(<ast>, ast_nodes=Node('Program'))).
        - save_path: str
            Path of the file to store the CFG in.
        - attributes: bool
            Whether to display the leaf attributes or not. Default: False.
        - format: str
            Format to save the graph in ('pdf', 'svg', 'png', etc). Default: 'pdf'.
    """

    dot = graphviz.Digraph()
    for child in cfg_nodes.children:
        dot = produce_cfg_one_child(child=child, data_flow=False, attributes=attributes)
    if save_path is None:
        dot.view()
    else:
        dot.render(save_path, view=False, format=format)
        # For backward compatibility, also render to EPS
        if format != 'eps':
            graphviz.render(filepath=save_path, engine='dot', format='eps')
    dot.clear()


def draw_pdg(dfg_nodes, attributes=False, save_path=None, format='pdf'):
    """
        Plot a PDG.

        -------
        Parameters:
        - dfg_nodes: Node
            Output of produce_dfg(produce_cfg(ast_to_ast_nodes(<ast>, ast_nodes=Node('Program')))).
        - save_path: str
            Path of the file to store the PDG in.
        - attributes: bool
            Whether to display the leaf attributes or not. Default: False.
        - format: str
            Format to save the graph in ('pdf', 'svg', 'png', etc). Default: 'pdf'.
    """

    dot = graphviz.Digraph()
    for child in dfg_nodes.children:
        dot = produce_cfg_one_child(child=child, data_flow=True, attributes=attributes)
    if save_path is None:
        dot.view()
    else:
        dot.render(save_path, view=False, format=format)
        # For backward compatibility, also render to EPS
        if format != 'eps':
            graphviz.render(filepath=save_path, engine='dot', format='eps')
    dot.clear()
