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
    "📊 Analyse DVF - Vraies Ventes (Ultra Léger)"
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

elif page == "📊 Analyse DVF - Vraies Ventes (Ultra Léger)":
    st.title("📊 Analyse DVF - Mode Ultra Léger (Anti-Blocage)")
    st.markdown("Ce mode analyse vos fichiers **un par un** en filtrant instantanément les données pour ne pas faire saturer votre tablette.")
    
    uploaded_file = st.sidebar.file_uploader("Importer un fichier CSV DVF (Faites-les un par un)", type=['csv'])

    if uploaded_file is not None:
        try:
            with st.spinner("Filtrage intelligent en cours..."):
                # Lecture optimisée : on ne charge que les colonnes strictement nécessaires
                colonnes = ['date_mutation', 'valeur_fonciere', 'nom_commune', 'adresse_nom_voie', 'type_local', 'surface_reelle_bati']
                df_brut = pd.read_csv(uploaded_file, usecols=lambda c: c in colonnes, low_memory=False)
                
                # Filtrage direct sur Nice
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
                        return "Hors Cible"
                
                df_nice['Quartier_Cible'] = df_nice['adresse_nom_voie'].apply(identifier_secteur)
                df_filtered = df_nice[df_nice['Quartier_Cible'] != "Hors Cible"].copy()
                df_filtered['valeur_fonciere'] = df_filtered['valeur_fonciere'].astype(int)
                
            if not df_filtered.empty:
                st.success(f"✅ Fichier validé : {len(df_filtered)} transactions pertinentes trouvées dans vos secteurs cibles !")
                st.dataframe(df_filtered.sort_values(by='date_mutation', ascending=False), use_container_width=True)
                
                prix_moyen = int(df_filtered['valeur_fonciere'].mean())
                st.metric("Prix moyen de cette sélection", f"{prix_moyen:,} €".replace(',', ' '))
            else:
                st.info("ℹ️ Ce fichier ne contient pas de transactions correspondant aux secteurs cibles (Carré d'Or, Promenade, Mont Boron). Vous pouvez passer au suivant.")
                
        except Exception as e:
            st.error(f- "Erreur de lecture sur ce fichier. Essayez de passer au suivant.")
    else:
        st.warning("⚠️ Veuillez importer un fichier CSV via le panneau latéral. Procédez **un par un** pour éviter toute saturation de la tablette.")
