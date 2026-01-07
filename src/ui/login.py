"""Login interface using streamlit_authenticator."""

import streamlit as st
import streamlit_authenticator as stauth


def init_authenticator():
    """Initialize the authenticator with hardcoded credentials for demo.
    
    In production, these should come from a database.
    """
    # Demo credentials (plaintext for now - will be hashed by Authenticate)
    credentials = {
        "usernames": {
            "alice": {
                "name": "Alice Dupont",
                "password": "alice123"
            },
            "bob": {
                "name": "Bob Martin",
                "password": "bob123"
            }
        }
    }
    
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
    
    # Check if user is authenticated
    if st.session_state.get("authentication_status"):
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
