import streamlit as st
import pandas as pd

@st.cache
def consolidate_files(files):
    # List to store all the dataframes
    dfs = []

    for file in files:
        # Read the Excel file into a DataFrame
        metadata = pd.read_excel(file, sheet_name='Metadata')
        name = metadata.loc[metadata['Key'] == 'Name', 'Value'].iloc[0]
        position = metadata.loc[metadata['Key'] == 'Engineer Level', 'Value'].iloc[0]
        
        df_results = pd.read_excel(file, sheet_name='Results')
        
        # Pivot the table
        df_pivot = df_results.pivot_table(index=df_results.index, columns='Skill', values='Difference').reset_index(drop=True)
        
        # Add name and position
        df_pivot['Name'] = name
        df_pivot['Engineer Level'] = position
        
        dfs.append(df_pivot)

    # Combine all dataframes into one
    consolidated_df = pd.concat(dfs, axis=0)
    
    # Rearrange columns
    cols = ['Name', 'Engineer Level'] + [col for col in consolidated_df if col not in ['Name', 'Engineer Level']]
    consolidated_df = consolidated_df[cols]

    return consolidated_df


def main():
    st.title("Engineers Data Consolidation")

    uploaded_files = st.file_uploader("Upload Files", type=['xlsx'], accept_multiple_files=True)

    if uploaded_files:
        consolidated_df = consolidate_files(uploaded_files)
        st.write(consolidated_df)

if __name__ == "__main__":
    main()
