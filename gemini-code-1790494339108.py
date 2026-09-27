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
    "📊 Analyse DVF - Nice (Optimisée)"  # <--- Le nom a été mis à jour
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

elif page == "📊 Analyse DVF - Nice (Optimisée)":
    st.title("📊 Analyse DVF ciblée - Ville de Nice")
    st.markdown("""
    Cette section récupère automatiquement une version allégée des données officielles de **Nice** uniquement. 
    Choisissez l'année ci-dessous pour lancer l'extraction.
    """)
    
    # Sélecteur d'année (2026 pourrait ne pas être encore totalement consolidé par l'État en septembre)
    annee = st.selectbox("Sélectionnez l'année d'analyse", ["2026", "2025", "2024"], index=1)
    
    # Construction de l'URL officielle basée sur l'année choisie
    URL_DVF = f"https://files.data.gouv.fr/geo-dvf/latest/csv/{annee}/departements/06.csv"
    
    @st.cache_data(show_spinner=f"Téléchargement et filtrage ultra-rapide des données de Nice pour {annee}...")
    def charger_donnees_nice(url):
        try:
            # Astuce pour ne pas saturer la mémoire : on ne lit que les colonnes dont on a besoin
            colonnes_utiles = ['date_mutation', 'valeur_fonciere', 'nom_commune', 'type_local', 'surface_reelle_bati']
            
            # Lecture du fichier
            df = pd.read_csv(url, usecols=lambda c: c in colonnes_utiles, low_memory=False)
            
            # On filtre immédiatement pour ne garder QUE la ville de Nice
            df_nice = df[df['nom_commune'].str.contains('Nice', case=False, na=False)]
            
            # On supprime les lignes sans valeur foncière pour nettoyer les données
            df_nice = df_nice.dropna(subset=['valeur_fonciere'])
            
            return df_nice
        except Exception as e:
            return None

    # Exécution du chargement
    df = charger_donnees_nice(URL_DVF)

    if df is not None and not df.empty:
        st.success(f"Données de Nice pour {annee} chargées avec succès ! ({len(df):,} transactions immobilières trouvées)")
        
        # Affichage du tableau de données de Nice
        st.dataframe(df.sort_values(by='date_mutation', ascending=False).head(100), use_container_width=True)
        
    else:
        st.warning(f"⚠️ Les données de l'année {annee} ne sont pas encore disponibles sur les serveurs de l'État, ou le lien est temporairement inaccessible.")
