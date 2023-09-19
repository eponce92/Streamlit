import streamlit as st
import pandas as pd
import plotly.express as px
import io
import datetime
import plotly.graph_objects as go
import numpy as np
import requests

st.set_page_config(layout="wide")

LEVELS = ['No knowledge', 'Knows but no practice', 'Can do with help', 'Can do alone', 'Can teach others', 'Expert']
TARGETS = {
    'MX Technitian Level 1': 1,
    'MX Technitian Level 2': 2,
    'MX Technitian Level 3': 3,
    'Engineer Level 1': 3,
    'Engineer Level 2': 4,
    'Engineer Level 3': 5
}

@st.cache_data
def get_skills():
    # Fetching the skills list from the GitHub raw URL
    url = "https://raw.githubusercontent.com/eponce92/Streamlit/main/skills_list.txt"
    response = requests.get(url)
    skills = response.text.split(",\n")
    return [skill.strip() for skill in skills]

def sanitize_key(skill_name, idx):
    return "priority_" + str(idx) + "_" + "".join(e for e in skill_name if e.isalnum())

@st.cache_data
def get_skills():
    # Fetching the skills list from the GitHub raw URL
    url = "https://raw.githubusercontent.com/eponce92/Streamlit/main/skills_list.txt"
    response = requests.get(url)
    skills = response.text.split(",\n")
    return [skill.strip() for skill in skills]

def to_excel(df):
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

def recommend_trainers(df, skill, threshold):
    top_experts = df[df[skill] >= threshold]['Name'].tolist() 
    return top_experts

def engineers_requiring_training(df, skill, setpoint):
    low_skill_engineers = df[df[skill] <= setpoint]['Name'].tolist()
    return low_skill_engineers

def get_next_training_date(frequency, start_date=datetime.datetime.now() + datetime.timedelta(weeks=2)):
    if frequency == "Weekly":
        return start_date + datetime.timedelta(weeks=1)
    elif frequency == "Bi-weekly":
        return start_date + datetime.timedelta(weeks=2)
    else:
        return start_date + datetime.timedelta(weeks=4)

def display_training_schedule(training_events):
    st.write("### Proposed Training Schedule")
    
    for event in training_events:
        st.write("---")  # horizontal line for separation
        st.subheader(event["Task"])
        st.write(f"**Date**: {event['Start'].strftime('%Y-%m-%d')}")
        
        trainers = event["Resource"]
        if trainers:
            st.write(f"**Recommended Trainers**: {trainers}")
        else:
            st.write("**Recommended Trainers**: Not specified")
        
        engineers = event.get("Engineers", [])
        if engineers:
            st.write(f"**Engineers**: {', '.join(engineers)}")
        else:
            st.write("**Engineers**: Not specified")

def main():
    st.title("Engineer Training Planning Tool")

    st.sidebar.title("Configuration")
    threshold = st.sidebar.slider("Skill Threshold for Training", -5, 5, 4, key="threshold_slider")
    training_frequency = st.sidebar.radio("Training Spread", ["Weekly", "Bi-weekly", "Monthly"])
    skill_setpoint = st.sidebar.slider("Skill Setpoint for Training Requirement", -5, 5, 0, key="setpoint_slider")

    uploaded_files = st.sidebar.file_uploader("Upload Files", type=['xlsx'], accept_multiple_files=True)
    if uploaded_files:
        consolidated_df = consolidate_files(uploaded_files)
        st.table(consolidated_df)

        download_data = to_excel(consolidated_df)
        st.download_button(label="Download Consolidated Data",
                           data=download_data,
                           file_name="consolidated_data.xlsx",
                           mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    else:
        st.warning("Please upload files.")
        return

    skill_priority_scores = {}
    for idx, skill in enumerate(get_skills()):
        key = sanitize_key(skill, idx)
        score = st.sidebar.slider(f"Priority score for {skill}", 1, 10, 5, key=key)
        skill_priority_scores[skill] = score

    skills_to_train = consolidated_df.drop(columns=['Name', 'Engineer Level']).mean()
    filtered_skills = skills_to_train[skills_to_train < threshold]
    sorted_skills = sorted(filtered_skills.items(), key=lambda x: skill_priority_scores[x[0]], reverse=True)
    sorted_skill_names = [item[0] for item in sorted_skills]

    training_date = datetime.datetime.now() + datetime.timedelta(weeks=2)
    training_events = []

    for skill in sorted_skill_names:
        trainers = recommend_trainers(consolidated_df, skill, threshold)
        engineers = engineers_requiring_training(consolidated_df, skill, skill_setpoint)

        event = {
            "Task": skill,
            "Start": training_date,
            "Resource": ", ".join(trainers),
            "Engineers": engineers
        }
        training_events.append(event)

        training_date = get_next_training_date(training_frequency, training_date)

    display_training_schedule(training_events)

    st.write("### Heatmaps")
    
    fig1 = px.imshow(consolidated_df.drop(columns=['Name', 'Engineer Level']).transpose(), 
                     title="All Engineers Skill Levels",
                     color_continuous_scale=["red", "yellow", "green"],
                     zmin=-5, zmax=5)
    
    fig2 = px.imshow(pd.DataFrame(consolidated_df.drop(columns=['Name', 'Engineer Level']).mean()).transpose(),
                     title="Average Skill Level Across All Engineers",
                     color_continuous_scale=["red", "yellow", "green"],
                     zmin=-5, zmax=5)

    st.plotly_chart(fig1, use_container_width=True)
    st.plotly_chart(fig2, use_container_width=True)


if __name__ == "__main__":
    main()
