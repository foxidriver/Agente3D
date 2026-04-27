# core/sidebar.py
import os
import streamlit as st
from typing import Dict, Any
from core.session_manager import save_session, load_session, list_sessions
from core.model_router import is_anthropic_model

def render_sidebar(config: Dict[str, Any]) -> tuple:
    """
    Renders the full sidebar UI components.
    Returns a tuple of (selected_model, selected_mode).
    """
    with st.sidebar:
        selected_model = _render_model_selector()
        st.divider()
        selected_mode = _render_mode_selector()
        st.divider()
        _render_session_manager()
        st.divider()
        _render_token_counter()
        st.divider()
        _render_clear_button(config)
    return selected_model, selected_mode

def _render_model_selector() -> str:
    """Renders the AI model selection dropdown and returns model ID."""
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
        if not selected_model:
            st.error("❌ No models found in environment variables")
            st.stop()
    except Exception as e:
        st.error(f"❌ Model loading error: {str(e)}")
        st.stop()

    # Display provider info
    if is_anthropic_model(selected_model):
        st.caption(f"🟠 Anthropic — `{selected_model}`")
    else:
        st.caption(f"🔵 Mistral — `{selected_model}`")
    
    return selected_model

def _render_mode_selector() -> str:
    """Renders the application mode selector."""
    st.markdown("### 🔧 Modalità")
    return st.radio(
        "Modalità",
        options=["Programmazione", "Progetti 3D"],
        label_visibility="collapsed"
    )

def _render_session_manager() -> None:
    """Renders session persistence controls (save/load)."""
    st.markdown("### 💾 Sessioni")
    session_id = st.text_input(
        "ID Sessione",
        value="default_session",
        label_visibility="collapsed",
        placeholder="ID Sessione"
    )
    
    col_save, col_load = st.columns(2)
    with col_save:
        if st.button("Salva", use_container_width=True, key="save_btn"):
            try:
                save_session(session_id, st.session_state.messages)
                st.success("✅ Saved!")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                
    with col_load:
        if st.button("Carica", use_container_width=True, key="load_btn"):
            try:
                st.session_state.messages = load_session(session_id)
                st.success("✅ Loaded!")
                st.rerun()
            except FileNotFoundError:
                st.error("❌ Not found")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

def _render_token_counter() -> None:
    """Displays cumulative token usage for the current session."""
    st.markdown("### 📊 Token")
    st.metric(label="Totale", value=st.session_state.get("total_tokens", 0))

def _render_clear_button(config: Dict[str, Any]) -> None:
    """Renders the chat reset button."""
    from core.session_state import reset_conversation
    if st.button("🗑️ Pulisci chat", type="primary", use_container_width=True):
        reset_conversation(config)
        st.rerun()