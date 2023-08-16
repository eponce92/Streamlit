import streamlit as st

def create_graph():
    dot_string = 'digraph {rankdir=LR;'
    dot_string += '"Line Input" -> C1;'
    dot_string += 'C1 -> S1_R1; C1 -> S1_R2;'
    dot_string += 'S1_R1 -> C2; S1_R2 -> C2;'
    dot_string += 'S1_R1 [label="Station 1  60s $40,000.00"];'
    dot_string += 'S1_R2 [label="Station 1  60s $40,000.00"];'
    dot_string += 'C2 -> S2_R1;'
    dot_string += 'S2_R1 [label="Station 2  60s $40,000.00"];'
    dot_string += 'S2_R1 -> "Line Output";'
    dot_string += '"Line Output" [shape=ellipse];'
    dot_string += 'C1 [shape=rectangle, label="Conveyance 1"];'
    dot_string += 'C2 [shape=rectangle, label="Conveyance 2"];'
    dot_string += '}'
    return dot_string

st.title("Manufacturing Line Simulation")

graph_dot_string = create_graph()
st.graphviz_chart(graph_dot_string)
