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


def _inject_opened_button_styles(opened_keys: set) -> None:
    """Injects CSS rules targeting each opened-file button by its Streamlit key."""
    if not opened_keys:
        return

    # Build one CSS rule per opened button key
    rules = []
    for key in opened_keys:
        selector = f'[data-testid="stButton"] button[kind="secondary"][id$="{key}"]'
        rules.append(f"""
            div:has(> [data-testid="stBaseButton-secondary"][key="{key}"]) button,
            div[data-testid="stBaseButton-secondary"] + div button
            {{ }}
        """)

    # Target by aria-label fallback: use key embedded in button label via unique prefix
    css_blocks = "\n".join(
        f'[data-testid="stBaseButton-secondary"][aria-label="{key}"] {{ '
        f'background-color: #1f6aa5 !important; color: white !important; '
        f'border: 2px solid #1a5a8f !important; }}'
        for key in opened_keys
    )
    st.markdown(f"<style>{css_blocks}</style>", unsafe_allow_html=True)


def _file_button(label: str, button_key: str, filepath: str) -> None:
    """Renders a file button, highlighted if already opened."""
    opened = st.session_state.get("opened_files", set())
    is_opened = button_key in opened

    # Use button type to visually distinguish state
    btn_type = "primary" if is_opened else "secondary"

    if st.button(label, key=button_key, use_container_width=True, type=btn_type):
        if not is_opened:
            _send_file_to_chat(filepath, button_key)


def _send_file_to_chat(filepath: str, button_key: str) -> None:
    """Reads a file and appends its content to the chat as a user message."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        filename = os.path.basename(filepath)
        message = f"📄 `{filename}`\n```python\n{content}\n```"
        st.session_state.messages.append({"role": "user", "content": message})

        if "opened_files" not in st.session_state:
            st.session_state.opened_files = set()
        st.session_state.opened_files.add(button_key)

        st.rerun()
    except Exception as e:
        st.error(f"Error reading file '{filepath}': {e}")


def _render_coding_context() -> None:
    """Scans Python files and renders each as a clickable button."""
    base_path = os.getcwd()
    try:
        root_files = [f for f in os.listdir(base_path) if f.endswith(".py")]
        for f in sorted(root_files):
            _file_button(f"📄 {f}", f"root_{f}", os.path.join(base_path, f))

        core_path = os.path.join(base_path, "core")
        if os.path.exists(core_path):
            core_files = [f for f in os.listdir(core_path) if f.endswith(".py")]
            for f in sorted(core_files):
                _file_button(f"⚙️ core/{f}", f"core_{f}", os.path.join(core_path, f))
        else:
            st.error("Folder `/core` not found.")
    except Exception as e:
        st.error(f"Error scanning workspace: {e}")


def _render_3d_tools() -> None:
    """Renders tools and assets for 3D Projects."""
    st.markdown("#### 🛠️ 3D Tools")
    st.button("Scan Assets", use_container_width=True)
    for i in range(15):
        st.caption(f"Asset_{i:02d}.obj - Ready")