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
    Cache control is enabled to reduce costs and latency on repeated calls.
    """
    if model is None:
        model = os.getenv("MODEL_REASONING")

    print(f"[DEBUG] Anthropic model: {repr(model)}")

    # System prompt with cache control enabled
    system_with_cache = [
        {
            "type": "text",
            "text": system_prompt,
            "cache_control": {"type": "ephemeral"}
        }
    ]

    try:
        response = client.messages.create(
            model=model,
            max_tokens=4096,
            system=system_with_cache,
            messages=messages
        )
        input_tokens = response.usage.input_tokens
        output_tokens = response.usage.output_tokens
        # Cache tokens are charged at reduced rate
        cache_read_tokens = getattr(response.usage, "cache_read_input_tokens", 0)
        cache_write_tokens = getattr(response.usage, "cache_creation_input_tokens", 0)
        total_tokens = input_tokens + output_tokens

        print(f"[DEBUG] Cache write tokens: {cache_write_tokens}")
        print(f"[DEBUG] Cache read tokens: {cache_read_tokens}")

        return response.content[0].text, total_tokens

    except Exception as error:
        print(f"[DEBUG] Anthropic error: {error}")
        return f"Error: {str(error)}", 0