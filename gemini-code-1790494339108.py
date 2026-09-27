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
    "📊 Analyse DVF - Nice (Automatique)"
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

elif page == "📊 Analyse DVF - Nice (Automatique)":
    st.title("📊 Analyse DVF - Ville de Nice (Connexion Directe)")
    st.markdown("Cette section interroge directement les serveurs officiels pour extraire et analyser les transactions de Nice en un clic, sans manipulation de fichiers lourds.")
    
    annee_selectionnee = st.selectbox("Sélectionnez l'année de référence", ["2025", "2024", "2023"], index=0)
    
    if st.button("Lancer l'analyse des données de Nice"):
        url_officielle = f"https://files.data.gouv.fr/geo-dvf/latest/csv/{annee_selectionnee}/departements/06.csv"
        
        with st.spinner(f"Récupération et filtrage des données de Nice pour {annee_selectionnee} en cours..."):
            try:
                # Lecture directe et filtrage immédiat pour ne garder que Nice
                colonnes = ['date_mutation', 'valeur_fonciere', 'nom_commune', 'adresse_nom_voie', 'type_local', 'surface_reelle_bati']
                df_brut = pd.read_csv(url_officielle, usecols=lambda c: c in colonnes, low_memory=False)
                
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
                        return "Autre Quartier Nice"
                
                df_nice['Secteur_Cible'] = df_nice['adresse_nom_voie'].apply(identifier_secteur)
                df_nice['valeur_fonciere'] = df_nice['valeur_fonciere'].astype(int)
                
                st.success(f"Données chargées avec succès ! {len(df_nice):,} transactions analysées pour Nice en {annee_selectionnee}.")
                
                # Statistiques globales
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Total des transactions à Nice", f"{len(df_nice):,}")
                with col2:
                    prix_moyen_nice = int(df_nice['valeur_fonciere'].mean())
                    st.metric("Valeur foncière moyenne globale", f"{prix_moyen_nice:,} €".replace(',', ' '))
                
                st.markdown("### 📋 Détail des transactions par secteur")
                st.dataframe(df_nice.sort_values(by='date_mutation', ascending=False).head(100), use_container_width=True)
                
            except Exception as e:
                st.error("⚠️ Impossible de joindre directement le serveur distant. Veuillez réessayer dans quelques instants.")
    else:
        st.info("💡 Cliquez sur le bouton ci-dessus pour lancer l'extraction automatique des données de Nice.")
