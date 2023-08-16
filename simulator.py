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

# Calculation Functions
def calculate_total_cycle_time(cycle_times, redundancies):
    return sum(cycle_time / redundancy for cycle_time, redundancy in zip(cycle_times, redundancies))

def calculate_total_budget(budgets, redundancies):
    return sum(budget * redundancy for budget, redundancy in zip(budgets, redundancies))

def calculate_total_output(total_cycle_time):
    return int((SHIFT_LENGTH_HOURS * SECONDS_PER_HOUR * NUM_SHIFTS_PER_DAY) / total_cycle_time)

# Graph Creation Function
def create_graph(cycle_times, budgets, redundancies):
    dot_string = 'digraph {rankdir=LR; "Line Input" -> {'
    for r in range(redundancies[0]):
        dot_string += f'S1_R{r+1} '
    dot_string += '};'
    for i in range(num_stations):
        for r in range(redundancies[i]):
            label = f'"Station {i+1}  {cycle_times[i]}s ${budgets[i]:,.2f}"'
            dot_string += f'S{i+1}_R{r+1} [label={label}];'
            conveyance_node = f'C{i+1}'
            if i < num_stations - 1:
                dot_string += f'S{i+1}_R{r+1} -> {conveyance_node};'
                next_nodes = " ".join(f'S{i+2}_R{r2+1}' for r2 in range(redundancies[i+1]))
                dot_string += f'{conveyance_node} -> {{{next_nodes}}};'
                dot_string += f'{conveyance_node} [shape=rectangle, label="Conveyance {i+1}"];'
    dot_string += f'S{num_stations}_R1 -> "Line Output"; "Line Output" [shape=ellipse];}'
    return dot_string

# Display Results
total_cycle_time = calculate_total_cycle_time(cycle_times, redundancies)
total_budget = calculate_total_budget(budgets, redundancies)
total_output = calculate_total_output(total_cycle_time)

st.subheader("Results")
st.write(f"Total Cycle Time: {total_cycle_time:.2f} seconds")
st.write(f"Total Budget: ${total_budget:,.2f}")
st.write(f"Total Output: {total_output:,} pills per day")

st.subheader("Graphical Representation")
graph_dot_string = create_graph(cycle_times, budgets, redundancies)
st.graphviz_chart(graph_dot_string)
