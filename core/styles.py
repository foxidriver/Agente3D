# core/styles.py
import streamlit as st
from typing import Dict, Any


def setup_page(config: Dict[str, Any]) -> None:
    """Configures the Streamlit page."""
    st.set_page_config(
        page_title=config["ui"]["title"],
        layout="wide",
        initial_sidebar_state="expanded"
    )


def apply_styles() -> None:
    """Injects custom CSS to maximize information density."""
    st.markdown("""
        <style>
            /* --- HIDE STREAMLIT CHROME --- */
            [data-testid="stHeader"]     { display: none !important; }
            [data-testid="stToolbar"]    { display: none !important; }
            [data-testid="stDecoration"] { display: none !important; }
            #MainMenu                    { display: none !important; }
            footer                       { display: none !important; }

            /* --- MAIN AREA --- */
            [data-testid="stAppViewBlockContainer"],
            .block-container {
                padding-top: 0.4rem !important;
                padding-bottom: 0.2rem !important;
                padding-left: 1rem !important;
                padding-right: 1rem !important;
                max-width: 100% !important;
            }

            /* --- SIDEBAR: kill top space --- */
            [data-testid="stSidebar"] { padding-top: 0 !important; }
            [data-testid="stSidebar"] > div:first-child { padding-top: 0.2rem !important; }
            [data-testid="stSidebarContent"] { padding-top: 0.2rem !important; }
            section[data-testid="stSidebar"] > div { padding-top: 0 !important; }

            /* --- SIDEBAR: compress internal block spacing --- */
            [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
                gap: 0.15rem !important;
            }
            [data-testid="stSidebar"] .stElementContainer {
                margin-bottom: 0.05rem !important;
            }
            [data-testid="stSidebar"] [data-testid="stMarkdown"] {
                margin-bottom: 0.05rem !important;
            }
            [data-testid="stSidebar"] hr {
                margin: 0.2rem 0 !important;
            }

            /* --- SIDEBAR: radio buttons --- */
            [data-testid="stSidebar"] [data-testid="stRadio"] > div {
                gap: 0.1rem !important;
            }
            [data-testid="stSidebar"] [data-testid="stRadio"] label {
                padding: 0 !important;
                font-size: 0.80rem !important;
            }

            /* --- SIDEBAR: selectbox --- */
            [data-testid="stSidebar"] [data-testid="stSelectbox"] {
                margin-bottom: 0.05rem !important;
            }

            /* --- SIDEBAR: text input --- */
            [data-testid="stSidebar"] [data-testid="stTextInput"] {
                margin-bottom: 0.05rem !important;
            }
            [data-testid="stSidebar"] [data-testid="stTextInput"] input {
                padding: 0.2rem 0.4rem !important;
                font-size: 0.80rem !important;
            }

            /* --- SIDEBAR BUTTONS --- */
            [data-testid="stSidebar"] .stButton > button {
                padding: 0.1rem 0.4rem !important;
                font-size: 0.78rem !important;
                height: auto !important;
                line-height: 1.2 !important;
                min-height: 0 !important;
            }

            /* --- HEADINGS --- */
            h1 { font-size: 1.1rem !important; margin: 0.1rem 0 0.2rem 0 !important; }
            h2 { font-size: 0.95rem !important; margin: 0.1rem 0 0.1rem 0 !important; }
            h3 { font-size: 0.88rem !important; margin: 0.05rem 0 0.05rem 0 !important; }
            h4 { font-size: 0.80rem !important; margin: 0.05rem 0 0.05rem 0 !important; }

            /* --- RIGHT PANEL BUTTONS --- */
            .stButton > button {
                padding: 0.05rem 0.4rem !important;
                font-size: 0.75rem !important;
                height: auto !important;
                line-height: 1.2 !important;
                min-height: 0 !important;
                border-radius: 4px !important;
            }
            [data-testid="stVerticalBlock"] [data-testid="stVerticalBlock"] {
                gap: 0.1rem !important;
            }

            /* --- TEXT --- */
            p, .stMarkdown p { font-size: 0.80rem !important; margin-bottom: 0.05rem !important; }
            small, .stCaption { font-size: 0.72rem !important; }
            label { font-size: 0.80rem !important; }

            /* --- CHAT MESSAGES --- */
            [data-testid="stChatMessage"] {
                padding: 0.25rem 0.4rem !important;
                margin-bottom: 0.15rem !important;
            }
        </style>
    """, unsafe_allow_html=True)