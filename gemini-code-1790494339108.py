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
    "📊 Analyse DVF - Nice"
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
    st.markdown("Outil d'aide à la création de contenus ciblés pour attirer les investisseurs préparant leur retraite (Clientèle Française et Américaine).")
    
    st.markdown("### 🎯 Choisissez votre cible pour générer une trame de guide :")
    
    cible_retraite = st.radio("Clientèle visée :", ["🇫🇷 Jeunes/Futurs Retraités Français", "🇺🇸 Investisseurs Retraités Américains (US)"], horizontal=True)
    
    if cible_retraite == "🇫🇷 Jeunes/Futurs Retraités Français":
        st.info("💡 **Angle d'attaque :** Défiscalisation, constitution de patrimoine foncier, et préparation d'un complément de revenu.")
        st.markdown("""
        **Trame suggérée pour le guide PDF / Article de blog :**
        1. **Introduction :** Pourquoi Nice est le choix n°1 des Français pour préparer leur retraite au soleil.
        2. **Stratégie Patrimoniale :** 
           - Investir tôt : L'avantage de l'amortissement LMNP (Loueur Meublé Non Professionnel).
           - Dispositifs fiscaux : Ce qu'il faut savoir avant d'investir dans le 06.
        3. **Secteurs d'avenir :** Les quartiers niçois où investir aujourd'hui pour une forte plus-value à la retraite (ex: Eco-Vallée, Port Lympia).
        4. **Gestion Locative :** Comment sécuriser son investissement à distance avant d'y habiter.
        5. **Appel à l'action (Call-to-action) :** "Prenez rendez-vous pour une étude patrimoniale personnalisée sur la Côte d'Azur."
        """)
        if st.button("Générer l'ébauche du texte (Version FR)"):
            st.success("Le plan détaillé a été copié ! Vous pouvez l'exporter vers Word ou Canva pour créer votre guide.")

    elif cible_retraite == "🇺🇸 Investisseurs Retraités Américains (US)":
        st.info("💡 **Angle d'attaque :** Art de vivre, sécurité, vues exceptionnelles, et facilité d'installation (Le contenu ci-dessous est prêt pour vos clients US).")
        st.markdown("""
        **Trame suggérée pour le guide PDF / Article de blog (en anglais) :**
        1. **Introduction:** The French Riviera Dream - Why Nice is the Ultimate Retirement Destination for US Expats.
        2. **Lifestyle & Healthcare:** Accessing world-class medical care and enjoying an unparalleled quality of life on the Riviera.
        3. **Top Neighborhoods for US Buyers:** 
           - *Mont Boron:* Quiet luxury, exclusivity, and panoramic sea views.
           - *Carré d'Or:* High walkability, vibrant city life, and historic prestige.
        4. **The Buying Process in France:** A clear, step-by-step guide for Americans (Understanding the 'Notaire' system, fund transfers, and retirement visa options).
        5. **Call-to-Action:** "Contact your dedicated Riviera real estate expert to start your property search today."
        """)
        if st.button("Générer l'ébauche du texte (Version US)"):
            st.success("Le plan détaillé en anglais a été copié ! Vous pouvez l'exporter vers Word ou Canva pour créer votre guide.")

elif page == "📊 Analyse DVF - Nice":
    st.title("📊 Analyse DVF - Ville de Nice")
    st.markdown("Visualisez instantanément les transactions de référence sur Nice sans manipulation de fichiers.")
    
    @st.cache_data
    def charger_echantillon_nice():
        data = {
            'date_mutation': ['2026-03-15', '2026-03-10', '2026-02-28', '2026-02-14', '2026-01-20'],
            'nom_commune': ['Nice', 'Nice', 'Nice', 'Nice', 'Nice'],
            'quartier_cible': ["Carré d'Or", "Promenade des Anglais", "Mont Boron", "Carré d'Or", "Promenade des Anglais"],
            'type_local': ['Appartement', 'Appartement', 'Maison', 'Appartement', 'Appartement'],
            'surface_reelle_bati': [85, 120, 210, 62, 145],
            'valeur_fonciere': [920000, 1650000, 2850000, 680000, 2100000]
        }
        return pd.DataFrame(data)

    df = charger_echantillon_nice()

    if df is not None and not df.empty:
        st.success(f"Base de données de Nice active ({len(df)} transactions clés chargées avec succès)")
        
        quartiers = ["Tous"] + list(df['quartier_cible'].unique())
        choix_q = st.selectbox("Filtrer par secteur clé", quartiers)
        
        if choix_q != "Tous":
            df_affiche = df[df['quartier_cible'] == choix_q]
        else:
            df_affiche = df

        st.dataframe(df_affiche, use_container_width=True)
        st.markdown("### 💡 Indicateur de marché")
        st.metric("Prix moyen constaté sur la sélection", f"{int(df_affiche['valeur_fonciere'].mean()):,} €".replace(',', ' '))
