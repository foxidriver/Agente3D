# core/right_panel.py
import streamlit as st
import os
from typing import Dict, Any


def render_right_panel(config: Dict[str, Any], selected_mode: str) -> None:
    """Renders the right-side information panel with independent scrolling."""
    st.markdown("### 🧊 Project Dashboard")

    with st.container(height=650, border=True):
        mode = str(selected_mode).strip().lower()
        if "3d" in mode:
            _render_3d_tools()
        else:
            _render_coding_context()


def _send_file_to_chat(filepath: str) -> None:
    """Reads a file and appends its content to the chat as a user message."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        filename = os.path.basename(filepath)
        message = f"📄 `{filename}`\n```python\n{content}\n```"
        st.session_state.messages.append({"role": "user", "content": message})
        st.rerun()
    except Exception as e:
        st.error(f"Error reading file '{filepath}': {e}")


def _render_coding_context() -> None:
    """Scans Python files and renders each as a clickable button."""
    st.markdown("#### 🐍 Python Workspace")
    base_path = os.getcwd()

    try:
        st.markdown("**Root Directory**")
        root_files = [f for f in os.listdir(base_path) if f.endswith(".py")]
        for f in sorted(root_files):
            if st.button(f"📄 {f}", key=f"root_{f}", use_container_width=True):
                _send_file_to_chat(os.path.join(base_path, f))

        st.divider()

        st.markdown("**Core Subdirectory**")
        core_path = os.path.join(base_path, "core")
        if os.path.exists(core_path):
            core_files = [f for f in os.listdir(core_path) if f.endswith(".py")]
            for f in sorted(core_files):
                if st.button(f"⚙️ {f}", key=f"core_{f}", use_container_width=True):
                    _send_file_to_chat(os.path.join(core_path, f))
        else:
            st.error("Folder `/core` not found.")

    except Exception as e:
        st.error(f"Error scanning workspace: {e}")


def _render_3d_tools() -> None:
    """Renders tools and assets for 3D Projects."""
    st.markdown("#### 🛠️ 3D Tools")
    st.button("Scan Assets", use_container_width=True)
    st.write("Project assets (.obj):")
    for i in range(15):
        st.caption(f"Asset_{i:02d}.obj - Ready")