"""Access request page for new users to register."""

import streamlit as st
import sqlite3
import re
from pathlib import Path

# Chemin vers la base de données
DB_PATH = Path(__file__).parent.parent.parent / "jdr_data.db"


def validate_email(email: str) -> bool:
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_username(username: str) -> bool:
    """Validate username format (alphanumeric, underscore, 3-20 chars)."""
    if len(username) < 3 or len(username) > 20:
        return False
    return re.match(r'^[a-zA-Z0-9_]+$', username) is not None


def username_exists(username: str) -> bool:
    """Check if username already exists in users or requests table."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Vérifier dans users et requests
    user_exists = c.execute(
        "SELECT 1 FROM users WHERE username = ?", (username,)
    ).fetchone()
    
    request_exists = c.execute(
        "SELECT 1 FROM requests WHERE username = ?", (username,)
    ).fetchone()
    
    conn.close()
    
    return user_exists is not None or request_exists is not None


def email_has_pending_request(email: str) -> bool:
    """Check if email already has a pending request."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    existing = c.execute(
        "SELECT 1 FROM requests WHERE email = ? AND status = 'PENDING'", (email,)
    ).fetchone()
    
    conn.close()
    
    return existing is not None


def submit_access_request(username: str, email: str) -> tuple[bool, str]:
    """Submit an access request to the database.
    
    Returns:
        tuple: (success: bool, message: str)
    """
    # Validations
    if not validate_username(username):
        return False, "❌ L'identifiant doit contenir 3-20 caractères (lettres, chiffres, tiret bas uniquement)"
    
    if not validate_email(email):
        return False, "❌ Veuillez entrer une adresse email valide"
    
    if username_exists(username):
        return False, "❌ Cet identifiant est déjà pris ou en attente de validation"
    
    if email_has_pending_request(email):
        return False, "⏳ Une demande d'accès est déjà en cours pour cet email"
    
    # Insérer la demande dans la base de données
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        c.execute('''
            INSERT INTO requests (username, email, status)
            VALUES (?, ?, 'PENDING')
        ''', (username, email))
        
        conn.commit()
        conn.close()
        
        return True, "✅ Demande d'accès envoyée ! L'administrateur vous contactera bientôt."
    
    except sqlite3.IntegrityError as e:
        return False, f"❌ Erreur lors de l'enregistrement : {str(e)}"
    except Exception as e:
        return False, f"❌ Erreur serveur : {str(e)}"


def show_access_request_page() -> bool:
    """Display the access request form.
    
    Returns:
        bool: True if user wants to go back to login, False otherwise.
    """
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("## 🧙‍♂️ JDR Manager")
        st.markdown("### Demande d'accès")
        st.markdown("---")
        
        # Input fields
        username = st.text_input(
            "Identifiant de votre choix",
            key="access_username",
            placeholder="mon_perso",
            help="3-20 caractères (lettres, chiffres, tiret bas)"
        )
        
        email = st.text_input(
            "Adresse email",
            key="access_email",
            placeholder="joueur@example.com",
            help="Vous recevrez un mot de passe temporaire à cette adresse"
        )
        
        st.markdown("---")
        
        # Buttons
        col_submit, col_back = st.columns(2)
        
        with col_submit:
            if st.button("📤 Envoyer ma demande", use_container_width=True):
                if username and email:
                    success, message = submit_access_request(username, email)
                    if success:
                        st.success(message)
                        st.session_state["access_request_sent"] = True
                    else:
                        st.error(message)
                else:
                    st.error("❌ Veuillez remplir tous les champs")
        
        with col_back:
            if st.button("⬅️ Retour au login", use_container_width=True):
                st.session_state["show_access_request"] = False
                st.rerun()
        
        # Message si demande déjà envoyée
        if st.session_state.get("access_request_sent"):
            st.info(
                "📧 Votre demande a été enregistrée. "
                "L'administrateur vous enverra un mot de passe temporaire par email.",
                icon="ℹ️"
            )
