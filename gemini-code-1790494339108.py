import streamlit as st
import pandas as pd

# Configuration de la page
st.set_page_config(page_title="Espace Acquéreurs & DVF - Nice", layout="wide")

# Menu de navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Aller à la section", [
    "Analyse des Secteurs Phares (US)", 
    "Suivi des Profils Acquéreurs", 
    "📄 Générateur de Lead - Guide Retraite",
    "📊 Analyse DVF - Marché de Nice"
])

if page == "Analyse des Secteurs Phares (US)":
    st.title("🌿 Espace de Gestion & Ciblage Acquéreurs - Nice")
    st.markdown("Stratégie pour une clientèle internationale (US) et à fort potentiel.")
    
    data_secteurs = {
        "Secteur": ["Carré d'Or", "Promenade des Anglais", "Mont Boron"],
        "Profil recherché": ["Urbain, actif, commerces et mer à pied", "Vue mer frontale, mythe azuréen", "Quiet luxury, intimité, panoramas"],
        "Budget moyen cible": ["1M€ - 3M€+", "1.5M€ - 5M€+", "2M€ - 6M€+"]
    }
    st.dataframe(pd.DataFrame(data_secteurs), use_container_width=True)

elif page == "Suivi des Profils Acquéreurs":
    st.title("👥 Suivi des Demandes Entrantes")
    nom_contact = st.text_input("Nom / Référence du contact")
    origine_ville = st.selectbox("Origine / Ville", ["France", "New York", "Boston", "Washington", "Autre"])
    secteur_interet = st.selectbox("Secteur d'intérêt", ["Carré d'Or", "Promenade des Anglais", "Mont Boron"])
    if st.button("Ajouter à la base"):
        st.success(f"Contact {nom_contact} ajouté !")

elif page == "📄 Générateur de Lead - Guide Retraite":
    st.title("📄 Générateur de Lead - Guide Retraite sur la Côte d'Azur")
    st.info("💡 Utilisez cet espace pour préparer vos arguments auprès des investisseurs.")

elif page == "📊 Analyse DVF - Marché de Nice":
    st.title("📊 Analyse DVF - Marché Immobilier de Nice & Sous-Secteurs")
    st.markdown("Exploitation avancée avec distinction des micro-localisations (ex: Mont Boron Sélect vs Périphérique).")
    
    # Lien officiel de l'État pour le département 06
    DEFAULT_DVF_URL = "https://files.data.gouv.fr/geo-dvf/latest/csv/2023/departements/06.csv"
    
    @st.cache_data(show_spinner="Téléchargement officiel et nettoyage des données DVF en cours (cela peut prendre 30 secondes)...")
    def charger_et_nettoyer_fichiers(source):
        try:
            # Lecture robuste depuis le lien web
            df = pd.read_csv(source, low_memory=False, sep=None, engine='python', on_bad_lines='skip')
            df.columns = [c.strip() for c in df.columns] # Nettoie les noms de colonnes
            return df
        except:
            return None

    # On charge les données via l'URL
    df_brut = charger_et_nettoyer_fichiers(DEFAULT_DVF_URL)

    # Sécurité intégrée si le serveur de l'État est lent
    if df_brut is None or df_brut.empty:
        st.warning("⚠️ Le serveur officiel est surchargé. Vous pouvez utiliser le fichier CSV de secours.")
        uploaded_file = st.sidebar.file_uploader("📁 Importer un fichier CSV DVF (06)", type=['csv'])
        if uploaded_file is not None:
            df_brut = charger_et_nettoyer_fichiers(uploaded_file)

    if df_brut is not None and not df_brut.empty:
        st.success(f"✅ Base de données chargée et normalisée ({len(df_brut):,} lignes brutes).")

        tab1, tab2 = st.tabs(["💰 Recherche & Analyse par Sous-Secteurs", "📈 Synthèse"])
        
        with tab1:
            recherche_rue = st.text_input("Entrez un terme de recherche (ex: MONT BORON) :", value="MONT BORON")
            
            if recherche_rue:
                masque_global = df_brut.astype(str).apply(lambda col: col.str.contains(recherche_rue, case=False, na=False)).any(axis=1)
                df_resultats = df_brut[masque_global].copy()
                
                if not df_resultats.empty:
                    col_valeur = next((c for c in df_resultats.columns if 'valeur_fonciere' in c.lower() or 'prix' in c.lower()), None)
                    col_voie = next((c for c in df_resultats.columns if 'voie' in c.lower() or 'adresse' in c.lower()), None)
                    col_mutation = next((c for c in df_resultats.columns if 'id_mutation' in c.lower()), None)
                    
                    if col_valeur and col_mutation:
                        # Nettoyage des prix
                        df_resultats['prix_net'] = pd.to_numeric(
                            df_resultats[col_valeur].astype(str).str.replace(',', '.').str.extract(r'([\d\.]+)', expand=False), 
                            errors='coerce'
                        )
                        
                        # DÉDUPLICATION : On ne garde qu'une seule ligne par vente (pour ne pas compter la cave et l'appartement séparément)
                        df_uniques = df_resultats.drop_duplicates(subset=[col_mutation])
                        
                        # --- CLASSEMENT DU MONT BORON ---
                        if "MONT BORON" in recherche_rue.upper():
                            def classifier_mont_boron(adresse):
                                adresse_str = str(adresse).upper()
                                if any(terme in adresse_str for terme in ['FORESTIERE', 'ALBAN', 'MONT BORON', 'REPUBLIQUE', 'MAETERLINCK']):
                                    return "⭐ Mont Boron - Adresses Sélectes (Boulevards / Corniches)"
                                else:
                                    return "🏡 Mont Boron - Abords / Périphérie"
                            
                            if col_voie:
                                df_uniques['Sous_Secteur'] = df_uniques[col_voie].apply(classifier_mont_boron)
                                
                                st.markdown("### 🏆 Analyse comparative des Vraies Ventes (Dédoublonnées)")
                                for sous_sec, groupe in df_uniques.groupby('Sous_Secteur'):
                                    prix_moyen = groupe['prix_net'].mean()
                                    st.markdown(f"**{sous_sec}** ({len(groupe)} ventes réelles) — Prix de vente moyen : **{prix_moyen:,.0f} €**".replace(",", " "))
                        
                        # Indicateurs globaux
                        st.markdown("#### 📊 Indicateurs globaux sur votre recherche :")
                        c1, c2 = st.columns(2)
                        c1.metric("Prix moyen (ventes uniques)", f"{df_uniques['prix_net'].mean():,.0f} €".replace(",", " "))
                        c2.metric("Prix médian", f"{df_uniques['prix_net'].median():,.0f} €".replace(",", " "))
                    
                    st.markdown("#### 📋 Détail brut des lignes correspondantes :")
                    st.dataframe(df_resultats.head(100), use_container_width=True)
                else:
                    st.warning("Aucun résultat trouvé.")
                    
        with tab2:
            st.markdown("### Synthèse des Secteurs")
            st.info("Données prêtes pour l'analyse patrimoniale.")
