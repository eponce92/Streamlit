import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math
def forward_kinematics(A, B, theta_degrees):
    theta = math.radians(theta_degrees)
    X = A + B * math.cos(theta)
    Z = B * math.sin(theta)
    return X, Z

def main():
    st.title("Compound Axis Kinematics Visualization")
    
    st.write("Here we visualize the kinematics of two linear slides mounted one on top of the other. The bottom slide (A) is horizontal, while the top slide (B) is mounted at an angle to the first. By compounding the movement of the two axes, we can achieve an effective X and Z movement in Cartesian space.")
    
    # Side view illustration
    fig, ax = plt.subplots()
    ax.arrow(0, 0, 1, 0, head_width=0.1, head_length=0.1, fc='blue', ec='blue')  # A axis
    ax.arrow(1, 0, 0.5, 0.5, head_width=0.1, head_length=0.1, fc='red', ec='red')  # B axis (example angle for illustration)
    ax.set_xlim(0, 2)
    ax.set_ylim(0, 1)
    st.pyplot(fig)
    
    # Sliders
    A = st.slider("Position of A Axis", 0.0, 50.0, 25.0)
    B = st.slider("Position of B Axis", 0.0, 50.0, 25.0)
    theta = st.slider("Angle θ of B Axis (Degrees)", 0, 90, 45)
    
    # Calculate kinematics
    X, Z = forward_kinematics(A, B, theta)
    
    # Display results
    st.write(f"X Coordinate: {X}")
    st.write(f"Z Coordinate: {Z}")
    
    # Real-time graph
    fig, ax = plt.subplots()
    ax.scatter(X, Z, color='green')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.set_xlabel("X")
    ax.set_ylabel("Z")
    st.pyplot(fig)

if __name__ == "__main__":
    main()
