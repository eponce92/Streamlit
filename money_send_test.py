import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')  # Set the backend of matplotlib to 'Agg'
import seaborn as sns

st.title("Article Price Database")

# Establish the connection to Google Sheets
conn = st.experimental_connection("gsheets", type=GSheetsConnection)

# Read the current data from the Google Sheet
df = conn.read(
    worksheet="Sheet1",
)

# If the sheet is empty, add headers
if df.empty:
    # Access the raw gspread worksheet
    spreadsheet = conn.client._open_spreadsheet()
    worksheet = spreadsheet.worksheet("Sheet1")
    worksheet.append_row(["Article", "Price"])
    st.experimental_rerun()  # Reload the app immediately after adding headers

# User input for new entries
st.subheader("Add a New Entry")
article_name = st.text_input("Article")
price = st.number_input("Price", min_value=0.0, step=0.01)

# Button to add the new entry to the Google Sheet
if st.button("Add Entry"):
    # Access the raw gspread worksheet again
    spreadsheet = conn.client._open_spreadsheet()
    worksheet = spreadsheet.worksheet("Sheet1")
    
    # Append the new data
    worksheet.append_row([article_name, price])

    st.success("Entry Added Successfully!")
    st.experimental_rerun()  # Reload the app after adding the entry

# Re-fetch the data to display in Streamlit
df_updated = conn.read(
    worksheet="Sheet1",
)

# Display the updated data to the user
st.subheader("Current Database")
st.dataframe(df_updated)

# Plotting the data
st.subheader("Article Price Visualization")

# Check if the DataFrame is not empty before plotting
if not df_updated.empty:
    # Create a bar plot
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(data=df_updated, x='Article', y='Price', hue='Article', palette="viridis", ax=ax)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, horizontalalignment='right')
    ax.legend(title='Articles')
    plt.tight_layout()

    # Display the plot in Streamlit
    st.pyplot(fig)
else:
    # Message to display if there is no data to plot
    st.write("No data available for visualization.")
