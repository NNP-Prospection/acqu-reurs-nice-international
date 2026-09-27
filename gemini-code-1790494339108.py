import streamlit as st
import pandas as pd
import glob
import os

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
    st.title("📊 Analyse DVF - Marché Immobilier de Nice & Sous-Secteurs")
    st.markdown("Exploitation avancée avec distinction des micro-localisations (ex: Mont Boron Sélect vs Périphérique).")
    
    @st.cache_data(show_spinner="Chargement et nettoyage intelligent des fichiers DVF...")
    def charger_et_nettoyer_fichiers():
        fichiers_csv = glob.glob("*.csv") + glob.glob("**/*.csv", recursive=True)
        if not fichiers_csv:
            return None
        
        liste_df = []
        for f in fichiers_csv:
            try:
                # Lecture robuste gérant les séparateurs point-virgule ou virgule
                df_temp = pd.read_csv(f, low_memory=False, sep=None, engine='python', on_bad_lines='skip')
                liste_df.append(df_temp)
            except:
                pass
                
        if liste_df:
            df_global = pd.concat(liste_df, ignore_index=True)
            # Nettoyage des noms de colonnes (suppression des espaces)
            df_global.columns = [c.strip() for c in df_global.columns]
            return df_global
        return None

    df_brut = charger_et_nettoyer_fichiers()

    if df_brut is not None and not df_brut.empty:
        st.success(f"✅ Base de données chargée et normalisée ({len(df_brut):,} lignes).")

        tab1, tab2 = st.tabs([
            "💰 1. Recherche & Analyse par Sous-Secteurs", 
            "📈 2. Synthèse & Stratégie Clientèle"
        ])
        
        with tab1:
            st.subheader("Filtrage intelligent et distinction des micro-marchés")
            st.markdown("Recherchez un secteur (ex: *Mont Boron*, *Anglais*, *France*) pour analyser finement les prix réels.")
            
            recherche_rue = st.text_input("Entrez un terme de recherche :", value="MONT BORON")
            
            if recherche_rue:
                # Recherche insensible à la casse sur l'ensemble du dataframe
                masque_global = df_brut.astype(str).apply(lambda col: col.str.contains(recherche_rue, case=False, na=False)).any(axis=1)
                df_resultats = df_brut[masque_global].copy()
                
                st.metric("Transactions correspondantes trouvées", f"{len(df_resultats):,}")
                
                if not df_resultats.empty:
                    # Identification des colonnes clés
                    col_valeur = next((c for c in df_resultats.columns if 'valeur_fonciere' in c.lower() or 'prix' in c.lower()), None)
                    col_voie = next((c for c in df_resultats.columns if 'voie' in c.lower() or 'adresse' in c.lower()), None)
                    col_surface = next((c for c in df_resultats.columns if 'surface' in c.lower()), None)
                    
                    if col_valeur:
                        # Nettoyage de la colonne valeur foncière (remplacement des virgules par des points si besoin et conversion en nombre)
                        df_resultats['prix_net'] = pd.to_numeric(
                            df_resultats[col_valeur].astype(str).str.replace(',', '.').str.extract(r'([\d\.]+)', expand=False), 
                            errors='coerce'
                        )
                        
                        # --- SOUS-CLASSEMENT STRATÉGIQUE (Exemple pour le Mont Boron) ---
                        if "MONT BORON" in recherche_rue.upper():
                            def classifier_mont_boron(adresse):
                                adresse_str = str(adresse).upper()
                                # Adresses les plus sélectes / recherchées du Mont Boron
                                if any(terme in adresse_str for terme in ['FORESTIERE', 'ALBAN', 'MONT BORON', 'REPUBLIQUE', 'MAETERLINCK', 'CORNICHE INF', 'CORN INF', 'CORN MOY']):
                                    return "⭐ Mont Boron - Secteur Très Sélect (Corniches / Hauteurs)"
                                else:
                                    return "🏡 Mont Boron - Secteur Périphérique / Abords"
                            
                            if col_voie:
                                df_resultats['Sous_Secteur'] = df_resultats[col_voie].apply(classifier_mont_boron)
                                
                                st.markdown("### 🏆 Analyse comparative par micro-localisation (Mont Boron)")
                                for sous_sec, groupe in df_resultats.groupby('Sous_Secteur'):
                                    prix_moyen = groupe['prix_net'].mean()
                                    st.markdown(f"**{sous_sec}** ({len(groupe)} transactions) — Prix moyen constaté : **{prix_moyen:,.0f} €**".replace(",", " "))
                        
                        # Indicateurs globaux sur la sélection
                        st.markdown("#### 📊 Indicateurs de la sélection :")
                        c1, c2 = st.columns(2)
                        c1.metric("Prix moyen global", f"{df_resultats['prix_net'].mean():,.0f} €".replace(",", " "))
                        c2.metric("Prix médian global", f"{df_resultats['prix_net'].median():,.0f} €".replace(",", " "))
                    
                    st.markdown("#### 📋 Détail des transactions :")
                    st.dataframe(df_resultats.head(100), use_container_width=True)
                else:
                    st.warning("Aucun résultat trouvé pour ce terme.")
            else:
                st.info("💡 Saisissez un mot-clé.")
                    
        with tab2:
            st.subheader("Synthèse & Argumentaire Clientèle")
            st.markdown("Positionnement des biens pour vos clients à fort pouvoir d'achat.")
            
            df_synthese_marche = pd.DataFrame({
                "Secteur Clé": ["Carré d'Or", "Promenade des Anglais", "Mont Boron"],
                "Micro-cibles": ["Piétonnier, Actifs, Luxe urbain", "Front de mer, Vues panoramiques", "Quiet Luxury, Adresses confidentielles"],
                "Atout Stratégique": ["Proximité immédiate des commerces", "Mythe azuréen et standing international", "Discrétion absolue et panoramas d'exception"]
            })
            st.dataframe(df_synthese_marche, use_container_width=True)
    else:
        st.warning("⚠️ Aucun fichier CSV détecté dans le dépôt.")
