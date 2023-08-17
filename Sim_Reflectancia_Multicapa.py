import numpy as np
import pandas as pd
import cmath
import matplotlib.pyplot as plt
import streamlit as st

# Function to calculate the Fresnel reflection coefficient at an interface
def fresnel_coefficient(n1, n2):
    return (n1 - n2) / (n1 + n2)

# Function to calculate the phase shift due to a single layer
def phase_shift(n, d, lambda_):
    return 2 * np.pi * n * d / lambda_

# Function to calculate the total reflectance of a multilayer stack
def total_reflectance(layers, lambda_, n_substrate):
    n_values = [1.0] + list(layers['Refractive index n']) + [n_substrate]
    d_values = [np.inf] + list(layers['Thickness (nm)']) + [np.inf]
    r = fresnel_coefficient(n_values[0], n_values[1])
    for i in range(1, len(n_values) - 1):
        r_i = fresnel_coefficient(n_values[i], n_values[i + 1])
        phi_i = phase_shift(n_values[i], d_values[i], lambda_)
        r = (r + r_i * cmath.exp(2j * phi_i)) / (1 + r * r_i * cmath.exp(2j * phi_i))
    return abs(r)**2

def plot_spectrum(data, n_substrate, lambda_min, lambda_max):
    if isinstance(data, pd.DataFrame):
        layers = data
    else:
        layers = pd.read_excel(data)
    wavelengths = np.linspace(lambda_min, lambda_max, 1000)
    reflectance = [total_reflectance(layers, lambda_, n_substrate) for lambda_ in wavelengths]
    
    # Create a DataFrame for the line chart
    chart_data = pd.DataFrame({
        'Longitud de onda (nm)': wavelengths,
        'Reflectancia': reflectance
    })
    
    # Plot the line chart using Streamlit's built-in line_chart function
    st.line_chart(chart_data, x='Longitud de onda (nm)', y='Reflectancia', use_container_width=True)


# Custom styling
st.markdown("""
    <style>
        .reportview-container {
            background: #f0f0f5;
        }
        .sidebar .sidebar-content {
            background: #f0f0f5;
        }
        h1, h2 {
            color: #333366;
        }
        h3 {
            color: #666699;
        }
    </style>
    """, unsafe_allow_html=True)

# Streamlit UI
st.title('Espectro de Reflectancia de la Multicapa')

option = st.selectbox('Seleccione una opción:', ['Subir archivo', 'Agregar capas manualmente'])

st.markdown("---")

if option == 'Subir archivo':
    st.subheader("Subir archivo Excel:")
    uploaded_file = st.file_uploader('', type=['xlsx', 'xls'])
    if uploaded_file:
        data = pd.read_excel(uploaded_file)
if option == 'Agregar capas manualmente':
    st.subheader('Agregar capas manualmente:')
    layers = []
    with st.expander('Capas de la multicapa:'):
        for i in range(st.session_state.get('num_layers', 1)):
            st.markdown(f"### Capa {i+1}")
            material = st.text_input('Material:', key=f'material_{i}')
            n = st.number_input('Índice de refracción:', key=f'n_{i}')
            thickness = st.number_input('Espesor (nm):', key=f'thickness_{i}')
            layers.append({'Material': material, 'Refractive index n': n, 'Thickness (nm)': thickness})
        if st.button('Agregar capa'):
            st.session_state.num_layers = st.session_state.get('num_layers', 1) + 1
    data = pd.DataFrame(layers)

st.markdown("---")

st.subheader("Parámetros:")
n_substrate = st.number_input('Índice de refracción del sustrato:', min_value=1.0, value=1.5)
lambda_min = st.number_input('Longitud de onda mínima (nm):', min_value=400.0, value=400.0)
lambda_max = st.number_input('Longitud de onda máxima (nm):', min_value=400.0, value=800.0)

if st.button('Graficar Espectro'):
    plot_spectrum(data, n_substrate, lambda_min, lambda_max)

# Documentation section
st.markdown("---")
st.header("Instrucciones para el uso del programa")
st.markdown("""
1. **Seleccione una opción**: Puede elegir entre subir un archivo Excel con las capas predefinidas o agregar capas manualmente.
2. **Subir archivo Excel**: Si elige subir un archivo, asegúrese de que tenga las columnas 'Material', 'Refractive index n' y 'Thickness (nm)'.
3. **Agregar capas manualmente**: Si elige agregar capas manualmente, complete los campos para cada capa y haga clic en 'Agregar capa' para agregar más capas.
4. **Parámetros**: Ingrese el índice de refracción del sustrato y el rango de longitudes de onda.
5. **Graficar Espectro**: Haga clic en este botón para calcular y visualizar el espectro de reflectancia.
""")

st.header("Explicación de la matemática y simulación")
st.subheader("Coeficiente de Reflexión de Fresnel")
st.write("El coeficiente de reflexión de Fresnel en cada interfaz se calcula usando la fórmula:")
st.latex(r"r = \frac{{n_1 - n_2}}{{n_1 + n_2}}")

st.subheader("Desplazamiento de Fase")
st.write("El desplazamiento de fase en cada capa se calcula usando la fórmula:")
st.latex(r"\phi = \frac{{2\pi n d}}{{\lambda}}")

st.subheader("Reflectancia Total")
st.write("""
La reflectancia total de la multicapa se calcula considerando tanto la reflectancia de Fresnel en cada interfaz como la interferencia de las ondas reflejadas. La fórmula recursiva es:
""")
st.latex(r"r = \frac{{r + r_i \cdot e^{2j\phi_i}}}{{1 + r \cdot r_i \cdot e^{2j\phi_i}}}")
st.write("Donde \( r_i \) es el coeficiente de reflexión de Fresnel en la interfaz actual y \( \phi_i \) es el desplazamiento de fase en la capa actual.")
st.write("La reflectancia final se obtiene tomando el valor absoluto al cuadrado del coeficiente de reflexión total:")
st.latex(r"R = |r|^2")