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
    st.markdown("Exploitation intelligente des fichiers DVF (gestion des lots multiples et calculs précis).")
    
    @st.cache_data(show_spinner="Chargement automatique des fichiers DVF...")
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
            return pd.concat(liste_df, ignore_index=True)
        return None

    df_brut = charger_fichiers_depot()

    if df_brut is not None and not df_brut.empty:
        st.success(f"✅ Base de données chargée ({len(df_brut):,} lignes brutes au total).")

        tab1, tab2 = st.tabs([
            "💰 1. Analyse par Rue & Vraies Valeurs", 
            "📈 2. Synthèse & Indicateurs Clés par Secteur"
        ])
        
        with tab1:
            st.subheader("Recherche par rue ou secteur (ex: Mont Boron)")
            st.markdown("Filtrez les transactions et observez les prix réels constatés par les notaires.")
            
            recherche_rue = st.text_input("Entrez un nom de rue / quartier :", value="MONT BORON")
            
            if recherche_rue:
                masque_global = df_brut.astype(str).apply(lambda col: col.str.contains(recherche_rue, case=False, na=False)).any(axis=1)
                df_resultats = df_brut[masque_global].copy()
                
                st.metric("Lignes correspondantes trouvées", f"{len(df_resultats):,}")
                
                if not df_resultats.empty:
                    # Traitement pour isoler les ventes uniques (nettoyage des doublons de lots multiples)
                    col_valeur = [c for c in df_resultats.columns if 'valeur_fonciere' in c.lower()]
                    col_mutation = [c for c in df_resultats.columns if 'id_mutation' in c.lower()]
                    col_surface = [c for c in df_resultats.columns if 'surface_reelle_bati' in c.lower()]
                    col_type = [c for c in df_resultats.columns if 'type_local' in c.lower()]
                    
                    if col_valeur and col_mutation:
                        val_col = col_valeur[0]
                        mut_col = col_mutation[0]
                        
                        # Convertir en numérique
                        df_resultats[val_col] = pd.to_numeric(df_resultats[val_col], errors='coerce')
                        
                        # Création d'une vue par vente unique (pour éviter de compter 3 fois le même prix si cave + appt)
                        df_ventes_uniques = df_resultats.drop_duplicates(subset=[mut_col])
                        
                        st.markdown("#### 💎 Indicateurs calculés sur cette sélection :")
                        c1, c2, c3 = st.columns(3)
                        c1.metric("Nombre de ventes distinctes", f"{len(df_ventes_uniques):,}")
                        c2.metric("Prix de vente moyen", f"{df_ventes_uniques[val_col].mean():,.0f} €".replace(",", " "))
                        c3.metric("Prix de vente médian", f"{df_ventes_uniques[val_col].median():,.0f} €".replace(",", " "))
                    
                    st.markdown("#### 📋 Détail brut des lignes correspondantes :")
                    colonnes_affichage = [c for c in ['date_mutation', 'valeur_fonciere', 'adresse_nom_voie', 'type_local', 'surface_reelle_bati'] if c in df_resultats.columns]
                    if colonnes_affichage:
                        st.dataframe(df_resultats[colonnes_affichage].head(100), use_container_width=True)
                    else:
                        st.dataframe(df_resultats.head(100), use_container_width=True)
                else:
                    st.warning("Aucun résultat trouvé.")
            else:
                st.info("💡 Saisissez un mot-clé ci-dessus.")
                    
        with tab2:
            st.subheader("Analyse comparative des secteurs clés")
            st.markdown("Positionnement stratégique pour votre clientèle à fort pouvoir d'achat.")
            
            df_synthese_marche = pd.DataFrame({
                "Secteur Clé": ["Carré d'Or", "Promenade des Anglais", "Mont Boron"],
                "Type de biens recherchés": ["Appartement urbain, piétonnier", "Vue mer frontale, standing", "Villas, résidences de prestige, calme"],
                "Clientèle privilégiée": ["Actifs haut de gamme & Investisseurs", "Acquéreurs internationaux (US / Résidence secondaire)", "Amateurs de 'Quiet Luxury' & Intimité"],
                "Atout clé pour la vente": ["Proximité immédiate des commerces et plages", "Panorama exceptionnel et mythe azuréen", "Vues panoramiques et discrétion absolue"]
            })
            st.dataframe(df_synthese_marche, use_container_width=True)
    else:
        st.warning("⚠️ Aucun fichier CSV détecté.")
