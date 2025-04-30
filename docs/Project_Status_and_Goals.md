# Project Status & Goals Summary (Detailed)

This document details the current status, capabilities, and planned development phases for the `static-pdg-js` project, intended for both human developers and AI agents.

**1. Initial State & Core Functionality:**

*   **Input:** JavaScript source code file (`.js`).
*   **Core Libraries:**
    *   `Esprima` (via Node.js subprocess): Parses JS into an initial AST (JSON format).
    *   `Graphviz` (Python library & system tool): Renders graph structures.
*   **Base Processing Pipeline (`src/build_pdg.py`, `src/build_ast.py`, `src/control_flow.py`, `src/data_flow.py`):**
    1.  JS Source → Esprima AST (JSON).
    2.  Esprima AST → Internal `Node` object tree (representing AST).
    3.  Internal AST → Control Flow Graph (CFG) represented by augmenting `Node` objects with control flow edges (`.control_dep_children`, `.statement_dep_children`).
    4.  CFG + AST → Program Dependence Graph (PDG) by adding data flow edges (`.data_dep_children`) to `Node` objects.
*   **Initial Visualization (`src/display_graph.py`):**
    *   Functions (`produce_ast`, `produce_cfg_one_child`) to convert internal `Node` representations (AST, CFG, PDG) into `graphviz.Digraph` objects.
    *   Functions (`draw_ast`, `draw_cfg`, `draw_pdg`) to render these `Digraph` objects, initially to PDF format.
*   **Initial CLI (`scripts/visualize_js.py`):** Basic script to run the pipeline and generate default PDF visualizations.
*   **Limitations:** Raw graphs were often too dense for effective analysis of non-trivial code.

**2. Accomplishments & Current Capabilities:**

*   **Multiple Output Formats:**
    *   **Module:** `src/display_graph.py` (updated `draw_*` functions).
    *   **CLI Flag:** `--format {pdf|svg|png}`.
    *   **Capability:** Renders graphs in vector (SVG) and raster (PNG) formats besides PDF.
*   **Depth-Limited AST Zoom (Basic Simplification):**
    *   **Module:** `src/display_graph.py` (`_produce_ast_limited`, updated `draw_ast`).
    *   **CLI Flag:** `--max-depth N`.
    *   **Capability:** Truncates AST visualization below depth `N`. (Limited utility due to uniform cutoff).
*   **Phase 1 - Semantic Concept Grouping (AST Enhancement):**
    *   **Module:** `src/semantic_concepts.py`.
    *   **Key Function:** `detect_concepts(node, groups)`.
    *   **Data Structure:** Adds a `node.concept` attribute (e.g., 'Function', 'Loop', 'Conditional') to each AST `Node` based on its `node.name` (AST type) via the `CONCEPT_GROUPS` mapping.
    *   **Module:** `src/display_graph.py` (`_produce_ast_semantic`, updated `draw_ast`).
    *   **CLI Flag:** `--collapse-concepts CONCEPT1,CONCEPT2,...`.
    *   **Capability:** Allows collapsing entire subtrees in the AST visualization if the root of the subtree has a concept listed in the flag. Replaces the subtree with a `...` placeholder node. Significantly improves high-level structural clarity of the AST.
*   **Phase 2 - Stub Summaries (AST Enhancement):**
    *   **Module:** `src/summarizer.py`.
    *   **Key Function:** `summarize_concepts(node)` (currently a stub).
    *   **Data Structure:** Adds a `node.summary` attribute (string) to each AST `Node`. Currently contains basic info: `f"{node.name} ({node.concept}), children: {len(node.children)}"`.
    *   **Module:** `src/display_graph.py` (updated `_produce_ast_semantic`, updated `draw_ast`).
    *   **CLI Flag:** `--summaries`.
    *   **Capability:** Includes the `node.summary` content in the rendered Graphviz node label. Infrastructure is ready for meaningful summaries.
    *   **AI Usage:** The `node.summary` attribute is intended to hold parseable natural language descriptions of the code block represented by the node.
*   **Combined Usage:** Flags `--collapse-concepts` and `--summaries` can be used together.

**3. Current Artifacts & State:**

*   **Available Outputs (via `scripts/visualize_js.py`):**
    *   Full, detailed AST (`.pdf`, `.svg`, `.png`).
    *   Full, detailed CFG (`.pdf`, `.svg`, `.png`).
    *   Full, detailed PDG (`.pdf`, `.svg`, `.png`).
    *   Depth-limited AST (`.pdf`, `.svg`, `.png`).
    *   Semantically collapsed AST (`.pdf`, `.svg`, `.png`).
    *   AST with (currently basic) summaries (`.pdf`, `.svg`, `.png`).
    *   Semantically collapsed AST with summaries (`.pdf`, `.svg`, `.png`).
*   **Internal State:** The core `Node` object tree can be annotated with `.concept` and `.summary` attributes for the AST portion of the graph.
*   **Limitations:** Semantic grouping and summarization are currently only applied to the AST visualization, not CFG or PDG.

**4. Overall Goal & Planned Enhancements (Multi-Phase Plan):**

Transform raw graphs into rich, multi-layered, interactive, and semantically annotated representations for human and AI consumption.

*   **Phase 1: Semantic Concept Grouping (AST)**
    *   **Input:** Raw AST `Node` tree.
    *   **Process:** Traverse tree, apply `CONCEPT_GROUPS` mapping to add `node.concept` attribute.
    *   **Output:** AST `Node` tree annotated with `.concept` labels.
    *   **Status:** ✅ Implemented (`src/semantic_concepts.py`).

*   **Phase 2: Natural-Language Summaries**
    *   **Input:** AST `Node` tree (ideally with `.concept` labels).
    *   **Process:** For nodes representing significant blocks (e.g., concept='Function', 'Loop'), generate a natural language summary (using templates or LLM) and store in `node.summary`.
    *   **Output:** AST `Node` tree annotated with `.summary` strings.
    *   **Status:** ➡️ Stub implemented (`src/summarizer.py`); needs meaningful summary generation.
    *   **AI Usage:** Provide natural language context for code blocks.

*   **Phase 3: Edge Semantics & Legends**
    *   **Input:** PDG `Node` tree (with data/control flow edges).
    *   **Process:** Label data flow edges with variable names/types. Style control flow edges based on path type (e.g., default vs. error). Generate a legend explaining edge styles/labels.
    *   **Output:** Enhanced Graphviz rendering rules and legend data.
    *   **Status:** ⚪ Not Started.
    *   **AI Usage:** Provide precise data flow information and control path context.

*   **Phase 4: Interactive Drill-Down Viewer**
    *   **Input:** Graph data (potentially exported as JSON) including node hierarchy, concepts, summaries, edge info.
    *   **Process:** Render graph using a JS library (D3, Cytoscape). Implement click-to-expand/collapse for collapsed nodes. Show summaries on hover/click.
    *   **Output:** Interactive HTML/JS application or Jupyter widget.
    *   **Status:** ⚪ Not Started.

*   **Phase 5: Textual Walkthrough Generation**
    *   **Input:** Semantically annotated graph (`Node` tree with concepts, summaries).
    *   **Process:** Traverse the graph (e.g., BFS/DFS on high-level concepts). Generate Markdown text combining summaries and links/embeds of relevant graph snippets.
    *   **Output:** `WALKTHROUGH.md` file.
    *   **Status:** ⚪ Not Started.
    *   **AI Usage:** Provide a linear, narrative explanation of the code structure and logic.

*   **Phase 6: AI Indexing & Embeddings**
    *   **Input:** Annotated graph (`Node` tree with concepts, summaries, edge semantics).
    *   **Process:** Serialize key node information (concept, summary, key relationships) into a structured format (JSON). Compute sentence embeddings for summaries. Store in a vector database.
    *   **Output:** Searchable index (`code_index.json`, vector store).
    *   **Status:** ⚪ Not Started.
    *   **AI Usage:** Allow efficient retrieval of semantically relevant code context based on natural language queries or code similarity.

--- 