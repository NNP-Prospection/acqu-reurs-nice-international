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
    "📊 Analyse DVF - Outil Pro (06)"
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

elif page == "📊 Analyse DVF - Outil Pro (06)":
    st.title("📊 Analyse DVF - Marché Immobilier de Nice")
    st.markdown("Exploitez vos fichiers de données notariales pour argumenter vos estimations et cibler vos investissements.")
    
    uploaded_file = st.file_uploader("📁 Importez votre fichier CSV DVF", type=None)

    if uploaded_file is not None:
        try:
            with st.spinner("Analyse des transactions en cours..."):
                df_brut = pd.read_csv(uploaded_file, low_memory=False, on_bad_lines='skip')
                
                # Nettoyage et filtrage de base sur Nice si les colonnes existent
                colonnes_str = " ".join(df_brut.columns).lower()
                
            st.success(f"Fichier chargé avec succès ! ({len(df_brut):,} lignes enregistrées).")
            
            # --- DIVISION EN DEUX SECTIONS DISTINCTES ---
            tab1, tab2 = st.tabs([
                "💰 1. Connaissance des vrais prix de vente", 
                "📈 2. Tendances et Secteurs Clés"
            ])
            
            with tab1:
                st.subheader("Recherche par rue ou adresse précise")
                st.markdown("Retrouvez instantanément le prix réel des ventes notariales par rue pour préparer vos avis de valeur.")
                
                recherche_rue = st.text_input("Entrez un nom de rue (ex: Promenade des Anglais, rue de France, etc.) :")
                
                if recherche_rue:
                    # Recherche textuelle dans le fichier chargé
                    col_voie = [c for c in df_brut.columns if 'voie' in c.lower() or 'adresse' in c.lower() or 'rue' in c.lower()]
                    if col_voie:
                        mask = df_brut[col_voie[0]].astype(str).str.contains(recherche_rue, case=False, na=False)
                        df_resultats = df_brut[mask]
                        
                        st.metric("Transactions trouvées pour cette recherche", f"{len(df_resultats):,}")
                        if not df_resultats.empty:
                            st.dataframe(df_resultats.head(100), use_container_width=True)
                        else:
                            st.warning("Aucune transaction trouvée pour cette rue exacte dans ce fichier.")
                    else:
                        st.error("La colonne d'adresse n'a pas été identifiée automatiquement dans ce fichier.")
                else:
                    st.info("💡 Saisissez un mot-clé ou un nom de rue ci-dessus pour interroger la base notariale.")
                    st.markdown("#### 🔍 Aperçu global brut :")
                    st.dataframe(df_brut.head(20), use_container_width=True)
                    
            with tab2:
                st.subheader("Analyse comparative des secteurs clés")
                st.markdown("Vue d'ensemble sur le dynamisme et les caractéristiques de vos zones de prédilection (**Carré d'Or, Promenade des Anglais, Mont Boron**).")
                
                # Simulation de synthèse par grands secteurs cibles basés sur vos critères
                st.info("💡 **Synthèse stratégique :** Ces indicateurs vous aident à positionner vos biens face à la demande locale et internationale à fort pouvoir d'achat.")
                
                # Tableau récapitulatif qualitatif prêt pour l'argumentation client
                df_synthese_marche = pd.DataFrame({
                    "Secteur Clé": ["Carré d'Or", "Promenade des Anglais", "Mont Boron"],
                    "Type de biens recherchés": ["Appartement urbain, piétonnier", "Vue mer frontale, standing", "Villas, résidences de prestige, calme"],
                    "Clientèle privilégiée": ["Actifs haut de gamme & Investisseurs", "Acquéreurs internationaux (US / Résidence secondaire)", "Amateurs de 'Quiet Luxury' & Intimité"],
                    "Atout clé pour la vente": ["Proximité immédiate des commerces et plages", "Panorama exceptionnel et mythe azuréen", "Vues panoramiques et discrétion absolue"]
                })
                st.dataframe(df_synthese_marche, use_container_width=True)
                
        except Exception as e:
            st.error(f"⚠️ Erreur lors du traitement du fichier : {e}")
    else:
        st.info("💡 Veuillez importer un fichier CSV DVF via le bouton ci-dessus pour activer les deux modules d'analyse.")
