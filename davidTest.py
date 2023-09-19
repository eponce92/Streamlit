import streamlit as st
import pandas as pd
import smtplib
import requests
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

LEVELS = ['No knowledge', 'Knows but no practice', 'Can do with help', 'Can do alone', 'Can teach others', 'Expert']
TARGETS = {
    'MX Technitian Level 1': 1,
    'MX Technitian Level 2': 2,
    'MX Technitian Level 3': 3,
    'Engineer Level 1': 3,
    'Engineer Level 2': 4,
    'Engineer Level 3': 5
}

SHOW_RESULTS = True  # Change this to False if you don't want to show the results
last_submitted_name = None  # Keep track of the last name submitted

@st.cache_data 
def get_skills():
    # Fetching the skills list from the GitHub raw URL
    url = "https://raw.githubusercontent.com/eponce92/Streamlit/main/skills_list.txt"
    response = requests.get(url)
    skills = response.text.split(",\n")
    return [skill.strip() for skill in skills]

def send_email(name, position, results_data):
    global last_submitted_name
    if name == last_submitted_name:
        st.warning("Duplicate submission detected. Email not sent.")
        return
    last_submitted_name = name
    
    msg = MIMEMultipart()
    msg['From'] = "david.almazan.tsla@gmail.com"
    msg['To'] = "david.almazan.tsla@gmail.com"
    msg['Subject'] = f"Auto-evaluation results for {name} ({position})"

    body = "Attached are the auto-evaluation results."
    msg.attach(MIMEText(body, 'plain'))

     # Save results to Excel
    filename = f"Results_{name}.xlsx"
    metadata = [['Name', name], ['Engineer Level', position]]
    df_metadata = pd.DataFrame(metadata, columns=['Key', 'Value'])
    df_results = pd.DataFrame(results_data, columns=['Skill', 'Self-Assessment', 'Difference'])

    # Save both metadata and results to the same Excel but different sheets
    with pd.ExcelWriter(filename) as writer:
        df_metadata.to_excel(writer, sheet_name='Metadata', index=False)
        df_results.to_excel(writer, sheet_name='Results', index=False)

    attachment = open(filename, "rb")
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f"attachment; filename= {filename}")
    msg.attach(part)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("david.almazan.tsla@gmail.com", "dtupyqjbdiufrwqp")
    text = msg.as_string()
    server.sendmail("david.almazan.tsla@gmail.com", "david.almazan.tsla@gmail.com", text)
    server.quit()

def main():
    st.title("Engineer Auto-Evaluation")
    
    name = st.text_input("Your Name:")
    position = st.selectbox("Your Engineer Level:", list(TARGETS.keys()))

    skills = get_skills()
    responses = {}
    
    for index, skill in enumerate(skills):
        key = f"selectbox_{index}_{skill}"
        responses[skill] = st.selectbox(f"How would you rate your {skill} skills?", LEVELS, key=key)

    if st.button("Submit"):
        results_data = []
        for skill, level in responses.items():
            difference = LEVELS.index(level) - TARGETS[position]
            results_data.append([skill, level, difference])

        send_email(name, position, results_data)

        if SHOW_RESULTS:
            results_df = pd.DataFrame(results_data, columns=['Skill', 'Self-Assessment', 'Difference'])
            st.write(results_df.to_html(index=False, classes='table table-striped table-hover'), unsafe_allow_html=True)

if __name__ == "__main__":
    main()
