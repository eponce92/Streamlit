
import streamlit as st
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt

def process_data(data, pressure, bore_size, mass, tip_diameter):
    # Convert Time and Milisecond columns to a single time in milliseconds
    data['Total Time (ms)'] = data['Milisecond']

    # Calculate velocity and acceleration
    data['Velocity (mm/ms)'] = data['Compaction (mm)'].diff() / data['Total Time (ms)'].diff()
    data['Smoothed Velocity (mm/ms)'] = data['Velocity (mm/ms)'].rolling(window=5).mean()
    data['Smoothed Acceleration (mm/ms^2)'] = data['Smoothed Velocity (mm/ms)'].diff() / data['Total Time (ms)'].diff()

    # Calculate forces
    P = pressure * 6894.76  # Pressure in Pascals (from psi to Pa)
    r = bore_size / 2  # Radius in meters
    A = math.pi * r**2  # Area of the piston
    F_pneumatic = P * A  # Pneumatic force
    F_inertia = mass * data['Smoothed Acceleration (mm/ms^2)'].abs().max() * 1000  # In m/s^2
    F_total = F_pneumatic + F_inertia

    return F_pneumatic, F_inertia, F_total

st.title("Pneumatic Cylinder Compaction Force Analysis")

# Upload the Excel file
uploaded_file = st.file_uploader("Choose an Excel file", type="xlsx")

if uploaded_file:
    data = pd.read_excel(uploaded_file)
    st.write("Data uploaded successfully!")

    # Parameters input
    st.sidebar.header("Parameters")
    pressure = st.sidebar.number_input("Pneumatic Pressure (psi)", min_value=0.0, value=65.0, step=0.1)
    bore_size = st.sidebar.number_input("Cylinder Bore Size (mm)", min_value=0.0, value=12.0, step=0.1) / 1000  # in meters
    mass = st.sidebar.number_input("Mass of the tool (kg)", min_value=0.0, value=0.5, step=0.01)
    tip_diameter = st.sidebar.number_input("Compactor Pin Diameter (thou)", min_value=0.0, value=25.0, step=0.1) * 0.0254  # in meters

    # Process data and calculate forces
    F_pneumatic, F_inertia, F_total = process_data(data, pressure, bore_size, mass, tip_diameter)

    st.write(f"Pneumatic Force: {F_pneumatic:.2f} N")
    st.write(f"Force due to Inertia: {F_inertia:.2f} N")
    st.write(f"Total Force: {F_total:.2f} N")

    # Plotting
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(data['Total Time (ms)'], data['Compaction (mm)'], label='Compaction (mm)')
    ax.set_xlabel('Time (ms)')
    ax.set_ylabel('Compaction (mm)')
    ax.set_title('Compaction vs Time')
    ax.grid(True)
    st.pyplot(fig)

else:
    st.write("Please upload an Excel file to proceed.")

