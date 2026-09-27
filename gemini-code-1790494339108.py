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
    st.markdown("Exploitation de votre base de données locale GitHub avec calcul du prix au m².")
    
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
                # --- NOUVELLE RECHERCHE STABLE ---
                mots_cles = recherche_rue.upper().split()
                mots_a_ignorer = ['RUE', 'AVENUE', 'AV', 'BOULEVARD', 'BD', 'BVD', 'PROMENADE', 'PROM', 'DE', 'DES', 'LA', 'LE', 'LES', 'DU', 'D']
                mots_utiles = [mot for mot in mots_cles if mot not in mots_a_ignorer]
                
                if not mots_utiles:
                    mots_utiles = mots_cles
                    
                masque_global = pd.Series(True, index=df_brut.index)
                
                # On cherche chaque mot indépendamment (plus de crash)
                for mot in mots_utiles:
                    masque_mot = df_brut.astype(str).apply(lambda col: col.str.contains(mot, case=False, na=False)).any(axis=1)
                    masque_global &= masque_mot
                    
                df_resultats = df_brut[masque_global].copy()
                
                if not df_resultats.empty:
                    col_valeur = next((c for c in df_resultats.columns if 'valeur_fonciere' in c.lower() or 'prix' in c.lower()), None)
                    col_voie = next((c for c in df_resultats.columns if 'voie' in c.lower() or 'adresse' in c.lower()), None)
                    col_mutation = next((c for c in df_resultats.columns if 'id_mutation' in c.lower()), None)
                    col_surface = next((c for c in df_resultats.columns if 'surface_reelle_bati' in c.lower() or 'surface' in c.lower()), None)
                    
                    if col_valeur and col_mutation and col_surface:
                        # Nettoyage des prix
                        df_resultats['prix_net'] = pd.to_numeric(
                            df_resultats[col_valeur].astype(str).str.replace(',', '.').str.replace(' ', '').str.extract(r'([\d\.]+)', expand=False), 
                            errors='coerce'
                        )
                        
                        # Nettoyage des surfaces
                        df_resultats['surface_nette'] = pd.to_numeric(
                            df_resultats[col_surface].astype(str).str.replace(',', '.').str.replace(' ', '').str.extract(r'([\d\.]+)', expand=False), 
                            errors='coerce'
                        )
                        
                        # DÉDUPLICATION : Une seule ligne par vente réelle
                        df_uniques = df_resultats.drop_duplicates(subset=[col_mutation]).copy()
                        
                        # On garde uniquement les ventes où l'on a un prix ET une surface valide (> 0)
                        df_uniques = df_uniques[(df_uniques['prix_net'] > 0) & (df_uniques['surface_nette'] > 0)].copy()
                        
                        # CALCUL DU PRIX AU MÈTRE CARRÉ
                        df_uniques['prix_m2'] = df_uniques['prix_net'] / df_uniques['surface_nette']
                        
                        # CLASSEMENT DU MONT BORON
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
                        
                        # Indicateurs globaux
                        st.markdown(f"#### 📊 Indicateurs globaux sur '{' '.join(mots_utiles)}' :")
                        if not df_uniques.empty:
                            c1, c2, c3 = st.columns(3)
                            c1.metric("Prix moyen au m²", f"{df_uniques['prix_m2'].mean():,.0f} €/m²".replace(",", " "))
                            c2.metric("Prix médian au m²", f"{df_uniques['prix_m2'].median():,.0f} €/m²".replace(",", " "))
                            c3.metric("Surface moyenne vendue", f"{df_uniques['surface_nette'].mean():,.0f} m²".replace(",", " "))
                        else:
                            st.warning("Aucune surface n'est renseignée pour ces ventes (impossible de calculer le prix au m²).")
                    
                    st.markdown("#### 📋 Détail des ventes retenues :")
                    colonnes_a_afficher = [c for c in ['date_mutation', col_voie, 'prix_net', 'surface_nette', 'prix_m2', 'type_local'] if c in df_uniques.columns]
                    if colonnes_a_afficher:
                        st.dataframe(df_uniques[colonnes_a_afficher].head(100).style.format({'prix_net': "{:,.0f} €", 'surface_nette': "{:,.0f} m²", 'prix_m2': "{:,.0f} €/m²"}), use_container_width=True)
                    else:
                        st.dataframe(df_resultats.head(100), use_container_width=True)
                else:
                    st.warning("Aucun résultat trouvé. L'adresse n'est peut-être pas dans cet extrait de données.")
                    
        with tab2:
            st.markdown("### Synthèse des Secteurs")
            st.info("Données prêtes pour l'analyse patrimoniale.")
    else:
        st.error("⚠️ Aucun fichier texte n'a pu être lu dans votre GitHub.")
