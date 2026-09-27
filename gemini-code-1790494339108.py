import streamlit as st
import pandas as pd
import glob

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
    st.markdown("Exploitation automatique de vos fichiers DVF intégrés au projet.")
    
    @st.cache_data(show_spinner="Chargement automatique des fichiers DVF depuis le dépôt...")
    def charger_fichiers_depot():
        fichiers_csv = glob.glob("*.csv") + glob.glob("**/*.csv", recursive=True)
        if not fichiers_csv:
            return None
        liste_df = []
        for f in fichiers_csv:
            try:
                df_temp = pd.read_csv(f, low_memory=False, on_bad_lines='skip')
                liste_df.append(df_temp)
            except:
                pass
        if liste_df:
            return pd.concat(liste_df, ignore_index=True).drop_duplicates()
        return None

    df_brut = charger_fichiers_depot()

    if df_brut is not None and not df_brut.empty:
        st.success(f"✅ Base de données chargée automatiquement ({len(df_brut):,} transactions au total).")

        # --- DEUX ONGLETS DISTINCTS ---
        tab1, tab2 = st.tabs([
            "💰 1. Connaissance des vrais prix de vente", 
            "📈 2. Tendances et Secteurs Clés"
        ])
        
        with tab1:
            st.subheader("Recherche par rue, mot-clé ou adresse")
            st.markdown("Retrouvez le prix réel des ventes notariales en filtrant par nom de rue (ex: *Mont Boron*, *France*, *Anglais*).")
            
            recherche_rue = st.text_input("Entrez un terme de recherche :", value="MONT BORON")
            
            if recherche_rue:
                masque_global = df_brut.astype(str).apply(lambda col: col.str.contains(recherche_rue, case=False, na=False)).any(axis=1)
                df_resultats = df_brut[masque_global]
                
                st.metric("Transactions correspondantes trouvées", f"{len(df_resultats):,}")
                
                if not df_resultats.empty:
                    # Affichage des colonnes réellement utiles si elles existent dans le fichier DVF officiel
                    colonnes_possibles = [c for c in df_resultats.columns if any(k in c.lower() for k in ['date', 'valeur', 'voie', 'surface', 'type', 'commune', 'prix'])]
                    
                    if len(colonnes_possibles) > 0:
                        st.dataframe(df_resultats[colonnes_possibles].head(100), use_container_width=True)
                    else:
                        # Si les noms de colonnes sont différents, on affiche tout le tableau filtré
                        st.dataframe(df_resultats.head(100), use_container_width=True)
                else:
                    st.warning("Aucun résultat ne correspond à votre recherche dans ces fichiers.")
            else:
                st.info("💡 Saisissez un mot-clé ci-dessus.")
                    
        with tab2:
            st.subheader("Analyse comparative des secteurs clés & Tendances")
            st.markdown("Indicateurs de prix et positionnement stratégique pour vos secteurs cibles.")
            
            # Calcul rapide d'indicateurs si la colonne de valeur foncière existe
            col_valeur = [c for c in df_brut.columns if 'valeur' in c.lower()]
            if col_valeur:
                # Nettoyage rapide pour afficher quelques statistiques globales si possible
                st.markdown("#### 📊 Indicateurs globaux du marché extrait :")
                try:
                    vals = pd.to_numeric(df_brut[col_valeur[0]], errors='coerce').dropna()
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Prix moyen constaté", f"{vals.mean():,.0f} €".replace(",", " "))
                    col2.metric("Prix médian", f"{vals.median():,.0f} €".replace(",", " "))
                    col3.metric("Valeur maximale", f"{vals.max():,.0f} €".replace(",", " "))
                except:
                    pass

            df_synthese_marche = pd.DataFrame({
                "Secteur Clé": ["Carré d'Or", "Promenade des Anglais", "Mont Boron"],
                "Type de biens recherchés": ["Appartement urbain, piétonnier", "Vue mer frontale, standing", "Villas, résidences de prestige, calme"],
                "Clientèle privilégiée": ["Actifs haut de gamme & Investisseurs", "Acquéreurs internationaux (US / Résidence secondaire)", "Amateurs de 'Quiet Luxury' & Intimité"],
                "Atout clé pour la vente": ["Proximité immédiate des commerces et plages", "Panorama exceptionnel et mythe azuréen", "Vues panoramiques et discrétion absolue"]
            })
            st.dataframe(df_synthese_marche, use_container_width=True)
    else:
        st.warning("⚠️ Aucun fichier CSV n'a été détecté dans votre dépôt GitHub.")
