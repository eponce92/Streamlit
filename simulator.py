import streamlit as st

def create_graph(num_stations):
    dot_string = 'digraph {rankdir=LR;'
    dot_string += '"Line Input" -> C1;'
    for i in range(1, num_stations + 1):
        dot_string += f'S{i} [label="Station {i}"];'
        dot_string += f'C{i} [shape=rectangle, label="Conveyance {i}"];'
        dot_string += f'C{i} -> S{i} -> C{i+1};'
    dot_string += '"Line Output" [shape=ellipse];'
    dot_string += f'C{num_stations} -> "Line Output";'
    dot_string += '}'
    return dot_string

st.title("Manufacturing Line Simulation")
num_stations = st.sidebar.number_input("Number of Stations", value=2, min_value=1)

graph_dot_string = create_graph(num_stations)
st.graphviz_chart(graph_dot_string)
