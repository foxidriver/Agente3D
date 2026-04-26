# agente.py
from dotenv import load_dotenv

from core.config_loader import get_config
from core.styles import setup_page, apply_styles
from core.sidebar import render_sidebar
from core.session_state import init_session_state
from core.chat_panel import render_chat, handle_input
import streamlit as st

# Load environment variables
load_dotenv()

# Bootstrap
config = get_config()
setup_page(config)
apply_styles()

# Sidebar (returns selected model)
selected_model = render_sidebar(config)

# Session state init + model-change detection
init_session_state(config, selected_model)

# Main area
st.title(config["ui"]["title"])
st.markdown(config["ui"]["subtitle"])

render_chat(st.session_state.messages)
handle_input(config, selected_model)