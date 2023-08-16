import streamlit as st
import graphviz as gv

# Constants
SHIFT_LENGTH_HOURS = 12
NUM_SHIFTS_PER_DAY = 2
SECONDS_PER_HOUR = 3600

# User Inputs Section
st.title("Manufacturing Line Simulation")
st.sidebar.header("User Inputs")
num_stations = st.sidebar.number_input("Number of Stations", value=1, min_value=1)
cycle_times = [
    st.sidebar.number_input(f"Cycle Time for Station {i+1} (seconds)", value=0, min_value=0) for i in range(num_stations)
]
budgets = [
    st.sidebar.number_input(f"Budget for Station {i+1} ($)", value=0.00, min_value=0.00, format="%.2f") for i in range(num_stations)
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
    dot = gv.Digraph(format='png')
    dot.attr(rankdir='LR')
    dot.node("Line Input")
    for i in range(num_stations):
        for r in range(redundancies[i]):
            dot.node(f"S{i+1}_R{r+1}", label=f"Station {i+1}\\nCycle Time: {cycle_times[i]}s\\nBudget: ${budgets[i]:,.2f}")
            if r == 0:
                if i == 0:
                    dot.edge("Line Input", f"S{i+1}_R{r+1}")
                else:
                    dot.edge(f"S{i}_R{redundancies[i-1]}", f"S{i+1}_R{r+1}")
            else:
                dot.edge(f"S{i+1}_R{r}", f"S{i+1}_R{r+1}")
    dot.node("Line Output")
    dot.edge(f"S{num_stations}_R{redundancies[-1]}", "Line Output")
    return dot

# Display Results
total_cycle_time = calculate_total_cycle_time(cycle_times, redundancies)
total_budget = calculate_total_budget(budgets, redundancies)
total_output = calculate_total_output(total_cycle_time)

st.subheader("Results")
st.write(f"Total Cycle Time: {total_cycle_time:.2f} seconds")
st.write(f"Total Budget: ${total_budget:,.2f}")
st.write(f"Total Output: {total_output:,} pills per day")

st.subheader("Graphical Representation")
graph = create_graph(cycle_times, budgets, redundancies)
st.graphviz_chart(str(graph))
