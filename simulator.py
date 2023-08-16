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

buffer_options = []
buffer_units = []
buffer_budgets = []
for i in range(num_stations):
    st.sidebar.subheader(f"Conveyance {i + 1} to {i + 2} Settings")
    is_buffer = st.sidebar.checkbox(f"Set as Buffer for Conveyance {i + 1} to {i + 2}?", value=False)
    buffer_options.append(is_buffer)

    if is_buffer:
        units = st.sidebar.number_input(f"Buffer Units for Conveyance {i + 1} to {i + 2}", value=0, min_value=0)
        budget = st.sidebar.number_input(f"Buffer Budget for Conveyance {i + 1} to {i + 2} ($)", value=40000.00, min_value=0.00, format="%.2f")
        buffer_units.append(units)
        buffer_budgets.append(budget)
    else:
        budget = st.sidebar.number_input(f"Conveyance Budget for Conveyance {i + 1} to {i + 2} ($)", value=40000.00, min_value=0.00, format="%.2f")
        buffer_units.append(0)
        buffer_budgets.append(budget)



# Calculation Functions
def calculate_buffer_impact(cycle_times, redundancies, buffer_options, buffer_units):
    buffer_impacts = []
    for i in range(len(cycle_times) - 1):
        upstream_cycle_time = cycle_times[i] / redundancies[i]
        downstream_cycle_time = cycle_times[i + 1] / redundancies[i + 1]
        if buffer_options[i] and downstream_cycle_time > upstream_cycle_time:
            # Buffer impact on cycle time
            impact = ((downstream_cycle_time - upstream_cycle_time) * buffer_units[i]) / downstream_cycle_time
        else:
            impact = 0
        buffer_impacts.append(impact)
    return buffer_impacts

def calculate_total_cycle_time(cycle_times, redundancies, buffer_impacts):
    return sum(cycle_time / redundancy for cycle_time, redundancy in zip(cycle_times, redundancies)) + sum(buffer_impacts)

def calculate_total_budget(budgets, conveyance_budgets, buffer_budgets, redundancies):
    return sum(budget * redundancy for budget, redundancy in zip(budgets, redundancies)) + sum(conveyance_budgets) + sum(buffer_budgets)


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



# Calculate buffer impact on cycle time
buffer_impacts = calculate_buffer_impact(cycle_times, redundancies, buffer_options, buffer_units)

# Updated calculations
total_cycle_time = calculate_total_cycle_time(cycle_times, redundancies, buffer_impacts)
total_budget = calculate_total_budget(budgets, conveyance_budgets, buffer_budgets, redundancies)
total_output = calculate_total_output(total_cycle_time)

st.subheader("Results")
st.write(f"Total Cycle Time: {total_cycle_time:.2f} seconds")
st.write(f"Total Budget: ${total_budget:,.2f}")
st.write(f"Total Output: {total_output:,} pills per day")


# Display Graphical Representation
graph_dot_string = create_graph(cycle_times, budgets, conveyance_budgets, redundancies, buffer_options, buffer_units, buffer_budgets)

st.graphviz_chart(graph_dot_string)
