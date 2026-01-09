"""Characters page - List and manage characters."""

import streamlit as st
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent.parent / "jdr_data.db"


def show_characters_page():
    """Display the characters list page."""
    st.title("📜 Mes Personnages")
    st.divider()
    
    username = st.session_state.get("username")
    
    # Fetch characters from database
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        characters = c.execute('''
            SELECT id, nom_perso, classe, pv_actuel, pv_max, xp
            FROM characters
            WHERE username = ?
            ORDER BY nom_perso
        ''', (username,)).fetchall()
        
        conn.close()
    except Exception as e:
        st.error(f"Erreur : {e}")
        characters = []
    
    # Create new character button
    col1, col2 = st.columns([4, 1])
    
    with col2:
        if st.button("➕ Nouveau Personnage", use_container_width=True, type="primary"):
            st.session_state["show_new_character_form"] = True
    
    st.divider()
    
    # Show new character form if requested
    if st.session_state.get("show_new_character_form", False):
        with st.form("new_character_form"):
            st.subheader("➕ Créer un Nouveau Personnage")
            
            nom = st.text_input("Nom du Personnage")
            classe = st.selectbox("Classe", ["Guerrier", "Mage", "Voleur", "Prêtre", "Rôdeur"])
            pv_max = st.number_input("Points de Vie Max", min_value=1, value=20)
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.form_submit_button("✅ Créer", type="primary", use_container_width=True):
                    if nom:
                        st.success(f"✅ Personnage '{nom}' créé!")
                        st.session_state["show_new_character_form"] = False
                    else:
                        st.error("❌ Veuillez entrer un nom")
            
            with col2:
                if st.form_submit_button("❌ Annuler", use_container_width=True):
                    st.session_state["show_new_character_form"] = False
    
    st.divider()
    
    # Display characters
    if characters:
        st.subheader(f"📋 Vos Personnages ({len(characters)})")
        
        for char_id, nom, classe, pv_actuel, pv_max, xp in characters:
            with st.container(border=True):
                col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
                
                with col1:
                    st.markdown(f"### {nom}")
                    st.caption(f"**Classe** : {classe}")
                
                with col2:
                    st.metric("PV", f"{pv_actuel}/{pv_max}")
                
                with col3:
                    st.metric("XP", xp if xp else 0)
                
                with col4:
                    col_a, col_b = st.columns(2)
                    with col_a:
                        if st.button("✏️", key=f"edit_{char_id}", help="Éditer"):
                            st.info("Édition - À implémenter")
                    with col_b:
                        if st.button("🗑️", key=f"delete_{char_id}", help="Supprimer"):
                            st.warning("Suppression - À implémenter")
    else:
        st.info("📭 Vous n'avez pas encore de personnage. Créez-en un pour commencer!")
