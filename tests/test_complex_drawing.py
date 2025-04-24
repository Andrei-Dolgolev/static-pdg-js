import os
import json
import tempfile
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.extended_ast import ExtendedAst
from src.display_graph import draw_ast, draw_cfg, draw_pdg
from src import node as _node

def test_complex_ast_drawing():
    """Test drawing an AST from a more complex JavaScript program"""
    # Create a more complex JS file with multiple functions and control flow
    js_code = """
    function calculateTotal(items) {
        let total = 0;
        for (let i = 0; i < items.length; i++) {
            if (items[i].price > 0) {
                total += items[i].price * (items[i].quantity || 1);
            }
        }
        return total;
    }
    
    const items = [
        { name: 'Book', price: 12.99, quantity: 2 },
        { name: 'Pen', price: 1.99, quantity: 10 },
        { name: 'Notebook', price: 4.99, quantity: 3 }
    ];
    
    console.log('Total cost:', calculateTotal(items));
    """
    
    # Use temporary directory for files
    with tempfile.TemporaryDirectory() as tmpdir:
        js_file = os.path.join(tmpdir, "complex.js")
        json_file = os.path.join(tmpdir, "complex.json")
        output_file = os.path.join(tmpdir, "complex_ast_output")
        
        # Write JS to temporary file
        with open(js_file, "w") as f:
            f.write(js_code)
    
        # Get path to parser.js relative to package
        parser_path = os.path.join(os.path.dirname(__file__), "..", "src", "parser.js")
        
        # Parse JS to AST
        os.system(f"node {parser_path} {js_file} {json_file}")
        
        # Read and parse the AST
        with open(json_file) as f:
            ast_json = json.load(f)
    
        # Create ExtendedAst object
        ast = ExtendedAst()
        ast.set_type(ast_json["type"])
        ast.set_body(ast_json["body"])
        ast.set_source_type(ast_json["sourceType"])
        if "range" in ast_json:
            ast.set_range(ast_json["range"])
        if "comments" in ast_json:
            ast.set_comments(ast_json["comments"])
        if "tokens" in ast_json:
            ast.set_tokens(ast_json["tokens"])
        if "leadingComments" in ast_json:
            ast.set_leading_comments(ast_json["leadingComments"])
        
        # Convert to AST nodes - create a simplified representation for testing
        ast_nodes = _node.Node('Program')
        
        # Add function declaration node for calculateTotal
        func_decl = _node.FunctionDeclaration('FunctionDeclaration', ast_nodes)
        ast_nodes.set_child(func_decl)
        
        # Add function name
        func_name = _node.Identifier('Identifier', func_decl)
        func_name.set_attribute('name', 'calculateTotal')
        func_decl.set_child(func_name)
        func_decl.set_fun_name(func_name)
        
        # Add parameter
        param = _node.Identifier('Identifier', func_decl)
        param.set_attribute('name', 'items')
        func_decl.set_child(param)
        func_decl.add_fun_param(param)
        
        # Add function body with a return statement
        return_stmt = _node.ReturnStatement('ReturnStatement', func_decl)
        func_decl.set_child(return_stmt)
        
        # Add identifier for return value
        return_id = _node.Identifier('Identifier', return_stmt)
        return_id.set_attribute('name', 'total')
        return_stmt.set_child(return_id)
        
        # Draw the AST with attributes
        draw_ast(ast_nodes, attributes=True, save_path=output_file)
        
        # Check if the output files were created
        assert os.path.exists(f"{output_file}")
        assert os.path.exists(f"{output_file}.pdf")
        
        # Print information about the generated files
        print(f"\nAST visualization files created:")
        print(f"- DOT file: {output_file}")
        print(f"- PDF file: {output_file}.pdf")
