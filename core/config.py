import yaml
import os
def load_config():
    """Load configuration from the config.yaml file."""
    config_path = os.path.join(os.path.dirname(__file__), "..", "config.yaml")
    with open(config_path, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)

# Global configuration available to all modules
CONFIG = load_config()