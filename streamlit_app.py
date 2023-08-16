import streamlit as st

# Input fields for the parameters
shift_length_hours = st.number_input("Shift Length (hours):", min_value=1)
shifts_per_day = st.number_input("Number of Shifts per Day:", min_value=1)
cycle_time_per_machine_seconds = st.number_input("Cycle Time per Machine (seconds):", min_value=1)
number_of_stations = st.number_input("Number of Stations:", min_value=1)
total_budget = st.number_input("Total Budget ($):", min_value=1)

# Perform calculations (similar to what we've done earlier)
# ...

# Display results
st.write(f"Daily Output: {daily_output} pills")
st.write(f"Budget per Station: ${budget_per_station}")
st.write(f"Cycle Time per Station: {cycle_time_per_station} seconds")
st.write(f"Cycle Time for Entire Process: {cycle_time_entire_process} seconds")

