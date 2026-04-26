# core/tools.py
import json
from typing import List, Dict, Any
from core.thingiverse import search_models
 
# Definition of tools for Mistral API
TOOLS: List[Dict[str, Any]] = [
    {
        "type": "function",
        "function": {
            "name": "search_thingiverse_models",
            "description": "Search for 3D models on Thingiverse based on a search query.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search term in English to find 3D models."
                    }
                },
                "required": ["query"]
            }
        }
    }
]
 
 
def execute_tool(tool_call: Any) -> str:
    """
    Executes the tool function based on the tool call from Mistral.
    Uses json.loads instead of eval for safe argument parsing.
    """
    function_name = tool_call.function.name
    arguments = tool_call.function.arguments
 
    if function_name == "search_thingiverse_models":
        try:
            args = json.loads(arguments)
            query = args.get("query", "")
            return search_models(query)
        except Exception as error:
            return f"Error executing tool: {str(error)}"
 
    return f"Error: Unknown tool '{function_name}'."
 
