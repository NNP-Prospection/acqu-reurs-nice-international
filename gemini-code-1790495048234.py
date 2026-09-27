import pandas as pd
import streamlit as st

st.set_page_title("Analyse des Ventes DVF - Nice", layout="wide")

st.title("🏡 Analyse des Données DVF & Dynamique de Marché à Nice")
st.markdown("""
Cet outil analyse les transactions immobilières pour identifier les zones et les types de biens 
les plus dynamiques (cibles prioritaires pour le réinvestissement et l'accompagnement post-vente).
""")

@st.cache_data
def load_dvf_data():
    # URL vers un échantillon ou l'API des données DVF (ici une structure type pour démonstration)
    # Vous pouvez remplacer par le chargement de votre fichier CSV DVF local ou de l'API officielle.
    url = "https://files.data.gouv.fr/geo-dvf/latest/csv/2023/communes/06/06088.csv" # Exemple pour Nice (Code INSEE 06088)
    try:
        df = pd.read_csv(url, low_memory=False)
        return df
    except Exception as e:
        st.error(f"Erreur lors du chargement des données DVF : {e}")
        return pd.DataFrame()

with st.spinner("Chargement des données DVF en cours..."):
    df_dvf = load_dvf_data()

if not df_dvf.empty:
    st.success("Données chargées avec succès !")
    
    # Nettoyage / Filtrage basique selon les colonnes courantes DVF
    # Colonnes typiques : 'valeur_fonciere', 'lib_voie', 'code_postal', 'type_local', 'surface_relle_bati'
    
    st.sidebar.header("Filtres d'analyse")
    
    # Filtrer par type de bien si la colonne existe
    if 'type_local' in df_dvf.columns:
        types_biens = df_dvf['type_local'].dropna().unique()
        selected_type = st.sidebar.selectbox("Type de bien", options=["Tous"] + list(types_biens))
        if selected_type != "Tous":
            df_dvf = df_dvf[df_dvf['type_local'] == selected_type]

    # Affichage des principales métriques
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total des transactions analysées", len(df_dvf))
    with col2:
        if 'valeur_fonciere' in df_dvf.columns:
            # Conversion en numérique propre
            prix_moyen = pd.to_numeric(df_dvf['valeur_fonciere'], errors='coerce').mean()
            st.metric("Valeur foncière moyenne", f"{prix_moyen:,.0f} €" if pd.notnull(prix_moyen) else "N/A")
    with col3:
        if 'code_postal' in df_dvf.columns:
            st.metric("Codes postaux couverts", df_dvf['code_postal'].nunique())

    st.subheader("Aperçu des dernières transactions enregistrées")
    st.dataframe(df_dvf.head(10))

    # Analyse par rue / secteur si disponible
    if 'lib_voie' in df_dvf.columns and 'valeur_fonciere' in df_dvf.columns:
        st.subheader("📍 Top des rues les plus dynamiques en volume de ventes")
        top_rues = df_dvf['lib_voie'].value_counts().head(10)
        st.bar_chart(top_rues)
else:
    st.info("Veuillez vérifier la disponibilité de la source de données.")