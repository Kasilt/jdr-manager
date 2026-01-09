"""Home page - Main application screen."""

import streamlit as st


def show_home_page():
    """Display the home page."""
    st.title("🏠 Accueil")
    st.divider()
    
    # Get current user
    username = st.session_state.get("username", "Joueur")
    
    st.markdown(f"### Bienvenue, {username}! 👋")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("📜 **3** Personnages", icon="ℹ️")
    
    with col2:
        st.success("🎭 **2** Campagnes Actives", icon="✅")
    
    with col3:
        st.warning("⚔️ **5** Combats en Attente", icon="⚠️")
    
    st.divider()
    
    st.subheader("🎲 Vos Dernières Actions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        #### Personnages Récents
        - **Conan** (Guerrier)
        - **Gandalf** (Mage)
        - **Legolas** (Archer)
        """)
    
    with col2:
        st.markdown("""
        #### Campagnes Actives
        - **Seigneur des Anneaux**
        - **Donjons & Dragons**
        """)
    
    st.divider()
    
    st.subheader("📝 Notes Rapides")
    st.text_area("Prenez des notes...", height=100, label_visibility="collapsed")
