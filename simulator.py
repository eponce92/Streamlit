import streamlit as st

# Constants
SHIFT_LENGTH_HOURS = 12
NUM_SHIFTS_PER_DAY = 2
SECONDS_PER_HOUR = 3600

# User Inputs Section
st.title("Manufacturing Line Simulation")
st.sidebar.header("User Inputs")
num_stations = st.sidebar.number_input("Number of Stations", value=2, min_value=1)
cycle_times = [
    st.sidebar.number_input(f"Cycle Time for Station {i+1} (seconds)", value=60, min_value=1) for i in range(num_stations)
]
budgets = [
    st.sidebar.number_input(f"Budget for Station {i+1} ($)", value=40000.00, min_value=0.00, format="%.2f") for i in range(num_stations)
]
redundancies = [
    st.sidebar.number_input(f"Redundancy Level for Station {i+1}", value=1, min_value=1) for i in range(num_stations)
]

# Graph Creation Function
def create_graph(cycle_times, budgets, redundancies):
    dot_string = 'digraph {rankdir=LR;'
    dot_string += '"Line Input" -> C1;'
    for i in range(num_stations):
        for r in range(redundancies[i]):
            dot_string += f'C{i+1} -> S{i+1}_R{r+1};'
            label = f'"Station {i+1}  {cycle_times[i]}s ${budgets[i]:,.2f}"'
            dot_string += f'S{i+1}_R{r+1} [label={label}];'
            dot_string += f'S{i+1}_R{r+1} -> C{i+2};'
        dot_string += f'C{i+1} [shape=rectangle, label="Conveyance {i+1}"];'
    dot_string += '"Line Output" [shape=ellipse];'
    dot_string += f'C{num_stations+1} -> "Line Output";'
    dot_string += '}'
    return dot_string

# Display Graphical Representation
graph_dot_string = create_graph(cycle_times, budgets, redundancies)
st.graphviz_chart(graph_dot_string)
