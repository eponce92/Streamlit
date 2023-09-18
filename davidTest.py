import streamlit as st
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

LEVELS = ['No knowledge', 'Knows but no practice', 'Can do with help', 'Can do alone', 'Can teach others']
TARGETS = {
    'MX Technitian Level 1': 0,
    'MX Technitian Level 2': 1,
    'MX Technitian Level 3': 2,
    'Engineer Level 1': 3,
    'Engineer Level 2': 4,
    'Engineer Level 3': 5
}
TARGET_VALUES = []

SHOW_RESULTS = True
last_submitted_name = None

def get_skills_from_excel(file):
    xl = pd.ExcelFile(file)
    df = xl.parse(xl.sheet_names[0])
    skills = df.iloc[4:, 2].dropna().tolist()
    return skills

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

    msg = MIMEMultipart()
    msg['From'] = "david.almazan.tsla@gmail.com"
    msg['To'] = "david.almazan.tsla@gmail.com"
    msg['Subject'] = f"Auto-evaluation results for {name} ({position})"

    body = "Attached are the auto-evaluation results."
    msg.attach(MIMEText(body, 'plain'))

    filename = f"Results_{name}.xlsx"
    metadata = [['Name', name], ['Engineer Level', position]]
    df_metadata = pd.DataFrame(metadata, columns=['Key', 'Value'])
    df_results = pd.DataFrame(results_data, columns=['Skill', 'Self-Assessment', 'Difference'])

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

    uploaded_file = st.file_uploader("Choose an Excel file", type="xlsx")

    if uploaded_file:
        SKILLS = get_skills_from_excel(uploaded_file)
        name = st.text_input("Your Name:")
        position = st.selectbox("Your Engineer Level:", list(TARGETS.keys()))

        responses = {}
   
        for skill in SKILLS:
            responses[skill] = st.selectbox(f"How would you rate your {skill} skills?", LEVELS, key=skill)

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
