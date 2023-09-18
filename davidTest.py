import streamlit as st
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

LEVELS = ['No knowledge', 'Knows but no practice', 'Can do with help', 'Can do alone', 'Can teach others']
TARGETS = {dict(zip(correct_target_levels, range(len(correct_target_levels))))}
SKILLS = {skills}
TARGET_VALUES = {target_values}

SHOW_RESULTS = True  # Change this to False if you don't want to show the results
last_submitted_name = None  # Keep track of the last name submitted

@st.cache_data 
def get_skills():
    return SKILLS

def get_target_value(skill, position):
    skill_index = SKILLS.index(skill)
    position_index = list(TARGETS.keys()).index(position)
    return TARGET_VALUES[skill_index][position_index]

def send_email(name, position, results_data):
    global last_submitted_name
    if name == last_submitted_name:
        st.warning("Duplicate submission detected. Email not sent.")
        return
    last_submitted_name = name
    
    # ... rest of the code remains unchanged ...

if __name__ == "__main__":
    main()
