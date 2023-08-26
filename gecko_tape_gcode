import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def generate_gcode(angle, spacing, depth, num_grooves=20):
    # Calculate the synchronized move based on the angle
    x_move = depth * np.tan(np.radians(angle))
    
    gcode = []
    current_x = 0

    for i in range(num_grooves):
        # Move synchronously to cut the groove
        gcode.append(f"G1 X{current_x + x_move:.3f} Z{-depth:.3f} F100 ; Cut groove {i+1}")
        
        # Synchronized retraction of the blade
        gcode.append(f"G1 X{current_x:.3f} Z0 ; Retract blade")
        
        # Move for the next groove
        current_x += spacing
        gcode.append(f"G1 X{current_x:.3f} ; Position for next groove")
    
    # End of program: Retract the blade and move to starting position
    gcode.append("G1 Z2.0 ; Final retraction")
    gcode.append("G1 X0 ; Move X to starting position")
    
    return gcode

st.title("G-code Generator for Groove Cutting")

# Input fields
angle = st.slider("Angle of Approach (degrees from vertical, 0-90)", 0, 90, 45)
spacing = st.number_input("Distance Between Grooves (mm)", 0.001, 10.0, 0.061)
depth = st.number_input("Depth of Grooves (mm)", 0.001, 10.0, 0.102)

# Generate G-code based on the parameters
gcode_output = generate_gcode(angle, spacing, depth)

# Display the G-code
st.text_area("Generated G-code:", "\n".join(gcode_output), height=250)

# Plot the side view of the G-code
x_values = [0]
z_values = [0]

current_x = 0
for line in gcode_output:
    if line.startswith("G1"):
        x_val = float(line.split("X")[1].split()[0])
        z_val = float(line.split("Z")[1].split()[0])
        x_values.extend([current_x, x_val])
        z_values.extend([z_val, z_val])
        current_x = x_val

plt.figure(figsize=(10,6))
plt.plot(x_values, z_values, '-o')
plt.title("Side View of the G-code Path")
plt.xlabel("X-axis (mm)")
plt.ylabel("Z-axis (mm)")
plt.grid(True)
st.pyplot(plt)
