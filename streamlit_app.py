import streamlit as st

# Function to perform calculations
def calculate_values(cycle_time_per_machine, number_of_stations, total_budget):
    shift_length_hours = 12
    shifts_per_day = 2
    shift_length_seconds = shift_length_hours * 60 * 60
    pills_per_shift_per_machine = shift_length_seconds / cycle_time_per_machine
    pills_per_shift_entire_line = pills_per_shift_per_machine / number_of_stations
    daily_output = pills_per_shift_entire_line * shifts_per_day
    budget_per_station = total_budget / number_of_stations
    cycle_time_per_station = cycle_time_per_machine
    cycle_time_entire_process = cycle_time_per_station * number_of_stations
    return daily_output, budget_per_station, cycle_time_per_station, cycle_time_entire_process

# Layout
st.title("Manufacturing Line Comparison Tool")
st.write("Compare two different manufacturing line options by modifying the values below.")

# Input for Option 1
st.sidebar.subheader("Option 1")
cycle_time_per_machine_1 = st.sidebar.number_input("Cycle Time per Machine (seconds):", min_value=1, value=60, key='cycle1')
number_of_stations_1 = st.sidebar.number_input("Number of Stations:", min_value=1, value=14, key='stations1')
total_budget_1 = st.sidebar.number_input("Total Budget ($):", min_value=0, value=800000, key='budget1')

# Input for Option 2
st.sidebar.subheader("Option 2")
cycle_time_per_machine_2 = st.sidebar.number_input("Cycle Time per Machine (seconds):", min_value=1, value=60, key='cycle2')
number_of_stations_2 = st.sidebar.number_input("Number of Stations:", min_value=1, value=14, key='stations2')
total_budget_2 = st.sidebar.number_input("Total Budget ($):", min_value=0, value=800000, key='budget2')

# Calculations for Option 1
daily_output_1, budget_per_station_1, cycle_time_per_station_1, cycle_time_entire_process_1 = calculate_values(cycle_time_per_machine_1, number_of_stations_1, total_budget_1)

# Calculations for Option 2
daily_output_2, budget_per_station_2, cycle_time_per_station_2, cycle_time_entire_process_2 = calculate_values(cycle_time_per_machine_2, number_of_stations_2, total_budget_2)

# Display results
st.subheader("Option 1 vs Option 2")
cols = st.columns(2)

with cols[0]:
    st.markdown("**Option 1**")
    st.write("Daily Output:", daily_output_1, "pills")
    st.write("Budget per Station: $", budget_per_station_1)
    st.write("Cycle Time per Station:", cycle_time_per_station_1, "seconds")
    st.write("Cycle Time for Entire Process:", cycle_time_entire_process_1, "seconds")

with cols[1]:
    st.markdown("**Option 2**")
    st.write("Daily Output:", daily_output_2, "pills")
    st.write("Budget per Station: $", budget_per_station_2)
    st.write("Cycle Time per Station:", cycle_time_per_station_2, "seconds")
    st.write("Cycle Time for Entire Process:", cycle_time_entire_process_2, "seconds")
