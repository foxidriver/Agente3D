# agente.py
import streamlit as st
from dotenv import load_dotenv
import os
import yaml
from typing import Dict, Any

# Importa solo le funzioni necessarie
from core.mistral_client import create_client, initial_messages, chat as mistral_chat
from core.anthropic_client import create_anthropic_client, chat as anthropic_chat
from core.session_manager import save_session, load_session, list_sessions
from core.error_handler import (
    handle_streamlit_errors,
    handle_api_errors,
    validate_config
)

# Load environment variables
load_dotenv()

# Check if config file exists
if not os.path.exists("config.yaml"):
    st.error("❌ Errore critico: file config.yaml non trovato!")
    st.stop()

# Load configuration with validation
try:
    with open("config.yaml", "r", encoding="utf-8") as config_file:
        config: Dict[str, Any] = yaml.safe_load(config_file)
        if not validate_config(config):
            st.stop()
except yaml.YAMLError as error:
    st.error(f"❌ Errore nel caricamento di config.yaml: {str(error)}")
    st.stop()
except Exception as e:
    st.error(f"❌ Errore imprevisto nel caricamento della configurazione: {str(e)}")
    st.stop()

# --- Helper functions ---
@handle_streamlit_errors
def is_anthropic_model(model: str) -> bool:
    """Returns True if the model is an Anthropic Claude model."""
    return model is not None and "claude" in model.lower()

@handle_streamlit_errors
def get_anthropic_messages(messages):
    """Filters out system messages for Anthropic API (system is passed separately)."""
    return [m for m in messages if m["role"] != "system"]

# --- Page config ---
@handle_streamlit_errors
def setup_page():
    st.set_page_config(
        page_title=config["ui"]["title"],
        layout="centered"
    )

# Initialize page
setup_page()

# --- Sidebar con gestione errori ---
try:
    with st.sidebar:
        st.markdown("### 🤖 Modello")
        available_models = {
            "Small — Routine": os.getenv("MODEL_DEFAULT"),
            "Reasoning — Complesso": os.getenv("MODEL_REASONING"),
            "Code — Programmazione": os.getenv("MODEL_CODE"),
        }

        try:
            selected_model_name = st.selectbox(
                "Seleziona:",
                options=list(available_models.keys()),
                index=0,
                label_visibility="collapsed"
            )
            selected_model = available_models[selected_model_name]

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

        st.divider()

        # --- Session management ---
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
                if st.button("Salva", use_container_width=True):
                    try:
                        save_session(session_id, st.session_state.messages)
                        st.success("✅ Salvata con successo!")
                    except Exception as e:
                        st.error(f"❌ Errore nel salvataggio: {str(e)}")

            with col_load:
                if st.button("Carica", use_container_width=True):
                    try:
                        st.session_state.messages = load_session(session_id)
                        st.success("✅ Caricata con successo!")
                        st.rerun()
                    except FileNotFoundError:
                        st.error("❌ Sessione non trovata")
                    except Exception as e:
                        st.error(f"❌ Errore nel caricamento: {str(e)}")

            if st.button("Elenca sessioni", use_container_width=True):
                try:
                    sessions = list_sessions()
                    if sessions:
                        for s in sessions:
                            st.caption(f"- {s}")
                    else:
                        st.caption("Nessuna sessione disponibile.")
                except Exception as e:
                    st.error(f"❌ Errore nell'elenco sessioni: {str(e)}")
        except Exception as e:
            st.error(f"❌ Errore nella gestione delle sessioni: {str(e)}")

        st.divider()

        # --- Token usage ---
        st.markdown("### 📊 Token utilizzati")
        try:
            st.metric(label="Totale", value=st.session_state.get("total_tokens", 0))
        except Exception as e:
            st.error(f"❌ Errore nel calcolo dei token: {str(e)}")

        st.divider()

        # --- Clear chat ---
        if st.button("🗑️ Pulisci chat", type="primary", use_container_width=True):
            try:
                st.session_state.messages = initial_messages(config["agent"]["system_prompt"])
                st.session_state.total_tokens = 0
                st.rerun()
            except Exception as e:
                st.error(f"❌ Errore nella pulizia della chat: {str(e)}")
except Exception as e:
    st.error(f"❌ Errore nella sidebar: {str(e)}")

# Initialize Session State with error handling
try:
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

    if "messages" not in st.session_state:
        try:
            st.session_state.messages = initial_messages(config["agent"]["system_prompt"])
        except Exception as e:
            st.error(f"❌ Errore nell'inizializzazione dei messaggi: {str(e)}")
            st.stop()

    if "current_model" not in st.session_state:
        st.session_state.current_model = selected_model

    if "total_tokens" not in st.session_state:
        st.session_state.total_tokens = 0

    if "debug_mode" not in st.session_state:
        st.session_state.debug_mode = False

except Exception as e:
    st.error(f"❌ Errore critico nell'inizializzazione: {str(e)}")
    st.stop()

# Detect model change → reset conversation
if st.session_state.current_model != selected_model:
    try:
        st.session_state.messages = initial_messages(config["agent"]["system_prompt"])
        st.session_state.current_model = selected_model
        st.session_state.total_tokens = 0
        st.info("⚠️ Modello cambiato: nuova conversazione avviata.")
        st.rerun()
    except Exception as e:
        st.error(f"❌ Errore nel cambio modello: {str(e)}")

# --- Main area ---
try:
    st.title(config["ui"]["title"])
    st.markdown(config["ui"]["subtitle"])

    # Display chat history
    try:
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.chat_message("user").write(message["content"])
            elif message["role"] == "assistant" and message.get("content"):
                st.chat_message("assistant").write(message["content"])
    except Exception as e:
        st.error(f"❌ Errore nella visualizzazione della cronologia chat: {str(e)}")

    # User input
    if user_input := st.chat_input("Scrivi un messaggio..."):
        try:
            st.session_state.messages.append({"role": "user", "content": user_input})
            st.chat_message("user").write(user_input)

            try:
                if is_anthropic_model(selected_model):
                    try:
                        system_prompt = config["agent"]["system_prompt"]
                        anthropic_messages = get_anthropic_messages(st.session_state.messages)
                        response_text, used_tokens = handle_api_errors(anthropic_chat)(
                            st.session_state.anthropic_client,
                            anthropic_messages,
                            system_prompt=system_prompt,
                            model=selected_model
                        )
                    except Exception as e:
                        response_text, used_tokens = None, 0
                else:
                    response_text, used_tokens = handle_api_errors(mistral_chat)(
                        st.session_state.mistral_client,
                        st.session_state.messages,
                        model=selected_model
                    )

                if response_text is not None:
                    st.session_state.total_tokens += used_tokens
                    st.session_state.messages.append({"role": "assistant", "content": response_text})
                    st.rerun()
            except Exception as e:
                st.error(f"❌ Errore nella gestione della risposta: {str(e)}")

        except Exception as e:
            st.error(f"❌ Errore nella gestione dell'input utente: {str(e)}")

except Exception as e:
    st.error(f"❌ Errore critico nell'area principale: {str(e)}")