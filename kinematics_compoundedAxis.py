import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math

def forward_kinematics(A, B, theta_degrees):
    theta = math.radians(theta_degrees)
    X = A + B * math.cos(theta)
    Z = B * math.sin(theta)
    return X, Z

def create_side_view(theta_degrees):
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.arrow(0, 0, 0.9, 0, head_width=0.05, head_length=0.05, fc='blue', ec='blue', width=0.03)
    theta = math.radians(theta_degrees)
    Bx = 0.9 * math.cos(theta)
    By = 0.9 * math.sin(theta)
    ax.arrow(0, 0, Bx, By, head_width=0.05, head_length=0.05, fc='red', ec='red', width=0.03)
    ax.set_xlim(0, 2)
    ax.set_ylim(0, 1)
    ax.set_aspect('equal', 'box')
    return fig

def main():
    st.title("Compound Axis Kinematics Visualization")
    
    st.write("Here we visualize the kinematics of two linear slides mounted one on top of the other. By compounding the movement of the two axes, we can achieve an effective X and Z movement in Cartesian space.")
    
    st.header("Setup")
    A_length = st.slider("Length of A Axis", 0.0, 100.0, 50.0)
    B_length = st.slider("Length of B Axis", 0.0, 100.0, 50.0)
    theta = st.slider("Angle θ of B Axis (Degrees)", 0, 90, 45)
    
    st.write("Side View:")
    st.pyplot(create_side_view(theta))
    
    st.header("Kinematics Formulas")
    st.latex(r"X = A + B \cos(\theta)")
    st.latex(r"Z = B \sin(\theta)")
    
    lock_x = st.checkbox("Lock X-axis")
    
    A = st.slider("Position of A Axis (0 to A Length)", 0.0, A_length, A_length/2)
    B = st.slider("Position of B Axis (0 to B Length)", 0.0, B_length, B_length/2)
    
    if lock_x:
        X_locked = forward_kinematics(A, B, theta)[0]
        A = X_locked - B * math.cos(math.radians(theta))
    
    X, Z = forward_kinematics(A, B, theta)
    
    st.write(f"X Coordinate: {X:.2f}")
    st.write(f"Z Coordinate: {Z:.2f}")
    
    fig, ax = plt.subplots()
    ax.scatter(X, Z, color='green')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.set_xlabel("X")
    ax.set_ylabel("Z")
    st.pyplot(fig)

if __name__ == "__main__":
    main()
