"""Login interface using streamlit_authenticator."""

import streamlit as st
import streamlit_authenticator as stauth
import sqlite3
from pathlib import Path

# Chemin vers la base de données
DB_PATH = Path(__file__).parent.parent.parent / "jdr_data.db"


def get_credentials_from_db():
    """Get credentials from database.
    
    Returns:
        dict: Credentials in the format expected by streamlit_authenticator
    """
    credentials = {
        "usernames": {}
    }
    
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        # Get all active users (not pending requests)
        users = c.execute('''
            SELECT username, name, password_hash, must_change_password
            FROM users
            ORDER BY username
        ''').fetchall()
        
        for username, name, password_hash, must_change_password in users:
            credentials["usernames"][username] = {
                "name": name or username,
                "password": password_hash,
                "must_change_password": bool(must_change_password)
            }
        
        conn.close()
    except Exception as e:
        st.error(f"Erreur de connexion à la base de données : {e}")
    
    return credentials


def init_authenticator():
    """Initialize the authenticator with credentials from database."""
    credentials = get_credentials_from_db()
    
    authenticator = stauth.Authenticate(
        credentials,
        cookie_name="jdr_manager_cookie",
        key="jdr_manager_key",
        cookie_expiry_days=30
    )
    
    return authenticator


def show_login_page(authenticator):
    """Display the login form and handle authentication.
    
    Returns:
        bool: True if user is authenticated, False otherwise.
    """
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("## 🧙‍♂️ JDR Manager")
        st.markdown("### Connexion")
        
        try:
            authenticator.login(location="main")
        except Exception as e:
            st.error(f"Erreur d'authentification : {e}")
            return False
        
        # Add link to access request
        st.markdown("---")
        col_login, col_request = st.columns(2)
        
        with col_request:
            if st.button("📝 Demande d'accès", use_container_width=True):
                st.session_state["show_access_request"] = True
                st.rerun()
    
    # Check if user is authenticated
    if st.session_state.get("authentication_status"):
        # Check if user must change password
        username = st.session_state.get("username")
        if username:
            # Query database to get must_change_password flag
            try:
                conn = sqlite3.connect(DB_PATH)
                c = conn.cursor()
                result = c.execute(
                    "SELECT must_change_password FROM users WHERE username = ?",
                    (username,)
                ).fetchone()
                conn.close()
                
                if result and result[0]:
                    st.session_state["must_change_password"] = True
            except Exception as e:
                st.error(f"Erreur : {e}")
        
        return True
    elif st.session_state.get("authentication_status") is False:
        st.error("❌ Identifiant ou mot de passe incorrect")
        return False
    
    return False


def show_logout_button(authenticator):
    """Display logout button in sidebar."""
    if st.session_state.get("authentication_status"):
        with st.sidebar:
            authenticator.logout(location="sidebar")
