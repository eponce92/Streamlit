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

# Streamlit UI
st.title('Espectro de Reflectancia de la Multicapa')

option = st.selectbox('Seleccione una opción:', ['Subir archivo', 'Agregar capas manualmente'])

if option == 'Subir archivo':
    file_path = st.file_uploader('Seleccione el archivo Excel:', type=['xlsx', 'xls'])
    if file_path:
        data = pd.read_excel(file_path)
else:
    layers = []
    st.subheader('Capas de la multicapa:')
    for i in range(st.session_state.get('num_layers', 1)):
        material = st.text_input(f'Material {i+1}:', key=f'material_{i}')
        n = st.number_input(f'Índice de refracción {i+1}:', key=f'n_{i}')
        thickness = st.number_input(f'Espesor (nm) {i+1}:', key=f'thickness_{i}')
        layers.append({'Material': material, 'Refractive index n': n, 'Thickness (nm)': thickness})
    if st.button('Agregar capa'):
        st.session_state.num_layers = st.session_state.get('num_layers', 1) + 1
    data = pd.DataFrame(layers)

n_substrate = st.number_input('Índice de refracción del sustrato:', min_value=1.0, value=1.5)
lambda_min = st.number_input('Longitud de onda mínima (nm):', min_value=400.0, value=400.0)
lambda_max = st.number_input('Longitud de onda máxima (nm):', min_value=400.0, value=800.0)

if st.button('Graficar Espectro'):
    plot_spectrum(data, n_substrate, lambda_min, lambda_max)
