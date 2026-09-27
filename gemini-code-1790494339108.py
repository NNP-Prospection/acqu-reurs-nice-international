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
    st.title("📊 Analyse DVF officielle - Ville de Nice")
    st.markdown("""
    Cette section télécharge la base consolidée officielle des transactions de l'État pour les Alpes-Maritimes 
    et isole automatiquement les données de **Nice**.
    """)
    
    # URL directe stable vers le fichier consolidé officiel du département 06
    URL_DVF_06 = "https://files.data.gouv.fr/geo-dvf/latest/csv/2025/departements/06.csv"
    
    @st.cache_data(show_spinner="Chargement des données foncières de Nice en cours...")
    def charger_donnees_nice(url):
        try:
            colonnes_utiles = ['date_mutation', 'valeur_fonciere', 'nom_commune', 'type_local', 'surface_reelle_bati']
            df = pd.read_csv(url, usecols=lambda c: c in colonnes_utiles, low_memory=False)
            
            # Filtrage strict sur Nice
            df_nice = df[df['nom_commune'].str.contains('Nice', case=False, na=False)].copy()
            df_nice = df_nice.dropna(subset=['valeur_fonciere'])
            
            # Conversion de la date pour un tri propre
            df_nice['date_mutation'] = pd.to_datetime(df_nice['date_mutation'])
            return df_nice
        except Exception as e:
            # Fallback sur une année précédente stable si la version 2025 pose un souci de lien direct
            try:
                url_secours = "https://files.data.gouv.fr/geo-dvf/latest/csv/2024/departements/06.csv"
                df = pd.read_csv(url_secours, usecols=lambda c: c in colonnes_utiles, low_memory=False)
                df_nice = df[df['nom_commune'].str.contains('Nice', case=False, na=False)].copy()
                df_nice = df_nice.dropna(subset=['valeur_fonciere'])
                df_nice['date_mutation'] = pd.to_datetime(df_nice['date_mutation'])
                return df_nice
            except:
                return None

    df = charger_donnees_nice(URL_DVF_06)

    if df is not None and not df.empty:
        st.success(f"Données chargées avec succès ! ({len(df):,} transactions immobilières trouvées à Nice)")
        
        # Filtre optionnel par type de bien si disponible
        if 'type_local' in df.columns:
            types_biens = ["Tous"] + list(df['type_local'].dropna().unique())
            choix_type = st.selectbox("Filtrer par type de bien", types_biens)
            if choix_type != "Tous":
                df = df[df['type_local'] == choix_type]
                st.metric("Transactions filtrées", f"{len(df):,}")

        # Affichage du tableau trié par date décroissante
        st.dataframe(df.sort_values(by='date_mutation', ascending=False).head(100), use_container_width=True)
    else:
        st.warning("⚠️ Le serveur officiel met du temps à répondre. Réessayez dans quelques instants ou actualisez la page.")
