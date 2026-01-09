import streamlit as st
from ui.login import init_authenticator
from ui.access_request import show_access_request_page
from ui.password_change import show_first_login_password_change
from ui.navigation import show_sidebar_menu
from ui.home import show_home_page
from ui.settings import show_settings_page
from ui.characters import show_characters_page
from ui.campaigns import show_campaigns_page
from ui.admin_pending import show_pending_requests_page
from ui.admin_approved import show_approved_requests_page

# Initialize session state for access request page
if "show_access_request" not in st.session_state:
    st.session_state["show_access_request"] = False

# Initialize session state for admin panel
if "show_admin_panel" not in st.session_state:
    st.session_state["show_admin_panel"] = False

# Initialize current page
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "home"

# Track previous authentication state to detect fresh logins
if "_prev_auth" not in st.session_state:
    st.session_state["_prev_auth"] = False

# Show access request page if user clicked on it
if st.session_state["show_access_request"]:
    show_access_request_page()
    st.stop()

# Initialize authenticator
authenticator = init_authenticator()

# Check authentication status
if not st.session_state.get("authentication_status"):
    # Show login page only if not authenticated
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("## 🧙‍♂️ JDR Manager")
        st.markdown("### Connexion")
        
        try:
            authenticator.login(location="main")
        except Exception as e:
            st.error(f"Erreur d'authentification : {e}")
        
        # Add link to access request
        st.markdown("---")
        col_login, col_request = st.columns(2)
        
        with col_request:
            if st.button("📝 Demande d'accès", use_container_width=True):
                st.session_state["show_access_request"] = True
                st.rerun()
    
    st.stop()

# Check authentication status again after login attempt
if not st.session_state.get("authentication_status"):
    st.stop()

# If user just logged in (transition False -> True), force landing on home
if st.session_state.get("authentication_status") and not st.session_state.get("_prev_auth"):
    st.session_state["current_page"] = "home"

# Update previous auth state
st.session_state["_prev_auth"] = bool(st.session_state.get("authentication_status"))

# Check if user must change password on first login
if st.session_state.get("authentication_status") and st.session_state.get("must_change_password", False):
    username = st.session_state.get("username")
    show_first_login_password_change(username)
    st.stop()

# Show sidebar menu
show_sidebar_menu(authenticator)

# Route to the appropriate page
page = st.session_state.get("current_page", "home")

if page == "home":
    show_home_page()
elif page == "settings":
    show_settings_page()
elif page == "characters":
    show_characters_page()
elif page == "campaigns":
    show_campaigns_page()
elif page == "pending_requests":
    show_pending_requests_page()
elif page == "approved_requests":
    show_approved_requests_page()
else:
    show_home_page()