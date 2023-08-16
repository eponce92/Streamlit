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
    st.sidebar.number_input(f"Cycle Time for Station {i + 1} (seconds)", value=60, min_value=1) for i in range(num_stations)
]
budgets = [
    st.sidebar.number_input(f"Budget for Station {i + 1} ($)", value=40000.00, min_value=0.00, format="%.2f")
    for i in range(num_stations)
]
conveyance_budgets = [
    st.sidebar.number_input(f"Conveyance Budget for Station {i + 1} to {i + 2} ($)", value=1000.00, min_value=0.00, format="%.2f")
    for i in range(num_stations)
]
redundancies = [
    st.sidebar.number_input(f"Redundancy Level for Station {i + 1}", value=1, min_value=1) for i in range(num_stations)
]

buffer_options = [
    st.sidebar.checkbox(f"Set Conveyance {i + 1} to {i + 2} as Buffer?", value=False)
    for i in range(num_stations)
]
buffer_units = [
    st.sidebar.number_input(f"Buffer Units for Conveyance {i + 1} to {i + 2}", value=0, min_value=0) if is_buffer else 0
    for i, is_buffer in enumerate(buffer_options)
]
buffer_budgets = [
    st.sidebar.number_input(f"Buffer Budget for Conveyance {i + 1} to {i + 2} ($)", value=0.00, min_value=0.00, format="%.2f") if is_buffer else 0.00
    for i, is_buffer in enumerate(buffer_options)
]

# Calculation Functions
def calculate_total_cycle_time(cycle_times, redundancies):
    return sum(cycle_time / redundancy for cycle_time, redundancy in zip(cycle_times, redundancies))

def calculate_total_budget(budgets, conveyance_budgets, redundancies):
    return sum(budget * redundancy for budget, redundancy in zip(budgets, redundancies)) + sum(conveyance_budgets)

def calculate_total_output(total_cycle_time):
    return int((SHIFT_LENGTH_HOURS * SECONDS_PER_HOUR * NUM_SHIFTS_PER_DAY) / total_cycle_time)

# Graph Creation Function
def create_graph(cycle_times, budgets, conveyance_budgets, redundancies, buffer_options, buffer_units, buffer_budgets):
    dot_string = 'digraph {rankdir=TB;'  # Vertical orientation
    dot_string += '"Line Input" -> C1;'
    for i in range(num_stations):
        for r in range(redundancies[i]):
            dot_string += f'C{i + 1} -> S{i + 1}_R{r + 1};'
            label = f'"Station {i + 1} ({r + 1})\\n{cycle_times[i]}s\\n${budgets[i]:,.2f}"'  # Station label
            dot_string += f'S{i + 1}_R{r + 1} [label={label}];'
            dot_string += f'S{i + 1}_R{r + 1} -> C{i + 2};'
        
        # Conveyance or Buffer label
        conveyance_label = f'"Conveyance {i + 1}\\n${conveyance_budgets[i]:,.2f}"'
        if buffer_options[i]:
            conveyance_label = f'"Buffer {i + 1} ({buffer_units[i]} units)\\n${buffer_budgets[i]:,.2f}"'  # Buffer label
        dot_string += f'C{i + 1} [shape=rectangle, label={conveyance_label}];'
    
    dot_string += f'C{num_stations + 1} [shape=rectangle, label="Conveyance {num_stations + 1}"];'
    dot_string += '"Line Output" [shape=ellipse];'
    dot_string += f'C{num_stations + 1} -> "Line Output";'
    dot_string += '}'
    return dot_string



# Display Results
total_cycle_time = calculate_total_cycle_time(cycle_times, redundancies)
total_budget = calculate_total_budget(budgets, conveyance_budgets, redundancies)
total_output = calculate_total_output(total_cycle_time)

st.subheader("Results")
st.write(f"Total Cycle Time: {total_cycle_time:.2f} seconds")
st.write(f"Total Budget: ${total_budget:,.2f}")
st.write(f"Total Output: {total_output:,} pills per day")

# Display Graphical Representation
graph_dot_string = create_graph(cycle_times, budgets, conveyance_budgets, redundancies)
st.graphviz_chart(graph_dot_string)
