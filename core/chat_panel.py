# core/chat_panel.py
import streamlit as st
from typing import Dict, Any
from core.model_router import route_chat


def render_chat(messages: list) -> None:
    """Renders the full chat history, skipping system messages."""
    try:
        for message in messages:
            if message["role"] == "user":
                st.chat_message("user").write(message["content"])
            elif message["role"] == "assistant" and message.get("content"):
                st.chat_message("assistant").write(message["content"])
    except Exception as e:
        st.error(f"❌ Errore nella visualizzazione della cronologia chat: {str(e)}")


def handle_input(config: Dict[str, Any], selected_model: str) -> None:
    """
    Handles the chat input box, sends the message to the correct API,
    and appends the assistant reply to the session state.
    """
    if user_input := st.chat_input("Scrivi un messaggio..."):
        try:
            st.session_state.messages.append({"role": "user", "content": user_input})
            st.chat_message("user").write(user_input)

            response_text, used_tokens = route_chat(
                mistral_client=st.session_state.mistral_client,
                anthropic_client=st.session_state.anthropic_client,
                messages=st.session_state.messages,
                model=selected_model,
                system_prompt=config["agent"]["system_prompt"]
            )

            if response_text is not None:
                st.session_state.total_tokens += used_tokens
                st.session_state.messages.append({"role": "assistant", "content": response_text})
                st.rerun()

        except Exception as e:
            st.error(f"❌ Errore nella gestione dell'input utente: {str(e)}")