# Semantic & Interactive Code Visualization Plan

This document outlines a step-by-step plan to turn raw AST/CFG/PDG graphs into human- and AI-readable, multi-level, semantic visualizations. Each phase builds on the previous one and delivers concrete artifacts.

---

## 1. Objectives

- Collapse low-level syntax into **meaningful concept nodes** (functions, loops, blocks)  
- Auto-generate **natural-language summaries** for each concept  
- Label edges with precise **data/control semantics**  
- Provide **interactive drill-down** (collapse/expand) in notebooks or web UI  
- Produce a **textual walkthrough** alongside the graph  
- Expose a **CLI/API** for automated pipelines and LLM consumption  

---

## 2. High-Level Architecture

```
JavaScript Source
      ↓
   Parser (Esprima)
      ↓
 AST → CFG → PDG
      ↓
 Semantic Annotator  ──► Concept Graph + Summaries
      ↓
 Graph Renderer 
   • collapsing rules  
   • edge labels
   • node tooltips
      ↓
 Export (SVG/HTML/Markdown)
      ↓
 Interactive Viewer / LLM Index
```

---

## 3. Phase Breakdown

### Phase 1: Semantic Concept Grouping

1. **Define Concept Types**
   - We categorize AST nodes into higher-level semantic groups. Example mapping:
     ```python
     # Concept categories for AST node types
     CONCEPT_GROUPS = {
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
         # ... add more as needed
     }
     ```

2. **Implement Concept Detector**
   - Traverse the AST node tree and assign each node a `concept` attribute based on its type.
   - Nodes without a mapping default to `'Other'`.
    ```python
    from src.node import Node

    def detect_concepts(node: Node, groups: dict = CONCEPT_GROUPS):
        # Tag this node with its concept
        node.concept = groups.get(node.name, 'Other')
        # Recursively tag all children
        for child in node.children:
            detect_concepts(child, groups)

    # Usage before rendering:
    ast_root = build_ast.ast_to_ast_nodes(esprima_ast)
    detect_concepts(ast_root)
    draw_ast(ast_root, collapse_concepts=['Function', 'Loop', 'Conditional'])
    ```

3. **Integrate into Renderer**
   - In `display_graph.py`, extend `_produce_ast_semantic` to collapse based on `node.concept` rather than raw `node.name`.
   - Example change:
     ```python
     def _produce_ast_semantic(node, attributes, graph, collapse_concepts):
         # Render this node as usual
         graph.node(str(node.id), f"{node.name}\n({node.concept})")

         for child in node.children:
             # If child's concept is in collapse list, insert placeholder
             if child.concept in collapse_concepts:
                 placeholder = f"{child.id}_placeholder"
                 graph.node(placeholder, '...')
                 graph.edge(str(node.id), placeholder)
             else:
                 graph.edge(str(node.id), str(child.id))
                 _produce_ast_semantic(child, attributes, graph, collapse_concepts)
                 if attributes:
                     append_leaf_attr(child, graph)
         return graph
     ```

4. **CLI Integration**
   - Add `--collapse-concepts` flag to `visualize_js.py`:
     ```bash
     python scripts/visualize_js.py sample.js --ast \
          --collapse-concepts Function,Loop,Conditional \
          -f svg -o semantic_view
     ```

_**Deliverable:**_  
- Updated `display_graph.py` with concept-based collapsing  
- CLI example:  
  ```bash
  python scripts/visualize_js.py sample.js --ast \
       --collapse-concepts Function,Loop,Conditional \
       -f svg -o semantic_view
  ```

---

### Phase 2: Natural-Language Summaries

1. **Template Summaries for Known Patterns**  
   - E.g.  
     ```
     Function {{name}}:
       - Parameters: {{param_list}}
       - Returns: {{return_type}}
       - Contains {{loop_count}} loops and {{if_count}} branches.
     ```
2. **LLM-Assisted Summarization**  
   - For arbitrary code blocks, call an LLM with prompts like:  
     > "Summarize the body of this function in one sentence."
3. **Attach Summaries**  
   - Store summary string in `node.attributes['summary']`  
   - In Graphviz, render as a second label or tooltip  
4. **Docs & CLI**  
   - `--summarize` flag to enable LLM queries  
   - Caching of summaries to avoid repeat calls  

_**Deliverable:**_  
- Functions that generate and attach summaries  
- Graphs with visible labels/tooltips (in HTML/SVG)  

---

### Phase 3: Edge Semantics & Legends

1. **Data‐Flow Edge Labels**  
   - When linking definitions to uses, label edges with variable names (`total ← price`)  
2. **Control‐Flow Path Highlighting**  
   - Identify "default" vs. "error" path; style differently (solid vs. dashed)  
3. **Legend Generation**  
   - In Graphviz footer or an adjacent Markdown panel, include a legend:  
     ```
     • solid black = control flow  
     • green label "x" = data flow of variable x  
     • gray box "..." = collapsed body
     ```  

_**Deliverable:**_  
- Enhanced graph style rules with semantic edge labels  
- Auto-generated legend in output  

---

### Phase 4: Interactive Drill-Down Viewer

1. **HTML+JavaScript Export**  
   - Export the Graphviz output as JSON (via `dot.source` or `graphviz.pipe(format='json')`)  
2. **D3.js / cytoscape.js Frontend**  
   - Build a tiny JS app that:  
     - Renders the graph  
     - Allows clicking a collapsed node to expand in place  
     - Shows summary tooltips on hover  
3. **Notebook Widget**  
   - Wrap the JS app in a Jupyter extension or iframe  

_**Deliverable:**_  
- `viewer.html` that loads `graph.json`  
- Jupyter notebook example with interactive graph  

---

### Phase 5: Textual Walkthrough Generation

1. **Walkthrough Script**  
   - Traverse the semantic graph in BFS order  
   - For each concept node, emit a Markdown section:  
     ```markdown
     ### Function: calculateTotal
     Summaries: Loops through items…  
     Graph: ![calc AST](calc_ast.svg)
     ```
2. **Combine Graph + Text**  
   - Produce a single `WALKTHROUGH.md` file alongside exported images  

_**Deliverable:**_  
- Complete Markdown document that reads like a tutorial  

---

### Phase 6: AI Indexing & Embeddings

1. **Serialize Summaries & Edge Descriptions**  
   - Create JSON entries for each node's summary + incoming/outgoing edge labels  
2. **Compute Embeddings**  
   - Use a sentence-transformer to embed each summary  
3. **Vector Store**  
   - Save to FAISS/Chroma… allows retrieval of relevant code concepts when prompted by an LLM  

_**Deliverable:**_  
- `code_index.json` + embedding store  
- Notebook demo of LLM querying the index to retrieve context  

---

## 4. Timeline & Milestones

| Week | Tasks                                          | Deliverables                            |
|------|------------------------------------------------|-----------------------------------------|
| 1    | Concept grouping & collapse                     | Updated `display_graph.py`, CLI flags  |
| 2    | Template + LLM summaries                        | Summary generator, graph labels         |
| 3    | Edge labeling & legend                          | Enhanced graphs + legend               |
| 4    | Interactive viewer                              | `viewer.html`, notebook demo           |
| 5    | Walkthrough Markdown generator                  | `WALKTHROUGH.md`                       |
| 6    | Embedding & indexing                            | `code_index.json`, demo retrieval      |

---

## 5. Next Steps

1. Approve Phase 1 implementation (concept collapse)  
2. Wire up CLI flags and update docs  
3. Prototype a small demo on `examples/sample.js` for rapid feedback  

Let me know which phase you'd like to tackle first or if you need refinements!

## Modular Architecture

To keep our semantic‐enrichment pipeline clean, testable, and extensible, we split each major phase into its own module. The directory layout becomes:

```
static-pdg-js/
├── src/
│   ├── semantic_concepts.py      # Phase 1: Concept detection and tagging
│   ├── summarizer.py             # Phase 2: Template & LLM‐based natural‐language summaries
│   ├── edge_labeler.py           # Phase 3: Data/control edge annotation and legend generation
│   ├── graph_renderer.py         # Phase 4: Graphviz wrapper that applies collapses, labels, and tooltips
│   ├── interactive_viewer/       # Phase 4: HTML+JS drill‐down UI (D3.js or Cytoscape.js)
│   │   ├── index.html
│   │   └── viewer.js
│   ├── walkthrough.py            # Phase 5: Markdown walkthrough generator
│   └── ai_indexer.py             # Phase 6: Summary serialization, embedding, and vector store API
├── scripts/
│   └── visualize_js.py           # CLI harness: wires modules together based on flags
└── docs/
    ├── Semantic Code improvments.md  # This plan
    └── (other .md files)
```

### Module Responsibilities

- **semantic_concepts.py**  
  `detect_concepts(root_node, groups)` traverses the AST and attaches a `node.concept` label drawn from a `CONCEPT_GROUPS` map.  

- **summarizer.py**  
  - **Template‐based**: functions like `summarize_function(node)` that produce simple bullet‐point summaries.  
  - **LLM‐based**: `llm_summarize(node_body)` that calls an LLM (with caching) to generate a one‐sentence overview.  

- **edge_labeler.py**  
  - `annotate_data_edges(root_node)` that walks data‐flow edges in the PDG and labels them with variable names/types.  
  - `annotate_control_edges(root_node)` that styles default vs. error paths and generates a legend.  

- **graph_renderer.py**  
  - Exposes a unified API:  
    ```python
    render_graph(
      root_node,
      collapse_concepts: List[str]=[],
      max_depth: Optional[int]=None,
      include_attributes: bool=False,
      output_format: str='pdf',
      summaries: bool=False
    ) -> Graphviz.Digraph
    ```  
  - Internally invokes concept collapse, summarizer, edge_labeler, and then produces the final DOT graph.  

- **interactive_viewer/**  
  - A small static web app that loads `graph.json` (exported via `graph_renderer`) and provides click‐to‐expand/contract functionality, plus tooltips showing summaries.  

- **walkthrough.py**  
  - `generate_walkthrough(root_node, images_path)` emits a Markdown (`WALKTHROUGH.md`) combining text summaries and embedded graph snippets.  

- **ai_indexer.py**  
  - `index_concepts(root_node)` serializes each node's `concept` + summary + edge labels into JSON.  
  - `embed_index(json_path, model='all-MiniLM-L6-v2')` computes embeddings and stores them in a vector store (FAISS/Chroma).  

### CLI Orchestration

In `scripts/visualize_js.py`, the main function becomes a thin coordinator: parse CLI flags, call `detect_concepts`, optionally call `summarize`, `edge_labeler`, then `render_graph`, and finally trigger `walkthrough.generate_walkthrough` or `ai_indexer.embed_index` as requested.  

This modular layout allows you to develop, test, and replace each piece independently—so you can swap in a new summarization engine or add more semantic groups without touching the graph‐rendering core.
