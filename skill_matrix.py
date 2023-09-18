import streamlit as st
import pandas as pd
import plotly.express as px
import io
import datetime
import calendar
import plotly.graph_objects as go
import numpy as np
import plotly.figure_factory as ff

st.set_page_config(layout="wide")

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

def main():
    st.title("Engineer Training Planning Tool")

    st.sidebar.title("Configuration")
    threshold = st.sidebar.slider("Skill Threshold for Training", -4, 4, 3)
    training_frequency = st.sidebar.radio("Training Spread", ["Weekly", "Bi-weekly", "Monthly"])
    skill_setpoint = st.sidebar.slider("Skill Setpoint for Training Requirement", -4, 4, 0)

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
    for skill in consolidated_df.columns.drop(['Name', 'Engineer Level']):
        score = st.sidebar.slider(f"Priority score for {skill}", 1, 10, 5)
        skill_priority_scores[skill] = score

    skills_to_train = consolidated_df.drop(columns=['Name', 'Engineer Level']).mean()
    filtered_skills = skills_to_train[skills_to_train < threshold]
    sorted_skills = sorted(filtered_skills.items(), key=lambda x: skill_priority_scores[x[0]], reverse=True)
    sorted_skill_names = [item[0] for item in sorted_skills]

    st.write("### Proposed Training Schedule")
    training_date = datetime.datetime.now() + datetime.timedelta(weeks=2)
    
    training_dates = []  
    training_events = []

    for skill in sorted_skill_names:
        trainers = recommend_trainers(consolidated_df, skill, threshold)
        engineers = engineers_requiring_training(consolidated_df, skill, skill_setpoint)

        training_dates.append(training_date)  

        event = {
            "Task": skill,
            "Start": training_date,
            "Finish": training_date + datetime.timedelta(hours=2),
            "Resource": ", ".join(trainers)
        }
        training_events.append(event)

        st.write(f"**{skill}**:")
        st.write(f"Date: {training_date.strftime('%Y-%m-%d')}")
        st.write(f"Recommended Trainers: {', '.join(trainers)}")
        st.write(f"Engineers: {', '.join(engineers)}")
        training_date = get_next_training_date(training_frequency, training_date)

    st.write("### Visualization")

    st.write("#### Training Schedule Calendar")
    dates = pd.date_range(start="2023-01-01", end="2023-12-31", freq='D')
    values = [1 if date in training_dates else 0 for date in dates]

    fig_calendar = go.Figure(data=go.Scatter(
        x=dates,
        y=values,
        mode='markers',
        marker=dict(
            size=10,
            color=values,
            colorscale='Viridis',
            showscale=False
        )
    ))

    fig_calendar.update_layout(
        title="Training Schedule in 2023",
        xaxis_title="Date",
        yaxis_title="Scheduled Training",
        yaxis=dict(tickvals=[0, 1], ticktext=['No Training', 'Training']),
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1m", step="month", stepmode="backward"),
                    dict(count=6, label="6m", step="month", stepmode="backward"),
                    dict(count=12, label="YTD", step="month", stepmode="todate"),
                    dict(count=12, label="1y", step="year", stepmode="backward"),
                    dict(step="all")
                ])
            ),
            type="date"
        ),
    )
    st.plotly_chart(fig_calendar, use_container_width=True)

    # Gantt Chart
    fig_gantt = ff.create_gantt(training_events, colors={'Machine Learning': 'rgb(220, 0, 0)', 'Python': 'rgb(170, 14, 200)'},  
                            index_col='Resource', title='Training Schedule',
                            show_colorbar=True, bar_width=0.2, showgrid_x=True, showgrid_y=True)
    st.plotly_chart(fig_gantt, use_container_width=True)

if __name__ == "__main__":
    main()
