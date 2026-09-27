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
    st.markdown("Exploitation de votre base de données locale GitHub.")
    
    @st.cache_data(show_spinner="Lecture automatique du fichier texte sur GitHub...")
    def charger_fichier_texte_github():
        # L'application cherche automatiquement un fichier texte (.txt ou .csv) dans votre GitHub
        fichiers_texte = glob.glob("*.txt") + glob.glob("*.csv")
        
        if not fichiers_texte:
            return None
            
        # Prend le premier fichier trouvé
        fichier_a_lire = fichiers_texte[0]
        
        try:
            # Demande à Python de lire le fichier texte et de s'adapter au format automatiquement
            df = pd.read_csv(fichier_a_lire, low_memory=False, sep=None, engine='python', on_bad_lines='skip')
            df.columns = [str(c).strip() for c in df.columns]
            return df, fichier_a_lire
        except Exception as e:
            st.error(f"Erreur de lecture : {e}")
            return None, None

    resultat = charger_fichier_texte_github()
    
    if resultat is not None and resultat[0] is not None:
        df_brut, nom_fichier = resultat
        st.success(f"✅ Fichier '{nom_fichier}' détecté et chargé automatiquement ! ({len(df_brut):,} lignes lues).")

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
                        # Nettoyage ultra-robuste des prix
                        df_resultats['prix_net'] = pd.to_numeric(
                            df_resultats[col_valeur].astype(str).str.replace(',', '.').str.replace(' ', '').str.extract(r'([\d\.]+)', expand=False), 
                            errors='coerce'
                        )
                        
                        # DÉDUPLICATION : Une seule ligne par vente réelle
                        df_uniques = df_resultats.drop_duplicates(subset=[col_mutation])
                        
                        # CLASSEMENT DU MONT BORON
                        if "MONT BORON" in recherche_rue.upper():
                            def classifier_mont_boron(adresse):
                                adresse_str = str(adresse).upper()
                                if any(terme in adresse_str for terme in ['FORESTIERE', 'ALBAN', 'MONT BORON', 'REPUBLIQUE', 'MAETERLINCK', 'JEAN LORRAIN']):
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
                    
                    st.markdown("#### 📋 Détail des lignes correspondantes :")
                    st.dataframe(df_resultats.head(100), use_container_width=True)
                else:
                    st.warning("Aucun résultat trouvé.")
                    
        with tab2:
            st.markdown("### Synthèse des Secteurs")
            st.info("Données prêtes pour l'analyse patrimoniale.")
    else:
        st.error("⚠️ Aucun fichier texte (.txt ou .csv) n'a été trouvé dans votre GitHub. Vérifiez qu'il est bien présent au même endroit que ce code.")
