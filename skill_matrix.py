import streamlit as st
import pandas as pd
import plotly.express as px
import io

# Set the page layout to wide mode
st.set_page_config(layout="wide")


def to_excel(df):
    """
    Convert a DataFrame into a BytesIO stream Excel format for download.
    """
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Consolidated_Data', index=False)
    return output.getvalue()


@st.cache(allow_output_mutation=True)
def consolidate_files(files):
    all_data = []
    for file in files:
        metadata = pd.read_excel(file, sheet_name='Metadata')
        name = metadata.loc[metadata['Key'] == 'Name', 'Value'].iloc[0]
        position = metadata.loc[metadata['Key'] == 'Engineer Level', 'Value'].iloc[0]
        df_results = pd.read_excel(file, sheet_name='Results')

        engineer_data = {
            'Name': name,
            'Engineer Level': position
        }
        for idx, row in df_results.iterrows():
            engineer_data[row['Skill']] = row['Difference']
        all_data.append(engineer_data)

    consolidated_df = pd.DataFrame(all_data)
    return consolidated_df


def main():
    st.title("Engineer Training Planning Tool")

    # Config Sidebar
    st.sidebar.title("Configuration")

    threshold = st.sidebar.slider("Skill Threshold", 0, 10, 5)
    training_frequency = st.sidebar.radio("Training Frequency", ["Weekly", "Bi-weekly", "Monthly"])
    priority = st.sidebar.slider("Skill Priority (1 is highest)", 1, 5, 1)
    trainers = st.sidebar.text_input("Enter Potential Trainers", "John, Jane, Doe")
    duration = st.sidebar.number_input("Expected Duration of Each Training (in hours)", 1, 10, 2)

    uploaded_files = st.sidebar.file_uploader("Upload Files", type=['xlsx'], accept_multiple_files=True)
    if uploaded_files:
        consolidated_df = consolidate_files(uploaded_files)
        
        # Skills Overview
        st.write("### Skills Overview")
        flagged_skills = consolidated_df.drop(columns=['Name', 'Engineer Level']).mean()
        flagged_skills = flagged_skills[flagged_skills < threshold]
        st.write("Skills Below Threshold: ", ", ".join(flagged_skills.index.tolist()))
        
        # Proposed Training Schedule
        st.write("### Proposed Training Schedule")
        # Simple illustration using markdown (actual scheduling may require more backend logic)
        sessions = int(6 / {'Weekly': 4, 'Bi-weekly': 2, 'Monthly': 1}[training_frequency])
        st.markdown(f"Suggested {sessions} training sessions over 6 months.")
        for idx in range(sessions):
            st.markdown(f"**Session {idx + 1}**: Focus on {flagged_skills.idxmax()} skill. Trainer: {trainers.split(',')[0]}")
            flagged_skills = flagged_skills.drop(flagged_skills.idxmax())

        # Skill Breakdown
        st.write("### Skill Breakdown")
        flagged_skills = consolidated_df.drop(columns=['Name', 'Engineer Level']).mean()
        flagged_skills = flagged_skills[flagged_skills < threshold]
        st.write(flagged_skills.sort_values(ascending=False))

        # Visualization
        st.write("### Visualization")
        st.write("#### Individual Skills Heatmap")
        fig_individual = px.imshow(consolidated_df.set_index('Name').drop(columns=['Engineer Level']),
                                   labels=dict(color="Difference"),
                                   color_continuous_scale=["red", "yellow", "green"])
        fig_individual.update_layout(xaxis_title="Skills", yaxis_title="Engineer Name")
        st.plotly_chart(fig_individual, use_container_width=True)

        st.write("#### Team Skills Heatmap")
        average_difference = consolidated_df.drop(columns=['Name', 'Engineer Level']).mean().to_frame().T
        fig_overall = px.imshow(average_difference,
                                labels=dict(color="Average Difference"),
                                color_continuous_scale=["red", "yellow", "green"])
        fig_overall.update_layout(xaxis_title="Skills", yaxis_title="Team Average")
        st.plotly_chart(fig_overall, use_container_width=True)
        
        # Save & Export
        download_data = to_excel(consolidated_df)
        st.sidebar.download_button(label="Download Consolidated Data",
                                   data=download_data,
                                   file_name="consolidated_data.xlsx",
                                   mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")


if __name__ == "__main__":
    main()
