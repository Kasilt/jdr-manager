"""Navigation module for sidebar menu and page routing."""

import streamlit as st
import sqlite3
from pathlib import Path

# Chemin vers la base de données
DB_PATH = Path(__file__).parent.parent.parent / "jdr_data.db"


def get_user_role(username: str) -> str:
    """Get user role from database.
    
    Args:
        username: The username to check
    
    Returns:
        str: 'admin' or 'joueur' or 'unknown'
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        result = c.execute(
            "SELECT role FROM users WHERE username = ?",
            (username,)
        ).fetchone()
        
        conn.close()
        return result[0] if result else "unknown"
    except Exception:
        return "unknown"


def show_sidebar_menu(authenticator):
    """Display the sidebar menu with navigation options.
    
    Args:
        authenticator: The Streamlit authenticator instance
    """
    with st.sidebar:
        # Logo and title section
        st.markdown("### 🧙‍♂️ JDR Manager")
        
        # Get current user info
        username = st.session_state.get("username")
        user_role = get_user_role(username) if username else "unknown"
        st.caption(f"👤 {username} • {user_role}", unsafe_allow_html=True)
        
        st.divider()
        
        # Initialize page session state
        if "current_page" not in st.session_state:
            st.session_state["current_page"] = "home"
        
        current_page = st.session_state.get("current_page", "home")
        
        # Build menu options based on role
        menu_options = {
            "🏠 Home": "home",
            "⚙️ Paramètres": "settings",
            "📋 Mes Personnages": "characters",
            "🎭 Campagnes": "campaigns",
        }
        
        # Add admin options if admin
        if user_role == "admin":
            menu_options["🔔 Demandes en Attente"] = "pending_requests"
            menu_options["⏳ Demandes Approuvées"] = "approved_requests"
        
        # Find current page label
        current_label = None
        for label, page in menu_options.items():
            if page == current_page:
                current_label = label
                break
        
        if current_label is None:
            current_label = "🏠 Home"
        
        # Menu selectbox
        selected = st.selectbox(
            "Navigation",
            options=list(menu_options.keys()),
            index=list(menu_options.keys()).index(current_label) if current_label in menu_options else 0,
            label_visibility="collapsed"
        )
        
        # Handle selection
        if selected in menu_options:
            new_page = menu_options[selected]
            if new_page != current_page:
                st.session_state["current_page"] = new_page
                st.rerun()
        
        st.divider()
        
        # Mode MJ toggle
        mode_mj = st.toggle("🎭 Mode Maître du Jeu")
        st.session_state["mode_mj"] = mode_mj
        
        st.divider()
        
        # Logout button
        if st.button("🚪 Logout", use_container_width=True):
            authenticator.logout(location="unrendered")
            st.session_state["authentication_status"] = False
            st.rerun()
