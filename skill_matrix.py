import streamlit as st
import pandas as pd
import plotly.express as px
import io


def to_excel(df):
    """
    Convert a DataFrame into a BytesIO stream Excel format for download
    """
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Consolidated_Data', index=False)
    return output.getvalue()


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

    # Split the screen into 4 columns: 
    # First column gets double the width for file uploads and the data table.
    # The other columns will be used for visualizations.
    col1, col2, col3, col4 = st.columns((2,1,1,1))

    with col1:
        uploaded_files = st.file_uploader("Upload Files", type=['xlsx'], accept_multiple_files=True)

        if uploaded_files:
            consolidated_df = consolidate_files(uploaded_files)
            st.write("### Consolidated Data Table")
            st.write(consolidated_df)

            # Download button within an expander for better organization.
            with st.expander("Download Options"):
                download_data = to_excel(consolidated_df)
                st.download_button(label="Download as Excel",
                                   data=download_data,
                                   file_name="consolidated_data.xlsx",
                                   mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    if uploaded_files:  # Checking again to ensure the data has been uploaded before rendering the plots
        # Visualizations section

        # Individual heatmap in col2
        with col2:
            st.write("#### Individual Skills Heatmap")
            fig_individual = px.imshow(consolidated_df.set_index('Name').drop(columns=['Engineer Level']),
                                       labels=dict(color="Difference"),
                                       color_continuous_scale=["red", "yellow", "green"])
            fig_individual.update_layout(xaxis_title="Skills", yaxis_title="Engineer Name")
            st.plotly_chart(fig_individual)

        # Overall team heatmap in col3 (or col4 depending on where you want it)
        with col3:
            st.write("#### Team Skills Heatmap")
            average_difference = consolidated_df.drop(columns=['Name', 'Engineer Level']).mean().to_frame().T
            fig_overall = px.imshow(average_difference,
                                    labels=dict(color="Average Difference"),
                                    color_continuous_scale=["red", "yellow", "green"])
            fig_overall.update_layout(xaxis_title="Skills", yaxis_title="Team Average")
            st.plotly_chart(fig_overall)

        # If you have any additional charts or content, you can place them in col4

if __name__ == "__main__":
    main()
