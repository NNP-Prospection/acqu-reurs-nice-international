import streamlit as st
import pandas as pd

st.set_page_config(page_title="DVF - Alpes-Maritimes (06)", layout="wide")

st.title("📊 Analyse des Valeurs Foncières (DVF) - Alpes-Maritimes (06)")
st.markdown("""
Cet outil analyse les données officielles des transactions notariales pour vous aider à identifier 
les zones les plus dynamiques et cibler les opportunités de réinvestissement.
""")

# URL officielle des données DVF pour le département 06 (Alpes-Maritimes)
DEFAULT_DVF_URL = "https://files.data.gouv.fr/geo-dvf/latest/csv/2023/departements/06.csv"

@st.cache_data(show_spinner="Téléchargement des données DVF du 06 en cours...")
def charger_donnees_url(url):
    try:
        df = pd.read_csv(url, low_memory=False)
        return df
    except Exception as e:
        return None

# Tentative de chargement via l'URL officielle
data_source = "url"
df = charger_donnees_url(DEFAULT_DVF_URL)

if df is None or df.empty:
    st.warning("⚠️ Le téléchargement direct depuis la source officielle a échoué ou est bloqué par le volume des données.")
    data_source = "upload"

# Sécurité intégrée : Bouton de secours pour importer un fichier CSV localement
st.sidebar.header("📁 Gestion des données")
uploaded_file = st.sidebar.file_uploader("Importer un fichier CSV DVF (06) de secours", type=['csv'])

if uploaded_file is not None:
    @st.cache_data
    def charger_donnees_upload(file):
        return pd.read_csv(file, low_memory=False)
    
    df = charger_donnees_upload(uploaded_file)
    data_source = "upload"
    st.sidebar.success("Fichier CSV chargé avec succès depuis votre ordinateur !")

# Traitement et affichage si les données sont disponibles
if df is not None and not df.empty:
    st.success(f"Données chargées avec succès ! ({len(df):,} transactions trouvées) via : **{'URL Officielle' if data_source == 'url' else 'Importation locale'}**")
    
    # Filtre optionnel par commune (ex: Nice ou autres communes du 06)
    if 'nom_commune' in df.columns:
        communes = sorted(df['nom_commune'].dropna().unique())
        selected_commune = st.selectbox("Filtrer par commune", ["Toutes"] + list(communes))
        
        if selected_commune != "Toutes":
            df_filtered = df[df['nom_commune'] == selected_commune]
        else:
            df_filtered = df
            
        st.metric("Nombre de mutations affichées", f"{len(df_filtered):,}")
        
        # Aperçu des principaux champs
        colonnes_a_afficher = [c for c in ['date_mutation', 'valeur_fonciere', 'nom_commune', 'type_local', 'surface_reelle_bati'] if c in df.columns]
        st.dataframe(df_filtered[colonnes_a_afficher].head(100), use_container_width=True)
    else:
        st.dataframe(df.head(100), use_container_width=True)
else:
    st.info("💡 Veuillez importer un fichier CSV des Alpes-Maritimes via le panneau latéral si le lien officiel ne répond pas.")
