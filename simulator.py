import streamlit as st

def create_ascii_representation(stations, groups):
    ascii_lines = ["[Line Input]"]
    
    for group in groups:
        group_stations = []
        max_length = max(len(f"[Station {i+1}  {stations[i]['cycle_time']}s ${stations[i]['budget']/1000:.2f}k]") for i in group)
        for i in group:
            station_info = f"[Station {i+1}  {stations[i]['cycle_time']}s ${stations[i]['budget']/1000:.2f}k]"
            group_stations.append(station_info.ljust(max_length))
        group_representation = " --+\n".join(group_stations) + " --+"
        ascii_lines.append(group_representation)
    
    ascii_lines.append("[Line Output]")

    return "\n".join(ascii_lines)

def calculate_cycle_time_and_budget(stations, groups):
    total_cycle_time = 0
    total_budget = sum(station['budget'] for station in stations)
    
    for group in groups:
        parallel_cycle_times = [stations[i]['cycle_time'] for i in group]
        total_cycle_time += max(parallel_cycle_times)
    
    return total_cycle_time, total_budget

# Main application
st.title("Manufacturing Line Simulator")

# Define stations
num_stations = st.number_input("Number of Stations:", min_value=1, value=3, format="%d")
stations = []
for i in range(num_stations):
    st.subheader(f"Station {i+1}")
    cycle_time = st.number_input(f"Cycle Time for Station {i+1} (seconds):", min_value=1, value=60, format="%d")
    budget = st.number_input(f"Budget for Station {i+1} ($):", min_value=0, value=100000, format="%d")
    stations.append({'cycle_time': cycle_time, 'budget': budget})

# Define groups
num_groups = st.number_input("Number of Groups:", min_value=1, value=2, format="%d")
groups = []
for i in range(num_groups):
    st.subheader(f"Group {i+1}")
    group_stations = st.multiselect(f"Select stations for Group {i+1}:", options=[f"Station {j+1}" for j in range(num_stations)])
    group_indices = [int(station.split()[-1]) - 1 for station in group_stations]
    groups.append(group_indices)

# Calculate and display results
total_cycle_time, total_budget = calculate_cycle_time_and_budget(stations, groups)
st.subheader("Results")
st.write("Total Cycle Time:", total_cycle_time, "seconds")
st.write("Total Budget: $", "{:,.2f}".format(total_budget))

# Display ASCII representation
st.subheader("Manufacturing Line Representation")
ascii_representation = create_ascii_representation(stations, groups)
st.text(ascii_representation)
