import streamlit as st
import numpy as np
import plotly.graph_objects as go
import base64

# Set the page layout to wide mode
st.set_page_config(layout="wide")

# Title of the App centered
st.title("G-code Generator for Gecko-Inspired Adhesive Fabrication")

st.markdown("""
## Context and Background

**Gecko Tape**:
Gecko tape is a bio-inspired adhesive technology that mimics the unique adhesion properties of gecko feet. Geckos can climb walls and ceilings thanks to millions of tiny hair-like structures on their feet. These structures create van der Waals forces, allowing the gecko to stick to surfaces without any liquid or sticky residues. 

The technology we're replicating is based on arrays of wedge-shaped silicone features that provide "controllable" or "on-off" adhesion. When these features are loaded in shear, they bend over, resulting in an increased contact area and thus, enhanced adhesion. This is similar to how gecko feet operate. By controlling the applied shear load, one can achieve attachment and detachment with minimal energy wastage.

**Research Reference**: 
The work is inspired by the research titled "APPLYING DRY ADHESIVES TO THE REAL WORLD" conducted by Elliot Wright Hawkes at Stanford University in June 2015. The research details the fabrication and application of gecko-inspired adhesives. You can access the research [here](https://stacks.stanford.edu/file/druid:jd262rc7265/thesis3-augmented.pdf).

## How the Program Works

1. **User Input**:
    - **Angle of Approach**: The angle (in degrees from vertical) at which the cutting tool approaches the material.
    - **Distance Between Grooves**: The spacing between each groove or adhesive feature.
    - **Depth of Grooves**: The depth of each groove or adhesive feature.
    - **Length of Pattern**: The total length over which the grooves should be made.
    - **Feed Rate**: The speed at which the tool moves.

2. **G-code Generation**:
    - The program calculates the necessary movements for the CNC machine.
    - It ensures synchronized movement in both the X and Z axes to maintain the specified angle of approach. Based on the formula: 
    \( x = d \times \tan(\theta) \)
    where:
    \( x \) is the X-axis movement,
    \( d \) is the depth, and
    \( \theta \) is the angle of approach.
    - After cutting each groove, the tool retracts at the same angle it entered.

3. **Visualization**:
    - The generated G-code path is visualized in two graphs.
    - The first graph provides a side view of the entire G-code path.
    - The second graph provides a zoomed-in view of the first few grooves.

4. **G-code Output**:
    - The generated G-code is displayed for user review.
    - An option to download the G-code as a `.gcode` file is provided.

**Use the sliders and input boxes below to customize the G-code parameters and visualize the cutting path.**
""")

# Display the attached picture from the thesis for better representation
st.image("https://raw.githubusercontent.com/eponce92/Streamlit/main/gecko_tape.png", caption="Representation of the machined shape", width=300)

# Define the necessary functions

def generate_gcode(angle, spacing, depth, pattern_length, feed_rate, move_rate, retraction_distance):
    num_grooves = int(pattern_length / spacing)
    x_move = depth * np.tan(np.radians(angle))
    gcode = ["G90 ; Set to absolute positioning",
             "G92 X0 Z0 ; Set current position as zero"]
    current_x = 0

    for i in range(num_grooves):
        gcode.append(f"; Cut groove {i+1}")

        # For the first groove, make a synchronized movement from the origin
        if i == 0:
            gcode.append(f"G1 X{x_move:.6f} Z{-depth:.6f} F{feed_rate}")
        else:
            gcode.append(f"G1 X{current_x + x_move:.6f} Z{-depth:.6f} F{feed_rate}")
        
        gcode.append(f"G1 X{current_x:.6f} Z0 F{feed_rate} ; Synchronized retraction")

        # Move to next groove starting position and add retraction
        current_x += spacing
        if i < num_grooves - 1:  # Don't move further if it's the last groove
            gcode.append(f"G1 X{current_x:.6f} Z0 F{move_rate}")
            gcode.append(f"G1 Z{retraction_distance:.6f} F{move_rate}")

    return gcode










def plot_gcode(x_values, z_values, title, x_range=None, y_range=None):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_values, y=z_values, mode='lines+markers', name='Path'))
    fig.update_layout(title=title, xaxis_title="X-axis (mm)", yaxis_title="Z-axis (mm)", 
                      xaxis_range=x_range, yaxis_range=y_range)
    return fig

# Organize layout with columns
col1, col2, col3 = st.columns([2,3,3])

with col1:
    st.markdown("### Parameters Input")
    angle = st.slider("Angle of Approach (degrees from vertical, 0-90)", 0, 90, 45)
    spacing = st.number_input("Distance Between Grooves (mm)", 0.000001, 10.0, 0.061, format="%.6f")
    depth = st.number_input("Depth of Grooves (mm)", 0.000001, 10.0, 0.102, format="%.6f")
    pattern_length = st.number_input("Length of Pattern (mm)", 0.000001, 500.0, 40.0, format="%.6f")
    feed_rate = st.number_input("Feed Rate (mm/min) - Cutting Speed", 1, 5000, 100)
    move_rate = st.number_input("Move Rate (mm/min) - Travel Speed", 1, 5000, 200)
    retraction_distance = st.number_input("Retraction Distance (mm) - Height above the material", 0.000001, 10.0, 0.200, format="%.6f")

    if st.button("Generate G-code"):
        gcode_output = generate_gcode(angle, spacing, depth, pattern_length, feed_rate, move_rate, retraction_distance)

        with col2:
            st.markdown("### G-code Output")
            st.text_area("Generated G-code:", "\n".join(gcode_output), height=500)
            b64 = base64.b64encode("\n".join(gcode_output).encode()).decode()
            st.markdown(f"<a href=\"data:file/txt;base64,{b64}\" download=\"grooves.gcode\" style=\"display: inline-block; padding: 0.5em 1em; background-color: red; color: white; text-decoration: none; border-radius: 4px;\">Download G-code</a>", unsafe_allow_html=True)

        x_values = [0]
        z_values = [0]
        current_x = 0
        current_z = retraction_distance
        for line in gcode_output:
            if line.startswith("G1"):
                if "X" in line:
                    x_val = float(line.split("X")[1].split()[0])
                    current_x = x_val
                if "Z" in line:
                    z_val = float(line.split("Z")[1].split()[0])
                    current_z = z_val
                x_values.append(current_x)
                z_values.append(current_z)

        with col3:
            st.markdown("### Visualization")
            st.plotly_chart(plot_gcode(x_values, z_values, "Side View of the G-code Path"), use_container_width=True)
            zoomed_x = x_values[:10]
            zoomed_z = z_values[:10]
            st.plotly_chart(plot_gcode(zoomed_x, zoomed_z, "Zoomed-in View of the First Few Grooves"), use_container_width=True)
