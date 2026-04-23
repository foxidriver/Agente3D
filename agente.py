# agente.py

import streamlit as st
from dotenv import load_dotenv
import os
import yaml
from typing import Dict, Any
from core.mistral_client import create_client, initial_messages, chat
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

# --- Streamlit UI ---
st.title(config["ui"]["title"])
st.markdown(config["ui"]["subtitle"])

# Model selection dropdown
available_models = {
    "Small (Routine tasks)": os.getenv("MODEL_DEFAULT"),
    "Large (Complex reasoning)": os.getenv("MODEL_REASONING"),
    "Code (Programming)": os.getenv("MODEL_CODE"),
}

selected_model_name = st.selectbox(
    "Select Mistral model:",
    options=list(available_models.keys()),
    index=0
)
selected_model = available_models[selected_model_name]

# Initialize client and memory
if "client" not in st.session_state:
    try:
        st.session_state.client = create_client()
    except ValueError as error:
        st.error(f"Error initializing Mistral client: {str(error)}")
        st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = initial_messages(config["agent"]["system_prompt"])

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

# Frame for token usage display
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

    print(f"[DEBUG] Selected model in Streamlit: {repr(selected_model)}")

    try:
        # Update chat call to handle the new return (text, tokens)
        response_text, used_tokens = chat(
            st.session_state.client,
            st.session_state.messages,
            model=selected_model
        )

        # Update total token count
        total_tokens += used_tokens
        token_counter.markdown(f"**Total tokens:** {total_tokens}")

        st.session_state.messages.append({"role": "assistant", "content": response_text})
        st.chat_message("assistant").write(response_text)
    except Exception as error:
        st.error(f"❌ Error: {str(error)}")

# Clear chat button
if st.button("Clear chat"):
    st.session_state.messages = initial_messages(config[""]["system_prompt"])
    total_tokens = 0
    token_counter.markdown(f"**Total tokens:** {total_tokens}")
    st.rerun()