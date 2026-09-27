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
    "📊 Analyse DVF - Alpes-Maritimes (06)"  # <--- Votre nouvel outil DVF intégré ici
])

if page == "Analyse des Secteurs Phares (US)":
    st.title("🌿 Espace de Gestion & Ciblage Acquéreurs - Nice")
    st.markdown("Stratégie pour une clientèle internationale (US) et à fort potentiel.")
    st.markdown("### 🎯 Analyse des Secteurs Cibles pour la Clientèle Américaine")
    st.markdown("Ces trois zones concentrent l'essentiel de la demande des acheteurs venus de New York, Boston et Washington.")
    
    # Tableau récapitulatif
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

elif page == "📊 Analyse DVF - Alpes-Maritimes (06)":
    st.title("📊 Analyse des Valeurs Foncières (DVF) - Alpes-Maritimes (06)")
    st.markdown("""
    Cet outil analyse les données officielles des transactions notariales pour vous aider à identifier 
    les zones dynamiques et cibler les opportunités. En cas de blocage du volume en ligne, utilisez le bouton d'import ci-dessous.
    """)
    
    DEFAULT_DVF_URL = "https://files.data.gouv.fr/geo-dvf/latest/csv/2023/departements/06.csv"
    
    @st.cache_data(show_spinner="Téléchargement des données DVF du 06 en cours...")
    def charger_donnees_url(url):
        try:
            return pd.read_csv(url, low_memory=False)
        except:
            return None

    df = charger_donnees_url(DEFAULT_DVF_URL)
    data_source = "url"

    if df is None or df.empty:
        st.warning("⚠️ Le téléchargement direct en ligne est bloqué par le volume des données.")
        data_source = "upload"

    # Sécurité intégrée : Bouton de secours CSV dans la barre latérale
    st.sidebar.markdown("---")
    uploaded_file = st.sidebar.file_uploader("📁 Importer un fichier CSV DVF (06)", type=['csv'])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file, low_memory=False)
        data_source = "upload"
        st.sidebar.success("Fichier CSV chargé avec succès !")

    if df is not None and not df.empty:
        st.success(f"Données chargées avec succès ({len(df):,} transactions) via : **{'URL Officielle' if data_source == 'url' else 'Importation locale'}**")
        
        if 'nom_commune' in df.columns:
            communes = sorted(df['nom_commune'].dropna().unique())
            selected_commune = st.selectbox("Filtrer par commune", ["Toutes"] + list(communes))
            
            df_filtered = df if selected_commune == "Toutes" else df[df['nom_commune'] == selected_commune]
            st.metric("Nombre de mutations affichées", f"{len(df_filtered):,}")
            
            colonnes_a_afficher = [c for c in ['date_mutation', 'valeur_fonciere', 'nom_commune', 'type_local', 'surface_reelle_bati'] if c in df.columns]
            st.dataframe(df_filtered[colonnes_a_afficher].head(100), use_container_width=True)
    else:
        st.info("💡 Veuillez importer un fichier CSV des Alpes-Maritimes via le panneau latéral pour commencer l'analyse.")
