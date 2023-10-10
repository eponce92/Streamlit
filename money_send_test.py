import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.title("Article Price Database")

# Establish the connection to Google Sheets
conn = st.experimental_connection("gsheets", type=GSheetsConnection)

# Read the current data from the Google Sheet
df = conn.read(
    worksheet="Sheet1",
    usecols=[0, 1]  # Assuming data is stored in the first two columns
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
    new_entry = pd.DataFrame({
        'Article Name': [article_name],
        'Price': [price]
    })

    # Re-read the Google Sheet to ensure we're working with the most recent version
    df_current = conn.read(
        worksheet="Sheet1",
        usecols=[0, 1]
    )
    df_current.dropna(how='all', inplace=True)

    # Add the new entry
    df_updated = pd.concat([df_current, new_entry], ignore_index=True)
    
    # Clear the worksheet before updating with new data
    conn.clear(worksheet="Sheet1")
    
    # Push the updated DataFrame to the Google Sheet starting from the correct columns (A and B)
    conn.update(worksheet="Sheet1", data=df_updated, start='A1')  # Explicitly specify start column and row

    st.success("Entry Added Successfully!")
    st.experimental_rerun()  # Reload the app to display the updated data

