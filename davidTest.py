import streamlit as st
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import openpyxl

def main():
    st.title("Engineer Self-Evaluation")
    
    # Input fields
    name = st.text_input("Name")
    positions = ["Associate Engineer", "Engineer", "Senior Engineer", "Staff Engineer", "Senior Staff Engineer"]
    position = st.selectbox("Position", positions)
    skills = {
        "PLC Programming": st.slider("PLC Programming", 0, 4),
        "Cognex Cameras": st.slider("Cognex Cameras", 0, 4),
        "Kistler Press": st.slider("Kistler Press", 0, 4),
        "Mechanical Troubleshooting": st.slider("Mechanical Troubleshooting", 0, 4),
        "Electrical Schematics & Troubleshooting": st.slider("Electrical Schematics & Troubleshooting", 0, 4),
        "Keyence Vision": st.slider("Keyence Vision", 0, 4),
        "Fanuc Programming": st.slider("Fanuc Programming", 0, 4),
        "Atlas Coptco Nutrunners": st.slider("Atlas Coptco Nutrunners", 0, 4)
    }
    
    submit = st.button("Submit")
    
    if submit:
        # Analyze the results
        results_data = analyze_results(position, skills)
        
        # Send the results via email
        send_email(name, position, results_data)

        # Optionally display the results (can turn this off later)
        display_results = True  # Set this to False if you don't want to display results to users
        if display_results:
            results_df = pd.DataFrame(results_data, columns=['Skill', 'Level', 'Difference'])
            st.table(results_df.set_index('Skill'))

def analyze_results(position, skills):
    TARGETS = {
        "Associate Engineer": 2,
        "Engineer": 2,
        "Senior Engineer": 3,
        "Staff Engineer": 3,
        "Senior Staff Engineer": 4
    }
    LEVELS = [
        "No Knowledge",
        "Knows with Assistance",
        "Can Perform with Assistance",
        "Can Perform Independently",
        "Can Train Others"
    ]
    
    target_level = TARGETS[position]
    results_data = []
    
    for skill, level in skills.items():
        difference = level - target_level
        results_data.append([skill, LEVELS[level], difference])
    
    return results_data

def send_email(name, position, results_data):
    # Create a new Excel file with the results
    df = pd.DataFrame(results_data, columns=['Skill', 'Level', 'Difference'])
    filename = f"{name}_{position}_evaluation.xlsx"
    df.to_excel(filename, index=False)

    # Set up the SMTP server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    
    # Log in to the server using the App Password
    server.login("david.almazan.tsla@gmail.com", "dtupyqjbdiufrwqp")
    
    # Set up the email
    msg = MIMEMultipart()
    msg['From'] = "david.almazan.tsla@gmail.com"
    msg['To'] = "david.almazan.tsla@gmail.com"
    msg['Subject'] = f"Self-evaluation results for {name} ({position})"
    body = f"Attached are the self-evaluation results for {name} ({position})."
    msg.attach(MIMEText(body, 'plain'))
    
    # Attach the Excel file
    attachment = open(filename, "rb")
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f"attachment; filename= {filename}")
    msg.attach(part)
    
    # Send the email
    server.sendmail("david.almazan.tsla@gmail.com", "david.almazan.tsla@gmail.com", msg.as_string())
    server.quit()

if __name__ == "__main__":
    main()
