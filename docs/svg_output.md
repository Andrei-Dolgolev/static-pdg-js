# SVG and Image Output Support

The graph visualization tools in `display_graph.py` now support SVG and other image format outputs.

## Usage

When calling any of the drawing functions (`draw_ast`, `draw_cfg`, `draw_pdg`), you can now specify the output format using the `format` parameter:

```python
from src.display_graph import draw_ast, draw_cfg, draw_pdg

# Generate an AST and save it as SVG
draw_ast(ast_nodes, save_path="output/my_ast", format="svg")

# Generate a CFG and save it as PNG
draw_cfg(cfg_nodes, save_path="output/my_cfg", format="png")

# Generate a PDG and save it as SVG
draw_pdg(dfg_nodes, save_path="output/my_pdg", format="svg")
```

## Supported Formats

The following formats are supported by Graphviz:

- `pdf` (default)
- `svg`
- `png`
- `jpg`
- `eps`
- Other formats supported by Graphviz

## Backward Compatibility

For backward compatibility, when generating a graph in any format other than EPS, the system will also generate an EPS version of the same graph. 