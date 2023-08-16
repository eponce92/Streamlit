import streamlit as st
import graphviz

# Constants
SHIFT_LENGTH_HOURS = 12
NUM_SHIFTS_PER_DAY = 2
SECONDS_PER_HOUR = 3600

def create_graphviz_chart(stations):
    dot = gv.Digraph()
    dot.node('Line Input')
    
    prev_node = 'Line Input'
    for i, station in enumerate(stations):
        redundancy = station['redundancy']
        label = f"Station {i+1} ({redundancy}x)\n{station['cycle_time']}s\n${station['budget']/1000:.2f}k"
        node_name = f"Station {i+1}"
        dot.node(node_name, label=label)
        dot.edge(prev_node, node_name)
        prev_node = node_name

    dot.node('Line Output')
    dot.edge(prev_node, 'Line Output')

    return dot

def calculate_line_metrics(stations):
    total_cycle_time = 0
    total_budget = 0
    for station in stations:
        redundancy = station['redundancy']
        cycle_time = station['cycle_time']
        budget = station['budget']
        total_cycle_time += cycle_time / redundancy
        total_budget += budget * redundancy
    
    # Calculate daily output
    shift_length_seconds = SHIFT_LENGTH_HOURS * SECONDS_PER_HOUR
    pills_per_shift = shift_length_seconds / total_cycle_time
    daily_output = pills_per_shift * NUM_SHIFTS_PER_DAY

    return total_cycle_time, total_budget, daily_output

# Main application
st.title("Manufacturing Line Simulator")

# Define stations
num_stations = st.number_input("Number of Stations:", min_value=1, value=3, format="%d")
stations = []
for i in range(num_stations):
    st.subheader(f"Station {i+1}")
    cycle_time = st.number_input(f"Cycle Time for Station {i+1} (seconds):", min_value=1, value=60, format="%d")
    budget = st.number_input(f"Budget for Station {i+1} ($):", min_value=0, value=100000, format="%d")
    redundancy = st.number_input(f"Redundancy for Station {i+1} (number of parallel units):", min_value=1, value=1, format="%d")
    stations.append({'cycle_time': cycle_time, 'budget': budget, 'redundancy': redundancy})

# Calculate and display results
total_cycle_time, total_budget, daily_output = calculate_line_metrics(stations)
st.subheader("Results")
st.write("Total Cycle Time:", total_cycle_time, "seconds")
st.write("Total Budget: $", "{:,.2f}".format(total_budget))
st.write("Total Output (per day):", int(daily_output), "pills")

# Display Graphviz chart
st.subheader("Manufacturing Line Representation")
graph = create_graphviz_chart(stations)
st.graphviz_chart(graph)
