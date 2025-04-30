# Using static-pdg-js in VS Code Extensions

This guide explains how to integrate the static-pdg-js package into VS Code extensions to provide JavaScript code analysis capabilities.

## Prerequisites

1. Have a VS Code extension project set up (using Yeoman generator: `yo code`)
2. Ensure Python and Node.js are available

## Installation

### 1. Install the static-pdg-js package

Add static-pdg-js as a dependency in your extension:

```bash
cd path/to/your/extension
pip install -e path/to/static-pdg-js
```

### 2. Set Up Node.js Dependencies

Make sure the required Node.js dependencies are installed in the src directory of static-pdg-js:

```bash
cd path/to/static-pdg-js/src
npm install esprima escodegen
```

## Integration

### Option 1: Using the Python Process from JavaScript

In your VS Code extension, you can spawn a Python process that uses static-pdg-js to analyze JavaScript code:

```javascript
// extension.js
const vscode = require('vscode');
const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

// Command to visualize JavaScript code
function visualizeJavaScriptCode(context) {
  return vscode.commands.registerCommand('extension.visualizeJS', async () => {
    const editor = vscode.window.activeTextEditor;
    if (!editor) {
      vscode.window.showErrorMessage('No active editor found');
      return;
    }

    const document = editor.document;
    if (document.languageId !== 'javascript') {
      vscode.window.showErrorMessage('This is not a JavaScript file');
      return;
    }

    // Save the current file if needed
    await document.save();
    const filePath = document.uri.fsPath;
    
    // Create a temporary directory for outputs
    const outputDir = path.join(context.extensionPath, 'output');
    if (!fs.existsSync(outputDir)) {
      fs.mkdirSync(outputDir);
    }
    
    // Run Python script to analyze
    const pythonProcess = spawn('python', [
      '-c',
      `
import sys
from src.build_pdg import get_data_flow
from src.display_graph import draw_ast, draw_cfg, draw_pdg

# Analyze JavaScript file
js_file = "${filePath.replace(/\\/g, '\\\\')}"
pdg = get_data_flow(js_file, benchmarks=dict())
      
# Generate visualizations
output_prefix = "${path.join(outputDir, 'output').replace(/\\/g, '\\\\')}"
draw_ast(pdg, attributes=True, save_path=output_prefix + "_ast")
draw_cfg(pdg, attributes=True, save_path=output_prefix + "_cfg")
draw_pdg(pdg, attributes=True, save_path=output_prefix + "_pdg")
      
print("Analysis complete!")
      `
    ]);
    
    // Handle process output
    pythonProcess.stdout.on('data', (data) => {
      console.log(`Python output: ${data}`);
    });
    
    pythonProcess.stderr.on('data', (data) => {
      console.error(`Python error: ${data}`);
      vscode.window.showErrorMessage(`Error analyzing JavaScript: ${data}`);
    });
    
    pythonProcess.on('close', (code) => {
      if (code === 0) {
        vscode.window.showInformationMessage('JavaScript analysis complete!');
        
        // Open the PDG visualization
        const pdfPath = path.join(outputDir, 'output_pdg.pdf');
        vscode.commands.executeCommand('vscode.open', vscode.Uri.file(pdfPath));
      } else {
        vscode.window.showErrorMessage(`Analysis process exited with code ${code}`);
      }
    });
  });
}

// Extension activation
function activate(context) {
  context.subscriptions.push(visualizeJavaScriptCode(context));
}

module.exports = { activate };
```

### Option 2: Using a Python Server

For more complex scenarios, you can create a Python server that uses the static-pdg-js package and communicates with your VS Code extension via JSON:

```javascript
// extension.js (partial)
const net = require('net');

// Start Python server
function startPythonServer() {
  const pythonProcess = spawn('python', [
    '-c',
    `
import socket
import json
import sys
from src.build_pdg import get_data_flow
from src.display_graph import draw_ast, draw_cfg, draw_pdg

# Create server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 0))  # Use any available port
server.listen(1)
port = server.getsockname()[1]

# Print the port for the extension to connect to
print(port)
sys.stdout.flush()

# Handle connections
conn, addr = server.accept()
while True:
    data = conn.recv(4096)
    if not data:
        break
    
    # Parse request
    request = json.loads(data.decode('utf-8'))
    js_file = request.get('file')
    output_dir = request.get('output_dir')
    
    # Analyze JavaScript file
    try:
        pdg = get_data_flow(js_file, benchmarks=dict())
        
        # Generate visualizations
        draw_ast(pdg, attributes=True, save_path=output_dir + "_ast")
        draw_cfg(pdg, attributes=True, save_path=output_dir + "_cfg")
        draw_pdg(pdg, attributes=True, save_path=output_dir + "_pdg")
        
        response = {'status': 'success', 'message': 'Analysis complete'}
    except Exception as e:
        response = {'status': 'error', 'message': str(e)}
    
    # Send response
    conn.sendall(json.dumps(response).encode('utf-8'))

conn.close()
server.close()
    `
  ]);
  
  // Get the server port from stdout
  return new Promise((resolve, reject) => {
    pythonProcess.stdout.once('data', (data) => {
      const port = parseInt(data.toString().trim(), 10);
      resolve({ process: pythonProcess, port });
    });
    
    pythonProcess.stderr.on('data', (data) => {
      console.error(`Python server error: ${data}`);
      reject(new Error(`Failed to start Python server: ${data}`));
    });
  });
}

// Send request to the Python server
async function analyzeJavaScript(server, filePath, outputDir) {
  return new Promise((resolve, reject) => {
    const client = new net.Socket();
    client.connect(server.port, 'localhost', () => {
      const request = {
        file: filePath,
        output_dir: outputDir
      };
      client.write(JSON.stringify(request));
    });
    
    let responseData = '';
    client.on('data', (data) => {
      responseData += data.toString();
      client.end();
    });
    
    client.on('close', () => {
      try {
        const response = JSON.parse(responseData);
        resolve(response);
      } catch (error) {
        reject(new Error(`Invalid response: ${responseData}`));
      }
    });
    
    client.on('error', (error) => {
      reject(error);
    });
  });
}
```

## Example VS Code Extension Package.json

```json
{
  "name": "js-analyzer-extension",
  "displayName": "JavaScript Analyzer",
  "description": "Analyze JavaScript code using static-pdg-js",
  "version": "0.1.0",
  "engines": {
    "vscode": "^1.60.0"
  },
  "categories": [
    "Programming Languages",
    "Visualization"
  ],
  "activationEvents": [
    "onCommand:extension.visualizeJS"
  ],
  "main": "./extension.js",
  "contributes": {
    "commands": [
      {
        "command": "extension.visualizeJS",
        "title": "Visualize JavaScript Code (AST, CFG, PDG)"
      }
    ],
    "menus": {
      "editor/context": [
        {
          "when": "resourceLangId == javascript",
          "command": "extension.visualizeJS",
          "group": "navigation"
        }
      ]
    }
  },
  "scripts": {
    "postinstall": "cd node_modules/static-pdg-js/src && npm install esprima escodegen"
  },
  "devDependencies": {
    "@types/node": "^14.0.0",
    "@types/vscode": "^1.60.0"
  }
}
```

## Notes on VS Code Extension Development

1. When packaging your extension, ensure Python and the required dependencies are included in your documentation as prerequisites
2. Consider providing a settings option to allow users to specify the Python executable path
3. You may need to adjust file paths for cross-platform compatibility
4. Error handling is critical since you're integrating multiple systems (VS Code, Python, and Node.js)

## Advanced Features

Here are some advanced features you could implement:

1. **Live Preview**: Show a WebView preview of the PDG as the user edits their JavaScript code
2. **Issues Panel Integration**: Detect potential bugs or issues in the code using the PDG analysis
3. **Refactoring Suggestions**: Use the PDG to suggest code improvements
4. **Custom Visualization Controls**: Allow users to toggle different aspects of the PDG visualization 