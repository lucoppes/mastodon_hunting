import streamlit as st
import sqlite3
import pandas as pd

# Título de la app
st.title("Visor de Base de Datos SQLite")

# Cargar archivo
db_file = st.file_uploader("Selecciona un archivo .db", type=["db"])

if db_file is not None:
    # Guardar temporalmente el archivo en disco para SQLite
    with open("mastodon.db", "wb") as f:
        f.write(db_file.read())

    conn = sqlite3.connect("mastodon.db")
    cursor = conn.cursor()

    # Obtener tablas
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]

    if tables:
        table = st.selectbox("Selecciona una tabla", tables)
        query = f"SELECT * FROM {table} LIMIT 100"
        df = pd.read_sql_query(query, conn)
        st.dataframe(df)
    else:
        st.warning("No se encontraron tablas en la base de datos.")