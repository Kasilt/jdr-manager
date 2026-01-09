"""Admin - Approved requests page."""

import streamlit as st
import sqlite3
import streamlit_authenticator as stauth
import secrets
from pathlib import Path

DB_PATH = Path(__file__).parent.parent.parent / "jdr_data.db"


def get_approved_requests():
    """Get all approved access requests from database.
    
    Returns:
        list: List of tuples (username, email, request_date, temp_password, status)
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        requests = c.execute('''
            SELECT username, email, request_date, temp_password, status
            FROM requests
            WHERE status = 'APPROVED'
            ORDER BY request_date DESC
        ''').fetchall()
        
        conn.close()
        return requests
    except Exception as e:
        st.error(f"Erreur : {e}")
        return []


def regenerate_password(username: str) -> tuple[bool, str, str]:
    """Regenerate temporary password for approved request.
    
    Returns:
        tuple: (success: bool, message: str, new_password: str)
    """
    try:
        # Generate new temporary password
        new_password = secrets.token_urlsafe(6)
        
        # Hash the new password
        hashed_pass = stauth.Hasher().hash(new_password)
        
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        # Update both tables
        c.execute('''
            UPDATE requests
            SET temp_password = ?
            WHERE username = ?
        ''', (new_password, username))
        
        c.execute('''
            UPDATE users
            SET password_hash = ?
            WHERE username = ?
        ''', (hashed_pass, username))
        
        conn.commit()
        conn.close()
        
        return True, f"✅ Nouveau mot de passe généré", new_password
    except Exception as e:
        return False, f"❌ Erreur : {str(e)}", ""


def show_approved_requests_page():
    """Display approved access requests awaiting first login."""
    st.title("⏳ Demandes Approuvées - En Attente 1ère Connexion")
    st.divider()
    
    requests = get_approved_requests()
    
    if not requests:
        st.info("✅ Aucune demande approuvée en attente")
        return
    
    st.subheader(f"📋 {len(requests)} demande(s) approuvée(s)")
    
    for username, email, request_date, temp_password, status in requests:
        with st.container(border=True):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"### {username}")
                st.caption(f"📧 {email}")
                st.caption(f"📅 Approuvé le : {request_date}")
            
            with col2:
                if temp_password:
                    st.success(f"🔐 **MDP Temporaire**\n`{temp_password}`")
                else:
                    st.warning("⚠️ Pas de MDP trouvé")
            
            col_a, col_b = st.columns(2)
            
            with col_a:
                if st.button("📋 Copier MDP", key=f"copy_{username}", 
                             help="Afficher le mot de passe pour copier"):
                    st.info(f"Mot de passe : **{temp_password}**")
            
            with col_b:
                if st.button("🔄 Régénérer", key=f"regen_{username}",
                             help="Générer un nouveau mot de passe"):
                    success, message, new_password = regenerate_password(username)
                    if success:
                        st.success(f"{message}\n🔐 Nouveau MDP: `{new_password}`")
                        st.rerun()
                    else:
                        st.error(message)
