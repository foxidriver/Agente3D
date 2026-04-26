import streamlit as st
from typing import Dict, Any

def setup_page(config: Dict[str, Any]) -> None:
    """
    Configures the Streamlit page. 
    Set layout to 'wide' to accommodate the 3-column dashboard.
    """
    st.set_page_config(
        page_title=config["ui"]["title"],
        layout="wide", # Essential for 3-column layout
        initial_sidebar_state="expanded"
    )

def apply_styles() -> None:
    """
    Injects custom CSS to manage independent scrolling and UI density.
    """
    st.markdown("""
        <style>
            /* Main container padding adjustment */
            [data-testid="stAppViewBlockContainer"] {
                padding-top: 2rem;
                padding-bottom: 1rem;
                padding-left: 3rem;
                padding-right: 3rem;
            }

            /* Compact sidebar styling */
            [data-testid="stSidebar"] {
                padding-top: 0.5rem;
            }

            /* Independent scrolling container tweaks */
            .stElementContainer {
                margin-bottom: 0.5rem;
            }
            
            /* Section headers styling */
            h3 {
                font-size: 1.1rem !important;
                font-weight: 700;
            }
        </style>
    """, unsafe_allow_html=True)