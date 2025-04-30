# Static PDG for JavaScript

A tool for static analysis of JavaScript code, creating Abstract Syntax Trees (AST), Control Flow Graphs (CFG), and Program Dependence Graphs (PDG).

## Features

- Parse JavaScript code using Esprima
- Build Abstract Syntax Trees (AST)
- Generate Control Flow Graphs (CFG)
- Create Program Dependence Graphs (PDG) with data flow analysis
- Visualize the different graph types as PDFs
- Analyze JavaScript dependencies and variable relationships

## Installation

### Prerequisites

- Python 3.7+
- Node.js and npm
- Graphviz (for visualization)

### Step 1: Install the Package

```bash
# Clone the repository
git clone https://github.com/your-username/static-pdg-js.git
cd static-pdg-js

# Install the package in development mode
pip install -e .
```

### Step 2: Install Node.js Dependencies

```bash
cd src
npm install esprima escodegen
```

### Step 3: Install Graphviz (for Visualization)

- **Linux:**
  ```bash
  sudo apt-get install graphviz
  ```

- **macOS:**
  ```bash
  brew install graphviz
  ```

- **Windows:**
  Download and install from [Graphviz website](https://graphviz.org/download/)

## Usage

### Command-Line Interface

The package provides a command-line tool to visualize JavaScript code:

```bash
# Generate all graphs (AST, CFG, PDG)
python scripts/visualize_js.py path/to/your/file.js

# Generate specific graph types
python scripts/visualize_js.py path/to/your/file.js --ast --cfg

# Set custom output filename prefix (default is "output")
python scripts/visualize_js.py path/to/your/file.js -o my_visualization

# Include node attributes in visualizations
python scripts/visualize_js.py path/to/your/file.js -a
```

### Python API

You can also use the package as a Python library:

```python
# Import the necessary modules
from src.build_pdg import get_data_flow
from src.display_graph import draw_ast, draw_cfg, draw_pdg

# Parse and build PDG
pdg = get_data_flow('your_file.js', benchmarks=dict())

# Generate AST visualization
draw_ast(pdg, attributes=True, save_path="output_ast")

# Generate CFG visualization
draw_cfg(pdg, attributes=True, save_path="output_cfg")

# Generate PDG visualization
draw_pdg(pdg, attributes=True, save_path="output_pdg")
```

### Batch Processing

To analyze all JavaScript files in a directory:

```python
from src.build_pdg import store_pdg_folder

# Analyze all JS files in the directory
store_pdg_folder('DIRECTORY_WITH_JS_FILES')
```

This will process all JavaScript files and store the PDGs in `DIRECTORY_WITH_JS_FILES/PDG`.

## Integration

### Jupyter Notebooks

The package can be used in Jupyter notebooks. See [js_analyzer_example.ipynb](js_analyzer_example.ipynb) for a complete example.

### VS Code Extensions

The package can be integrated into VS Code extensions. See [VSCode_Extension_Guide.md](VSCode_Extension_Guide.md) for detailed instructions.

## Advanced Usage

### Customizing the Analysis

You can customize the analysis process by modifying parameters in the `get_data_flow` function:

```python
pdg = get_data_flow(
    input_file='your_file.js', 
    benchmarks=dict(),
    beautiful_print=True,  # Print the AST beautifully
    check_var=True,        # Check for unknown variables
    save_path_ast="ast",   # Save AST visualization
    save_path_cfg="cfg",   # Save CFG visualization
    save_path_pdg="pdg"    # Save PDG visualization
)
```

### Working with the PDG

The PDG contains rich information about the code structure:

```python
# Access node information
for child in pdg.children:
    print(f"Node: {child.name}")
    print(f"Attributes: {child.attributes}")
    
    # Check control dependencies
    for ctrl_dep in child.control_dep_children:
        print(f"Control dependency: {ctrl_dep.name}")
    
    # Check data dependencies
    for data_dep in child.data_dep_children:
        print(f"Data dependency: {data_dep.name}")
```

## Troubleshooting

### Common Issues

1. **Import Errors**: If you encounter import errors, make sure you're using the package as installed with `pip install -e .`

2. **Node.js Dependency Errors**: Ensure that the Esprima and Escodegen packages are installed in the `src` directory.

3. **Graphviz Errors**: If visualization fails, check that Graphviz is properly installed and accessible from your PATH.

### Debug Mode

For more detailed output during analysis:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Then run your analysis
pdg = get_data_flow('your_file.js', benchmarks=dict())
```

## License

This project is licensed under the AGPL3 license - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

Based on research by Aurore Fass. See the original papers:
- DoubleX [paper](https://swag.cispa.saarland/papers/fass2021doublex.pdf)
- HideNoSeek [paper](https://swag.cispa.saarland/papers/fass2019hidenoseek.pdf)
- JStap [paper](https://swag.cispa.saarland/papers/fass2019jstap.pdf) 