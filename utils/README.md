# static-pdg-js Utilities

This directory contains utility scripts for the static-pdg-js package.

## Contents

- `fix_import.py` - Simple script to fix relative imports in the package
- `fix_imports_complete.py` - More comprehensive script to fix import issues
- `manual_fix.py` - Script to properly fix imports for Python packaging
- `create_notebook.py` - Script to generate a Jupyter notebook example

## Utility Scripts

### fix_import.py

A basic script that uses regular expressions to fix relative imports in Python files. Specifically targets the `from . import X as Y` pattern.

Usage:
```bash
python utils/fix_import.py
```

### fix_imports_complete.py

A more comprehensive fix script that handles various types of relative imports:
- `from . import X as Y` → `import src.X as Y`
- `from .X import Y` → `from src.X import Y`

Usage:
```bash
python utils/fix_imports_complete.py
```

### manual_fix.py

A script designed to properly fix imports in the entire project to ensure it works properly when installed and used in notebooks or extensions.

This script:
1. Fixes problematic imports with proper Python packaging syntax
2. Creates proper `__init__.py` files if needed
3. Provides guidance on how to install the package

Usage:
```bash
python utils/manual_fix.py
```

### create_notebook.py

A script that generates a Jupyter notebook example for analyzing JavaScript code with static-pdg-js.

This script:
1. Creates a well-structured notebook with explanatory markdown cells
2. Includes code cells for importing the package, analyzing JavaScript, and visualizing results
3. Demonstrates how to display PDFs directly in the notebook

Usage:
```bash
python utils/create_notebook.py
```
The notebook is saved to `examples/js_analyzer_example.ipynb`.

## When to Use These Scripts

These scripts are useful in the following scenarios:

1. **Development Setup**: When you first clone the repository and encounter import errors
2. **Packaging**: When you want to package the library for distribution
3. **Integration**: When integrating the library with Jupyter notebooks or VS Code extensions

The recommended approach is to use `manual_fix.py` as it provides the most comprehensive fix solution. 