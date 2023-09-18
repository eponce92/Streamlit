import streamlit as st
import pandas as pd

def consolidate_data(uploaded_files):
    # Create an empty DataFrame to store the consolidated results
    consolidated_df = pd.DataFrame()
    
    # Process each uploaded file
    for file in uploaded_files:
        # Read the Excel file into a DataFrame
        data = pd.read_excel(file)
        # Pivot the data so that the skills become columns
        pivoted_data = data.pivot(index=None, columns='Skill', values='Difference')
        # Add the engineer's name to the DataFrame (assuming it's in the filename)
        name = file.name.replace("Results_", "").replace(".xlsx", "")
        pivoted_data.insert(0, "Name", name)
        
        # Append the pivoted data to the consolidated DataFrame
        consolidated_df = consolidated_df.append(pivoted_data, ignore_index=True)
    
    return consolidated_df

def main():
    st.title("Engineer Skills Consolidator")
    
    uploaded_files = st.file_uploader("Upload all the Excel files", type="xlsx", accept_multiple_files=True)
    
    if uploaded_files:
        consolidated_data = consolidate_data(uploaded_files)
        st.table(consolidated_data)

if __name__ == "__main__":
    main()
