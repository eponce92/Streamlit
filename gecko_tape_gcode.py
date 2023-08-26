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
    - It ensures synchronized movement in both the X and Z axes to maintain the specified angle of approach, based on the formula \( x = d \times \tan(\theta) \) where \( x \) is the X-axis movement, \( d \) is the depth, and \( \theta \) is the angle of approach.
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
st.image("https://raw.githubusercontent.com/eponce92/Streamlit/main/gecko_tape.png", caption="Representation of the machined shape", width=300))



# Organize layout with columns
col1, col2, col3 = st.columns([2,3,3])  # Adjusting column widths

with col1:
    st.markdown("### Parameters Input")
    angle = st.slider("Angle of Approach (degrees from vertical, 0-90)", 0, 90, 45)
    spacing = st.number_input("Distance Between Grooves (mm)", 0.000001, 10.0, 0.061, format="%.6f")
    depth = st.number_input("Depth of Grooves (mm)", 0.000001, 10.0, 0.102, format="%.6f")
    pattern_length = st.number_input("Length of Pattern (mm)", 0.000001, 500.0, 40.0, format="%.6f")
    feed_rate = st.number_input("Feed Rate (mm/min)", 1, 5000, 100)

    if st.button("Generate G-code"):
        gcode_output = generate_gcode(angle, spacing, depth, pattern_length, feed_rate)

        with col2:
            st.markdown("### G-code Output")
            st.text_area("Generated G-code:", "\n".join(gcode_output), height=500)
            b64 = base64.b64encode("\n".join(gcode_output).encode()).decode()
            st.markdown(f"<a href=\"data:file/txt;base64,{b64}\" download=\"grooves.gcode\" style=\"display: inline-block; padding: 0.5em 1em; background-color: red; color: white; text-decoration: none; border-radius: 4px;\">Download G-code</a>", unsafe_allow_html=True)

        x_values = [0]
        z_values = [0]
        current_x = 0
        current_z = 0
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
