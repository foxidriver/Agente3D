# core/session_manager.py

import pickle
import os
from typing import List, Dict, Any

def save_session(session_id: str, messages: List[Dict[str, Any]]) -> None:
    """
    Save the chat session to a file.

    Args:
        session_id (str): Unique identifier for the session.
        messages (List[Dict[str, Any]]): List of messages in the session.
    """
    session_dir = "sessions"
    if not os.path.exists(session_dir):
        os.makedirs(session_dir)

    session_path = os.path.join(session_dir, f"{session_id}.pkl")
    with open(session_path, "wb") as file:
        pickle.dump(messages, file)

def load_session(session_id: str) -> List[Dict[str, Any]]:
    """
    Load the chat session from a file.

    Args:
        session_id (str): Unique identifier for the session.

    Returns:
        List[Dict[str, Any]]: List of messages in the session.
    """
    session_path = os.path.join("sessions", f"{session_id}.pkl")
    if not os.path.exists(session_path):
        raise FileNotFoundError(f"Session {session_id} not found.")

    with open(session_path, "rb") as file:
        return pickle.load(file)

def list_sessions() -> List[str]:
    """
    List all available sessions.

    Returns:
        List[str]: List of session IDs.
    """
    session_dir = "sessions"
    if not os.path.exists(session_dir):
        return []

    return [f.split(".")[0] for f in os.listdir(session_dir) if f.endswith(".pkl")]