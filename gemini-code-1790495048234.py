import streamlit as st
import pandas as pd

# Menu de navigation latéral existant
st.sidebar.title("Navigation")
page = st.sidebar.radio("Aller au fichier / section", [
    "Analyse des Secteurs Phares (US)", 
    "Suivi des Profils Acquéreurs", 
    "Analyse DVF - Alpes-Maritimes (06)"  # <--- Votre nouvel outil DVF ici
])

if page == "Analyse des Secteurs Phares (US)":
    st.title("📊 Espace de Gestion & Ciblage Acquéreurs - Nice")
    st.markdown("Stratégie pour une clientèle internationale (US) et à fort potentiel.")
    # ... (votre code existant pour les acquéreurs)

elif page == "Analyse DVF - Alpes-Maritimes (06)":
    st.title("📊 Analyse des Valeurs Foncières (DVF) - Alpes-Maritimes (06)")
    st.markdown("Source officielle et sécurité par import CSV en cas de blocage du volume.")
    
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
        st.warning("⚠️ Téléchargement direct bloqué ou volumineux.")
        data_source = "upload"

    uploaded_file = st.sidebar.file_uploader("Importer un fichier CSV DVF (06)", type=['csv'])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file, low_memory=False)
        data_source = "upload"
        st.sidebar.success("Fichier CSV chargé avec succès !")

    if df is not None and not df.empty:
        st.success(f"Données chargées ({len(df):,} transactions) via : **{'URL Officielle' if data_source == 'url' else 'Import local'}**")
        if 'nom_commune' in df.columns:
            communes = sorted(df['nom_commune'].dropna().unique())
            selected_commune = st.selectbox("Filtrer par commune", ["Toutes"] + list(communes))
            df_filtered = df if selected_commune == "Toutes" else df[df['nom_commune'] == selected_commune]
            st.metric("Transactions affichées", f"{len(df_filtered):,}")
            st.dataframe(df_filtered[['date_mutation', 'valeur_fonciere', 'nom_commune', 'type_local', 'surface_reelle_bati']].head(100), use_container_width=True)
    else:
        st.info("💡 Veuillez importer un fichier CSV via le panneau latéral.")
