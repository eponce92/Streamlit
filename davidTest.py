import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import openpyxl

TARGETS = {
    'Associate Engineer': 4,
    'Engineer': 3,
    'Senior Engineer': 2,
    'Staff Engineer': 1,
    'Senior Staff Engineer': 0
}

SKILLS = [
    "PLC Programming",
    "Cognex Cameras",
    "Kistler press",
    "Mechanical troubleshooting",
    "Electrical schematics and troubleshooting",
    "Keyence vision",
    "Fanuc Programming",
    "Atlas coptco nutrunners"
]

LEVELS = [
    "Can train others",
    "Can do it on their own without help",
    "Can do it with some help",
    "Has the knowledge but lacks the practice",
    "No knowledge"
]

SHOW_RESULTS = True  # Change this to False to hide results from the user

def main():
    st.title("Self-Assessment Tool")

    name = st.text_input("Enter your name:", "")
    position = st.selectbox("Select your engineering level:", list(TARGETS.keys()))

    responses = {skill: st.selectbox(f"How competent are you at {skill}?", LEVELS) for skill in SKILLS}

    results_data = calculate_differences(responses, position)

    if SHOW_RESULTS:
        results_df = pd.DataFrame(results_data, columns=['Skill', 'Self-Assessment', 'Difference'])
        st.table(results_df.style.hide_index().set_table_styles({
            'Skill': 'font-weight: bold'
        }))
    
    send_email(name, position, results_data)

def calculate_differences(responses, position):
    differences = {}
    for skill, level in responses.items():
        diff = LEVELS.index(level) - TARGETS[position]
        differences[skill] = {
            'Self-Assessment': level,
            'Difference': diff
        }

    return differences

def send_email(name, position, data):
    df = pd.DataFrame(data).transpose()
    df.to_excel("results.xlsx", index=False)

    from_email = "david.almazan.tsla@gmail.com"
    to_email = "david.almazan.tsla@gmail.com"

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = f"Self-Assessment Results for {name} ({position})"

    body = "Attached are the self-assessment results."
    msg.attach(MIMEText(body, 'plain'))

    with open("results.xlsx", "rb") as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename=results.xlsx")
        msg.attach(part)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("david.almazan.tsla@gmail.com", "tesla2023")
    server.sendmail(from_email, to_email, msg.as_string())
    server.quit()

if __name__ == "__main__":
    main()
