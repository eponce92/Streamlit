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
    top_experts = df[df[skill] > 3]['Name'].tolist()
    return ", ".join(top_experts)

def engineers_requiring_training(df, skill, setpoint):
    """Find engineers below the skill setpoint."""
    low_skill_engineers = df[df[skill] < setpoint]['Name'].tolist()
    return ", ".join(low_skill_engineers)

def main():
    st.title("Engineer Training Planning Tool")

    # Config Sidebar
    st.sidebar.title("Configuration")
    threshold = st.sidebar.slider("Skill Threshold for Training", -4, 4, 3)
    training_frequency = st.sidebar.radio("Training Frequency", ["Weekly", "Bi-weekly", "Monthly"])
    skill_setpoint = st.sidebar.slider("Skill Setpoint for Training Requirement", -4, 4, 0)

    uploaded_files = st.sidebar.file_uploader("Upload Files", type=['xlsx'], accept_multiple_files=True)
    if uploaded_files:
        consolidated_df = consolidate_files(uploaded_files)
        st.session_state.consolidated_df = consolidated_df
    elif 'consolidated_df' not in st.session_state:
        st.warning("Please upload files.")
        return
    else:
        consolidated_df = st.session_state.consolidated_df

    # Setting skill priority as scores from 1 to 10
    skill_priority_scores = {}
    for skill in consolidated_df.columns.drop(['Name', 'Engineer Level']):
        score = st.sidebar.slider(f"Priority score for {skill}", 1, 10, 5)
        skill_priority_scores[skill] = score

    # Sorting skills based on priority
    skills_to_train = consolidated_df.drop(columns=['Name', 'Engineer Level']).mean()
    filtered_skills = skills_to_train[skills_to_train < threshold]
    sorted_skills = sorted(filtered_skills.items(), key=lambda x: skill_priority_scores[x[0]], reverse=True)
    sorted_skill_names = [item[0] for item in sorted_skills]

    st.write("### Proposed Training Schedule")
    for skill in sorted_skill_names:
        trainers = recommend_trainers(consolidated_df, skill)
        engineers = engineers_requiring_training(consolidated_df, skill, skill_setpoint)
        st.markdown(f"**Training for {skill}** - Recommended Trainers: {trainers} - Engineers: {engineers}")

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
