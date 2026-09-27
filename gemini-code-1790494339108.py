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

elif page == "📊 Analyse DVF - Marché de Nice":
    st.title("📊 Analyse DVF - Marché Immobilier de Nice")
    st.markdown("Exploitez vos extraits DVF pour vos avis de valeur et études de marché.")
    
    # Initialisation de la mémoire persistante sécurisée
    if 'df_global_memoire' not in st.session_state:
        st.session_state.df_global_memoire = None

    # Si la mémoire est vide, on affiche le sélecteur de fichiers accessible
    if st.session_state.df_global_memoire is None:
        uploaded_files = st.file_uploader("📁 Importer vos fichiers DVF (CSV)", accept_multiple_files=True)

        if uploaded_files:
            try:
                with st.spinner("Traitement et mémorisation des fichiers en cours..."):
                    liste_df = [pd.read_csv(f, low_memory=False, on_bad_lines='skip') for f in uploaded_files]
                    st.session_state.df_global_memoire = pd.concat(liste_df, ignore_index=True)
                st.rerun()
            except Exception as e:
                st.error(f"Erreur lors de la lecture des fichiers : {e}")
    
    # Si les données sont chargées en mémoire, l'interface complète s'affiche
    if st.session_state.df_global_memoire is not None:
        df_brut = st.session_state.df_global_memoire
        
        col1, col2 = st.columns([4, 1])
        with col1:
            st.success(f"✅ Base de données active en mémoire ({len(df_brut):,} transactions prêtes).")
        with col2:
            if st.button("🔄 Réinitialiser"):
                st.session_state.df_global_memoire = None
                st.rerun()

        # --- DEUX ONGLETS DISTINCTS ---
        tab1, tab2 = st.tabs([
            "💰 1. Connaissance des vrais prix de vente", 
            "📈 2. Tendances et Secteurs Clés"
        ])
        
        with tab1:
            st.subheader("Recherche par rue, mot-clé ou adresse")
            st.markdown("Retrouvez le prix réel des ventes notariales en filtrant par nom de rue (ex: *Anglais*, *France*, *Massena*).")
            
            recherche_rue = st.text_input("Entrez un terme de recherche :")
            
            if recherche_rue:
                masque_global = df_brut.astype(str).apply(lambda col: col.str.contains(recherche_rue, case=False, na=False)).any(axis=1)
                df_resultats = df_brut[masque_global]
                
                st.metric("Transactions correspondantes trouvées", f"{len(df_resultats):,}")
                if not df_resultats.empty:
                    colonnes_affichage = [c for c in ['date_mutation', 'valeur_fonciere', 'adresse_nom_voie', 'type_local', 'surface_reelle_bati'] if c in df_resultats.columns]
                    st.dataframe(df_resultats[colonnes_affichage].head(100), use_container_width=True)
                else:
                    st.warning("Aucun résultat ne correspond à votre recherche dans ces fichiers.")
            else:
                st.info("💡 Saisissez un mot-clé ci-dessus (nom de rue, etc.) pour filtrer la base notariale.")
                st.markdown("#### 🔍 Aperçu des transactions :")
                colonnes_affichage = [c for c in ['date_mutation', 'valeur_fonciere', 'adresse_nom_voie', 'type_local', 'surface_reelle_bati'] if c in df_brut.columns]
                st.dataframe(df_brut[colonnes_affichage].head(20), use_container_width=True)
                    
        with tab2:
            st.subheader("Analyse comparative des secteurs clés")
            st.markdown("Vue d'ensemble sur le dynamisme de vos zones de prédilection (**Carré d'Or, Promenade des Anglais, Mont Boron**).")
            
            st.info("💡 **Synthèse stratégique :** Indicateurs clés pour positionner vos biens face à la demande à fort pouvoir d'achat.")
            
            df_synthese_marche = pd.DataFrame({
                "Secteur Clé": ["Carré d'Or", "Promenade des Anglais", "Mont Boron"],
                "Type de biens recherchés": ["Appartement urbain, piétonnier", "Vue mer frontale, standing", "Villas, résidences de prestige, calme"],
                "Clientèle privilégiée": ["Actifs haut de gamme & Investisseurs", "Acquéreurs internationaux (US / Résidence secondaire)", "Amateurs de 'Quiet Luxury' & Intimité"],
                "Atout clé pour la vente": ["Proximité immédiate des commerces et plages", "Panorama exceptionnel et mythe azuréen", "Vues panoramiques et discrétion absolue"]
            })
            st.dataframe(df_synthese_marche, use_container_width=True)
    else:
        st.info("💡 Veuillez sélectionner vos fichiers CSV via le bouton ci-dessus pour lancer l'analyse.")
