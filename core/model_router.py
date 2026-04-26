# core/model_router.py
from typing import Tuple
from core.mistral_client import chat as mistral_chat
from core.anthropic_client import chat as anthropic_chat
from core.error_handler import handle_api_errors


def is_anthropic_model(model: str) -> bool:
    """Returns True if the model identifier belongs to Anthropic Claude."""
    return model is not None and "claude" in model.lower()


def get_anthropic_messages(messages: list) -> list:
    """Strips system messages from the list (Anthropic receives system separately)."""
    return [m for m in messages if m["role"] != "system"]


def route_chat(
    mistral_client,
    anthropic_client,
    messages: list,
    model: str,
    system_prompt: str
) -> Tuple[str | None, int]:
    """
    Routes the chat request to the correct API client based on the model name.
    Returns (response_text, used_tokens). response_text is None on error.
    """
    if is_anthropic_model(model):
        anthropic_messages = get_anthropic_messages(messages)
        response_text, used_tokens = handle_api_errors(anthropic_chat)(
            anthropic_client,
            anthropic_messages,
            system_prompt=system_prompt,
            model=model
        )
    else:
        response_text, used_tokens = handle_api_errors(mistral_chat)(
            mistral_client,
            messages,
            model=model
        )

    return response_text, used_tokens