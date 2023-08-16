import streamlit as st
def create_ascii_representation(stations, connections):
    ascii_lines = []
    current_line = ""
    max_station_length = max(len(f"[Station {i+1}  {s['cycle_time']}s ${s['budget']/1000:.2f}k]") for i, s in enumerate(stations))

    for i, connection in enumerate(connections):
        station_info = f"[Station {i+1}  {stations[i]['cycle_time']}s ${stations[i]['budget']/1000:.2f}k]".ljust(max_station_length)

        if connection['type'] == 'series':
            current_line += station_info + " --> "
        elif connection['type'] == 'parallel':
            current_line += station_info + " --+"
            ascii_lines.append(current_line)
            ascii_lines.append(" " * (len(current_line) - 1) + "|")
            current_line = " " * (len(current_line) - 1) + "+--"

    # Add last station
    i = len(stations) - 1
    station_info = f"[Station {i+1}  {stations[i]['cycle_time']}s ${stations[i]['budget']/1000:.2f}k]".ljust(max_station_length)
    current_line += station_info
    ascii_lines.append(current_line)

    # Add final output line
    ascii_lines.append(" " * (len(current_line) - 1) + "+--> [Final Output]")

    return "\n".join(ascii_lines)





# Function to calculate cycle time and budget
def calculate_cycle_time_and_budget(stations, connections):
    total_cycle_time = 0
    total_budget = sum(station['budget'] for station in stations)
    
    for connection in connections:
        if connection['type'] == 'series':
            total_cycle_time += sum(stations[i]['cycle_time'] for i in connection['stations'])
        elif connection['type'] == 'parallel':
            total_cycle_time += max(stations[i]['cycle_time'] for i in connection['stations'])
    
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

# Define connections
st.subheader("Connections")
connection_options = ['series', 'parallel']
connections = []
for i in range(num_stations - 1):
    st.write(f"Connection between Station {i+1} and Station {i+2}")
    connection_type = st.selectbox(f"Type of Connection {i+1}:", connection_options, index=0)
    connections.append({'stations': [i, i+1], 'type': connection_type})

# Calculate and display results
total_cycle_time, total_budget = calculate_cycle_time_and_budget(stations, connections)
st.subheader("Results")
st.write("Total Cycle Time:", total_cycle_time, "seconds")
st.write("Total Budget: $", "{:,.2f}".format(total_budget))


# Calculate and display results
total_cycle_time, total_budget = calculate_cycle_time_and_budget(stations, connections)
st.subheader("Results")
st.write("Total Cycle Time:", total_cycle_time, "seconds")
st.write("Total Budget: $", "{:,.2f}".format(total_budget))

# Display ASCII representation
st.subheader("Manufacturing Line Representation")
ascii_representation = create_ascii_representation(stations, connections)
st.text(ascii_representation)
