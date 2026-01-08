"""JDR Component Laboratory - Demonstrating Streamlit UI patterns."""

import streamlit as st
import sqlite3
from pathlib import Path
from ui.admin import show_admin_requests_panel

# Chemin vers la base de données
DB_PATH = Path(__file__).parent.parent.parent / "jdr_data.db"


def get_user_role(username: str) -> str:
    """Get user role from database.
    
    Args:
        username: The username to check
    
    Returns:
        str: 'admin' or 'joueur' or 'unknown'
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        result = c.execute(
            "SELECT role FROM users WHERE username = ?",
            (username,)
        ).fetchone()
        
        conn.close()
        return result[0] if result else "unknown"
    except Exception:
        return "unknown"


def show_lab():
    """Display the JDR component laboratory with UI examples."""
    
    st.title("🧙‍♂️ Laboratoire de Composants JDR")
    
    # Get current user info
    username = st.session_state.get("username")
    user_role = get_user_role(username) if username else "unknown"

    # 1. La Barre latérale (Sidebar) - Parfait pour les menus ou infos fixes
    with st.sidebar:
        st.header("Fiche technique")
        st.caption(f"👤 {username} ({user_role})")
        mode_mj = st.toggle("Mode Maître du Jeu")  # Un interrupteur moderne

    # 2. Check if user is admin
    if user_role == "admin":
        tab1, tab2, tab_admin = st.tabs(["🎒 Inventaire", "📜 Sorts / Compétences", "👑 Administration"])
        
        with tab_admin:
            show_admin_requests_panel()
    else:
        tab1, tab2 = st.tabs(["🎒 Inventaire", "📜 Sorts / Compétences"])

    # 2. Les Colonnes (Pour ne pas avoir une liste verticale infinie)
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Attributs")
        nom = st.text_input("Nom du Personnage", value="Conan")
        # number_input avec min, max et valeur par défaut
        force = st.number_input("Force", min_value=1, max_value=20, value=10)
        
    with col2:
        st.subheader("Détails")
        # Une liste déroulante
        classe = st.selectbox("Classe", ["Guerrier", "Mage", "Voleur"])
        # Une jauge visuelle (slider)
        pv = st.slider("Points de Vie actuels", 0, 50, 25)

    st.divider()  # Une ligne de séparation horizontale

    # 3. Les Onglets (Tabs) - Pour organiser l'inventaire et les sorts
    with tab1:
        # Sélection multiple
        items = st.multiselect("Équipement", ["Épée longue", "Arc", "Ration", "Torche"])
        st.write(f"Vous portez (plein de truc): {items}")

    with tab2:
        # Case à cocher
        furtif = st.checkbox("Compétence : Furtivité")
        if furtif:
            st.info("Le personnage se déplace en silence...")

    st.divider()

    # 4. Action
    if st.button("🎲 Faire un test de Force", type="primary"):
        st.success(f"{nom} utilise sa Force de {force} et a toujours {pv} points de vie !")
