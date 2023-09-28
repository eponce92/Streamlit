import streamlit as st
import pandas as pd
import numpy as np
import math
import plotly.express as px


def polynomial_fit_data(data, degree=40):
    """Fit a polynomial to the data within the focused range and replace the original compaction values."""
    focus_indices = (data['Total Time (ms)'] >= 1550) & (data['Total Time (ms)'] <= 2000)
    focused_data = data[focus_indices]
    
    coefficients = np.polyfit(focused_data['Total Time (ms)'], focused_data['Compaction (mm)'], degree)
    poly = np.poly1d(coefficients)
    
    # Replace the compaction values in the focused range with the polynomial-fitted values
    data.loc[focus_indices, 'Compaction (mm)'] = poly(focused_data['Total Time (ms)'])
    
    # Compute velocity and acceleration directly from the polynomial-fitted compaction data
    data['Velocity (mm/ms)'] = data['Compaction (mm)'].diff() / data['Total Time (ms)'].diff()
    data['Smoothed Velocity (mm/ms)'] = data['Velocity (mm/ms)'].rolling(window=5).mean()
    data['Smoothed Acceleration (mm/ms^2)'] = data['Smoothed Velocity (mm/ms)'].diff() / data['Total Time (ms)'].diff()
    
    return data


def modified_process_data(data, pressure, bore_size, mass, tip_diameter):
    """Process the uploaded data and compute required metrics."""
    
    # Convert Time and Milisecond columns to a single time in milliseconds
    data['Total Time (ms)'] = data['Milisecond']
    
    # Apply polynomial fit
    data = polynomial_fit_data(data)

    # Calculate forces
    P = pressure * 6894.76  # Pressure in Pascals (from psi to Pa)
    r = bore_size / 2  # Radius in meters
    A = math.pi * r**2  # Area of the piston
    F_pneumatic = P * A  # Pneumatic force
    
    # Calculate inertial force for each time point
    data['Inertial Force (N)'] = mass * data['Smoothed Acceleration (mm/ms^2)'] * 1000  # Convert mm/ms^2 to m/s^2
    
    # Total force = constant pneumatic force + variable inertial force
    data['Total Force (N)'] = F_pneumatic + data['Inertial Force (N)']

    # Calculate pressure on the tip
    tip_area_mm2 = math.pi * (tip_diameter / 2)**2  # Area in mm^2
    max_force = data['Total Force (N)'].max()
    max_force_lbs = max_force * 0.2248  # Force in lbs
    pressure_tip_psi = max_force_lbs / (tip_area_mm2 / 645.16)  # Pressure in PSI

    return data, F_pneumatic, pressure_tip_psi


st.title("Pneumatic Cylinder Compaction Force Analysis")



st.write("""
### Pneumatic Cylinder Compaction Force Analysis

This application processes data from a PLC trend on an IL-100 distance sensor observing a pneumatic actuator. 
The main objective is to determine the peak force the cylinder exerts on powder during compaction.

#### Modifications:
- **Data Range Focus**: The analysis concentrates on the time range from 1550ms to 2000ms to focus on the main portion of the compaction event.
- **Polynomial Fit**: A 40th-degree polynomial fit has been applied to the 'Compaction (mm)' data within this time range.
- **Recalculated Metrics**: Metrics like velocity, acceleration, and forces have been recalculated based on the polynomial-fitted data.

#### Key Metrics and Calculations:

- **PSI (Pounds per Square Inch)**: This metric indicates the internal pressure within the pneumatic cylinder.

- **Flow**: Represents the rate at which air enters the pneumatic cylinder, which can influence the speed of the piston's movement.

- **Pneumatic Force (N)**: This is the force exerted by the pneumatic cylinder due to the air pressure inside.
""")

st.latex(r'F_{\text{pneumatic}} = P \times A')
st.write("""
Where:
- \( P \) is the pressure, converted from PSI to Pascals:
""")
st.latex(r'P = \text{PSI} \times 6894.76')
st.write("""
- \( A \) is the piston's area, calculated from the bore size:
""")
st.latex(r'A = \pi \times \left( \frac{\text{bore size}}{2} \right)^2')

st.write("""
- **Inertial Force (N)**: The force resulting from the tool's acceleration during the piston's movement.
""")
st.latex(r'F_{\text{inertia}} = m \times a')
st.write("""
Where:
- \( m \) is the mass of the tool.
- \( a \) is the acceleration, derived from the rate of change of velocity.

- **Total Force (N)**: The combined force of the pneumatic and inertial components during compaction.
""")
st.latex(r'F_{\text{total}} = F_{\text{pneumatic}} + F_{\text{inertia}}')

st.write("""
- **Pressure on the Tip (PSI)**: Represents the pressure experienced by the material being compacted.
""")
st.latex(r'\text{Pressure on the tip} = \frac{\text{Total Force in Pounds}}{\text{Tip Area in Square Inches}}')
st.write("""
Where the Total Force is converted to Pounds and the Tip Area is calculated using its diameter.

To use the application, upload the data file and adjust the parameters on the sidebar as needed. The results, accompanied by interactive plots, provide a comprehensive analysis of the compaction process.
""")



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
    bore_size = st.sidebar.number_input("Cylinder Bore Size (mm)", min_value=0.0, value=12.0, step=0.1) / 1000  # in meters
    mass = st.sidebar.number_input("Mass of the tool (kg)", min_value=0.0, value=0.5, step=0.01)
    tip_diameter = st.sidebar.number_input("Compactor Pin Diameter (thou)", min_value=0.0, value=25.0, step=0.1) * 0.0254  # in meters

    # Process data and calculate forces
    data, F_pneumatic, pressure_tip_psi = modified_process_data(data, pressure, bore_size, mass, tip_diameter)



    # Display results
    st.header("Results:")
    st.write(f"**Pneumatic Force**: {F_pneumatic:.2f} N")
    peak_inertia_force = data['Inertial Force (N)'].max()
    st.write(f"**Peak Force due to Inertia**: {peak_inertia_force:.2f} N")

    peak_total_force = data['Total Force (N)'].max() 
    st.write(f"**Peak Total Force**: {peak_total_force:.2f} N")
    st.write(f"**Pressure on the Compaction Pin Tip**: {pressure_tip_psi:.2f} PSI")

   
    # Interactive Plotting using plotly
    
    # Fitted Compaction (Distance) vs Time
    fig1 = px.line(data, x='Total Time (ms)', y='Compaction (mm)', title='Fitted Compaction (Distance) vs Time', range_x=[1550, 2000])
    st.plotly_chart(fig1)
    
    # Velocity vs Time
    fig2 = px.line(data, x='Total Time (ms)', y='Velocity (mm/ms)', title='Velocity vs Time', range_x=[1550, 2000])
    st.plotly_chart(fig2)
    
    # Acceleration vs Time
    fig3 = px.line(data, x='Total Time (ms)', y='Smoothed Acceleration (mm/ms^2)', title='Acceleration vs Time', range_x=[1550, 2000])
    st.plotly_chart(fig3)
    
    # Inertial Force vs Time
    fig4 = px.line(data, x='Total Time (ms)', y='Inertial Force (N)', title='Inertial Force vs Time', range_x=[1550, 2000])
    st.plotly_chart(fig4)



else:
    st.write("Please upload an Excel file to proceed.")
