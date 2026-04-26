# core/styles.py
import streamlit as st
from typing import Dict, Any


def setup_page(config: Dict[str, Any]) -> None:
    """Configures the Streamlit page (must be called before any other st command)."""
    st.set_page_config(
        page_title=config["ui"]["title"],
        layout="centered"
    )


def apply_styles() -> None:
    """Injects compact CSS for the sidebar and global layout."""
    st.markdown("""
        <style>
            /* Reduce general sidebar padding */
            [data-testid="stSidebar"] {
                padding-top: 0.5rem;
            }
            [data-testid="stSidebar"] .block-container {
                padding-top: 0.5rem;
                padding-bottom: 0.5rem;
            }
            /* Reduce margins between sidebar elements */
            [data-testid="stSidebar"] .stMarkdown {
                margin-bottom: 0rem;
            }
            [data-testid="stSidebar"] h3 {
                font-size: 0.85rem;
                margin-top: 0.3rem;
                margin-bottom: 0.2rem;
            }
            /* Reduce selectbox size */
            [data-testid="stSidebar"] .stSelectbox {
                margin-bottom: 0rem;
            }
            /* Reduce button size */
            [data-testid="stSidebar"] .stButton button {
                padding: 0.2rem 0.5rem;
                font-size: 0.8rem;
            }
            /* Reduce caption size */
            [data-testid="stSidebar"] .stCaption {
                font-size: 0.75rem;
                margin-bottom: 0rem;
            }
            /* Reduce metric size */
            [data-testid="stSidebar"] [data-testid="stMetric"] {
                padding: 0.2rem 0rem;
            }
            [data-testid="stSidebar"] [data-testid="stMetricValue"] {
                font-size: 1rem;
            }
            [data-testid="stSidebar"] [data-testid="stMetricLabel"] {
                font-size: 0.75rem;
            }
            /* Reduce divider spacing */
            [data-testid="stSidebar"] hr {
                margin-top: 0.3rem;
                margin-bottom: 0.3rem;
            }
            /* Reduce text input spacing */
            [data-testid="stSidebar"] .stTextInput {
                margin-bottom: 0.2rem;
            }
        </style>
    """, unsafe_allow_html=True)