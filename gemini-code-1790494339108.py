import streamlit as st
import pandas as pd

# Configuration de la page
st.set_page_config(page_title="Espace Acquéreurs & DVF - Nice", layout="wide")

# Menu de navigation unifié
st.sidebar.title("Navigation")
page = st.sidebar.radio("Aller à la section", [
    "Analyse des Secteurs Phares (US)", 
    "Suivi des Profils Acquéreurs", 
    "📄 Générateur de Lead - Guide Retraite",
    "📊 Analyse DVF - Vraies Ventes (Ciblé)"
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
    origine_ville = st.selectbox("Origine / Ville", ["France (Local/National)", "New York (JFK/EWR)", "Boston (BOS)", "Washington (IAD)", "Autre"])
    secteur_interet = st.selectbox("Secteur d'intérêt", ["Carré d'Or", "Promenade des Anglais", "Mont Boron"])
    budget = st.text_input("Budget estimé", placeholder="Ex: 1.5M€")
    
    if st.button("Ajouter à la base de prospection"):
        st.success(f"Contact {nom_contact} ({origine_ville}) ajouté avec succès pour le secteur {secteur_interet} !")

elif page == "📄 Générateur de Lead - Guide Retraite":
    st.title("📄 Générateur de Lead - Guide Retraite sur la Côte d'Azur")
    st.markdown("Outil d'aide à la création de contenus ciblés pour attirer les investisseurs préparant leur retraite.")
    
    cible_retraite = st.radio("Clientèle visée :", ["🇫🇷 Jeunes/Futurs Retraités Français", "🇺🇸 Investisseurs Retraités Américains (US)"], horizontal=True)
    
    if cible_retraite == "🇫🇷 Jeunes/Futurs Retraités Français":
        st.info("💡 **Angle d'attaque :** Défiscalisation, constitution de patrimoine foncier, et préparation d'un complément de revenu.")
        st.markdown("""
        **Trame suggérée pour le guide PDF / Article de blog :**
        1. **Introduction :** Pourquoi Nice est le choix n°1 des Français pour préparer leur retraite au soleil.
        2. **Stratégie Patrimoniale :** L'avantage de l'amortissement LMNP et les dispositifs fiscaux.
        3. **Secteurs d'avenir :** Les quartiers niçois où investir aujourd'hui pour une forte plus-value.
        4. **Gestion Locative :** Comment sécuriser son investissement à distance.
        5. **Call-to-action :** "Prenez rendez-vous pour une étude patrimoniale personnalisée."
        """)
        
    elif cible_retraite == "🇺🇸 Investisseurs Retraités Américains (US)":
        st.info("💡 **Angle d'attaque :** Art de vivre, sécurité, vues exceptionnelles, et facilité d'installation.")
        st.markdown("""
        **Trame suggérée pour le guide PDF / Article de blog (en anglais) :**
        1. **Introduction:** The French Riviera Dream - Why Nice is the Ultimate Retirement Destination.
        2. **Lifestyle & Healthcare:** Accessing world-class medical care and enjoying the Riviera.
        3. **Top Neighborhoods:** Mont Boron (Quiet luxury & Views) and Carré d'Or (Walkable & Vibrant).
        4. **The Buying Process:** A clear guide for Americans (Notaire system, visas, etc.).
        5. **Call-to-Action:** "Contact your dedicated Riviera real estate expert."
        """)

elif page == "📊 Analyse DVF - Vraies Ventes (Ciblé)":
    st.title("📊 Analyse DVF - Vraies Ventes de l'État (Nice Premium)")
    st.markdown("Ce module filtre **uniquement** vos secteurs de prédilection en analysant le nom des rues sur les données officielles.")
    
    annee = st.selectbox("Sélectionnez l'année d'analyse :", ["2026", "2025", "2024", "2023"], index=1)
    
    # ---------------------------------------------------------
    # SECURITÉ : BOUTON D'IMPORTATION MANUELLE (MULTIPLE)
    # ---------------------------------------------------------
    st.sidebar.markdown("---")
    st.sidebar.warning("📁 **Plan B (Import manuel)**")
    
    # NOUVEAUTÉ : On autorise la sélection de plusieurs fichiers (accept_multiple_files=True)
    uploaded_files = st.sidebar.file_uploader("Importez ici vos fichiers CSV (plusieurs possibles)", type=['csv'], accept_multiple_files=True)

    colonnes_utiles = ['date_mutation', 'valeur_fonciere', 'nom_commune', 'adresse_nom_voie', 'type_local', 'surface_reelle_bati']

    def filtrer_nice_premium(df_brut):
        # On s'assure d'avoir la colonne des communes pour éviter les erreurs
        if 'nom_commune' not in df_brut.columns:
            return pd.DataFrame()
            
        df_nice = df_brut[df_brut['nom_commune'].str.contains('Nice', case=False, na=False)].copy()
        df_nice = df_nice.dropna(subset=['valeur_fonciere', 'adresse_nom_voie'])
        
        def identifier_secteur(rue):
            rue = str(rue).upper()
            if 'ANGLAIS' in rue:
                return "Promenade des Anglais"
            elif any(mot in rue for mot in ['BORON', 'ALBAN', 'BATTERIE', 'FORESTIER', 'MACCARANI']):
                return "Mont Boron"
            elif any(mot in rue for mot in ['FRANCE', 'BUFFA', 'MASSENA', 'GRIMALDI', 'PARADIS', 'KARR', 'HALEVY', 'SUEDE', 'CONGRES', 'RIVOLI', 'MEDECIN', 'VICTOR HUGO']):
                return "Carré d'Or"
            else:
                return "Hors Cible"
        
        df_nice['Quartier_Cible'] = df_nice['adresse_nom_voie'].apply(identifier_secteur)
        df_premium = df_nice[df_nice['Quartier_Cible'] != "Hors Cible"].copy()
        df_premium['valeur_fonciere'] = df_premium['valeur_fonciere'].astype(int)
        return df_premium

    @st.cache_data(show_spinner=f"Connexion automatique aux serveurs de l'État pour {annee}...")
    def charger_vraies_donnees(annee_choisie):
        url = f"https://files.data.gouv.fr/geo-dvf/latest/csv/{annee_choisie}/departements/06.csv"
        try:
            storage_options = {'User-Agent': 'Mozilla/5.0'}
            df = pd.read_csv(url, usecols=lambda c: c in colonnes_utiles, low_memory=False, storage_options=storage_options)
            return filtrer_nice_premium(df)
        except Exception as e:
            return None

    df_reelles = None
    
    # Choix de la source : Fichiers uploadés OU téléchargement automatique
    if uploaded_files: # S'il y a au moins un fichier
        try:
            liste_dfs = []
            for file in uploaded_files:
                df_temp = pd.read_csv(file, usecols=lambda c: c in colonnes_utiles, low_memory=False)
                liste_dfs.append(df_temp)
            
            # On regroupe tous les fichiers ensemble (concaténation)
            df_raw = pd.concat(liste_dfs, ignore_index=True)
            df_reelles = filtrer_nice_premium(df_raw)
            st.sidebar.success(f"{len(uploaded_files)} fichier(s) combiné(s) avec succès !")
        except Exception as e:
            st.error("Erreur de lecture du fichier. Vérifiez qu'il s'agit bien d'un fichier DVF.")
    else:
        df_reelles = charger_vraies_donnees(annee)

    # Affichage des résultats
    if df_reelles is not None and not df_reelles.empty:
        st.success(f"Opération réussie ! {len(df_reelles)} transactions trouvées dans vos secteurs cibles.")
        
        secteurs = ["Tous les secteurs cibles"] + list(df_reelles['Quartier_Cible'].unique())
        choix_secteur = st.selectbox("Filtrer par secteur précis :", secteurs)
        
        if choix_secteur != "Tous les secteurs cibles":
            df_affiche = df_reelles[df_reelles['Quartier_Cible'] == choix_secteur]
        else:
            df_affiche = df_reelles

        st.dataframe(df_affiche.sort_values(by='date_mutation', ascending=False)[['date_mutation', 'Quartier_Cible', 'adresse_nom_voie', 'type_local', 'surface_reelle_bati', 'valeur_fonciere']], use_container_width=True)
        
        if not df_affiche.empty:
            prix_moyen = int(df_affiche['valeur_fonciere'].mean())
            st.metric(f"Prix moyen constaté dans la sélection", f"{prix_moyen:,} €".replace(',', ' '))
            
    elif not uploaded_files:
        st.error(f"Impossible de récupérer automatiquement les données de {annee}.")
