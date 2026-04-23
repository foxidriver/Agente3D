# anthropic_client.py
import os
from typing import List, Dict, Union, Tuple
import anthropic


def create_anthropic_client() -> anthropic.Anthropic:
    """Creates and returns the Anthropic client."""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("Anthropic API key not found in environment variables.")
    return anthropic.Anthropic(api_key=api_key)


def chat(
    client: anthropic.Anthropic,
    messages: List[Dict[str, Union[str, List[Dict]]]],
    system_prompt: str,
    model: str = None
) -> Tuple[str, int]:
    """
    Sends messages to Anthropic and returns the text response and token count.
    The system prompt is passed as a separate parameter (Anthropic API requirement).
    """
    if model is None:
        model = os.getenv("MODEL_REASONING")

    print(f"[DEBUG] Anthropic model: {repr(model)}")

    try:
        response = client.messages.create(
            model=model,
            max_tokens=4096,
            system=system_prompt,
            messages=messages
        )
        input_tokens = response.usage.input_tokens
        output_tokens = response.usage.output_tokens
        total_tokens = input_tokens + output_tokens
        return response.content[0].text, total_tokens

    except Exception as error:
        print(f"[DEBUG] Anthropic error: {error}")
        return f"Error: {str(error)}", 0