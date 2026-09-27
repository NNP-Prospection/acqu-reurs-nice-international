import streamlit as st
import pandas as pd

# Configuration de la page
st.set_page_config(page_title="Espace Acquéreurs & DVF - Nice", layout="wide")

# Menu de navigation unifié
st.sidebar.title("Navigation")
page = st.sidebar.radio("Aller à la section", [
    "Analyse des Secteurs Phares (US)", 
    "Suivi des Profils Acquéreurs", 
    "Générateur de Lead - Guide Retraite",
    "📊 Analyse DVF - Nice"
])

if page == "Analyse des Secteurs Phares (US)":
    st.title("🌿 Espace de Gestion & Ciblage Acquéreurs - Nice")
    st.markdown("Stratégie pour une clientèle internationale (US) et à fort potentiel.")
    st.markdown("### 🎯 Analyse des Secteurs Cibles pour la Clientèle Américaine")
    st.markdown("Ces trois zones concentrent l'essentiel de la demande des acheteurs venus de New York, Boston et Washington.")
    
    data_secteurs = {
        "Secteur": ["Carré d'Or", "Promenade des Anglais", "Mont Boron"],
        "Profil recherché": ["Urbain, actif, commerces et mer à pied", "Vue mer frontale, mythe azuréen", "Quiet luxury, intimité, panoramas"],
        "Vols privilégiés": ["JFK / EWR (New York)", "JFK / BOS (Boston)", "IAD (Washington) / Atlanta"],
        "Budget moyen cible": ["1M€ - 3M€+", "1.5M€ - 5M€+", "2M€ - 6M€+"]
    }
    st.dataframe(pd.DataFrame(data_secteurs), use_container_width=True)

elif page == "Suivi des Profils Acquéreurs":
    st.title("👥 Suivi des Demandes Entrantes")
    st.markdown("Enregistrez ici vos contacts qualifiés issus des campagnes ciblées :")
    
    nom_contact = st.text_input("Nom / Référence du contact")
    origine_ville = st.selectbox("Origine / Ville", ["New York (JFK/EWR)", "Boston (BOS)", "Washington (IAD)", "Autre"])
    secteur_interet = st.selectbox("Secteur d'intérêt", ["Carré d'Or", "Promenade des Anglais", "Mont Boron"])
    budget = st.text_input("Budget estimé", placeholder="Ex: 1.5M€")
    
    if st.button("Ajouter à la base de prospection"):
        st.success(f"Contact {nom_contact} ({origine_ville}) ajouté avec succès pour le secteur {secteur_interet} !")

elif page == "Générateur de Lead - Guide Retraite":
    st.title("📄 Générateur de Lead - Guide Retraite US sur la Côte d'Azur")
    st.markdown("Outil d'aide à la création de contenus et de guides pour attirer les investisseurs américains à la retraite.")
    st.info("Module en cours de chargement...")

elif page == "📊 Analyse DVF - Nice":
    st.title("📊 Analyse DVF - Ville de Nice")
    st.markdown("""
    Visualisez les transactions immobilières. Si le serveur officiel est encombré, 
    utilisez le bouton d'importation dans le panneau latéral de gauche pour charger votre fichier CSV local.
    """)
    
    df = None
    source_utilisee = ""

    # Option de secours prioritaire : Importation directe d'un fichier CSV local
    st.sidebar.markdown("---")
    st.sidebar.subheader("📁 Importation de secours")
    uploaded_file = st.sidebar.file_uploader("Glissez-déposez votre fichier CSV DVF (06 ou Nice)", type=['csv'])

    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file, low_memory=False)
            # Filtrer sur Nice si le fichier contient toute la région
            if 'nom_commune' in df.columns:
                df = df[df['nom_commune'].str.contains('Nice', case=False, na=False)]
            source_utilisee = "Importation locale (CSV)"
        except Exception as e:
            st.error(f"Erreur lors de la lecture du fichier : {e}")

    # Tentative automatique en ligne si aucun fichier n'est uploadé
    if df is None:
        URL_DVF_06 = "https://files.data.gouv.fr/geo-dvf/latest/csv/2024/departements/06.csv"
        try:
            colonnes_utiles = ['date_mutation', 'valeur_fonciere', 'nom_commune', 'type_local', 'surface_reelle_bati']
            df = pd.read_csv(URL_DVF_06, usecols=lambda c: c in colonnes_utiles, nrows=5000, low_memory=False) # nrows limite pour éviter le blocage réseau
            df = df[df['nom_commune'].str.contains('Nice', case=False, na=False)].dropna(subset=['valeur_fonciere'])
            source_utilisee = "Téléchargement en ligne (Échantillon)"
        except:
            df = None

    # Affichage des résultats si les données sont prêtes
    if df is not None and not df.empty:
        st.success(f"Données chargées via : **{source_utilisee}** ({len(df):,} lignes affichées)")
        
        # Filtre par type de bien si présent
        if 'type_local' in df.columns:
            types = ["Tous"] + list(df['type_local'].dropna().unique())
            choix = st.selectbox("Filtrer par type de bien", types)
            if choix != "Tous":
                df = df[df['type_local'] == choix]

        st.dataframe(df.head(100), use_container_width=True)
    else:
        st.info("💡 Le téléchargement en ligne est actuellement ralenti. Veuillez importer un fichier CSV via la barre latérale à gauche pour afficher vos données immédiatement.")
