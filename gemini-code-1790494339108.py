import streamlit as st
import pandas as pd

# Configuration de la page
st.set_page_config(
    page_title="Espace Acquéreurs - Nice International",
    page_icon="🌴",
    layout="wide"
)

st.title("🌴 Espace de Gestion & Ciblage Acquéreurs - Nice")
st.markdown("### Stratégie pour une clientèle internationale (US) et à fort potentiel.")

# Menu latéral pour choisir l'action
menu = st.sidebar.selectbox(
    "Navigation", 
    ["Analyse des Secteurs Phares (US)", "Suivi des Profils Acquéreurs", "Générateur de Lead - Guide Retraite"]
)

if menu == "Analyse des Secteurs Phares (US)":
    st.header("🎯 Analyse des Secteurs Cibles pour la Clientèle Américaine")
    st.markdown("Ces trois zones concentrent l'essentiel de la demande des acheteurs venus de New York, Boston et Washington.")

    secteurs_data = [
        {
            "Secteur": "Carré d'Or",
            "Profil recherché": "Urbain, actif, commerces et mer à pied",
            "Vols privilégiés": "JFK / EWR (New York)",
            "Budget moyen cible": "1M€ - 3M€+"
        },
        {
            "Secteur": "Promenade des Anglais",
            "Profil recherched": "Vue mer frontale, mythe azuréen",
            "Vols privilégiés": "JFK / BOS (Boston)",
            "Budget moyen cible": "1.5M€ - 5M€+"
        },
        {
            "Secteur": "Mont Boron",
            "Profil recherché": "Quiet luxury, intimité, panoramas",
            "Vols privilégiés": "IAD (Washington) / Atlanta",
            "Budget moyen cible": "2M€ - 6M€+"
        }
    ]
    
    df_secteurs = pd.DataFrame(secteurs_data)
    st.table(df_secteurs)

elif menu == "Suivi des Profils Acquéreurs":
    st.header("👥 Suivi des Demandes Entrantes")
    st.write("Enregistrez ici vos contacts qualifiés issus des campagnes ciblées :")
    
    # Formulaire de saisie rapide d'un acquéreur
    with st.form("form_acquereur"):
        nom = st.text_input("Nom / Référence du contact")
        origine = st.selectbox("Origine / Ville", ["New York (JFK/EWR)", "Boston (BOS)", "Washington (IAD)", "Autre international", "France (Résidence secondaire)"])
        secteur_souhaite = st.selectbox("Secteur d'intérêt", ["Carré d'Or", "Promenade des Anglais", "Mont Boron"])
        budget = st.text_input("Budget estimé", "Ex: 1.5M€")
        submit = st.form_submit_button("Ajouter à la base de prospection")
        
        if submit:
            st.success(f"Acquéreur '{nom}' ({origine}) enregistré avec succès pour le secteur {secteur_souhaite} !")

elif menu == "Générateur de Lead - Guide Retraite":
    st.header("📘 Tunnel Inbound Marketing : S'installer à Nice")
    st.write("Aperçu de la page de capture pour attirer les futurs retraités ou expatriés :")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **Contenu du Guide Offert :**
        1. Pourquoi Nice est l'eldorado des investisseurs internationaux.
        2. Comparatif exclusif : Carré d'Or vs Mont Boron.
        3. Guide fiscal et pratique de l'acquisition en France pour les non-résidents.
        """)
    with col2:
        st.info("💡 **Conseil :** Ce module peut être relié à une page web simple (Landing Page) pour collecter automatiquement les emails de vos futurs acheteurs.")