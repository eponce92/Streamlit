import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.title("Visualización y Adición a Google Sheets")

# Crea la conexión a GSheets
conn = st.experimental_connection("gsheets", type=GSheetsConnection)

# Lee la hoja de cálculo de Google como un DataFrame
df = conn.read(
    worksheet="Sheet1",
    usecols=[0, 1],  # Usar solo las dos primeras columnas
)

# Elimina cualquier fila que pueda estar completamente vacía
df.dropna(how='all', inplace=True)

# Muestra el DataFrame actual en Streamlit
st.subheader("Contenido actual de la hoja:")
st.dataframe(df)

# Formulario para agregar una nueva entrada
with st.form(key='new_entry_form'):
    st.subheader("Añadir una nueva entrada")
    
    new_name = st.text_input("Nombre")
    new_age = st.number_input("Edad", min_value=0)

    # Cuando se envíe el formulario, agregue la nueva entrada al DataFrame y luego a Google Sheets
    submit_button = st.form_submit_button("Añadir")
    if submit_button:
        new_entry = pd.DataFrame({
            'Names': [new_name],
            'Ages': [new_age]
        })

        # Añade la nueva entrada y actualiza la hoja
        df = pd.concat([df, new_entry], ignore_index=True)
        conn.update(
            worksheet="Sheet1",
            data=df
        )

        st.cache_data.clear()  # Limpia el caché de datos
        st.experimental_rerun()  # Recarga la app

        st.success("Entrada añadida con éxito!")
