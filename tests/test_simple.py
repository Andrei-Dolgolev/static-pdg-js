import os
import json
import tempfile
from src.extended_ast import ExtendedAst

def test_simple_js_parsing():
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
    ast.ast = ast_json
    
    # Basic assertions
    assert ast.get_type() == "Program"
    assert ast.get_source_type() == "module"
    
    # Temporary files will be cleaned up automatically when the context manager exits
