import streamlit as st

# Function to perform calculations
def calculate_values(cycle_time_per_machine, number_of_stations, total_budget):
    shift_length_hours = 12
    shifts_per_day = 2
    shift_length_seconds = shift_length_hours * 60 * 60
    pills_per_shift_per_machine = shift_length_seconds / cycle_time_per_machine
    pills_per_shift_entire_line = pills_per_shift_per_machine / number_of_stations
    daily_output = round(pills_per_shift_entire_line * shifts_per_day)
    budget_per_station = "${:,.2f}".format(total_budget / number_of_stations)
    cycle_time_per_station = cycle_time_per_machine
    cycle_time_entire_process = cycle_time_per_station * number_of_stations
    return daily_output, budget_per_station, cycle_time_per_station, cycle_time_entire_process

# Function to calculate additional budget based on production goals
def calculate_additional_budget(daily_output, target_daily_output, total_budget):
    number_of_additional_lines = (target_daily_output - daily_output) / daily_output
    additional_budget_required = "${:,.2f}".format(number_of_additional_lines * total_budget)
    return round(number_of_additional_lines), additional_budget_required

# Layout
st.title("Manufacturing Line Comparison Tool (for Ehsan :)")
st.write("Compare two different manufacturing line options by modifying the values below.")

# Input for Option 1
st.sidebar.subheader("Option 1")
cycle_time_per_machine_1 = st.sidebar.number_input("Cycle Time per Machine (seconds):", min_value=1, value=60, key='cycle1')
number_of_stations_1 = st.sidebar.number_input("Number of Stations:", min_value=1, value=14, key='stations1')
total_budget_1 = st.sidebar.number_input("Total Budget ($):", min_value=0, value=800000, key='budget1', format="%d")

# Input for Option 2
st.sidebar.subheader("Option 2")
cycle_time_per_machine_2 = st.sidebar.number_input("Cycle Time per Machine (seconds):", min_value=1, value=60, key='cycle2')
number_of_stations_2 = st.sidebar.number_input("Number of Stations:", min_value=1, value=14, key='stations2')
total_budget_2 = st.sidebar.number_input("Total Budget ($):", min_value=0, value=800000, key='budget2', format="%d")

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
    st.write("Budget per Station:", budget_per_station_1)
    st.write("Cycle Time per Station:", cycle_time_per_station_1, "seconds")
    st.write("Cycle Time for Entire Process:", cycle_time_entire_process_1, "seconds")

with cols[1]:
    st.markdown("**Option 2**")
    st.write("Daily Output:", daily_output_2, "pills")
    st.write("Budget per Station:", budget_per_station_2)
    st.write("Cycle Time per Station:", cycle_time_per_station_2, "seconds")
    st.write("Cycle Time for Entire Process:", cycle_time_entire_process_2, "seconds")

# New Section for Production Goals
st.subheader("Production Goals and Budget Calculation")
target_daily_output = st.number_input("Enter Target Daily Output (e.g., 10000 pills):", min_value=0, value=10000, format="%d")
option_to_calculate = st.selectbox("Choose Option to Calculate Budget:", ["Option 1", "Option 2"])

if option_to_calculate == "Option 1":
    daily_output = daily_output_1
    total_budget_option = total_budget_1
else:
    daily_output = daily_output_2
    total_budget_option = total_budget_2

number_of_additional_lines, additional_budget_required = calculate_additional_budget(daily_output, target_daily_output, total_budget_option)
st.write("Number of Additional Lines Required:", number_of_additional_lines)
st.write("Additional Budget Required:", additional_budget_required)


# Legend and Explanation Section
st.subheader("Legend and Calculations Explanation")

# Daily Output Calculation
st.markdown("**Daily Output Calculation:**")
st.latex(r"\text{{Shift Length (seconds)}} = 12 \text{{ hours}} \times 60 \text{{ minutes}} \times 60 \text{{ seconds}}")
st.latex(r"\text{{Pills per Shift per Machine}} = \frac{{\text{{Shift Length}}}}{{\text{{Cycle Time per Machine}}}}")
st.latex(r"\text{{Pills per Shift for Entire Line}} = \frac{{\text{{Pills per Shift per Machine}}}}{{\text{{Number of Stations}}}}")
st.latex(r"\text{{Daily Output}} = \text{{Pills per Shift for Entire Line}} \times 2 \text{{ (shifts per day)}}")

# Budget per Station Calculation
st.markdown("**Budget per Station Calculation:**")
st.latex(r"\text{{Budget per Station}} = \frac{{\text{{Total Budget}}}}{{\text{{Number of Stations}}}}")

# Cycle Time Calculation
st.markdown("**Cycle Time Calculation:**")
st.latex(r"\text{{Cycle Time per Station}} = \text{{Cycle Time per Machine}}")
st.latex(r"\text{{Cycle Time for Entire Process}} = \text{{Cycle Time per Station}} \times \text{{Number of Stations}}")

# Additional Budget for Production Goals
st.markdown("**Additional Budget for Production Goals:**")
st.latex(r"\text{{Number of Additional Lines}} = \frac{{\text{{Target Daily Output}} - \text{{Current Daily Output}}}}{{\text{{Current Daily Output}}}}")
st.latex(r"\text{{Additional Budget Required}} = \text{{Number of Additional Lines}} \times \text{{Total Budget for One Line}}")

# Assumptions
st.markdown("**Assumptions:**")
st.markdown("""
- The manufacturing line consists of stations set up in series.
- The cycle time accumulates across the stations.
- The budget is divided evenly across all stations.
""")

