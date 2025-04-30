# JavaScript PDG Visualization Example

This example demonstrates how to use the static-pdg-js tool to visualize JavaScript code.

## Files in this Example

- `sample.js`: A simple JavaScript file containing various control flow and data flow patterns
- `standalone_visualize.py`: A simplified script to extract the AST from the JavaScript file
- `sample_ast.json`: The output AST in JSON format

## Import Compatibility Issues

The static-pdg-js repository has some import compatibility issues when used as a standalone tool. The main issues are:

1. The repository uses relative imports (`from . import module`) which cause errors when running scripts from outside the source directory
2. The package structure expects installation with `pip install -e .`

## Sample JavaScript Code

The `sample.js` file demonstrates several JavaScript patterns:

```javascript
// A simple JavaScript sample with various constructs for visualization

function calculateTotal(items) {
    let total = 0;
    
    for (let i = 0; i < items.length; i++) {
        const item = items[i];
        if (item.price > 0) {
            total += item.price * (item.quantity || 1);
        }
    }
    
    return total;
}

// Example data
const inventory = [
    { id: 1, name: 'Widget', price: 9.99, quantity: 5 },
    { id: 2, name: 'Gadget', price: 19.99, quantity: 2 },
    { id: 3, name: 'Sample', price: 0, quantity: 10 }
];

// Calculate and output the total
const total = calculateTotal(inventory);
console.log(`Total: $${total.toFixed(2)}`);

// Conditional logic
if (total > 50) {
    console.log('Bulk discount applied!');
} else {
    console.log('Regular pricing');
}
```

## How to Use the Repository (with Fixes)

To properly use the static-pdg-js repository:

1. Install the package in development mode:
   ```
   pip install -e .
   ```

2. Install Node.js dependencies:
   ```
   cd src
   npm install esprima escodegen
   ```

3. Fix import issues before running scripts:
   - Change relative imports in source files from `from . import module` to direct imports
   - Or run scripts from within the package structure

4. Use the Python API as shown in the README:
   ```python
   from src.build_pdg import get_data_flow
   from src.display_graph import draw_ast, draw_cfg, draw_pdg
   
   pdg = get_data_flow('sample.js', benchmarks=dict())
   draw_ast(pdg, attributes=True, save_path='output_ast')
   draw_cfg(pdg, attributes=True, save_path='output_cfg')
   draw_pdg(pdg, attributes=True, save_path='output_pdg')
   ```

## Simplified AST Extraction

The `standalone_visualize.py` script demonstrates a simplified approach to extract the AST from a JavaScript file using the Esprima parser directly, without depending on the rest of the static-pdg-js codebase. 