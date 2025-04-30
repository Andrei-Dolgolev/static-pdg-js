# Phase 2: Natural-Language Summaries with LLM

"""
Module to generate natural-language summaries for AST nodes using an LLM API.
"""
import os
import logging
import requests
import json
from typing import Dict, Tuple, Optional, Any

import src.node as _node

# In-memory cache for LLM summaries to avoid redundant API calls
# Cache key: (filename, range_tuple), Value: summary_text
llm_cache: Dict[Tuple[str, Tuple[int, int]], str] = {}

# Default summary for when extraction or API call fails
DEFAULT_SUMMARY = "Could not generate summary"

def summarize_concepts(node: _node.Node) -> _node.Node:
    """
    Recursively annotate each node with a natural-language summary string stored in node.summary.
    Uses an LLM API to generate meaningful summaries based on the code snippet.
    
    Parameters:
    -----------
    node : _node.Node
        The AST node to summarize (and its children recursively)
    
    Returns:
    --------
    _node.Node
        The input node with .summary attributes set on it and all descendants
    """
    # Generate summary for this node
    summary = _generate_llm_summary(node)
    setattr(node, 'summary', summary)
    
    # Recurse through children
    for child in getattr(node, 'children', []):
        summarize_concepts(child)
    
    return node


def _generate_llm_summary(node: _node.Node) -> str:
    """
    Generate a natural-language summary for a single AST node using an LLM API.
    
    The function:
    1. Extracts the code snippet corresponding to the node
    2. Checks if a summary is already cached for this snippet
    3. If not cached, calls the LLM API to generate a summary
    4. Caches and returns the summary
    
    Parameters:
    -----------
    node : _node.Node
        The AST node to summarize
    
    Returns:
    --------
    str
        A natural-language summary of the node's purpose/functionality
    """
    # Get concept for context
    concept = getattr(node, 'concept', 'Other')
    
    # Extract code snippet
    code_snippet = _extract_code_snippet(node)
    if not code_snippet:
        return f"{node.name} ({concept})"
    
    # Create cache key
    filename = getattr(node, 'filename', '')
    char_range = node.attributes.get('range', (0, 0))
    cache_key = (filename, tuple(char_range))
    
    # Check cache
    if cache_key in llm_cache:
        logging.debug(f"Cache hit for {node.name} at {filename}:{char_range}")
        return llm_cache[cache_key]
    
    # Call LLM API
    summary = _call_llm_api(code_snippet, node)
    
    # Cache the result
    llm_cache[cache_key] = summary
    
    return summary


def _extract_code_snippet(node: _node.Node) -> Optional[str]:
    """
    Extract the JavaScript code snippet corresponding to the given AST node.
    
    Parameters:
    -----------
    node : _node.Node
        The AST node to extract code for
    
    Returns:
    --------
    Optional[str]
        The extracted code snippet, or None if extraction failed
    """
    try:
        # Get filename and character range
        filename = getattr(node, 'filename', None)
        if not filename:
            logging.warning(f"Node {node.name} (id: {node.id}) has no filename")
            return None
        
        char_range = node.attributes.get('range')
        if not char_range or len(char_range) != 2:
            logging.warning(f"Node {node.name} (id: {node.id}) has invalid range: {char_range}")
            return None
        
        # Read the file
        with open(filename, 'r', encoding='utf-8') as f:
            file_content = f.read()
        
        # Extract the snippet
        start, end = char_range
        if start < 0 or end > len(file_content) or start >= end:
            logging.warning(f"Invalid range {char_range} for file {filename} (length: {len(file_content)})")
            return None
        
        snippet = file_content[start:end]
        return snippet
    
    except Exception as e:
        logging.error(f"Error extracting code snippet: {e}")
        return None


def _call_llm_api(code_snippet: str, node: _node.Node) -> str:
    """
    Call an LLM API to generate a summary for the given code snippet.
    
    Parameters:
    -----------
    code_snippet : str
        The JavaScript code snippet to summarize
    node : _node.Node
        The AST node (for context)
    
    Returns:
    --------
    str
        The generated summary, or a default message if the API call failed
    """
    # Get API key from environment variable
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        logging.warning("OPENAI_API_KEY environment variable not set")
        return f"{node.name} ({getattr(node, 'concept', 'Other')})"
    
    # Prepare the prompt
    concept = getattr(node, 'concept', 'Other')
    prompt = f"""
    Provide a concise, one-sentence summary of the purpose of this JavaScript code.
    The code is a {concept} node in the AST.
    
    ```javascript
    {code_snippet}
    ```
    
    Your summary should be brief (under 100 characters) and focus on what the code does, not how it does it.
    """
    
    # Call the API
    try:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant that summarizes JavaScript code snippets."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3,
            "max_tokens": 100
        }
        
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            data=json.dumps(payload),
            timeout=10  # 10 second timeout
        )
        
        if response.status_code == 200:
            result = response.json()
            summary = result["choices"][0]["message"]["content"].strip()
            
            # Truncate if too long
            if len(summary) > 100:
                summary = summary[:97] + "..."
                
            return summary
        else:
            logging.error(f"API error: {response.status_code} - {response.text}")
            return f"{node.name} ({concept})"
            
    except Exception as e:
        logging.error(f"Error calling LLM API: {e}")
        return f"{node.name} ({concept})"