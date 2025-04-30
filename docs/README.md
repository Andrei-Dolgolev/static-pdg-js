# static-pdg-js Documentation

This directory contains documentation for the static-pdg-js package.

## Available Documentation

- [Package Documentation](PACKAGE.md) - Comprehensive documentation of the package
- [VS Code Extension Guide](VSCode_Extension_Guide.md) - Guide for integrating with VS Code
- [Sample Documentation](SAMPLE_README.md) - Documentation for the included examples
- [Visualization Options](visualization.md) - Information about visualization options and formats
- [SVG Output Support](svg_output.md) - Guide to using SVG and other image formats

## Using the Package

The static-pdg-js package provides tools for analyzing JavaScript code by creating Abstract Syntax Trees (AST), Control Flow Graphs (CFG), and Program Dependence Graphs (PDG).

## Visualization Formats

By default, the package generates PDF visualizations, but it also supports other formats:

- PDF - Default format, good for high-quality documents
- SVG - Vector graphics format, good for web display and interactive notebooks
- PNG - Raster graphics format, good for inclusion in documents
- Other formats supported by Graphviz

To specify a different format, use the `format` parameter in the drawing functions:

```python
from src.display_graph import draw_ast, draw_cfg, draw_pdg

# Generate AST in SVG format
draw_ast(pdg, attributes=True, save_path="output_ast", format="svg")

# Generate CFG in PNG format
draw_cfg(pdg, attributes=True, save_path="output_cfg", format="png")
```

Or when using the command-line tool:

```bash
python scripts/visualize_js.py example.js --format svg
``` 