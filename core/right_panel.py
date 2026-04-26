import streamlit as st
import os
from typing import Dict, Any

def render_right_panel(config: Dict[str, Any], selected_mode: str) -> None:
    """
    Renders the right-side information panel with independent scrolling.
    """
    st.markdown("### 🧊 Project Dashboard")
    
    # Independent scrollable container
    with st.container(height=650, border=True):
        # Normalize mode string
        mode = str(selected_mode).strip().lower()
        
        if "3d" in mode:
            _render_3d_tools()
        else:
            _render_coding_context()

def _render_coding_context() -> None:
    """
    Scans and lists Python files in the root and core directories.
    """
    st.markdown("#### 🐍 Python Workspace")
    base_path = os.getcwd()
    
    try:
        # 1. Root Files
        st.markdown("**Root Directory**")
        root_files = [f for f in os.listdir(base_path) if f.endswith(".py")]
        if root_files:
            for f in sorted(root_files):
                st.caption(f"📄 {f}")
        else:
            st.caption("No .py files found in root.")

        st.divider()

        # 2. Core Subdirectory
        st.markdown("**Core Subdirectory**")
        core_path = os.path.join(base_path, "core")
        
        if os.path.exists(core_path):
            core_files = [f for f in os.listdir(core_path) if f.endswith(".py")]
            if core_files:
                for f in sorted(core_files):
                    st.caption(f"⚙️ {f}")
            else:
                st.caption("No .py files found in /core.")
        else:
            st.error("Folder `/core` not found.")

    except Exception as e:
        st.error(f"Error scanning workspace: {e}")

def _render_3d_tools() -> None:
    """
    Renders tools and assets for 3D Projects.
    """
    st.markdown("#### 🛠️ 3D Tools")
    st.button("Scan Assets", use_container_width=True)
    
    st.write("Project assets (.obj):")
    for i in range(15):
        st.caption(f"Asset_{i:02d}.obj - Ready")