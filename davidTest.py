import streamlit as st
from datetime import date, timedelta

SKILLS = [
    "Programacion de PLC",
    "Cognex Cameras",
    "Kistler press",
    "Mechanical troubleshooting",
    "Electrical schematics and troubleshooting",
    "Keyence vision",
    "Fanuc Programming",
    "Atlas coptco nutrunners"
]

LEVELS = {
    0: "No tiene conocimiento",
    1: "Tiene el conocimiento pero no tiene la práctica",
    2: "Lo puede hacer pero con ayuda",
    3: "Lo puede hacer solo sin ayuda",
    4: "Puede entrenar a otros"
}

TARGETS = {
    "ingeniero asociado": 2,
    "ingeniero": 3,
    "ingeniero senior": 4
}

def main():
    st.title("Autoevaluación de Habilidades para Ingenieros en Tesla")
    st.write("Por favor, llena el siguiente formulario:")

    name = st.text_input("Nombre:")
    position = st.selectbox("Posición:", list(TARGETS.keys()))

    responses = {}
    for skill in SKILLS:
        responses[skill] = st.selectbox(f"{skill}:", list(LEVELS.values()))

    if st.button("Enviar"):
        differences = calculate_differences(responses, position)
        st.write(f"Resultados de autoevaluación de {name} ({position}):")
        
        for skill, level in responses.items():
            difference = list(LEVELS.values()).index(level) - TARGETS[position]
            st.write(f"{skill}: {level} (Diferencia: {difference})")
        
        training_dates = generate_training_schedule(differences)
        
        st.write("Calendario de entrenamientos:")
        if training_dates:
            for topic, training_date in training_dates:
                st.date_input(f"Entrenamiento para {topic}:", value=training_date, disabled=True)
        else:
            st.write("No se requiere entrenamiento adicional.")

def calculate_differences(responses, position):
    differences = {}
    for skill, level in responses.items():
        differences[skill] = list(LEVELS.values()).index(level) - TARGETS[position]
    return differences

def generate_training_schedule(differences):
    topics_with_diff_below_neg_one = [topic for topic, diff in differences.items() if diff <= -1]
    training_dates = []

    current_date = date.today() + timedelta(days=7)
    for topic in topics_with_diff_below_neg_one:
        training_dates.append((topic, current_date))
        current_date += timedelta(weeks=4)  # Agrega 4 semanas para el siguiente entrenamiento

    return training_dates

if __name__ == "__main__":
    main()
