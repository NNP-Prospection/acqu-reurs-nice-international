import pandas as pd
import streamlit as st

st.set_page_config(page_title="Analyse DVF - Nice", layout="wide")

st.title("🏡 Analyse des Ventes Immobilières (DVF) - Nice")
st.markdown("""
Cet outil analyse les données officielles des transactions notariales pour vous aider à identifier 
les zones les plus dynamiques et cibler les opportunités de réinvestissement.
""")

@st.cache_data
def load_data():
    # Lien direct vers le fichier CSV officiel des données DVF géolocalisées pour le département 06 (Alpes-Maritimes)
    url = "https://files.data.gouv.fr/geo-dvf/latest/csv/2024/departements/06.csv"
    try:
        df = pd.read_csv(url, low_memory=False)
        return df
    except Exception as e:
        st.error(f"Impossible de charger le fichier DVF distant : {e}")
        return pd.DataFrame()

with st.spinner("Chargement des données DVF des Alpes-Maritimes... Veuillez patienter quelques secondes."):
    df = load_data()

if not df.empty:
    st.success(f"Données chargées avec succès ! ({len(df):,} transactions trouvées au total sur le département)")
    
    # Filtrer spécifiquement pour la commune de Nice si la colonne 'nom_commune' existe
    if 'nom_commune' in df.columns:
        df_nice = df[df['nom_commune'].str.upper() == 'NICE'].copy()
    else:
        df_nice = df.copy()

    st.metric("Transactions filtrées pour Nice", len(df_nice))

    # Affichage d'un aperçu
    st.subheader("Aperçu des dernières transactions")
    st.dataframe(df_nice[['date_mutation', 'valeur_fonciere', 'voie', 'code_postal', 'type_local', 'surface_relle_bati']].head(15))

    # Top des voies si les colonnes existent
    if 'voie' in df_nice.columns and 'valeur_fonciere' in df_nice.columns:
        st.subheader("📍 Rues enregistrant le plus de transactions")
        top_rues = df_nice['voie'].dropna().value_counts().head(10)
        st.bar_chart(top_rues)
else:
    st.warning("Le chargement automatique n'a pas abouti. Vous pouvez aussi téléverser un extrait CSV de vos données DVF directement ici.")
    
    uploaded_file = st.file_uploader("Importer un fichier CSV DVF local", type=["csv"])
    if uploaded_file is not None:
        df_local = pd.read_csv(uploaded_file, low_memory=False)
        st.success("Fichier local chargé avec succès !")
        st.dataframe(df_local.head(10))
