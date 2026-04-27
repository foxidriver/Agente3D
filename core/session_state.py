# core/session_state.py
import streamlit as st
from typing import Dict, Any
from datetime import datetime
from core.mistral_client import create_client, initial_messages
from core.anthropic_client import create_anthropic_client


def init_session_state(config: Dict[str, Any], selected_model: str) -> None:
    """
    Initializes all Streamlit session state variables on first run.
    Handles model changes by resetting the conversation.
    """
    _init_clients()
    _init_messages(config)
    _init_counters(selected_model)
    _init_session_id()
    _handle_model_change(config, selected_model)


def _init_clients() -> None:
    """Initializes API clients if not already present in session state."""
    if "mistral_client" not in st.session_state:
        try:
            st.session_state.mistral_client = create_client()
        except ValueError as error:
            st.error(f"❌ Configurazione errata per il client Mistral: {str(error)}")
            st.stop()
        except Exception as e:
            st.error(f"❌ Errore imprevisto nel client Mistral: {str(e)}")
            st.stop()

    if "anthropic_client" not in st.session_state:
        try:
            st.session_state.anthropic_client = create_anthropic_client()
        except ValueError as error:
            st.error(f"❌ Configurazione errata per il client Anthropic: {str(error)}")
            st.stop()
        except Exception as e:
            st.error(f"❌ Errore imprevisto nel client Anthropic: {str(e)}")
            st.stop()


def _init_messages(config: Dict[str, Any]) -> None:
    """Initializes the message history with the system prompt."""
    if "messages" not in st.session_state:
        try:
            st.session_state.messages = initial_messages(config["agent"]["system_prompt"])
        except Exception as e:
            st.error(f"❌ Errore nell'inizializzazione dei messaggi: {str(e)}")
            st.stop()


def _init_counters(selected_model: str) -> None:
    """Initializes token counter and current model tracker."""
    if "current_model" not in st.session_state:
        st.session_state.current_model = selected_model
    if "total_tokens" not in st.session_state:
        st.session_state.total_tokens = 0


def _init_session_id() -> None:
    """Initializes a unique session ID based on current timestamp."""
    if "session_id" not in st.session_state:
        st.session_state.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")


def _handle_model_change(config: Dict[str, Any], selected_model: str) -> None:
    """Resets the conversation when the user switches model."""
    if st.session_state.current_model != selected_model:
        try:
            st.session_state.messages = initial_messages(config["agent"]["system_prompt"])
            st.session_state.current_model = selected_model
            st.session_state.total_tokens = 0
            st.info("⚠️ Modello cambiato: nuova conversazione avviata.")
            st.rerun()
        except Exception as e:
            st.error(f"❌ Errore nel cambio modello: {str(e)}")


def reset_conversation(config: Dict[str, Any]) -> None:
    """Resets messages, token counter, and generates a fresh session ID."""
    st.session_state.messages = initial_messages(config["agent"]["system_prompt"])
    st.session_state.total_tokens = 0
    st.session_state.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")