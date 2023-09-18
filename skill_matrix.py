import streamlit as st
import pandas as pd

@st.cache
def consolidate_files(files):
    # List to store all the dataframes
    dfs = []
    
    for file in files:
        # Read the Excel file into a DataFrame
        df = pd.read_excel(file)
        
        # Pivot the table
        df_pivot = df.pivot_table(index=['Engineer Level', df.index], columns='Skill', values='Difference').reset_index(drop=True)
        
        # Add name from filename (assuming filename format is Results_{name}.xlsx)
        df_pivot['Name'] = file.name.split('_')[1].replace('.xlsx', '')
        
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
