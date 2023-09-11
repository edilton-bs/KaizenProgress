import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import base64
import spotipy
import random
from spotipy.oauth2 import SpotifyClientCredentials

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="2173f16a9c7c4c90bc3ebecbfed52a15",
                                                           client_secret="2685aa5dbd0b40de870759851e02f58a"))

# Configurações iniciais do Streamlit
st.title('📈 Meu progresso')

csv_file = "metas_data.csv"

# Ler os dados do CSV
try:
    data = pd.read_csv(csv_file)
except FileNotFoundError:
    data = pd.DataFrame(columns=["NOME", "META", "VALOR"])
    data.to_csv(csv_file, index=False)

# Seção para adicionar metas está aqui
with st.expander("Add dados"):
    with st.form(key="add_goal"):
        available_names = data["NOME"].unique().tolist() if not data.empty else []
        name = st.selectbox("Nome", options=available_names)
        meta_value = st.number_input("Valor", value=0)
        submit_button = st.form_submit_button("Adicionar/Atualizar Valor")

        if submit_button and not data.empty:
            meta_name = data[data["NOME"] == name]['META'].iloc[0]
            data.loc[len(data)] = [name, meta_name, meta_value]
            data.to_csv(csv_file, index=False)
            st.success(f"Valor para {name} adicionado com sucesso!")

# Verifica se a meta foi atingida e plota gráficos fora do bloco 'if submit_button'
if not data.empty:
    total_value = data[data["NOME"] == name]['VALOR'].sum()
    meta_name = data[data["NOME"] == name]['META'].iloc[0]
    
    if total_value >= meta_name:
        st.success(f"Parabéns, {name}! Você conseguiu!")

        # Busca faixas baseadas em um critério
        tracks = sp.search(q='genre:"Indie"', type='track', limit=50)
        
        # Verifica se temos faixas na resposta
        if tracks['tracks']['items']:
            # Escolhe uma faixa aleatória
            
            random_track = random.choice(tracks['tracks']['items'])
            
            
            # Exibe informações sobre a faixa
            track_name = random_track['name']
            track_artist = random_track['artists'][0]['name']
            track_link = random_track['external_urls']['spotify']
            
            st.success(f"Sua recompensa é ouvir a música: [{track_name} de {track_artist}]({track_link})")
        else:
            st.warning("Não foi possível encontrar uma faixa. Tente novamente mais tarde.")
    



    # Gráfico de linha não-acumulativo com pontos
    st.write(f"Progresso: {total_value}/{meta_name}")
    #for name in st.session_state.data["NOME"].unique():
    df = data[data["NOME"] == name][["VALOR"]]
    plt.figure(figsize=(10, 4))
    plt.plot(df["VALOR"], marker='o')
    plt.title(f"Progresso de {name}")
    plt.xlabel("Tempo")
    plt.ylabel("Valor")
    st.pyplot(plt)
    
    # Gráfico da meta escolhida usando Matplotlib
    st.write(f"Progresso da Meta: {name}")
    df = data[data["NOME"] == name][["VALOR"]].cumsum()
    plt.figure(figsize=(10, 4))
    plt.plot(df["VALOR"], marker='o')
    plt.title(f"Progresso Cumulativo da Meta: {name}")
    plt.xlabel("Tempo")
    plt.ylabel("Valor Cumulativo")
    st.pyplot(plt)

