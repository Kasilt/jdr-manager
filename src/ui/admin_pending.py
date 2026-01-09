"""Admin - Pending requests page."""

import streamlit as st
import sqlite3
import streamlit_authenticator as stauth
import secrets
from pathlib import Path

DB_PATH = Path(__file__).parent.parent.parent / "jdr_data.db"


def get_pending_requests():
    """Get all pending access requests from database.
    
    Returns:
        list: List of tuples (username, email, request_date, temp_password, status)
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        requests = c.execute('''
            SELECT username, email, request_date, temp_password, status
            FROM requests
            WHERE status = 'PENDING'
            ORDER BY request_date DESC
        ''').fetchall()
        
        conn.close()
        return requests
    except Exception as e:
        st.error(f"Erreur : {e}")
        return []


def approve_request(username: str, email: str) -> tuple[bool, str, str]:
    """Approve an access request and generate temporary password.
    
    Returns:
        tuple: (success: bool, message: str, temp_password: str)
    """
    try:
        # Generate temporary password (8 chars, alphanumeric + special chars)
        temp_password = secrets.token_urlsafe(6)
        
        # Hash the temporary password
        hashed_pass = stauth.Hasher().hash(temp_password)
        
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        # Check if username already exists
        existing = c.execute(
            "SELECT 1 FROM users WHERE username = ?", (username,)
        ).fetchone()
        
        if existing:
            return False, f"❌ L'utilisateur '{username}' existe déjà", ""
        
        # Create user with temporary password
        c.execute('''
            INSERT INTO users (username, name, email, password_hash, role, must_change_password)
            VALUES (?, ?, ?, ?, 'joueur', 1)
        ''', (username, username, email, hashed_pass))
        
        # Update request status and save temp_password
        c.execute('''
            UPDATE requests
            SET status = 'APPROVED', temp_password = ?
            WHERE username = ?
        ''', (temp_password, username))
        
        conn.commit()
        conn.close()
        
        return True, f"✅ Accès approuvé pour '{username}'", temp_password
    
    except sqlite3.IntegrityError as e:
        return False, f"❌ Erreur d'intégrité : {str(e)}", ""
    except Exception as e:
        return False, f"❌ Erreur : {str(e)}", ""


def reject_request(username: str) -> tuple[bool, str]:
    """Reject an access request.
    
    Returns:
        tuple: (success: bool, message: str)
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        c.execute('''
            UPDATE requests
            SET status = 'REJECTED'
            WHERE username = ?
        ''', (username,))
        
        conn.commit()
        conn.close()
        
        return True, f"✅ Demande '{username}' rejetée"
    except Exception as e:
        return False, f"❌ Erreur : {str(e)}"


def show_pending_requests_page():
    """Display pending access requests."""
    st.title("🔔 Demandes en Attente")
    st.divider()
    
    requests = get_pending_requests()
    
    if not requests:
        st.info("✅ Aucune demande en attente")
        return
    
    st.subheader(f"📋 {len(requests)} demande(s) en attente")
    
    for username, email, request_date, _, status in requests:
        with st.container(border=True):
            col1, col2, col3 = st.columns([2, 2, 1])
            
            with col1:
                st.markdown(f"### {username}")
                st.caption(f"📧 {email}")
            
            with col2:
                st.caption(f"📅 Demande du : {request_date}")
            
            with col3:
                col_a, col_b = st.columns(2)
                
                with col_a:
                    if st.button("✅ Approuver", key=f"approve_{username}"):
                        success, message, temp_password = approve_request(username, email)
                        if success:
                            st.success(f"{message}\n🔐 MDP: `{temp_password}`")
                            st.rerun()
                        else:
                            st.error(message)
                
                with col_b:
                    if st.button("❌ Rejeter", key=f"reject_{username}"):
                        success, message = reject_request(username)
                        if success:
                            st.success(message)
                            st.rerun()
                        else:
                            st.error(message)
