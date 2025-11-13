
import streamlit as st
import pandas as pd
from google.cloud import firestore
from google.oauth2 import service_account
import json

key_dict = json.loads(st.secrets["textkey"])
creds =service_account.Credentials.from_service_account_info(key_dict)

db = firestore.Client(credentials=creds, project="names-project-certificado-tec")

st.title("Netflix app")

@st.cache_data
def cargar_datos():
    docs = db.collection("movies").stream()
    data = []
    for doc in docs:
        d = doc.to_dict()
        data.append(d)
    df = pd.DataFrame(data)
    return df

data = cargar_datos()
filtered_data=data.copy()
sidebar=st.sidebar

agree = sidebar.checkbox('Mostrar todos los filmes')

myname = sidebar.text_input('Título del filme:')
filtrar_filme = sidebar.button("Buscar filmes")

if myname and not agree:
    directores_filtrados = (data[data['name'].str.contains(myname, case=False, na=False)]['director'].dropna().unique())
else:
    directores_filtrados = data['director'].dropna().unique()

director=sidebar.selectbox("Seleccionar Director:", options=["(Todos)"] + sorted(directores_filtrados.tolist()))
filtrar_director=sidebar.button("Filtrar director")

if 'filtro_nombre' not in st.session_state:
    st.session_state.filtro_nombre = ""
if 'filtro_director' not in st.session_state:
    st.session_state.filtro_director = "(Todos)"

if filtrar_filme:
    st.session_state.filtro_nombre = myname
if filtrar_director:
    st.session_state.filtro_director = director

if not agree:
    if st.session_state.filtro_nombre:
        filtered_data = filtered_data[
            filtered_data['name'].str.contains(st.session_state.filtro_nombre, case=False, na=False)
        ]
    if st.session_state.filtro_director != "(Todos)":
        filtered_data = filtered_data[
            filtered_data['director'] == st.session_state.filtro_director
        ]

with st.sidebar.form("Nuevo filme"):
    nuevo_nombre = st.text_input('Name: ')
    nuevo_company = st.selectbox("Company", options=sorted(data['company'].dropna().unique().tolist()))
    nuevo_director = st.selectbox("Director", options=sorted(data['director'].dropna().unique().tolist()))
    nuevo_genre = st.selectbox("Genre", options=sorted(data['genre'].dropna().unique().tolist()))

    new_film=st.form_submit_button("Nuevo filme")

    if new_film:
        if (not nuevo_nombre) or (not nuevo_director) or (not nuevo_company) or (not nuevo_genre):
            st.error("⚠️ Todos los campos deben tener datos.")
        else:
            nuevo_film = {
                "name": nuevo_nombre,
                "company": nuevo_company,
                "director": nuevo_director,
                "genre": nuevo_genre}

            db.collection("movies").add(nuevo_film)
            data = pd.concat([data, pd.DataFrame([nuevo_film])], ignore_index=True)
            filtered_data=data.copy()
            st.success(f"Filme '{nuevo_nombre}' agregado exitosamente.")

            st.cache_data.clear()
            st.rerun()

st.write(f"Total de filmes mostrados: {filtered_data.shape[0]}")
st.dataframe(filtered_data)

