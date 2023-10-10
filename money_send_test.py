import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.title("Article Price Database")

# Establish the connection to Google Sheets
conn = st.experimental_connection("gsheets", type=GSheetsConnection)

# Read the current data from the Google Sheet
df = conn.read(
    worksheet="Sheet1",
)

# Display current data to the user
st.subheader("Current Database")
st.dataframe(df)

# User input for new entries
st.subheader("Add a New Entry")
article_name = st.text_input("Article Name")
price = st.number_input("Price", min_value=0.0, step=0.01)

# Button to add the new entry to the Google Sheet
if st.button("Add Entry"):
    # Access the raw gspread worksheet
    spreadsheet = conn.client._open_spreadsheet()
    worksheet = spreadsheet.worksheet("Sheet1")

    # Append the new data
    worksheet.append_row([article_name, price])

    st.success("Entry Added Successfully!")
    st.experimental_rerun()  # Reload the app to display the updated data
