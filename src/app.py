import streamlit as st
from ui.login import init_authenticator, show_login_page, show_logout_button
from ui.access_request import show_access_request_page
from ui.password_change import show_first_login_password_change
from ui.lab import show_lab

# Initialize session state for access request page
if "show_access_request" not in st.session_state:
    st.session_state["show_access_request"] = False

# Show access request page if user clicked on it
if st.session_state["show_access_request"]:
    show_access_request_page()
    st.stop()

# Initialize authenticator
authenticator = init_authenticator()

# Check authentication status
if not show_login_page(authenticator):
    st.stop()

# Check if user must change password on first login
if st.session_state.get("authentication_status") and st.session_state.get("must_change_password", False):
    username = st.session_state.get("username")
    show_first_login_password_change(username)
    st.stop()

# Show logout button
show_logout_button(authenticator)

# Display the lab
show_lab()