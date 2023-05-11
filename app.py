import streamlit as st
from soccerapi.api import Api888Sport
import datetime

st.set_page_config(
    page_title="bet.py",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.sidebar.markdown(
    "<div align='center'><img src='https://github.com/antoniomlo/Data_Science/blob/main/img/amlo-1.png?raw=true' width='100'></div>",
    unsafe_allow_html=True,
)
st.sidebar.title(" ")
st.sidebar.title(" ")
st.sidebar.title("""😁 Olá, seja bem-vindo(a)""")
st.sidebar.write(
    """Aqui você encontra as odds das principais ligas do mundo!"""
)
st.sidebar.subheader(
    """🚀 [Portfólio](https://www.figma.com/proto/BlN1MI7h6WY9FadR1yufiu/Portf%C3%B3lio?page-id=0%3A1&type=design&node-id=314-165&viewport=-15%2C627%2C0.12&scaling=scale-down&starting-point-node-id=314%3A165&hotspot-hints=0)"""
)
st.sidebar.subheader("""✉️ Contato""")
st.sidebar.markdown(
    """
<a href="mailto:antoniomlm26@gmail.com" target="_blank"><img width=35 src="https://i.redd.it/izqwm1g21b751.png"/></a>
<a href="https://www.linkedin.com/in/antoniomlo/" target="_blank"><img width=50 src="https://static.vecteezy.com/system/resources/previews/018/930/587/original/linkedin-logo-linkedin-icon-transparent-free-png.png"/></a>
""",
    unsafe_allow_html=True,
)


st.image(
    "https://github.com/antoniomlo/streamlit/blob/main/API/LinkedIn%20cover%20-%202.png?raw=true"
)
# Criando a instância da API
api = Api888Sport()

# Obtendo a lista de competições disponíveis
competitions = api.competitions()

# Obtendo a entrada do usuário para selecionar o país
country = st.sidebar.selectbox("Selecione o país", list(competitions.keys()))

# Obtendo as ligas correspondentes ao país selecionado
leagues = list(competitions[country].keys())

# Obtendo a entrada do usuário para selecionar a liga
league = st.sidebar.selectbox("Selecione a liga", leagues)

# Obtendo a URL com base na liga selecionada
url = competitions[country][league]
# Obtendo as odds para a URL especificada
odds = api.odds(url)

# Criando um menu dropdown para selecionar o jogo
jogo_selecionado = st.selectbox("Selecione um jogo", sorted([f"{data['home_team']} X {data['away_team']}" for data in odds]))

# Filtrando o DataFrame para exibir as informações do jogo selecionado
data_jogo = [data for data in odds if f"{data['home_team']} X {data['away_team']}" == jogo_selecionado][0]

# Exibindo as informações do jogo selecionado
st.subheader(f"**{data_jogo['home_team']} X {data_jogo['away_team']}**")
datetime_obj = datetime.datetime.strptime(data_jogo['time'], "%Y-%m-%dT%H:%M:%SZ") - datetime.timedelta(hours=3)
date_str = datetime_obj.strftime("%d/%m %Hh:%M")
st.caption(f"**{date_str}**")

st.markdown("**Resultados full-time**")
col1, col2, col3 = st.columns([1,1,1])
col1.metric(label="Casa", value=f"{data_jogo['full_time_result']['1']/1000:.2f}",delta_color="normal")
col2.metric(label="Empate", value=f"{data_jogo['full_time_result']['X']/1000:.2f}",delta_color="off")
col3.metric(label="Fora", value=f"{data_jogo['full_time_result']['2']/1000:.2f}",delta_color="inverse")

st.markdown("**Chance dupla**")
col1, col2, col3 = st.columns([1,1,1])
col1.metric(label="Casa ou Empate", value=f"{data_jogo['double_chance']['1X']/1000:.2f}",delta_color="normal")
col2.metric(label="Fora ou Empate", value=f"{data_jogo['double_chance']['2X']/1000:.2f}",delta_color="off")
col3.metric(label="Casa ou Fora", value=f"{data_jogo['double_chance']['12']/1000:.2}")

col1, col2 = st.columns([1,1])
col1.markdown("**Gols**")
col1.write(f"- Acima de 2,5 gols: {data_jogo['under_over']['O2.5']/1000:.2f}")
col1.write(f"- Abaixo de 2,5 gols: {data_jogo['under_over']['U2.5']/1000:.2f}")

col2.markdown("**Ambas marcam**")
col2.write(f"- Sim: {data_jogo['both_teams_to_score']['yes']/1000:.2f}")
col2.write(f"- Não: {data_jogo['both_teams_to_score']['no']/1000:.2f}")

# Obtendo a lista completa de jogos disponíveis para a liga selecionada
jogos = sorted([f"{data['home_team']} X {data['away_team']} - {date_str}" for data in odds])

# Exibindo a lista completa de jogos na sidebar
st.sidebar.header("Lista de jogos")

# Defina o número máximo de jogos a serem mostrados antes de pressionar o expander
max_jogos = 5

# Defina a variável de controle para rastrear o estado do expander
ver_todos_jogos = st.sidebar.expander("Ver Todos os Jogos")

# Mostre a lista de jogos
with ver_todos_jogos:
    for jogo in jogos:
        st.write(f"⚽ {jogo}")