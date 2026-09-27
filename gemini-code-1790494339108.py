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
    st.markdown("Ce module interroge la base de données réelle de l'État et filtre **uniquement** vos secteurs de prédilection en analysant le nom des rues.")
    
    annee = st.selectbox("Sélectionnez l'année d'analyse (les données de l'État sont mises à jour par semestre)", ["2026", "2025", "2024"], index=1)
    
    @st.cache_data(show_spinner=f"Connexion aux serveurs de l'État pour {annee}...")
    def charger_vraies_donnees(annee_choisie):
        url = f"https://files.data.gouv.fr/geo-dvf/latest/csv/{annee_choisie}/departements/06.csv"
        try:
            colonnes_utiles = ['date_mutation', 'valeur_fonciere', 'nom_commune', 'adresse_nom_voie', 'type_local', 'surface_reelle_bati']
            df = pd.read_csv(url, usecols=lambda c: c in colonnes_utiles, low_memory=False)
            
            # On ne garde que Nice et les lignes avec des prix
            df_nice = df[df['nom_commune'].str.contains('Nice', case=False, na=False)].copy()
            df_nice = df_nice.dropna(subset=['valeur_fonciere', 'adresse_nom_voie'])
            
            # Fonction pour deviner le quartier selon la rue
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
            
            # On ne garde QUE vos 3 quartiers
            df_premium = df_nice[df_nice['Quartier_Cible'] != "Hors Cible"]
            
            # Nettoyage de l'affichage
            df_premium['valeur_fonciere'] = df_premium['valeur_fonciere'].astype(int)
            return df_premium
        except Exception as e:
            return None

    df_reelles = charger_vraies_donnees(annee)

    if df_reelles is not None and not df_reelles.empty:
        st.success(f"Vraies données chargées ! {len(df_reelles)} transactions trouvées dans vos secteurs cibles pour {annee}.")
        
        secteurs = ["Tous les secteurs cibles"] + list(df_reelles['Quartier_Cible'].unique())
        choix_secteur = st.selectbox("Filtrer par secteur précis :", secteurs)
        
        if choix_secteur != "Tous les secteurs cibles":
            df_affiche = df_reelles[df_reelles['Quartier_Cible'] == choix_secteur]
        else:
            df_affiche = df_reelles

        # On affiche les données triées par date (les plus récentes d'abord)
        st.dataframe(df_affiche.sort_values(by='date_mutation', ascending=False)[['date_mutation', 'Quartier_Cible', 'adresse_nom_voie', 'type_local', 'surface_reelle_bati', 'valeur_fonciere']], use_container_width=True)
        
        if not df_affiche.empty:
            prix_moyen = int(df_affiche['valeur_fonciere'].mean())
            st.metric(f"Prix moyen constaté (Vraies ventes {annee})", f"{prix_moyen:,} €".replace(',', ' '))
    else:
        st.warning(f"⚠️ Impossible de charger les vraies données de {annee}. Les serveurs de l'État sont peut-être surchargés, réessayez dans un instant.")
