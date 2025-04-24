import os
import json
import tempfile
from src.extended_ast import ExtendedAst
from src.display_graph import draw_ast
from src import node as _node

def test_ast_drawing():
    """Test drawing an AST from a simple JavaScript program"""
    # Create a simple JS file
    js_code = """
    function add(a, b) {
        return a + b;
    }
    console.log(add(2, 3));
    """
    
    # Use temporary directory for files
    with tempfile.TemporaryDirectory() as tmpdir:
        js_file = os.path.join(tmpdir, "temp.js")
        json_file = os.path.join(tmpdir, "temp.json")
        output_file = os.path.join(tmpdir, "ast_output")
        
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
        
        # Convert to AST nodes
        ast_nodes = _node.Node('Program')
        
        # Add function declaration node
        func_decl = _node.FunctionDeclaration('FunctionDeclaration', ast_nodes)
        ast_nodes.set_child(func_decl)
        
        # Add function name (identifier)
        func_name = _node.Identifier('Identifier', func_decl)
        func_name.set_attribute('name', 'add')
        func_decl.set_child(func_name)
        func_decl.set_fun_name(func_name)
        
        # Add parameters
        param1 = _node.Identifier('Identifier', func_decl)
        param1.set_attribute('name', 'a')
        func_decl.set_child(param1)
        func_decl.add_fun_param(param1)
        
        param2 = _node.Identifier('Identifier', func_decl)
        param2.set_attribute('name', 'b')
        func_decl.set_child(param2)
        func_decl.add_fun_param(param2)
        
        # Add function body (return statement)
        return_stmt = _node.ReturnStatement('ReturnStatement', func_decl)
        func_decl.set_child(return_stmt)
        
        # Add binary expression (a + b)
        binary_expr = _node.Node('BinaryExpression', return_stmt)
        binary_expr.set_attribute('operator', '+')
        return_stmt.set_child(binary_expr)
        
        # Add operands
        id_a = _node.Identifier('Identifier', binary_expr)
        id_a.set_attribute('name', 'a')
        binary_expr.set_child(id_a)
        
        id_b = _node.Identifier('Identifier', binary_expr)
        id_b.set_attribute('name', 'b')
        binary_expr.set_child(id_b)
        
        # Draw the AST
        draw_ast(ast_nodes, attributes=True, save_path=output_file)
        
        # Check if the output files were created
        assert os.path.exists(f"{output_file}")
        assert os.path.exists(f"{output_file}.pdf")
