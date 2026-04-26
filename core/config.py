# core/config.py
# NOTE: This file is kept for backward compatibility only.
# New code should use core.config_loader.get_config() directly.
from core.config_loader import get_config
 
CONFIG = get_config()
 
 
def load_config():
    """Deprecated: use get_config() from core.config_loader instead."""
    return get_config()
