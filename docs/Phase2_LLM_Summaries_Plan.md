# Plan: Phase 2 - LLM-Based Natural-Language Summaries

**Goal:** Enhance `src/summarizer.py` to generate meaningful natural-language summaries for AST nodes using an external LLM API, replacing the current stub implementation. These summaries will be stored in the `node.summary` attribute and displayed in visualizations when the `--summaries` flag is used.

**Architecture & Workflow:**

```mermaid
graph TD
    A[scripts/visualize_js.py] -- User runs with --summaries --> B(Call src/semantic_concepts.detect_concepts);
    B -- Adds node.concept --> C[AST Node Tree];
    A --> D(Call src/summarizer.summarize_concepts);
    D -- Calls _llm_summarize for nodes --> E{_llm_summarize(node)};
    subgraph "src/summarizer.py"
        E -- 1. Extract Code Snippet --> F[Read Original JS File (using node.filename, node.range)];
        E -- 2. Check Cache --> G[In-Memory Cache (dict)];
        E -- 3. Call LLM API (if not cached) --> H[External LLM API];
        H -- LLM Summary --> E;
        G -- Cached Summary --> E;
        E -- 4. Update Cache --> G;
        E -- Generated/Cached Summary --> I(Set node.summary);
    end
    I --> C;
    C --> J[src/display_graph.py];
    J -- Reads node.summary --> K[Render Visualization with Summaries];

    style E fill:#f9f,stroke:#333,stroke-width:2px
    style H fill:#ccf,stroke:#333,stroke-width:2px
    style G fill:#ffcc99,stroke:#333,stroke-width:1px,stroke-dasharray: 5 5
```

**Detailed Implementation Plan:**

1.  **Modify `src/summarizer.py`:**
    *   Introduce an in-memory dictionary for caching at the module level: `llm_cache = {}`.
    *   Modify `summarize_concepts(node)`:
        *   Keep the recursive traversal.
        *   For each `node`, call a new helper function `_generate_llm_summary(node)`.
        *   Assign the returned summary to `setattr(node, 'summary', summary_text)`.
    *   Implement `_generate_llm_summary(node)`:
        *   **Code Extraction:**
            *   Retrieve `filename = node.filename`. Handle cases where it might be missing.
            *   Retrieve `char_range = node.attributes.get('range')`. Handle cases where it might be missing.
            *   If `filename` and `char_range` are valid:
                *   Read the content of `filename`.
                *   Extract `code_snippet = file_content[char_range[0]:char_range[1]]`.
            *   If extraction fails, return a default message like "Could not extract code snippet."
        *   **Caching Logic:**
            *   Define `cache_key = (filename, tuple(char_range))`.
            *   If `cache_key in llm_cache`: return `llm_cache[cache_key]`.
        *   **LLM API Call:**
            *   **(Placeholder)** Define which LLM API and library to use (e.g., `openai`, `anthropic`).
            *   **(Placeholder)** Retrieve API key (e.g., from `os.environ.get("YOUR_LLM_API_KEY")`). Handle missing key error.
            *   Define the prompt (e.g., "Provide a concise, one-sentence summary of the purpose of this JavaScript code: ```javascript\n{code_snippet}\n```").
            *   Make the API call with the `code_snippet` and prompt.
            *   Include error handling (try/except) for the API call (network errors, API errors, timeouts). Return a default error message on failure.
        *   **Response Processing:**
            *   Extract the summary text from the LLM response.
            *   **(Optional)** Add basic post-processing (e.g., strip whitespace).
        *   **Cache Update:**
            *   If the API call was successful, store the result: `llm_cache[cache_key] = summary_text`.
        *   **Return:** Return `summary_text`.

2.  **Verify Prerequisites:**
    *   **Filename Availability:** Double-check `src/build_ast.py` (`ast_to_ast_nodes`) and `src/build_pdg.py` (`get_data_flow`) to ensure `node.filename` is reliably passed down or attached to the root node and accessible during traversal in `summarizer.py`.
    *   **Range Attribute:** Confirm that Esprima consistently provides the `range` attribute needed for snippet extraction.

3.  **API Key Management:**
    *   **Strategy:** Use environment variables initially (e.g., `YOUR_LLM_API_KEY`). Document this requirement.

4.  **Testing:**
    *   Test with `scripts/visualize_js.py --summaries` on `examples/sample.js`.
    *   Verify that summaries appear in the output visualization (e.g., SVG).
    *   Check caching behavior (e.g., by adding print statements or running twice).
    *   Test error handling (e.g., by providing an invalid API key or simulating network errors).