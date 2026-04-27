# core/mistral_client.py
import os
from typing import List, Dict, Union, Tuple, Any
from mistralai.client import Mistral
from core.tools import TOOLS, execute_tool

def create_client() -> Mistral:
    """Creates and returns the Mistral client."""
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        raise ValueError("Mistral API key not found in environment variables.")
    return Mistral(api_key=api_key)

def initial_messages(custom_prompt: str = None) -> List[Dict[str, str]]:
    """Returns the initial list of messages with the system prompt."""
    return [{"role": "system", "content": custom_prompt}]

def count_tokens(text: str) -> int:
    """Simple approximation of token count based on character length."""
    return (len(text) // 4) + 2

def chat(
    client: Mistral,
    messages: List[Dict[str, Any]],
    model: str = None
) -> Tuple[str, int]:
    """
    Sends messages to Mistral and returns the text response and token count.
    Converts SDK objects to dicts for Streamlit compatibility.
    """
    if model is None:
        model = os.getenv("MODEL_DEFAULT")
    
    try:
        # First call to check if tools are needed
        response = client.chat.complete(
            model=model,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto"
        )
    except Exception as error:
        print(f"[DEBUG] Mistral error: {error}")
        return f"Error: {str(error)}", 0

    message_obj = response.choices[0].message
    
    # Handle tool call if requested by the model
    if message_obj.tool_calls:
        # Convert SDK message object to a serializable dict for Streamlit/History
        # We include the tool_calls in the dict format Mistral expects
        tool_calls_list = [
            {
                "id": tc.id,
                "type": "function",
                "function": {
                    "name": tc.function.name,
                    "arguments": tc.function.arguments
                }
            } for tc in message_obj.tool_calls
        ]
        
        messages.append({
            "role": "assistant",
            "content": message_obj.content or "",
            "tool_calls": tool_calls_list
        })
        
        # Execute each tool
        for tool_call in message_obj.tool_calls:
            try:
                result = execute_tool(tool_call)
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": tool_call.function.name,
                    "content": str(result)
                })
            except Exception as error:
                return f"Error executing tool: {str(error)}", 0
        
        # Final call
        try:
            final_response = client.chat.complete(
                model=model,
                messages=messages
            )
            final_content = final_response.choices[0].message.content
            return final_content, count_tokens(str(messages)) + count_tokens(final_content)
            
        except Exception as error:
            return f"Error in final Mistral call: {str(error)}", 0

    # Standard response: convert to dict for Streamlit safety
    content = message_obj.content
    return content, count_tokens(str(messages)) + count_tokens(content)