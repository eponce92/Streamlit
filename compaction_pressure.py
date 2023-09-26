import streamlit as st
import pandas as pd
import numpy as np
import math
import plotly.express as px

def process_data(data, pressure, bore_size, mass, tip_diameter):
    """Process the uploaded data and compute required metrics."""
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

# Documentation
st.write("""
### Pneumatic Cylinder Compaction Force Analysis
This application processes data from a PLC trend on an IL-100 distance sensor observing a pneumatic actuator. 
The main objective is to determine the peak force the cylinder exerts on powder during compaction.

#### Key Metrics:
- **PSI**: Represents the internal pressure of the pneumatic cylinder.
- **Flow**: Indicates the flow rate of air into the cylinder, influencing piston speed.
- **Pneumatic Force**: Calculated from the internal pressure and the cylinder's bore size.
    - \( F_{\text{pneumatic}} = P \times A \)
    where \( P \) is the pressure in Pascals and \( A \) is the piston's area.
- **Inertial Force**: Represents the force due to the tool's acceleration.
    - \( F_{\text{inertia}} = m \times a \)
    where \( m \) is the mass of the tool and \( a \) is its acceleration.
- **Total Force**: The sum of pneumatic and inertial forces.
- **Pressure on the Tip**: Represents the pressure experienced by the material being compacted.
    - Calculated by dividing the total force by the compactor pin's tip area.

To use the application, upload the data file and adjust the parameters on the sidebar as needed. The results will be displayed along with interactive plots for a comprehensive analysis.
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
    data, F_pneumatic, pressure_tip_psi = process_data(data, pressure, bore_size, mass, tip_diameter)


    # Display results
    st.header("Results:")
    st.write(f"**Pneumatic Force**: {F_pneumatic:.2f} N")
    peak_inertia_force = data['Inertial Force (N)'].max()
    st.write(f"**Peak Force due to Inertia**: {peak_inertia_force:.2f} N")

    peak_total_force = data['Total Force (N)'].max() 
    st.write(f"**Peak Total Force**: {peak_total_force:.2f} N")
    st.write(f"**Pressure on the Compaction Pin Tip**: {pressure_tip_psi:.2f} PSI")

    # Interactive Plotting using plotly
    st.subheader("Compaction vs Time")
    fig1 = px.line(data, x='Total Time (ms)', y='Compaction (mm)', title='Compaction vs Time')
    st.plotly_chart(fig1)

    st.subheader("Smoothed Acceleration vs Time")
    fig2 = px.line(data, x='Total Time (ms)', y='Smoothed Acceleration (mm/ms^2)', title='Smoothed Acceleration vs Time')
    st.plotly_chart(fig2)

    # Displaying the total force vs time graph.
    st.subheader("Total Force vs Time")
    fig3 = px.line(data, x='Total Time (ms)', y='Total Force (N)', title='Total Force vs Time')

    # Annotate the peak total force
    max_force_time = data['Total Time (ms)'][data['Total Force (N)'].idxmax()]
    fig3.add_annotation(
        x=max_force_time,
        y=peak_total_force,
        text=f"Peak Force: {peak_total_force:.2f} N",
        showarrow=True,
        arrowhead=4,
        ax=0,
        ay=-40
    )

    
    st.plotly_chart(fig3)


else:
    st.write("Please upload an Excel file to proceed.")
