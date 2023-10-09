import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.title("Visualización de Google Sheets")

# Crea la conexión a GSheets
conn = st.experimental_connection("gsheets", type=GSheetsConnection)

# Lee la hoja de cálculo de Google como un DataFrame
# Asumiendo que la hoja en la que estás interesado se llama "Sheet1" 
# (esto es solo un nombre predeterminado, reemplázalo si tu hoja tiene un nombre diferente)
df = conn.read(
    worksheet="Sheet1",  
    usecols=[0, 1],  # Usar solo las dos primeras columnas
)

# Muestra el DataFrame en Streamlit
st.dataframe(df)
