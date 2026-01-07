import streamlit as st
from ui.login import init_authenticator, show_login_page, show_logout_button
from ui.lab import show_lab

# Initialize authenticator
authenticator = init_authenticator()

# Check authentication status
if not show_login_page(authenticator):
    st.stop()

# Show logout button
show_logout_button(authenticator)

# Display the lab
show_lab()