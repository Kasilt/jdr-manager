"""Password change page for first login."""

import streamlit as st
import sqlite3
import streamlit_authenticator as stauth
from pathlib import Path

# Chemin vers la base de données
DB_PATH = Path(__file__).parent.parent.parent / "jdr_data.db"


def validate_password(password: str) -> tuple[bool, str]:
    """Validate password requirements.
    
    Returns:
        tuple: (is_valid: bool, message: str)
    """
    if len(password) < 8:
        return False, "Le mot de passe doit contenir au moins 8 caractères"
    
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    
    if not (has_upper and has_lower and has_digit):
        return False, "Le mot de passe doit contenir des majuscules, minuscules et chiffres"
    
    return True, "✅ Mot de passe valide"


def change_password_first_login(username: str, new_password: str) -> tuple[bool, str]:
    """Change password for first login and clear must_change_password flag.
    
    Also marks the access request as ACTIVE (completed first login).
    
    Returns:
        tuple: (success: bool, message: str)
    """
    is_valid, message = validate_password(new_password)
    if not is_valid:
        return False, f"❌ {message}"
    
    try:
        # Hash the new password
        hashed_pass = stauth.Hasher().hash(new_password)
        
        # Update in database
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        # Update user password and clear flag
        c.execute('''
            UPDATE users
            SET password_hash = ?, must_change_password = 0
            WHERE username = ?
        ''', (hashed_pass, username))
        
        # Mark access request as ACTIVE (first login completed)
        c.execute('''
            UPDATE requests
            SET status = 'ACTIVE'
            WHERE username = ? AND status = 'APPROVED'
        ''', (username,))
        
        conn.commit()
        conn.close()
        
        return True, "✅ Mot de passe changé avec succès !"
    
    except Exception as e:
        return False, f"❌ Erreur lors du changement de mot de passe : {str(e)}"


def show_first_login_password_change(username: str):
    """Display the first login password change form.
    
    Args:
        username: The username of the connected user
    """
    st.warning(
        "⚠️ Vous devez changer votre mot de passe avant de continuer",
        icon="⚠️"
    )
    
    st.markdown("## 🔐 Changement de mot de passe obligatoire")
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown(f"**Utilisateur** : {username}")
        st.markdown("**Exigences** :")
        st.markdown("- Au moins 8 caractères")
        st.markdown("- Au moins une majuscule")
        st.markdown("- Au moins une minuscule")
        st.markdown("- Au moins un chiffre")
        
        st.markdown("---")
        
        new_password = st.text_input(
            "Nouveau mot de passe",
            type="password",
            key="new_password"
        )
        
        confirm_password = st.text_input(
            "Confirmer le mot de passe",
            type="password",
            key="confirm_password"
        )
        
        if st.button("🔐 Changer le mot de passe", use_container_width=True):
            if not new_password or not confirm_password:
                st.error("❌ Veuillez remplir tous les champs")
            elif new_password != confirm_password:
                st.error("❌ Les mots de passe ne correspondent pas")
            else:
                success, message = change_password_first_login(username, new_password)
                if success:
                    st.success(message)
                    st.session_state["must_change_password"] = False
                    st.rerun()
                else:
                    st.error(message)
