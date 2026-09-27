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
    st.markdown("Exploitation de votre base de données locale GitHub avec calcul du prix au m² et adresses précises.")
    
    @st.cache_data(show_spinner="Lecture automatique de vos fichiers sur GitHub...")
    def charger_fichiers_github():
        fichiers = glob.glob("*.txt") + glob.glob("*.csv") + glob.glob("**/*.csv", recursive=True)
        if not fichiers:
            return None, 0
            
        liste_df = []
        for f in fichiers:
            try:
                df = pd.read_csv(f, sep=None, engine='python', on_bad_lines='skip')
                liste_df.append(df)
            except Exception as e:
                pass
                
        if liste_df:
            df_global = pd.concat(liste_df, ignore_index=True)
            df_global.columns = [str(c).strip() for c in df_global.columns]
            return df_global, len(fichiers)
        
        return None, 0

    df_brut, nb_fichiers = charger_fichiers_github()
    
    if df_brut is not None and not df_brut.empty:
        st.success(f"✅ {nb_fichiers} fichier(s) détecté(s) et chargé(s) automatiquement ! ({len(df_brut):,} lignes lues).")

        tab1, tab2 = st.tabs(["💰 Recherche & Analyse au m²", "📈 Synthèse"])
        
        with tab1:
            recherche_rue = st.text_input("Entrez un nom de rue (ex: ANGLAIS, MASSENA, MONT BORON) :", value="ANGLAIS")
            
            if recherche_rue:
                # --- MOTEUR DE RECHERCHE ---
                mots_cles = recherche_rue.upper().split()
                mots_a_ignorer = ['RUE', 'AVENUE', 'AV', 'BOULEVARD', 'BD', 'BVD', 'PROMENADE', 'PROM', 'DE', 'DES', 'LA', 'LE', 'LES', 'DU', 'D']
                mots_utiles = [mot for mot in mots_cles if mot not in mots_a_ignorer]
                
                if not mots_utiles:
                    mots_utiles = mots_cles
                    
                masque_global = pd.Series(True, index=df_brut.index)
                for mot in mots_utiles:
                    masque_mot = df_brut.astype(str).apply(lambda col: col.str.contains(mot, case=False, na=False)).any(axis=1)
                    masque_global &= masque_mot
                    
                df_resultats = df_brut[masque_global].copy()
                
                if not df_resultats.empty:
                    col_valeur = next((c for c in df_resultats.columns if 'valeur_fonciere' in c.lower() or 'prix' in c.lower()), None)
                    col_voie = next((c for c in df_resultats.columns if 'voie' in c.lower() or 'adresse' in c.lower() and 'numero' not in c.lower()), None)
                    col_mutation = next((c for c in df_resultats.columns if 'id_mutation' in c.lower()), None)
                    col_surface = next((c for c in df_resultats.columns if 'surface_reelle_bati' in c.lower() or 'surface' in c.lower()), None)
                    
                    if col_valeur and col_mutation and col_surface:
                        df_resultats['prix_net'] = pd.to_numeric(
                            df_resultats[col_valeur].astype(str).str.replace(',', '.').str.replace(' ', '').str.extract(r'([\d\.]+)', expand=False), 
                            errors='coerce'
                        )
                        df_resultats['surface_nette'] = pd.to_numeric(
                            df_resultats[col_surface].astype(str).str.replace(',', '.').str.replace(' ', '').str.extract(r'([\d\.]+)', expand=False), 
                            errors='coerce'
                        )
                        
                        df_uniques = df_resultats.drop_duplicates(subset=[col_mutation]).copy()
                        df_uniques = df_uniques[(df_uniques['prix_net'] > 0) & (df_uniques['surface_nette'] > 0)].copy()
                        df_uniques['prix_m2'] = df_uniques['prix_net'] / df_uniques['surface_nette']
                        
                        # --- RECONSTRUCTION DE L'ADRESSE COMPLÈTE ---
                        df_uniques['Adresse_Complete'] = ""
                        # Recherche de la colonne contenant le numéro de rue
                        col_num = next((c for c in df_uniques.columns if c in ['adresse_numero', 'numero_voie']), None)
                        
                        if col_num:
                            # Ajoute le numéro en évitant les ".0" décimaux
                            numeros = df_uniques[col_num].fillna('').astype(str).str.replace(r'\.0$', '', regex=True)
                            df_uniques['Adresse_Complete'] += numeros + " "
                            
                        if col_voie:
                            # Ajoute le nom de la rue
                            df_uniques['Adresse_Complete'] += df_uniques[col_voie].fillna('').astype(str)
                            
                        df_uniques['Adresse_Complete'] = df_uniques['Adresse_Complete'].str.strip()

                        # --- CLASSEMENT DU MONT BORON ---
                        if "BORON" in recherche_rue.upper():
                            def classifier_mont_boron(adresse):
                                adresse_str = str(adresse).upper()
                                if any(terme in adresse_str for terme in ['FORESTIERE', 'ALBAN', 'MONT BORON', 'REPUBLIQUE', 'MAETERLINCK', 'JEAN LORRAIN']):
                                    return "⭐ Mont Boron - Adresses Sélectes"
                                else:
                                    return "🏡 Mont Boron - Abords / Périphérie"
                            
                            if col_voie:
                                df_uniques['Sous_Secteur'] = df_uniques[col_voie].apply(classifier_mont_boron)
                                st.markdown("### 🏆 Analyse comparative au m²")
                                for sous_sec, groupe in df_uniques.groupby('Sous_Secteur'):
                                    prix_moyen_m2 = groupe['prix_m2'].mean()
                                    st.markdown(f"**{sous_sec}** ({len(groupe)} ventes) — Prix moyen : **{prix_moyen_m2:,.0f} € / m²**".replace(",", " "))
                        
                        # --- INDICATEURS GLOBAUX ---
                        st.markdown(f"#### 📊 Indicateurs globaux sur '{' '.join(mots_utiles)}' :")
                        if not df_uniques.empty:
                            c1, c2, c3 = st.columns(3)
                            c1.metric("Prix moyen au m²", f"{df_uniques['prix_m2'].mean():,.0f} €/m²".replace(",", " "))
                            c2.metric("Prix médian au m²", f"{df_uniques['prix_m2'].median():,.0f} €/m²".replace(",", " "))
                            c3.metric("Surface moyenne vendue", f"{df_uniques['surface_nette'].mean():,.0f} m²".replace(",", " "))
                        
                        # --- AFFICHAGE DU TABLEAU PROPRE ---
                        st.markdown("#### 📋 Détail des ventes retenues :")
                        
                        # Sélection des colonnes utiles
                        colonnes_brutes = ['date_mutation', 'Adresse_Complete', 'prix_net', 'surface_nette', 'prix_m2', 'type_local']
                        colonnes_a_afficher = [c for c in colonnes_brutes if c in df_uniques.columns]
                        df_affichage = df_uniques[colonnes_a_afficher].copy()
                        
                        # Renommage esthétique pour les professionnels
                        renommage = {
                            'date_mutation': 'Date',
                            'Adresse_Complete': 'Adresse',
                            'prix_net': 'Prix Net',
                            'surface_nette': 'Surface',
                            'prix_m2': 'Prix au m²',
                            'type_local': 'Type de Bien'
                        }
                        df_affichage = df_affichage.rename(columns=renommage)
                        
                        # Application du formatage visuel (espaces, euros, m²)
                        format_dict = {}
                        if 'Prix Net' in df_affichage.columns: format_dict['Prix Net'] = "{:,.0f} €"
                        if 'Surface' in df_affichage.columns: format_dict['Surface'] = "{:,.0f} m²"
                        if 'Prix au m²' in df_affichage.columns: format_dict['Prix au m²'] = "{:,.0f} €/m²"
                        
                        st.dataframe(df_affichage.sort_values(by='Date', ascending=False).head(100).style.format(format_dict), use_container_width=True)
                        
                    else:
                        st.dataframe(df_resultats.head(100), use_container_width=True)
                else:
                    st.warning("Aucun résultat trouvé. L'adresse n'est peut-être pas dans cet extrait de données.")
                    
        with tab2:
            st.markdown("### Synthèse des Secteurs")
            st.info("Données prêtes pour l'analyse patrimoniale.")
    else:
        st.error("⚠️ Aucun fichier texte n'a pu être lu dans votre GitHub.")
