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
EXCEL_FILE_PATH = "/mnt/data/Training Matrix_Rev2.xlsx"

def get_skills_from_excel():
    # Load the excel file
    xl = pd.ExcelFile(EXCEL_FILE_PATH)
    # Extract the first sheet (assuming the data is in the first sheet)
    df = xl.parse(xl.sheet_names[0])
    # Extract skills from column C starting from C5
    skills = df.iloc[4:, 2].dropna().tolist()
    return skills

SKILLS = get_skills_from_excel()
TARGET_VALUES = []

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

    msg = MIMEMultipart()
    msg['From'] = "david.almazan.tsla@gmail.com"
    msg['To'] = "david.almazan.tsla@gmail.com"
    msg['Subject'] = f"Auto-evaluation results for {name} ({position})"

    body = "Attached are the auto-evaluation results."
    msg.attach(MIMEText(body, 'plain'))

     # Save results to Excel
    filename = f"Results_{name}.xlsx"  # Define filename here if it's not defined earlier
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

if __name__ == "__main__":
    main()
