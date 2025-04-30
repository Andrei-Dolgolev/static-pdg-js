#!/usr/bin/env python3
"""
Script to create a sample Jupyter notebook
"""

import json
import os

# Define a minimal notebook
notebook = {
    "cells": [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# JavaScript Code Analysis with static-pdg-js\n",
                "\n",
                "This notebook demonstrates how to use the static-pdg-js package to analyze JavaScript code and visualize its AST, CFG, and PDG."
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## Setup\n",
                "\n",
                "First, ensure the package is installed in development mode:"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Uncomment and run if needed\n",
                "# !pip install -e .."
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## Import Required Modules"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "import os\n",
                "import sys\n",
                "\n",
                "# Add the repository root to the path if needed\n",
                "if '..' not in sys.path:\n",
                "    sys.path.insert(0, '..')\n",
                "\n",
                "from src.build_pdg import get_data_flow\n",
                "from src.display_graph import draw_ast, draw_cfg, draw_pdg"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## Use Existing Sample JavaScript File\n",
                "\n",
                "We'll use the existing sample.js file in the examples directory:"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Path to the sample JavaScript file\n",
                "sample_file = 'sample.js'\n",
                "\n",
                "# Display the contents of the file\n",
                "with open(sample_file, 'r') as f:\n",
                "    js_code = f.read()\n",
                "    \n",
                "print(js_code)"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## Generate and Visualize the PDG\n",
                "\n",
                "Now we'll use the static-pdg-js package to analyze the JavaScript code:"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Define an output directory for visualizations\n",
                "output_dir = 'notebook_output'\n",
                "os.makedirs(output_dir, exist_ok=True)\n",
                "\n",
                "# Analyze the sample file\n",
                "print(f\"Analyzing {sample_file}...\")\n",
                "pdg = get_data_flow(sample_file, benchmarks=dict())\n",
                "\n",
                "if pdg:\n",
                "    # Generate AST visualization\n",
                "    ast_output = os.path.join(output_dir, 'sample_ast')\n",
                "    print(f\"Generating AST visualization: {ast_output}.pdf\")\n",
                "    draw_ast(pdg, attributes=True, save_path=ast_output)\n",
                "    \n",
                "    # Generate CFG visualization\n",
                "    cfg_output = os.path.join(output_dir, 'sample_cfg')\n",
                "    print(f\"Generating CFG visualization: {cfg_output}.pdf\")\n",
                "    draw_cfg(pdg, attributes=True, save_path=cfg_output)\n",
                "    \n",
                "    # Generate PDG visualization\n",
                "    pdg_output = os.path.join(output_dir, 'sample_pdg')\n",
                "    print(f\"Generating PDG visualization: {pdg_output}.pdf\")\n",
                "    draw_pdg(pdg, attributes=True, save_path=pdg_output)\n",
                "    \n",
                "    print(\"Visualization complete!\")\n",
                "else:\n",
                "    print(\"Error: Failed to build PDG\")"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## Display the Visualizations in the Notebook\n",
                "\n",
                "We can display the generated PDFs directly in the notebook:"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "from IPython.display import IFrame\n",
                "\n",
                "# Display the AST visualization\n",
                "print(\"Abstract Syntax Tree (AST):\")\n",
                "IFrame(f\"{output_dir}/sample_ast.pdf\", width=800, height=600)"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## Conclusion\n",
                "\n",
                "This notebook demonstrated how to use the static-pdg-js package to analyze JavaScript code and generate visualizations of the code structure. You can explore the AST, CFG, and PDG files to gain insights into the code's structure and dependencies."
            ]
        }
    ],
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "codemirror_mode": {
                "name": "ipython",
                "version": 3
            },
            "file_extension": ".py",
            "mimetype": "text/x-python",
            "name": "python",
            "nbconvert_exporter": "python",
            "pygments_lexer": "ipython3",
            "version": "3.10.12"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 4
}

# Save the notebook to the examples directory
output_path = os.path.join('examples', 'js_analyzer_example.ipynb')
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(notebook, f, indent=1)

print(f"Created notebook: {output_path}") 