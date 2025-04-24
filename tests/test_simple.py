import os
import json
from src import ExtendedAst

def test_simple_js_parsing():
    # Create a simple JS file
    js_code = """
    function add(a, b) {
        return a + b;
    }
    console.log(add(2, 3));
    """
    
    # Write JS to temporary file
    with open("temp.js", "w") as f:
        f.write(js_code)
    
    # Get path to parser.js relative to package
    parser_path = os.path.join(os.path.dirname(__file__), "..", "src", "parser.js")
    
    # Parse JS to AST
    os.system(f"node {parser_path} temp.js temp.json")
    
    # Read and parse the AST
    with open("temp.json") as f:
        ast_json = json.load(f)
    
    # Create ExtendedAst object
    ast = ExtendedAst()
    ast.ast = ast_json
    
    # Basic assertions
    assert ast.get_type() == "Program"
    assert ast.get_source_type() == "module"
    
    # Cleanup
    os.remove("temp.js")
    os.remove("temp.json")
