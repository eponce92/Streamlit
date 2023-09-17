import streamlit as st
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

LEVELS = ['No knowledge', 'Knows but no practice', 'Can do with help', 'Can do alone', 'Can teach others']
TARGETS = {
    'Associate Engineer': 0,
    'Engineer': 1,
    'Senior Engineer': 2,
    'Staff Engineer': 3,
    'Senior Staff Engineer': 4
}

SHOW_RESULTS = True  # Change this to False if you don't want to show the results
last_submitted_name = None  # Keep track of the last name submitted

@st.cache
def get_skills():
    return [
        'PLC Programming',
        'Cognex Cameras',
        'Kistler press',
        'Mechanical troubleshooting',
        'Electrical schematics and troubleshooting',
        'Keyence vision',
        'Fanuc Programming',
        'Atlas coptco nutrunners'
    ]

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
    df = pd.DataFrame(results_data, columns=['Skill', 'Self-Assessment', 'Difference'])
    filename = f"Results_{name}.xlsx"
    df.to_excel(filename, index=False)

    attachment = open(filename, "rb")
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f"attachment; filename= {filename}")
    msg.attach(part)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("david.almazan.tsla@gmail.com", "dtupyqjbdiufrwqp")  # Use the app password here
    text = msg.as_string()
    server.sendmail("david.almazan.tsla@gmail.com", "david.almazan.tsla@gmail.com", text)
    server.quit()

def main():
    st.title("Engineer Auto-Evaluation")
    
    name = st.text_input("Your Name:")
    position = st.selectbox("Your Engineer Level:", list(TARGETS.keys()))

    skills = get_skills()
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

if __name__ == "__main__":
    main()
