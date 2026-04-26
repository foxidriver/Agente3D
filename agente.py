import streamlit as st
from dotenv import load_dotenv

from core.config_loader import get_config
from core.styles import setup_page, apply_styles
from core.sidebar import render_sidebar
from core.session_state import init_session_state
from core.chat_panel import render_chat, handle_input
from core.right_panel import render_right_panel

# 1. Setup & Environment
load_dotenv()
config = get_config()
setup_page(config)
apply_styles()

# 2. Sidebar (Left Column - Independent)
selected_model, selected_mode = render_sidebar(config)

# 3. State Management
init_session_state(config, selected_model)

# 4. Main UI Grid (Center and Right Columns)
col_chat, col_info = st.columns([2, 1], gap="large")

# --- CENTER COLUMN: Chat ---
with col_chat:
    st.title(config["ui"]["title"])
    
    # Independent scroll area for chat history
    with st.container(height=550, border=True):
        render_chat(st.session_state.messages)
    
    # Input field stays at the bottom of the column
    handle_input(config, selected_model)

# --- RIGHT COLUMN: Info Panel ---
with col_info:
    # Logic delegated to right_panel module
    render_right_panel(config, selected_mode)