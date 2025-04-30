# static-pdg-js Examples

This directory contains example scripts and files demonstrating how to use the static-pdg-js package.

## Contents

- `sample.js` - A sample JavaScript file with various control flow and data flow patterns
- `output/` - Directory containing visualization outputs (AST, CFG, PDG) for the sample.js file
- `package_visualize.py` - Script demonstrating how to use the package API to visualize JavaScript
- `direct_visualize.py` - Script with direct imports of the package modules
- `standalone_visualize.py` - Simplified script for AST extraction without complex dependencies
- `sample_visualize.py` - Similar to package_visualize.py but with simpler imports
- `js_analyzer_example.ipynb` - Jupyter notebook demonstrating analysis in notebook environment

## Running the Examples

### Using the Package API

```bash
# Using the package API
python package_visualize.py
```

This will analyze `sample.js` and generate three visualizations:
- `output/sample_ast.pdf` - Abstract Syntax Tree
- `output/sample_cfg.pdf` - Control Flow Graph
- `output/sample_pdg.pdf` - Program Dependence Graph

### Using Standalone Extraction

```bash
# Using the standalone extractor
python standalone_visualize.py
```

This simpler script uses only the Esprima parser through the Node.js bridge, without relying on the full package. It creates `sample_ast.json` with the raw AST.

## Visualization Files

The `output/` directory contains several types of files:
- `.pdf` files - Visualizations viewable in any PDF viewer
- `.eps` files - Encapsulated PostScript files for high-quality vector graphics
- `.json` files - Raw AST data in JSON format
- Files without extensions - Graphviz DOT files used to generate the visualizations

## Jupyter Notebook

The `js_analyzer_example.ipynb` notebook demonstrates how to use the package in a Jupyter environment. It includes:
- Creating a sample JavaScript file
- Analyzing the file with static-pdg-js
- Visualizing the resulting graphs
- Displaying the visualization directly in the notebook 