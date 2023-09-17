import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from datetime import date, timedelta
import smtplib
from email.message import EmailMessage

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

LEVELS = {
    0: "No Knowledge",
    1: "Has Knowledge but Lacks Practice",
    2: "Can Do with Assistance",
    3: "Can Do Independently",
    4: "Can Train Others"
}

TARGETS = {
    "Associate Engineer": 1,
    "Engineer": 2,
    "Senior Engineer": 3,
    "Staff Engineer": 4,
    "Senior Staff Engineer": 5
}

SHOW_RESULTS = True  # Set to False before deploying

def main():
    st.title("Skill Self-assessment for Tesla Engineers")
    st.write("Please fill out the following form:")

    name = st.text_input("Name:")
    position = st.selectbox("Position:", list(TARGETS.keys()))

    responses = {}
    for skill in SKILLS:
        responses[skill] = st.selectbox(f"{skill}:", list(LEVELS.values()))

    if st.button("Submit"):
        differences = calculate_differences(responses, position)
        
        results_table = []
        for skill, level in responses.items():
            difference = list(LEVELS.values()).index(level) - TARGETS[position]
            results_table.append([skill, level, difference])

        if SHOW_RESULTS:
            st.table(results_table)

        send_email(name, position, results_table)

def calculate_differences(responses, position):
    differences = {}
    for skill, level in responses.items():
        differences[skill] = list(LEVELS.values()).index(level) - TARGETS[position]
    return differences

def send_email(name, position, results_table):
    msg = EmailMessage()
    msg.set_content(str(results_table))
    msg["Subject"] = f"Self-assessment Results for {name} - {position}"
    msg["From"] = "your_email@gmail.com"  # Change this
    msg["To"] = "destination_email@gmail.com"  # Change this

    # Connect to the mail server
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login("your_email@gmail.com", "your_password")  # Change these
    server.send_message(msg)
    server.quit()

if __name__ == "__main__":
    main()
