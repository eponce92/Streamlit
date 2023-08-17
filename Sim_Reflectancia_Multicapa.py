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

def plot_spectrum(file_path, n_substrate, lambda_min, lambda_max):
    data = pd.read_excel(file_path)
    wavelengths = np.linspace(lambda_min, lambda_max, 1000)
    reflectance = [total_reflectance(data, lambda_, n_substrate) for lambda_ in wavelengths]
    fig = plt.figure(figsize=(10, 6))
    plt.plot(wavelengths, reflectance, color='blue')
    plt.title('Espectro de reflectancia de la multicapa')
    plt.xlabel('Longitud de onda (nm)')
    plt.ylabel('Reflectancia')
    plt.grid(True)
    st.pyplot(fig)

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
    file_path = st.file_uploader('', type=['xlsx', 'xls'])
    if file_path:
        data = pd.read_excel(file_path)
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

# Documentation Section
st.markdown("---")
st.header("Documentación")

st.subheader("Instrucciones para usar el programa")
st.write("""
1. **Seleccionar una opción**: Puede subir un archivo Excel con las capas de la multicapa o agregar las capas manualmente.
2. **Subir archivo Excel**: Si selecciona "Subir archivo", debe cargar un archivo Excel con las columnas 'Material', 'Índice de refracción n', y 'Espesor (nm)'.
3. **Agregar capas manualmente**: Si selecciona "Agregar capas manualmente", debe ingresar los detalles de cada capa y hacer clic en "Agregar capa" para agregar más capas.
4. **Parámetros**: Ingrese el índice de refracción del sustrato y el rango de longitudes de onda.
5. **Graficar Espectro**: Haga clic en este botón para visualizar el espectro de reflectancia de la multicapa.
""")

st.subheader("Cómo funciona la simulación")
st.write("""
La simulación utiliza la teoría de las ondas de luz y la ecuación de Fresnel para calcular la reflectancia en cada interfaz de la multicapa. Considera la interferencia de las ondas reflejadas en cada interfaz y el desplazamiento de fase debido al recorrido óptico dentro de cada capa.

Las fórmulas clave son:

- Coeficiente de reflexión de Fresnel:
  \[
  r = \frac{{n_1 - n_2}}{{n_1 + n_2}}
  \]

- Desplazamiento de fase en una capa:
  \[
  \phi = \frac{{2\pi n d}}{{\lambda}}
  \]

- Reflectancia total de la multicapa:
  Se calcula iterativamente, tomando en cuenta la reflectancia de Fresnel en cada interfaz y la interferencia de las ondas reflejadas.

La multicapa está depositada sobre un sustrato de vidrio con un índice de refracción especificado, y la luz incide normalmente sobre la multicapa.
""")
