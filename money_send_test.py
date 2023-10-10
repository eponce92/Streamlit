import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import matplotlib.pyplot as plt
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
    worksheet.append_row(["Article Name", "Price"])
    st.experimental_rerun()  # Reload the app immediately after adding headers

# User input for new entries
st.subheader("Add a New Entry")
article_name = st.text_input("Article Name")
price = st.number_input("Price", min_value=0.0, step=0.01)

# Button to add the new entry to the Google Sheet
if st.button("Add Entry"):
    # Access the raw gspread worksheet again
    spreadsheet = conn.client._open_spreadsheet()
    worksheet = spreadsheet.worksheet("Sheet1")
    
    # Append the new data
    worksheet.append_row([article_name, price])

    st.success("Entry Added Successfully!")
    st.cache_data.clear()  # Clearing the cache
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
plt.figure(figsize=(12, 6))
sns.barplot(data=df_updated, x='Article Name', y='Price', palette="viridis")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
st.pyplot()
