# core/config_loader.py
import os
import yaml
import streamlit as st
from typing import Dict, Any
from core.error_handler import validate_config

_config: Dict[str, Any] | None = None


def get_config() -> Dict[str, Any]:
    """Loads and validates config.yaml. Returns cached config on subsequent calls."""
    global _config
    if _config is not None:
        return _config

    if not os.path.exists("config.yaml"):
        st.error("❌ Errore critico: file config.yaml non trovato!")
        st.stop()

    try:
        with open("config.yaml", "r", encoding="utf-8") as config_file:
            loaded = yaml.safe_load(config_file)
            if not validate_config(loaded):
                st.stop()
            _config = loaded
            return _config
    except yaml.YAMLError as error:
        st.error(f"❌ Errore nel caricamento di config.yaml: {str(error)}")
        st.stop()
    except Exception as e:
        st.error(f"❌ Errore imprevisto nel caricamento della configurazione: {str(e)}")
        st.stop()