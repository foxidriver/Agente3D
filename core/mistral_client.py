import os
import yaml
from typing import List, Dict, Union
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

def chat(
    client: Mistral,
    messages: List[Dict[str, Union[str, List[Dict]]]],
    model: str = None  # Parametro opzionale
) -> str:
    """
    Sends messages to Mistral and returns the text response.
    Uses the model specified by the user or the default from .env.
    """
    # Se il modello non è specificato, usa quello predefinito da .env
    if model is None:
        model = os.getenv("MISTRAL_MODEL_DEFAULT")  # Nessun valore hardcoded!

    print(f"[DEBUG] Modello selezionato: {repr(model)}")  # Stampa il modello con repr() per vedere eventuali apici
    print(f"[DEBUG] Tipo del modello: {type(model)}")    # Stampa il tipo (dovrebbe essere str)

    try:
        response = client.chat.complete(
            model=model,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto"
        )
        return response.choices[0].message.content
    except Exception as error:
        print(f"[DEBUG] Errore completo: {error}")  # Stampa l'errore completo
        print(f"[DEBUG] Tipo dell'errore: {type(error)}")  # Stampa il tipo dell'errore
        return f"Error: {str(error)}"

    if message.tool_calls:
        tool_call = message.tool_calls[0]
        try:
            result = execute_tool(tool_call)
        except Exception as error:
            return f"Error executing tool: {str(error)}"

        messages.append({
            "role": "assistant",
            "content": "",
            "tool_calls": [{
                "id": tool_call.id,
                "type": "function",
                "function": {
                    "name": tool_call.function.name,
                    "arguments": tool_call.function.arguments
                }
            }]
        })
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": result
        })

        try:
            final_response = client.chat.complete(
                model=model,  # Usa lo stesso modello per la risposta finale
                messages=messages
            )
            return final_response.choices[0].message.content
        except Exception as error:
            return f"Error in final Mistral call: {str(error)}"

    return message.content