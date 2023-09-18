import streamlit as st
import pandas as pd
import plotly.express as px
import io

# Set the page layout to wide mode
st.set_page_config(layout="wide")


def to_excel(df):
    """Convert a DataFrame into a BytesIO stream Excel format for download."""
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


def recommend_trainers(df, skill):
    """Recommend trainers based on engineer level for a given skill."""
    top_experts = df[df[skill] > 2]['Name'].tolist()
    return ", ".join(top_experts)


def main():
    st.title("Engineer Training Planning Tool")

    # Config Sidebar
    st.sidebar.title("Configuration")
    threshold = st.sidebar.slider("Skill Threshold for Training", -4, 4, 0)
    training_frequency = st.sidebar.radio("Training Frequency", ["Weekly", "Bi-weekly", "Monthly"])

    uploaded_files = st.sidebar.file_uploader("Upload Files", type=['xlsx'], accept_multiple_files=True)
    if uploaded_files:
        consolidated_df = consolidate_files(uploaded_files)

        # Skills Overview
        st.write("### Skills Overview")
        skills_to_train = consolidated_df.drop(columns=['Name', 'Engineer Level']).mean()
        skills_to_train = skills_to_train[skills_to_train < threshold]

        # Proposed Training Schedule
        st.write("### Proposed Training Schedule")
        
        skills_below_threshold = skills_to_train.index.tolist()
        max_sessions = min(len(skills_below_threshold), sessions)
        
        for i in range(max_sessions):
            skill = skills_below_threshold[i]
            trainers = recommend_trainers(consolidated_df, skill)
            st.markdown(f"**Training for {skill}**: Recommended Trainers: {trainers}")
        
        # Calendar Planning
        st.write("### Training Calendar")
        
        # Ensure equal lengths for all columns
        remaining_sessions = sessions - max_sessions
        skills_for_calendar = skills_below_threshold[:max_sessions] + ["-"] * remaining_sessions
        trainers_for_calendar = [recommend_trainers(consolidated_df, skill) for skill in skills_for_calendar]
        
        st.table(pd.DataFrame({
            "Week": weeks,
            "Skill": skills_for_calendar,
            "Recommended Trainer": trainers_for_calendar
        }))


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
