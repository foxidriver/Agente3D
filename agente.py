# agente.py
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
    st.error("Error: config.yaml file not found!")
    st.stop()
 
# Load configuration
try:
    with open("config.yaml", "r", encoding="utf-8") as config_file:
        config: Dict[str, Any] = yaml.safe_load(config_file)
except yaml.YAMLError as error:
    st.error(f"Error loading config.yaml: {str(error)}")
    st.stop()
 
# --- Helper functions ---
 
def is_anthropic_model(model: str) -> bool:
    """Returns True if the model is an Anthropic Claude model."""
    return model is not None and "claude" in model.lower()
 
def get_anthropic_messages(messages):
    """Filters out system messages for Anthropic API (system is passed separately)."""
    return [m for m in messages if m["role"] != "system"]
 
# --- Streamlit UI ---
st.title(config["ui"]["title"])
st.markdown(config["ui"]["subtitle"])
 
# Model selection dropdown
available_models = {
    "Small (Routine tasks)": os.getenv("MODEL_DEFAULT"),
    "Reasoning (Complex tasks)": os.getenv("MODEL_REASONING"),
    "Code (Programming)": os.getenv("MODEL_CODE"),
}
selected_model_name = st.selectbox(
    "Select model:",
    options=list(available_models.keys()),
    index=0
)
selected_model = available_models[selected_model_name]
 
# Initialize Mistral client
if "mistral_client" not in st.session_state:
    try:
        st.session_state.mistral_client = create_client()
    except ValueError as error:
        st.error(f"Error initializing Mistral client: {str(error)}")
        st.stop()
 
# Initialize Anthropic client
if "anthropic_client" not in st.session_state:
    try:
        st.session_state.anthropic_client = create_anthropic_client()
    except ValueError as error:
        st.error(f"Error initializing Anthropic client: {str(error)}")
        st.stop()
 
# Initialize messages and current model tracking
if "messages" not in st.session_state:
    st.session_state.messages = initial_messages(config["agent"]["system_prompt"])
 
if "current_model" not in st.session_state:
    st.session_state.current_model = selected_model
 
# Detect model change → reset conversation
if st.session_state.current_model != selected_model:
    st.session_state.messages = initial_messages(config["agent"]["system_prompt"])
    st.session_state.current_model = selected_model
    st.info("⚠️ Modello cambiato: nuova conversazione avviata.")
    st.rerun()
 
# Show active provider badge
if is_anthropic_model(selected_model):
    st.caption(f"🟠 Provider: Anthropic — `{selected_model}`")
else:
    st.caption(f"🔵 Provider: Mistral — `{selected_model}`")
 
# Session management
session_id = st.text_input("Session ID", value="default_session")
if st.button("Save Session"):
    save_session(session_id, st.session_state.messages)
    st.success(f"Session {session_id} saved successfully.")
if st.button("Load Session"):
    try:
        st.session_state.messages = load_session(session_id)
        st.success(f"Session {session_id} loaded successfully.")
    except FileNotFoundError as error:
        st.error(str(error))
 
# List available sessions
if st.button("List Sessions"):
    sessions = list_sessions()
    if sessions:
        st.write("Available sessions:")
        for session in sessions:
            st.write(f"- {session}")
    else:
        st.write("No sessions found.")
 
# Token usage display
token_container = st.container()
token_container.markdown("### Token Usage")
token_counter = token_container.empty()
total_tokens = 0
token_counter.markdown(f"**Total tokens:** {total_tokens}")
 
# Display chat history
for message in st.session_state.messages:
    if message["role"] == "user":
        st.chat_message("user").write(message["content"])
    elif message["role"] == "assistant" and message.get("content"):
        st.chat_message("assistant").write(message["content"])
 
# User input
if user_input := st.chat_input("Write a message..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)
 
    print(f"[DEBUG] Selected model: {repr(selected_model)}")
 
    try:
        if is_anthropic_model(selected_model):
            # Anthropic: pass system prompt separately, filter it from messages
            system_prompt = config["agent"]["system_prompt"]
            anthropic_messages = get_anthropic_messages(st.session_state.messages)
            response_text, used_tokens = anthropic_chat(
                st.session_state.anthropic_client,
                anthropic_messages,
                system_prompt=system_prompt,
                model=selected_model
            )
        else:
            # Mistral: system prompt is included in messages list
            response_text, used_tokens = mistral_chat(
                st.session_state.mistral_client,
                st.session_state.messages,
                model=selected_model
            )
 
        total_tokens += used_tokens
        token_counter.markdown(f"**Total tokens:** {total_tokens}")
        st.session_state.messages.append({"role": "assistant", "content": response_text})
        st.chat_message("assistant").write(response_text)
 
    except Exception as error:
        st.error(f"❌ Error: {str(error)}")
 
# Clear chat button
if st.button("Clear chat"):
    st.session_state.messages = initial_messages(config["agent"]["system_prompt"])
    total_tokens = 0
    token_counter.markdown(f"**Total tokens:** {total_tokens}")
    st.rerun()
