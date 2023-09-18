import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache(allow_output_mutation=True)
def consolidate_files(files):
    # List to store all the dataframes
    all_data = []

    for file in files:
        # Read the Excel file into a DataFrame
        metadata = pd.read_excel(file, sheet_name='Metadata')
        name = metadata.loc[metadata['Key'] == 'Name', 'Value'].iloc[0]
        position = metadata.loc[metadata['Key'] == 'Engineer Level', 'Value'].iloc[0]
        
        df_results = pd.read_excel(file, sheet_name='Results')
        
        # Creating a dictionary to store data for each engineer
        engineer_data = {
            'Name': name,
            'Engineer Level': position
        }
        # Updating the dictionary with skill differences
        for idx, row in df_results.iterrows():
            engineer_data[row['Skill']] = row['Difference']
        
        all_data.append(engineer_data)

    # Converting list of dictionaries to DataFrame
    consolidated_df = pd.DataFrame(all_data)

    return consolidated_df



def main():
    st.title("Engineers Data Consolidation")

    uploaded_files = st.file_uploader("Upload Files", type=['xlsx'], accept_multiple_files=True)

    if uploaded_files:
        consolidated_df = consolidate_files(uploaded_files)
        st.write(consolidated_df)

        # Creating a heatmap with a custom color scale
        fig = px.imshow(consolidated_df.set_index('Name').drop(columns=['Engineer Level']),
                        labels=dict(color="Difference"),
                        title="Skills Difference Heatmap",
                        color_continuous_scale=["red", "yellow", "green"])  # Adjusting the color scale
        fig.update_layout(xaxis_title="Skills", yaxis_title="Engineer Name")
        st.plotly_chart(fig)

if __name__ == "__main__":
    main()
