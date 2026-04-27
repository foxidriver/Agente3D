# core/sidebar.py
import os
import streamlit as st
from typing import Dict, Any
from core.session_manager import load_session, list_sessions, rename_session, delete_session
from core.model_router import is_anthropic_model


def render_sidebar(config: Dict[str, Any]) -> tuple:
    """Renders the full sidebar UI. Returns (selected_model, selected_mode)."""
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


@st.dialog("📂 Gestione Sessioni")
def _session_manager_dialog() -> None:
    """Modal dialog listing all sessions with load, rename, delete actions."""
    sessions = list_sessions()
    if not sessions:
        st.info("Nessuna sessione salvata.")
        return

    for sid in sorted(sessions, reverse=True):
        col_name, col_load, col_rename, col_delete = st.columns([3, 1, 1, 1])
        col_name.caption(sid)

        if col_load.button("📥", key=f"load_{sid}", help="Carica"):
            try:
                st.session_state.messages = load_session(sid)
                st.session_state.session_id = sid
                st.rerun()
            except Exception as e:
                st.error(f"❌ {str(e)}")

        if col_rename.button("✏️", key=f"rename_{sid}", help="Rinomina"):
            st.session_state[f"renaming_{sid}"] = True

        if col_delete.button("🗑️", key=f"delete_{sid}", help="Elimina"):
            try:
                delete_session(sid)
                st.rerun()
            except Exception as e:
                st.error(f"❌ {str(e)}")

        if st.session_state.get(f"renaming_{sid}"):
            new_name = st.text_input("Nuovo nome:", key=f"newname_{sid}")
            if st.button("Conferma", key=f"confirm_{sid}") and new_name:
                try:
                    rename_session(sid, new_name)
                    st.session_state.pop(f"renaming_{sid}")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ {str(e)}")


def _render_session_manager() -> None:
    """Renders session info and the button to open the session manager dialog."""
    st.caption(f"ID: `{st.session_state.get('session_id', '—')}`")
    st.write("")
    st.write("")
    if st.button("📂 Gestisci sessioni", use_container_width=True):
        _session_manager_dialog()


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