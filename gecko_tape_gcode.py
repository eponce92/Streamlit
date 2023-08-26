import streamlit as st
import numpy as np
import plotly.graph_objects as go
import base64

# Set the page layout to wide mode
st.set_page_config(layout="wide")

def generate_gcode(angle, spacing, depth, pattern_length, feed_rate):
    num_grooves = int(pattern_length / spacing)
    x_move = depth * np.tan(np.radians(angle))
    gcode = ["G90 ; Set to absolute positioning",
             "G92 X0 Z0 ; Set current position as zero"]
    current_x = 0

    for i in range(num_grooves):
        gcode.append(f"; Cut groove {i+1}")
        gcode.append(f"G1 X{current_x + x_move:.6f} Z{-depth:.6f} F{feed_rate} ")
        gcode.append(f"G1 X{current_x:.6f} Z0 ; Synchronized retraction")
        current_x += spacing
        gcode.append(f"G1 X{current_x:.6f} ; Position for next groove")
    
    return gcode

def plot_gcode(x_values, z_values, title, x_range=None, y_range=None):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_values, y=z_values, mode='lines+markers', name='Path'))
    fig.update_layout(title=title, xaxis_title="X-axis (mm)", yaxis_title="Z-axis (mm)", 
                      xaxis_range=x_range, yaxis_range=y_range)
    return fig

st.title("G-code Generator for Groove Cutting")

# Organize layout with columns
col1, col2, col3 = st.columns([2,3,3])  # Adjusting column widths

with col1:
    angle = st.slider("Angle of Approach (degrees from vertical, 0-90)", 0, 90, 45)
    spacing = st.number_input("Distance Between Grooves (mm)", 0.000001, 10.0, 0.061, format="%.6f")
    depth = st.number_input("Depth of Grooves (mm)", 0.000001, 10.0, 0.102, format="%.6f")
    pattern_length = st.number_input("Length of Pattern (mm)", 0.000001, 500.0, 40.0, format="%.6f")
    feed_rate = st.number_input("Feed Rate (mm/min)", 1, 5000, 100)
    
    if st.button("Generate G-code"):
        gcode_output = generate_gcode(angle, spacing, depth, pattern_length, feed_rate)
        st.text_area("Generated G-code:", "\n".join(gcode_output), height=500)

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

        with col2:
            st.plotly_chart(plot_gcode(x_values, z_values, "Side View of the G-code Path"), use_container_width=True)

        with col3:
            zoomed_x = x_values[:10]
            zoomed_z = z_values[:10]
            st.plotly_chart(plot_gcode(zoomed_x, zoomed_z, "Zoomed-in View of the First Few Grooves"), use_container_width=True)

        b64 = base64.b64encode("\n".join(gcode_output).encode()).decode()
        st.markdown(f"<a href=\"data:file/txt;base64,{b64}\" download=\"grooves.gcode\">Download G-code</a>", unsafe_allow_html=True)
