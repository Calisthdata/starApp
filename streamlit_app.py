import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Tood AI - École", page_icon="🤖", layout="wide")

# 1. Dataset Educatif
@st.cache_data
def load_educational_data():
    data = {
        "Animal": ["Chien", "Chat", "Lion", "Éléphant", "Panda", "Kangourou", "Pingouin", "Aigle", "Requin", "Loup", "Vache", "Serpent"],
        "Continent": ["Europe", "Asie", "Afrique", "Afrique", "Asie", "Océanie", "Antarctique", "Amérique", "Europe", "Europe", "Europe", "Asie"],
        "Cri": ["Aboie", "Miaule", "Rugit", "Barrit", "Grogne", "Tousse", "Brait", "Glapit","Clic","Hurle", "Meugle", "Siffle"],
        "Alimentation": ["Omnivore", "Carnivore", "Carnivore", "Herbivore", "Herbivore", "Herbivore", "Carnivore", "Carnivore", "Carnivore", "Carnivore", "Herbivore", "Omnivore"],
        "Vitesse_max_kmh": [45, 48, 80, 40, 32, 70, 36, 160, 19, 83, 36, 20],
        "Dangerosité": [3, 2, 9, 7, 8, 6, 1, 9, 2, 2, 5, 9],
        "Caractéristiques": [
            "Fidèle, aime les os, domestique.",
            "Indépendant, aime le lait, agile.",
            "Roi de la savane, prédateur alpha, vit en groupe.",
            "Grandes oreilles, trompe, très intelligent.",
            "Il est gros et doux, proche cousin de l'ours",
            "Le kangourou saute très haut",
            "Le pinguin glisse sur la banquise",
            "On l'appel : Roi des cieux",
            "Prédateur marin, dents tranchantes, cartilagineux.",
            "Vit en meute, chasseur nocturne, sauvage.",
            "Produit du lait, calme, vit en ferme."
            ],
        "Le_Savais_Tu": [
            "Le chien est le meilleur ami de l'homme depuis 15 000 ans.",
            "Un chat peut sauter jusqu'à 6 fois sa taille !",
            "Le rugissement d'un lion s'entend à 8 kilomètres à la ronde.",
            "L'éléphant est le seul mammifère qui ne peut pas sauter.",
            "Un panda passe 12 heures par jour à manger du bambou.",
            "Le kangourou utilise sa queue comme une troisième jambe pour s'équilibrer.",
            "Les pingouins ne volent pas dans l'air, ils 'volent' sous l'eau !",
            "L'aigle peut voir un lapin à plus de 3 kilomètres de distance."
            "Prédateur marin, dents tranchantes, cartilagineux.",
            "Vit en meute, chasseur nocturne, sauvage.",
            "Produit du lait, calme, vit en ferme.",
            "Rampe, peut être venimeux, peau écailleuse."
        ]
    }
    return pd.DataFrame(data)

df = load_educational_data()

# --- INTERFACE ---
st.sidebar.title("🏫 Menu Scolaire")
choice = st.sidebar.selectbox("Que veux-tu faire ?", ["Discuter avec le Robot","Recherche & Caractéristiques", "Explorer la Carte", "Le Coin des Statistiques"])

if choice == "Discuter avec le Robot":
    st.title("🤖 Tood Ai")
    st.info("Je suis Tood, ton assitant IA qui t'aide à en apprendre plus sur les animaux. Pose-moi une question sur un animal")

    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Bonjour ! Je connais plein de secrets sur la nature. Demande-moi : 'Qui barrit ?' ou 'Parle moi du Panda'."}]

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    if prompt := st.chat_input("Ta question ici..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        res = "Je ne sais pas encore ça, mais je vais apprendre !"
        p_low = prompt.lower()

        for _, row in df.iterrows():
            if row['Cri'].lower() in p_low:
                if "lion" in p_low and row['Animal'] == "Chien":
                    response = f"Faux. Selon mes données, c'est le **{row['Animal']}** qui {row['Cri'].lower()}."
                else:
                    response = f"L'animal qui {row['Cri'].lower()} est le **{row['Animal']}**."
                break
            elif row['Animal'].lower() in p_low:
                response = f"Le **{row['Animal']}** est {row['Alimentation'].lower()}. Note de danger : {row['Dangerosité']}/10. {row['Caractéristiques']}"
                break


        for _, row in df.iterrows():
            if row['Cri'].lower() in p_low:
                res = f"C'est le **{row['Animal']}** ! Sais-tu que : {row['Le_Savais_Tu']}"
                break
            elif row['Animal'].lower() in p_low:
                res = f"Le **{row['Animal']}** vit en **{row['Continent']}**. {row['Le_Savais_Tu']}"
                break
        
        with st.chat_message("assistant"):
            st.write(res)
        st.session_state.messages.append({"role": "assistant", "content": res})
elif choice == "Recherche & Caractéristiques":
    st.title("🔍 Recherche Avancée")
    search_query = st.text_input("Recherchez un mot-clé dans les caractéristiques (ex: 'lait', 'sauvage', 'trompe')")
    
    if search_query:
        # Filtrage du dataframe selon les caractéristiques
        results = df[df['Caractéristiques'].str.contains(search_query, case=False, na=False)]
        
        if not results.empty:
            st.write(f"Résultat(s) pour : '{search_query}'")
            st.dataframe(results[['Animal', 'Alimentation', 'Caractéristiques']], use_container_width=True)
        else:
            st.warning("Aucun animal ne correspond à cette caractéristique.")
    else:
        st.info("Entrez un mot pour filtrer les animaux.")

elif choice == "Explorer la Carte":
    st.title("🌍 Voyage autour du monde")
    st.write("Clique sur un continent pour voir ses animaux :")
    cont = st.selectbox("Choisis un continent", df['Continent'].unique())
    selected_animals = df[df['Continent'] == cont]
    st.table(selected_animals[['Animal', 'Alimentation', 'Le_Savais_Tu']])

elif choice == "Le Coin des Statistiques":
    st.title("📊 Les Records des Animaux")
    
    # Graphique de vitesse pour les enfants
    fig = px.bar(df, x="Animal", y="Vitesse_max_kmh", color="Continent", 
                 title="Qui court le plus vite ? (en km/h)",
                 labels={'Vitesse_max_kmh': 'Vitesse (km/h)'})
    st.plotly_chart(fig, use_container_width=True)
    st.title("📊 Dashboard des Données")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Niveau de Dangerosité")
        fig_danger = px.bar(df, x="Animal", y="Dangerosité", color="Animal", 
                            title="Classement par Danger (1-10)", color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig_danger, use_container_width=True)
        
    with col2:
        st.subheader("Répartition par Alimentation")
        fig_diet = px.pie(df, names="Alimentation", title="Régimes alimentaires", 
                          hole=0.4, color_discrete_sequence=px.colors.qualitative.Safe)
        st.plotly_chart(fig_diet, use_container_width=True)

    st.subheader("Données Brutes")
    st.table(df)
