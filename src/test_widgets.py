import streamlit as st

st.title("🧙‍♂️ Laboratoire de Composants JDR")

# 1. La Barre latérale (Sidebar) - Parfait pour les menus ou infos fixes
with st.sidebar:
    st.header("Fiche technique")
    mode_mj = st.toggle("Mode Maître du Jeu") # Un interrupteur moderne

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

st.divider() # Une ligne de séparation horizontale

# 3. Les Onglets (Tabs) - Pour organiser l'inventaire et les sorts
tab1, tab2 = st.tabs(["🎒 Inventaire", "📜 Sorts / Compétences"])

with tab1:
    # Sélection multiple
    items = st.multiselect("Équipement", ["Épée longue", "Arc", "Ration", "Torche"])
    st.write(f"Vous portez : {items}")

with tab2:
    # Case à cocher
    furtif = st.checkbox("Compétence : Furtivité")
    if furtif:
        st.info("Le personnage se déplace en silence...")

st.divider()

# 4. Action
if st.button("🎲 Faire un test de Force", type="primary"):
    st.success(f"{nom} utilise sa Force de {force} !")