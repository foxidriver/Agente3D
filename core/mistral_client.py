# mistral_client

import os
import yaml
from typing import List, Dict, Union, Tuple
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
    system_prompt = custom_prompt
    return [{"role": "system", "content": system_prompt}]

def count_tokens(text: str) -> int:
    """
    A simple approximation of token count based on character length.
    """
    return (len(text) // 4) + 2  # Approssimazione semplice

def chat(
    client: Mistral,
    messages: List[Dict[str, Union[str, List[Dict]]]],
    model: str = None  # Parametro opzionale
) -> Tuple[str, int]:
    """
    Sends messages to Mistral and returns the text response and il numero di token utilizzati.
    Uses the model specified by the user or the default from .env.
    """
    # Se il modello non è specificato, usa quello predefinito da .env
    if model is None:
        model = os.getenv("MODEL_DEFAULT")

    print(f"[DEBUG] Modello selezionato: {repr(model)}")
    print(f"[DEBUG] Tipo del modello: {type(model)}")

    try:
        response = client.chat.complete(
            model=model,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto"
        )

        # Conta i token nella richiesta e nella risposta
        input_tokens = sum(count_tokens(msg["content"]) for msg in messages if msg.get("content"))
        output_tokens = count_tokens(response.choices[0].message.content)
        total_tokens = input_tokens + output_tokens

        return response.choices[0].message.content, total_tokens

    except Exception as error:
        print(f"[DEBUG] Errore completo: {error}")
        print(f"[DEBUG] Tipo dell'errore: {type(error)}")
        return f"Error: {str(error)}", 0

    if message.tool_calls:
        tool_call = message.tool_calls[0]
        try:
            result = execute_tool(tool_call)
        except Exception as error:
            return f"Error executing tool: {str(error)}", 0

        messages.append({
            "role": "assistant",
            "content": "",
            "tool_calls": [{
                "id": tool_call.id,
                "type": "function",
                "name": tool_call.function.name,
                "arguments": tool_call.function.arguments
            }]
        })
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": result
        })

        try:
            final_response = client.chat.complete(
                model=model,
                messages=messages
            )
            final_input_tokens = sum(count_tokens(msg["content"]) for msg in messages if msg.get("content"))
            final_output_tokens = count_tokens(final_response.choices[0].message.content)
            final_total_tokens = final_input_tokens + final_output_tokens

            return final_response.choices[0].message.content, final_total_tokens
        except Exception as error:
            return f"Error in final Mistral call: {str(error)}", 0

    return message.content, 0

 
