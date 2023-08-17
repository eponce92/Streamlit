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
    # ... (same as original code) ...

def plot_spectrum(file_path, n_substrate, lambda_min, lambda_max):
    data = pd.read_excel(file_path)

    # Define the range of wavelengths
    wavelengths = np.linspace(lambda_min, lambda_max, 1000)

    # Calculate the reflectance spectrum
    reflectance = [total_reflectance(data, lambda_, n_substrate) for lambda_ in wavelengths]

    # Create a Figure instance
    fig = plt.figure(figsize=(10, 6))

    # Plot the reflectance spectrum
    plt.plot(wavelengths, reflectance, color='blue')
    plt.title('Espectro de reflectancia de la multicapa')
    plt.xlabel('Longitud de onda (nm)')
    plt.ylabel('Reflectancia')
    plt.grid(True)

    # Show plot with Streamlit
    st.pyplot(fig)

# Streamlit UI
st.title('Espectro de Reflectancia de la Multicapa')
file_path = st.file_uploader('Seleccione el archivo Excel:', type=['xlsx', 'xls'])
if file_path:
    n_substrate = st.number_input('Índice de refracción del sustrato:', min_value=1.0, value=1.5)
    lambda_min = st.number_input('Longitud de onda mínima (nm):', min_value=400.0, value=400.0)
    lambda_max = st.number_input('Longitud de onda máxima (nm):', min_value=400.0, value=800.0)
    if st.button('Graficar Espectro'):
        plot_spectrum(file_path, n_substrate, lambda_min, lambda_max)
