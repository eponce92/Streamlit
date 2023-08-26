import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import base64
import plotly.graph_objects as go


def generate_gcode(angle, spacing, depth, pattern_length):
    # Calculate the number of grooves based on the pattern length and spacing
    num_grooves = int(pattern_length / spacing)
    
    # Calculate the synchronized move based on the angle
    x_move = depth * np.tan(np.radians(angle))
    
    # Start with absolute positioning and zeroing commands
    gcode = ["G90 ; Set to absolute positioning",
             "G92 X0 Z0 ; Set current position as zero"]
    current_x = 0

    for i in range(num_grooves):
        # Move synchronously to cut the groove
        gcode.append(f"G1 X{current_x + x_move:.6f} Z{-depth:.6f} F100 ; Cut groove {i+1}")
        
        # Synchronized retraction of the blade
        gcode.append(f"G1 X{current_x:.6f} Z0 ; Retract blade")
        
        # Move for the next groove
        current_x += spacing
        gcode.append(f"G1 X{current_x:.6f} ; Position for next groove")
    
    # End of program: Retract the blade and move to starting position
    gcode.append("G1 Z2.0 ; Final retraction")
    gcode.append("G1 X0 ; Move X to starting position")
    
    return gcode


def get_file_content(gcode_output):
    """Generate a downloadable file for the G-code"""
    return "\n".join(gcode_output)

st.title("G-code Generator for Groove Cutting")

# Input fields with 6 decimal points format
angle = st.slider("Angle of Approach (degrees from vertical, 0-90)", 0, 90, 45)
spacing = st.number_input("Distance Between Grooves (mm)", 0.000001, 10.0, 0.061, format="%.6f")
depth = st.number_input("Depth of Grooves (mm)", 0.000001, 10.0, 0.102, format="%.6f")
pattern_length = st.number_input("Length of Pattern (mm)", 0.000001, 500.0, 40.0, format="%.6f")

# Generate G-code based on the parameters
gcode_output = generate_gcode(angle, spacing, depth, pattern_length)

# Display the G-code
st.text_area("Generated G-code:", "\n".join(gcode_output), height=250)

# Plot the side view of the G-code
def plot_gcode(x_values, z_values, title, x_range=None, y_range=None):
    fig = go.Figure()

    # Plotting the G-code path
    fig.add_trace(go.Scatter(x=x_values, y=z_values, mode='lines+markers', name='Path'))
    
    # Setting titles and labels
    fig.update_layout(title=title, xaxis_title="X-axis (mm)", yaxis_title="Z-axis (mm)", 
                      xaxis_range=x_range, yaxis_range=y_range)
    return fig

# Full view plot
st.plotly_chart(plot_gcode(x_values, z_values, "Side View of the G-code Path"))

# Zoomed-in view of the first few grooves
zoomed_x = x_values[:10]
zoomed_z = z_values[:10]
st.plotly_chart(plot_gcode(zoomed_x, zoomed_z, "Zoomed-in View of the First Few Grooves"))

# Downloadable link for G-code
b64 = base64.b64encode(get_file_content(gcode_output).encode()).decode()
st.markdown(f"<a href=\"data:file/txt;base64,{b64}\" download=\"grooves.gcode\">Download G-code</a>", unsafe_allow_html=True)
