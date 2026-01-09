"""Account settings page."""

import streamlit as st
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent.parent / "jdr_data.db"


def show_settings_page():
    """Display the account settings page."""
    st.title("⚙️ Paramètres du Compte")
    st.divider()
    
    username = st.session_state.get("username", "Utilisateur")
    
    # Get user email
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        user = c.execute(
            "SELECT name, email FROM users WHERE username = ?",
            (username,)
        ).fetchone()
        conn.close()
        
        user_name = user[0] if user else username
        user_email = user[1] if user else "Non défini"
    except Exception:
        user_name = username
        user_email = "Non défini"
    
    # Display user info
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 👤 Informations de Compte")
        st.write(f"**Nom d'utilisateur** : {username}")
        st.write(f"**Nom complet** : {user_name}")
        st.write(f"**Email** : {user_email}")
    
    with col2:
        st.markdown("### 🔒 Sécurité")
        with st.form("password_form"):
            new_password = st.text_input("Nouveau mot de passe", type="password")
            confirm_password = st.text_input("Confirmer le mot de passe", type="password")
            
            if st.form_submit_button("Changer le mot de passe", type="primary"):
                if not new_password or not confirm_password:
                    st.error("❌ Veuillez remplir tous les champs")
                elif new_password != confirm_password:
                    st.error("❌ Les mots de passe ne correspondent pas")
                else:
                    st.success("✅ Mot de passe changé (fonctionnalité à implémenter)")
    
    st.divider()
    
    st.markdown("### 🎨 Préférences")
    col1, col2 = st.columns(2)
    
    with col1:
        theme = st.selectbox("Thème", ["Clair", "Sombre", "Auto"])
    
    with col2:
        language = st.selectbox("Langue", ["Français", "English"])
    
    st.divider()
    
    st.markdown("### 📊 Statistiques")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Personnages", 3)
    with col2:
        st.metric("Campagnes", 2)
    with col3:
        st.metric("Combats", 5)
    with col4:
        st.metric("Connexions", 12)
