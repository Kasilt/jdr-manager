"""Admin page for managing access requests."""

import streamlit as st
import sqlite3
import streamlit_authenticator as stauth
import secrets
from pathlib import Path
from datetime import datetime

# Chemin vers la base de données
DB_PATH = Path(__file__).parent.parent.parent / "jdr_data.db"


def get_pending_requests():
    """Get all pending AND approved access requests from database.
    
    Excludes ACTIVE requests (users who completed first login).
    
    Returns:
        list: List of tuples (username, email, request_date, temp_password, status)
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        requests = c.execute('''
            SELECT username, email, request_date, temp_password, status
            FROM requests
            WHERE status IN ('PENDING', 'APPROVED')
            ORDER BY status DESC, request_date DESC
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
        temp_password = secrets.token_urlsafe(6)  # Produces 8 chars
        
        # Hash the temporary password
        hashed_pass = stauth.Hasher().hash(temp_password)
        
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        # Check if username already exists (safety check)
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
        
        # Update request status and save temp_password in clear text
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
        
        # Update request status
        c.execute('''
            UPDATE requests
            SET status = 'REJECTED'
            WHERE username = ?
        ''', (username,))
        
        conn.commit()
        conn.close()
        
        return True, f"❌ Demande rejetée pour '{username}'"
    
    except Exception as e:
        return False, f"Erreur : {str(e)}"


def show_admin_requests_panel():
    """Display the admin panel for managing access requests."""
    st.markdown("## 👑 Gestion des Demandes d'Accès")
    st.markdown("---")
    
    # Get all pending and approved requests
    all_requests = get_pending_requests()
    
    if not all_requests:
        st.info("✅ Aucune demande en attente", icon="ℹ️")
        return
    
    # Séparer les demandes par statut
    pending_requests = [r for r in all_requests if r[4] == 'PENDING']
    approved_requests = [r for r in all_requests if r[4] == 'APPROVED']
    
    # Afficher les demandes en attente de validation
    if pending_requests:
        st.markdown("### 🔔 En Attente de Validation")
        st.markdown(f"**{len(pending_requests)} demande(s) en attente**")
        st.markdown("---")
        
        for username, email, request_date, temp_password, status in pending_requests:
            with st.container(border=True):
                col1, col2, col3 = st.columns([2, 1, 1])
                
                with col1:
                    st.markdown(f"**Identifiant** : `{username}`")
                    st.markdown(f"**Email** : {email}")
                    st.caption(f"Demande du : {request_date}")
                
                with col2:
                    if st.button("✅ Approuver", key=f"approve_{username}", use_container_width=True):
                        success, message, new_temp_password = approve_request(username, email)
                        if success:
                            st.success(message)
                            st.info(
                                f"🔐 **Mot de passe temporaire** : `{new_temp_password}`\n\n"
                                f"À envoyer à {email}",
                                icon="📧"
                            )
                            st.rerun()
                        else:
                            st.error(message)
                
                with col3:
                    if st.button("❌ Rejeter", key=f"reject_{username}", use_container_width=True):
                        success, message = reject_request(username)
                        if success:
                            st.info(message)
                            st.rerun()
                        else:
                            st.error(message)
    
    # Afficher les demandes approuvées (en attente de 1ère connexion)
    if approved_requests:
        st.markdown("### ⏳ Approuvées - En Attente de Première Connexion")
        st.markdown(f"**{len(approved_requests)} demande(s) approuvée(s)**")
        st.markdown("---")
        
        for username, email, request_date, temp_password, status in approved_requests:
            with st.container(border=True):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"**Identifiant** : `{username}`")
                    st.markdown(f"**Email** : {email}")
                    st.caption(f"Approuvé le : {request_date}")
                    
                    # Afficher le MDP temporaire
                    if temp_password:
                        st.success(
                            f"🔐 **Mot de passe temporaire** : `{temp_password}`\n\n"
                            f"*(Cliquez sur le code pour copier)*",
                            icon="✅"
                        )
                    else:
                        st.warning("⚠️ Pas de mot de passe temporaire trouvé", icon="⚠️")
                
                with col2:
                    if st.button("📋 Copier MDP", key=f"copy_{username}", use_container_width=True):
                        if temp_password:
                            st.info(f"Mot de passe à copier : `{temp_password}`", icon="📋")
                        else:
                            st.error("Pas de mot de passe disponible")
                    
                    if st.button("🔄 Régénérer", key=f"regenerate_{username}", use_container_width=True):
                        # Régénérer un nouveau MDP
                        new_temp_password = secrets.token_urlsafe(6)
                        hashed_pass = stauth.Hasher().hash(new_temp_password)
                        
                        try:
                            conn = sqlite3.connect(DB_PATH)
                            c = conn.cursor()
                            
                            # Mettre à jour le MDP dans requests
                            c.execute(
                                'UPDATE requests SET temp_password = ? WHERE username = ?',
                                (new_temp_password, username)
                            )
                            
                            # Mettre à jour le hash dans users
                            c.execute(
                                'UPDATE users SET password_hash = ? WHERE username = ?',
                                (hashed_pass, username)
                            )
                            
                            conn.commit()
                            conn.close()
                            
                            st.success(f"✅ Nouveau mot de passe généré : `{new_temp_password}`", icon="🔄")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Erreur : {str(e)}")
