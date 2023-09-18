import streamlit as st
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

LEVELS = ['No knowledge', 'Knows but no practice', 'Can do with help', 'Can do alone', 'Can teach others']
SHOW_RESULTS = True  # Change this to False if you don't want to show the results
last_submitted_name = None  # Keep track of the last name submitted

@st.cache(allow_output_mutation=True)
def get_data_from_excel(file):
    df = pd.read_excel(file)
    
    # Extract skill list
    skills = df['C'].dropna().tolist()
    
    # Extract target levels
    targets = {col: idx for idx, col in enumerate(df.columns[3:].tolist())}
    
    return skills, targets

def send_email(name, position, results_data):
    ...
    # (The email sending function remains unchanged.)

def main():
    st.title("Engineer Auto-Evaluation")
    
    uploaded_file = st.file_uploader("Upload Training Matrix Excel File", type="xlsx")
    
    if uploaded_file:
        skills, TARGETS = get_data_from_excel(uploaded_file)
        
        name = st.text_input("Your Name:")
        position = st.selectbox("Your Engineer Level:", list(TARGETS.keys()))

        responses = {}
    
        for skill in skills:
            responses[skill] = st.selectbox(f"How would you rate your {skill} skills?", LEVELS)

        if st.button("Submit"):
            results_data = []
            for skill, level in responses.items():
                difference = LEVELS.index(level) - TARGETS[position]
                results_data.append([skill, level, difference])

            send_email(name, position, results_data)

            if SHOW_RESULTS:
                results_df = pd.DataFrame(results_data, columns=['Skill', 'Self-Assessment', 'Difference'])
                st.write(results_df.to_html(index=False, classes='table table-striped table-hover'), unsafe_allow_html=True)
    else:
        st.warning("Please upload the Training Matrix Excel file to proceed.")

if __name__ == "__main__":
    main()
