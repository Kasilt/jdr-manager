"""Campaigns page - List JDR campaigns."""

import streamlit as st


def show_campaigns_page():
    """Display the campaigns list page."""
    st.title("🎭 Liste des JDR")
    st.divider()
    
    # Create new campaign button
    col1, col2 = st.columns([4, 1])
    
    with col2:
        if st.button("➕ Nouvelle Campagne", use_container_width=True, type="primary"):
            st.session_state["show_new_campaign_form"] = True
    
    st.divider()
    
    # Show new campaign form if requested
    if st.session_state.get("show_new_campaign_form", False):
        with st.form("new_campaign_form"):
            st.subheader("➕ Créer une Nouvelle Campagne")
            
            nom = st.text_input("Nom de la Campagne")
            description = st.text_area("Description")
            maitre_jeu = st.text_input("Maître du Jeu")
            joueurs = st.number_input("Nombre de Joueurs", min_value=1, value=4)
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.form_submit_button("✅ Créer", type="primary", use_container_width=True):
                    if nom:
                        st.success(f"✅ Campagne '{nom}' créée!")
                        st.session_state["show_new_campaign_form"] = False
                    else:
                        st.error("❌ Veuillez entrer un nom")
            
            with col2:
                if st.form_submit_button("❌ Annuler", use_container_width=True):
                    st.session_state["show_new_campaign_form"] = False
    
    st.divider()
    
    st.subheader("📋 Campagnes Disponibles")
    
    # Sample campaigns
    campaigns = [
        {
            "nom": "Seigneur des Anneaux",
            "maitre_jeu": "Gandalf",
            "joueurs": 5,
            "statut": "Actif"
        },
        {
            "nom": "Donjons & Dragons",
            "maitre_jeu": "Merlin",
            "joueurs": 4,
            "statut": "Actif"
        },
        {
            "nom": "Pathfinder",
            "maitre_jeu": "Elminster",
            "joueurs": 3,
            "statut": "En Pause"
        }
    ]
    
    for campaign in campaigns:
        with st.container(border=True):
            col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
            
            with col1:
                st.markdown(f"### {campaign['nom']}")
                st.caption(f"**MJ** : {campaign['maitre_jeu']}")
            
            with col2:
                st.metric("Joueurs", campaign['joueurs'])
            
            with col3:
                status_color = "🟢" if campaign['statut'] == "Actif" else "🟡"
                st.write(f"{status_color} {campaign['statut']}")
            
            with col4:
                col_a, col_b = st.columns(2)
                with col_a:
                    if st.button("📖", key=f"view_{campaign['nom']}", help="Voir"):
                        st.info("Détails - À implémenter")
                with col_b:
                    if st.button("⚙️", key=f"edit_{campaign['nom']}", help="Gérer"):
                        st.info("Gestion - À implémenter")
