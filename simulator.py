import streamlit as st

def create_ascii_representation(stations, connections):
    ascii_lines = []
    current_line = ""
    max_station_length = max(len(f"[Station {i+1}  {s['cycle_time']}s ${s['budget']/1000:.2f}k]") for i, s in enumerate(stations))
    
    for connection in connections:
        from_group = connection['from_group']
        to_group = connection['to_group']
        
        from_stations = ", ".join([f"Station {i+1}" for i in from_group])
        to_stations = ", ".join([f"Station {i+1}" for i in to_group])
        
        station_info = f"[{from_stations}]".ljust(max_station_length)
        next_station_info = f"[{to_stations}]".ljust(max_station_length)
        
        current_line = station_info + " --+"
        ascii_lines.append(current_line)
        
        for to_station in to_group:
            ascii_lines.append(" " * (len(current_line) - 1) + "|")
            station_info = f"[Station {to_station+1}  {stations[to_station]['cycle_time']}s ${stations[to_station]['budget']/1000:.2f}k]".ljust(max_station_length)
            current_line = " " * (len(current_line) - 1) + "+-- " + station_info
            ascii_lines.append(current_line)
    
    # Add final output line
    ascii_lines.append(" " * (len(current_line) - 1) + "+--> [Final Output]")

    return "\n".join(ascii_lines)

def calculate_cycle_time_and_budget(stations, connections):
    total_cycle_time = 0
    total_budget = sum(station['budget'] for station in stations)
    
    for connection in connections:
        parallel_cycle_times = [stations[i]['cycle_time'] for i in connection['to_group']]
        total_cycle_time += max(parallel_cycle_times)
    
    return total_cycle_time, total_budget

# Main application
st.title("Manufacturing Line Simulator")

# Define stations
num_stations = st.number_input("Number of Stations:", min_value=1, value=4, format="%d")
stations = []
for i in range(num_stations):
    st.subheader(f"Station {i+1}")
    cycle_time = st.number_input(f"Cycle Time for Station {i+1} (seconds):", min_value=1, value=60, format="%d")
    budget = st.number_input(f"Budget for Station {i+1} ($):", min_value=0, value=100000, format="%d")
    stations.append({'cycle_time': cycle_time, 'budget': budget})

# Define connections
st.subheader("Connections")
connections = []
from_group = st.multiselect("Select stations for Group 1 (e.g., Station 1):", options=[f"Station {i+1}" for i in range(num_stations)])
to_group = st.multiselect("Select stations for Group 2 (parallel with Group 1):", options=[f"Station {i+1}" for i in range(num_stations) if f"Station {i+1}" not in from_group])
next_station = st.selectbox("Select next station connected in series:", options=[f"Station {i+1}" for i in range(num_stations) if f"Station {i+1}" not in from_group and f"Station {i+1}" not in to_group])

from_group_indices = [int(station.split()[-1]) - 1 for station in from_group]
to_group_indices = [int(station.split()[-1]) - 1 for station in to_group]
next_station_index = int(next_station.split()[-1]) - 1

connections.append({'from_group': from_group_indices, 'to_group': to_group_indices})
connections.append({'from_group': to_group_indices, 'to_group': [next_station_index]})

# Calculate and display results
total_cycle_time, total_budget = calculate_cycle_time_and_budget(stations, connections)
st.subheader("Results")
st.write("Total Cycle Time:", total_cycle_time, "seconds")
st.write("Total Budget: $", "{:,.2f}".format(total_budget))

# Display ASCII representation
st.subheader("Manufacturing Line Representation")
ascii_representation = create_ascii_representation(stations, connections)
st.text(ascii_representation)
