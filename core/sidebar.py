# core/sidebar.py
import os
import streamlit as st
from typing import Dict, Any
from core.session_manager import save_session, load_session, list_sessions
from core.model_router import is_anthropic_model
 
 
def render_sidebar(config: Dict[str, Any]) -> str:
    """
    Renders the full sidebar UI.
    Returns the currently selected model identifier string.
    """
    with st.sidebar:
        selected_model = _render_model_selector()
        st.divider()
        _render_session_manager()
        st.divider()
        _render_token_counter()
        st.divider()
        _render_clear_button(config)
 
    return selected_model
 
 
def _render_model_selector() -> str:
    """Renders the model selection dropdown and returns the selected model id."""
    st.markdown("### 🤖 Modello")
 
    available_models = {
        "Small — Routine": os.getenv("MODEL_DEFAULT"),
        "Reasoning — Complesso": os.getenv("MODEL_REASONING"),
        "Code — Programmazione": os.getenv("MODEL_CODE"),
    }
 
    try:
        selected_name = st.selectbox(
            "Seleziona:",
            options=list(available_models.keys()),
            index=0,
            label_visibility="collapsed"
        )
        selected_model = available_models[selected_name]
 
        if selected_model is None:
            st.error("❌ Nessun modello disponibile nelle variabili d'ambiente")
            st.stop()
    except Exception as e:
        st.error(f"❌ Errore nel caricamento dei modelli: {str(e)}")
        st.stop()
 
    if is_anthropic_model(selected_model):
        st.caption(f"🟠 Anthropic — `{selected_model}`")
    else:
        st.caption(f"🔵 Mistral — `{selected_model}`")
 
    return selected_model
 
 
def _render_session_manager() -> None:
    """Renders the session save/load/list controls."""
    st.markdown("### 💾 Sessioni")
 
    try:
        session_id = st.text_input(
            "ID Sessione",
            value="default_session",
            label_visibility="collapsed",
            placeholder="ID Sessione"
        )
 
        col_save, col_load = st.columns(2)
        with col_save:
            if st.button("Salva", use_container_width=True, key="save_button"):
                try:
                    save_session(session_id, st.session_state.messages)
                    st.success("✅ Salvata!")
                except Exception as e:
                    st.error(f"❌ Errore: {str(e)}")
 
        with col_load:
            if st.button("Carica", use_container_width=True, key="load_button"):
                try:
                    st.session_state.messages = load_session(session_id)
                    st.success("✅ Caricata!")
                    st.rerun()
                except FileNotFoundError:
                    st.error("❌ Sessione non trovata")
                except Exception as e:
                    st.error(f"❌ Errore: {str(e)}")
 
        if st.button("Elenca sessioni", use_container_width=True, key="list_button"):
            try:
                sessions = list_sessions()
                if sessions:
                    for s in sessions:
                        st.caption(f"- {s}")
                else:
                    st.caption("Nessuna sessione disponibile.")
            except Exception as e:
                st.error(f"❌ Errore: {str(e)}")
 
    except Exception as e:
        st.error(f"❌ Errore nella gestione delle sessioni: {str(e)}")
 
 
def _render_token_counter() -> None:
    """Renders the cumulative token usage metric."""
    st.markdown("### 📊 Token")
    try:
        st.metric(label="Totale", value=st.session_state.get("total_tokens", 0))
    except Exception as e:
        st.error(f"❌ Errore token: {str(e)}")
 
 
def _render_clear_button(config: Dict[str, Any]) -> None:
    """Renders the clear chat button and handles the reset logic."""
    from core.session_state import reset_conversation
 
    if st.button("🗑️ Pulisci chat", type="primary", use_container_width=True, key="clear_button"):
        try:
            reset_conversation(config)
            st.rerun()
        except Exception as e:
            st.error(f"❌ Errore nella pulizia della chat: {str(e)}")
 
