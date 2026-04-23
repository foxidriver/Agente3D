# core/error_handler.py
import streamlit as st
from functools import wraps
from typing import Callable, Any, Tuple

def handle_streamlit_errors(func: Callable) -> Callable:
    """
    Decoratore per gestire gli errori nelle funzioni Streamlit.
    Mostra messaggi di errore appropriati e ferma l'esecuzione se necessario.
    """
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            st.error(f"❌ Errore critico: {str(e)}")
            if st.session_state.get("debug_mode", False):
                st.code(f"Dettagli: {str(e)}", language="python")
            return None
    return wrapper

def handle_api_errors(func: Callable) -> Callable:
    """
    Decoratore per gestire gli errori nelle chiamate API.
    Restituisce valori di default in caso di errore.
    """
    @wraps(func)
    def wrapper(*args, **kwargs) -> Tuple[Any, int]:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            st.error(f"❌ Errore API: {str(e)}")
            if st.session_state.get("debug_mode", False):
                st.code(f"Dettagli errore API: {str(e)}", language="python")
            return None, 0
    return wrapper

def validate_config(config: dict) -> bool:
    """Valida la struttura del file di configurazione."""
    required_keys = ["ui", "agent"]
    if not all(key in config for key in required_keys):
        st.error("❌ Configurazione non valida: mancano chiavi richieste")
        return False
    return True