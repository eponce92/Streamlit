import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def compute_metrics(data, pressure, bore_size, mass):
    """Compute metrics based on input data and parameters."""
    # Fit the 40th-degree polynomial to the data
    coefficients = np.polyfit(data['Milisecond'], data['Compaction (mm)'], 40)
    polynomial_fit = np.poly1d(coefficients)
    data['Fitted Compaction (mm)'] = polynomial_fit(data['Milisecond'])

    # Calculate velocity and acceleration using the fitted compaction data
    data['Fitted Velocity (mm/ms)'] = -data['Fitted Compaction (mm)'].diff() / data['Milisecond'].diff()
    data['Fitted Acceleration (mm/ms^2)'] = data['Fitted Velocity (mm/ms)'].diff() / data['Milisecond'].diff()

    # Calculate pneumatic force
    P = pressure * 6894.76  # Pressure in Pascals (from psi to Pa)
    r = bore_size / 2 / 1000  # Radius in meters
    A = np.pi * r**2  # Area of the piston
    F_pneumatic = P * A  # Pneumatic force

    # Calculate inertial force using the fitted acceleration data
    data['Fitted Inertial Force (N)'] = mass * data['Fitted Acceleration (mm/ms^2)'] * 1000  # Convert mm/ms^2 to m/s^2
    
    # Results
    range_data = data[(data['Milisecond'] >= 1700) & (data['Milisecond'] <= 1900)]
    peak_inertia_force = range_data['Fitted Inertial Force (N)'].min()  # Finding the largest negative force
    peak_total_force = abs(F_pneumatic) + abs(peak_inertia_force)  # Summing absolute values of the forces
    
    return data, F_pneumatic, peak_inertia_force, peak_total_force




st.title("Pneumatic Cylinder Compaction Force Analysis")

# Upload the Excel file
uploaded_file = st.file_uploader("Choose an Excel file", type="xlsx")

if uploaded_file:
    try:
        data = pd.read_excel(uploaded_file)
        st.write("Data uploaded successfully!")
    except Exception as e:
        st.write("Error reading the uploaded file. Please ensure the file format and content are correct.")
        st.stop()

    # Parameters input
    st.sidebar.header("Parameters")
    pressure = st.sidebar.number_input("Pneumatic Pressure (psi)", min_value=0.0, value=65.0, step=0.1)
    bore_size = st.sidebar.number_input("Cylinder Bore Size (mm)", min_value=0.0, value=12.0, step=0.1)
    mass = st.sidebar.number_input("Mass of the tool (kg)", min_value=0.0, value=0.5, step=0.01)
    tip_diameter_thou = st.sidebar.number_input("Compactor Pin Diameter (thou)", min_value=0.0, value=25.0, step=0.1)
    
    # Filter the data from 1550ms to 2000ms and compute metrics
    focused_data = data[(data['Milisecond'] >= 1550) & (data['Milisecond'] <= 2000)]
    focused_data, F_pneumatic, peak_inertia_force, peak_total_force = compute_metrics(focused_data, pressure, bore_size, mass)
    
    # Display results
    st.header("Results:")
    st.write(f"**Pneumatic Force**: {F_pneumatic:.2f} N")
    st.write(f"**Peak Force due to Inertia**: {peak_inertia_force:.2f} N")
    st.write(f"**Peak Total Force**: {peak_total_force:.2f} N")
    
    # Calculating Pressure on the Compaction Pin Tip (corrected method)
    tip_diameter_inches = tip_diameter_thou * 0.001  # Convert thou to inches
    tip_area_in2 = np.pi * (tip_diameter_inches / 2)**2  # Area in square inches
    peak_total_force_lbs = peak_total_force * 0.2248  # Convert Newtons to pounds
    pressure_tip_psi_corrected = peak_total_force_lbs / tip_area_in2  # Pressure in PSI
    st.write(f"**Pressure on the Compaction Pin Tip**: {pressure_tip_psi_corrected:.2f} PSI")

    
    # Plotting
    metrics = ['Fitted Compaction (mm)', 'Fitted Velocity (mm/ms)', 'Fitted Acceleration (mm/ms^2)', 'Fitted Inertial Force (N)']
    titles = ['Fitted Compaction (Distance) vs Time', 'Fitted Velocity vs Time', 'Fitted Acceleration vs Time', 'Fitted Inertial Force vs Time']
    colors = ['blue', 'green', 'red', 'purple']  # Different colors for each graph
    
    # Determine the common Y-axis limits
    all_values = np.concatenate([focused_data[metric].values for metric in metrics])
    y_min = all_values.min()
    y_max = all_values.max()
    
    for metric, title, color in zip(metrics, titles, colors):
        st.subheader(title)
        fig, ax = plt.subplots(figsize=(15, 6))
        ax.plot(focused_data['Milisecond'], focused_data[metric], color=color)
        ax.axhline(0, color='gray', linewidth=0.5)  # Color the X-axis (where Y=0) in gray
        ax.grid(True)
        ax.set_xlabel('Milisecond')
        ax.set_ylabel(metric)
        ax.set_xlim(1600, 1950)  # Setting the X-axis range for all plots
        ax.set_ylim(y_min, y_max)  # Setting the same Y-axis range for all plots
    
        # Adding a label for the computed peak force in the last graph
        if metric == 'Fitted Inertial Force (N)':
            peak_time = focused_data['Milisecond'][focused_data[metric] == peak_inertia_force].iloc[0]
            ax.annotate(f'Peak: {peak_inertia_force:.2f} N', 
                        xy=(peak_time, peak_inertia_force), 
                        xytext=(peak_time-15, peak_inertia_force+5),  # Adjusting text position for better visibility
                        arrowprops=dict(facecolor='black', arrowstyle='->'))
    
        st.pyplot(fig)

else:
    st.write("Please upload an Excel file to proceed.")
