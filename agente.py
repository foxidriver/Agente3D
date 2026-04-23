import streamlit as st
from dotenv import load_dotenv
import os
import yaml
from typing import Dict, Any
from core.mistral_client import create_client, initial_messages, chat as mistral_chat
from core.anthropic_client import create_anthropic_client, chat as anthropic_chat
from core.session_manager import save_session, load_session, list_sessions

# Load environment variables
load_dotenv()

# Check if config file exists
if not os.path.exists("config.yaml"):
    st.error("Errore: file config.yaml non trovato!")
    st.stop()

# Load configuration
try:
    with open("config.yaml", "r", encoding="utf-8") as config_file:
        config: Dict[str, Any] = yaml.safe_load(config_file)
except yaml.YAMLError as error:
    st.error(f"Errore nel caricamento di config.yaml: {str(error)}")
    st.stop()

# --- Helper functions ---

def is_anthropic_model(model: str) -> bool:
    """Returns True if the model is an Anthropic Claude model."""
    return model is not None and "claude" in model.lower()

def get_anthropic_messages(messages):
    """Filters out system messages for Anthropic API (system is passed separately)."""
    return [m for m in messages if m["role"] != "system"]

# --- Page config ---
st.set_page_config(
    page_title=config["ui"]["title"],
    layout="centered"
)

# --- Sidebar ---
with st.sidebar:
    st.markdown("### 🤖 Modello")
    available_models = {
        "Small — Routine": os.getenv("MODEL_DEFAULT"),
        "Reasoning — Complesso": os.getenv("MODEL_REASONING"),
        "Code — Programmazione": os.getenv("MODEL_CODE"),
    }
    selected_model_name = st.selectbox(
        "Seleziona:",
        options=list(available_models.keys()),
        index=0,
        label_visibility="collapsed"
    )
    selected_model = available_models[selected_model_name]

    if is_anthropic_model(selected_model):
        st.caption(f"🟠 Anthropic — `{selected_model}`")
    else:
        st.caption(f"🔵 Mistral — `{selected_model}`")

    st.divider()

    # --- Session management ---
    st.markdown("### 💾 Sessioni")
    session_id = st.text_input("ID Sessione", value="default_session", label_visibility="collapsed", placeholder="ID Sessione")

    col_save, col_load = st.columns(2)
    with col_save:
        if st.button("Salva", use_container_width=True):
            save_session(session_id, st.session_state.messages)
            st.success("Salvata!")
    with col_load:
        if st.button("Carica", use_container_width=True):
            try:
                st.session_state.messages = load_session(session_id)
                st.success("Caricata!")
                st.rerun()
            except FileNotFoundError:
                st.error("Non trovata")

    if st.button("Elenca sessioni", use_container_width=True):
        sessions = list_sessions()
        if sessions:
            for s in sessions:
                st.caption(f"- {s}")
        else:
            st.caption("Nessuna sessione disponibile.")

    st.divider()

    # --- Token usage ---
    st.markdown("### 📊 Token utilizzati")
    st.metric(label="Totale", value=st.session_state.get("total_tokens", 0))

    st.divider()

    # --- Clear chat ---
    if st.button("🗑️ Pulisci chat", type="primary", use_container_width=True):
        st.session_state.messages = initial_messages(config["agent"]["system_prompt"])
        st.session_state.total_tokens = 0
        st.rerun()

# --- Initialize Session State ---

if "mistral_client" not in st.session_state:
    try:
        st.session_state.mistral_client = create_client()
    except ValueError as error:
        st.error(f"Errore nell'inizializzazione del client Mistral: {str(error)}")
        st.stop()

if "anthropic_client" not in st.session_state:
    try:
        st.session_state.anthropic_client = create_anthropic_client()
    except ValueError as error:
        st.error(f"Errore nell'inizializzazione del client Anthropic: {str(error)}")
        st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = initial_messages(config["agent"]["system_prompt"])

if "current_model" not in st.session_state:
    st.session_state.current_model = selected_model

if "total_tokens" not in st.session_state:
    st.session_state.total_tokens = 0

# Detect model change → reset conversation
if st.session_state.current_model != selected_model:
    st.session_state.messages = initial_messages(config["agent"]["system_prompt"])
    st.session_state.current_model = selected_model
    st.session_state.total_tokens = 0
    st.info("⚠️ Modello cambiato: nuova conversazione avviata.")
    st.rerun()

# --- Main area: title and chat ---
st.title(config["ui"]["title"])
st.markdown(config["ui"]["subtitle"])

# Display chat history
for message in st.session_state.messages:
    if message["role"] == "user":
        st.chat_message("user").write(message["content"])
    elif message["role"] == "assistant" and message.get("content"):
        st.chat_message("assistant").write(message["content"])

# User input
if user_input := st.chat_input("Scrivi un messaggio..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    try:
        if is_anthropic_model(selected_model):
            system_prompt = config["agent"]["system_prompt"]
            anthropic_messages = get_anthropic_messages(st.session_state.messages)
            response_text, used_tokens = anthropic_chat(
                st.session_state.anthropic_client,
                anthropic_messages,
                system_prompt=system_prompt,
                model=selected_model
            )
        else:
            response_text, used_tokens = mistral_chat(
                st.session_state.mistral_client,
                st.session_state.messages,
                model=selected_model
            )

        st.session_state.total_tokens += used_tokens
        st.session_state.messages.append({"role": "assistant", "content": response_text})
        st.rerun()

    except Exception as error:
        st.error(f"❌ Errore: {str(error)}")