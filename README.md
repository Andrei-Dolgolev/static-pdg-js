# Static PDG for JavaScript

A tool for static analysis of JavaScript code that creates Abstract Syntax Trees (AST), Control Flow Graphs (CFG), and Program Dependence Graphs (PDG).

## Repository Structure

```
static-pdg-js/
├── src/               # Core source code
├── scripts/           # CLI scripts
├── examples/          # Usage examples
│   └── output/        # Example visualizations
├── docs/              # Documentation
├── utils/             # Utility scripts
└── tests/             # Test files
```

## Features

- Parse JavaScript code using Esprima
- Build Abstract Syntax Trees (AST)
- Generate Control Flow Graphs (CFG)
- Create Program Dependence Graphs (PDG) with data flow analysis
- Visualize the different graph types as PDFs, SVGs, or PNG images
- Analyze JavaScript dependencies and variable relationships

## Installation

### Prerequisites

- Python 3.7+
- Node.js and npm
- Graphviz (for visualization)

### Setup

```bash
# Clone the repository
git clone https://github.com/your-username/static-pdg-js.git
cd static-pdg-js

# Install the package in development mode
pip install -e .

# Install Node.js dependencies
cd src
npm install esprima escodegen
```

## Quick Start

```bash
# Generate all graphs (AST, CFG, PDG) for a JavaScript file
python scripts/visualize_js.py path/to/your/file.js

# Generate specific graph types
python scripts/visualize_js.py path/to/your/file.js --ast --cfg

# Generate graphs in SVG format
python scripts/visualize_js.py path/to/your/file.js --format svg

# Generate graphs in PNG format with custom output prefix
python scripts/visualize_js.py path/to/your/file.js --format png --output my_graphs
```

## Documentation

For more detailed documentation, please refer to:

- [Package Documentation](docs/PACKAGE.md) - Comprehensive documentation of the package
- [VS Code Extension Guide](docs/VSCode_Extension_Guide.md) - Guide for integrating with VS Code
- [Example Documentation](docs/SAMPLE_README.md) - Documentation for the included examples

## Examples

Several example scripts are provided in the `examples/` directory:

- `sample.js` - A sample JavaScript file for visualization
- `package_visualize.py` - Visualize JS code using the package
- `standalone_visualize.py` - A standalone script for AST extraction

To see the results of visualizing the sample.js file, look in `examples/output/`.

## License

This project is licensed under the AGPL3 license - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

Based on research by Aurore Fass. See the original papers:
- DoubleX [paper](https://swag.cispa.saarland/papers/fass2021doublex.pdf) & [code](https://github.com/Aurore54F/DoubleX)
- HideNoSeek [paper](https://swag.cispa.saarland/papers/fass2019hidenoseek.pdf) & [code](https://github.com/Aurore54F/HideNoSeek)
- JStap [paper](https://swag.cispa.saarland/papers/fass2019jstap.pdf) & [code](https://github.com/Aurore54F/JStap)
