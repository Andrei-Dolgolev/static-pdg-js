# Visualization Options

## Overview

The static-pdg-js tool provides capabilities to visualize JavaScript code as different types of graphs:

- Abstract Syntax Tree (AST)
- Control Flow Graph (CFG)
- Program Dependence Graph (PDG)

## Using the Visualization Script

The `visualize_js.py` script in the `scripts` directory can be used to generate these visualizations:

```bash
python scripts/visualize_js.py path/to/your/file.js [options]
```

### Command Line Options

| Option | Description |
|--------|-------------|
| `--output`, `-o` | Output file prefix (default: "output") |
| `--ast` | Generate AST visualization |
| `--cfg` | Generate CFG visualization |
| `--pdg` | Generate PDG visualization |
| `--all` | Generate all visualizations (default if no graph type is specified) |
| `--attributes`, `-a` | Include node attributes in visualizations |
| `--format`, `-f` | Output format: pdf, svg, or png (default: pdf) |
| `--max-depth` | Maximum depth for AST visualization (zoom level, default: full) |
| `--collapse-concepts` | Comma-separated list of concepts to collapse (e.g., Function,Loop,Conditional) |
| `--summaries` | Generate and include natural-language summaries for AST nodes |

## Semantic Enhancements

The tool supports two types of semantic enhancements for AST visualizations:

### Concept Grouping

The `--collapse-concepts` option allows you to collapse specific types of AST nodes based on their semantic concept. This helps simplify complex ASTs by hiding implementation details.

Example:
```bash
python scripts/visualize_js.py example.js --ast --collapse-concepts Function,Loop,Conditional
```

This will collapse all Function, Loop, and Conditional nodes in the AST visualization, replacing their subtrees with placeholder nodes.

### LLM-Based Summaries

The `--summaries` option enables natural-language summaries for AST nodes. These summaries are generated using an LLM (Large Language Model) API and provide concise descriptions of what each code block does.

#### Setting Up the LLM API

To use the LLM-based summarizer, you need to set up an OpenAI API key:

1. Obtain an API key from [OpenAI](https://platform.openai.com/)
2. Set the API key as an environment variable:

```bash
# For Linux/macOS
export OPENAI_API_KEY="your-api-key-here"

# For Windows (Command Prompt)
set OPENAI_API_KEY=your-api-key-here

# For Windows (PowerShell)
$env:OPENAI_API_KEY="your-api-key-here"
```

Example usage:
```bash
python scripts/visualize_js.py example.js --ast --summaries --format svg
```

This will generate an AST visualization with natural-language summaries for each node, making the code structure easier to understand.

## Examples

Generate all visualizations in PDF format:
```bash
python scripts/visualize_js.py example.js --all
```

Generate only the PDG in SVG format:
```bash
python scripts/visualize_js.py example.js --pdg --format svg
```

Generate AST with node attributes in PNG format:
```bash
python scripts/visualize_js.py example.js --ast --attributes --format png --output my_ast
```

Generate AST with collapsed concepts and summaries:
```bash
python scripts/visualize_js.py example.js --ast --collapse-concepts Function,Loop --summaries --format svg
```

## Output Files

The script will generate files with the following naming convention:
- `{output_prefix}_ast.{format}` - For AST visualization
- `{output_prefix}_cfg.{format}` - For CFG visualization
- `{output_prefix}_pdg.{format}` - For PDG visualization

Where `{output_prefix}` is the value provided to the `--output` option (default: "output") and `{format}` is the chosen output format (pdf, svg, or png).