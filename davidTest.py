import streamlit as st
from datetime import datetime, timedelta
import calendar

# Función para mostrar el calendario de entrenamiento
def display_calendar(training_dates):
    if not training_dates:
        st.write("¡Buenas noticias! No se requieren entrenamientos adicionales.")
        return
    
    current_month = training_dates[0][1].month
    current_year = training_dates[0][1].year

    cal = calendar.TextCalendar(calendar.SUNDAY)
    for training, date in training_dates:
        if date.month != current_month:
            current_month = date.month
            st.text(cal.formatmonth(current_year, current_month))
        st.write(f"{date.strftime('%Y-%m-%d')} - Entrenamiento en: {training}")

# Función para generar el calendario de entrenamiento
def generate_training_schedule(sorted_discrepancies):
    start_date = datetime.now() + timedelta(weeks=1)
    trainings = [skill for skill, discrepancy in sorted_discrepancies if discrepancy >= 1]
    
    training_dates = []
    for i, training in enumerate(trainings):
        training_date = start_date + timedelta(weeks=i*4)
        training_dates.append((training, training_date))

    return training_dates

def main():
    st.title("Autoevaluación de habilidades para ingenieros en Tesla")
    
    skills = [
        "Programacion de PLC",
        "Cognex Cameras",
        "Kistler press",
        "Mechanical troubleshooting",
        "Electrical schematics and troubleshooting",
        "Keyence vision",
        "Fanuc Programming",
        "Atlas coptco nutrunners"
    ]

    levels = [
        "No tiene conocimiento",
        "Tiene el conocimiento pero no tiene la práctica",
        "Lo puede hacer pero con ayuda",
        "Lo puede hacer solo sin ayuda",
        "Puede entrenar a otros"
    ]

    st.subheader("Completa el formulario de autoevaluación")
    engineer_name = st.text_input("Nombre del ingeniero", "")
    engineer_level = st.selectbox("Nivel del ingeniero", ["Ingeniero Asociado", "Ingeniero", "Ingeniero Senior"])
    
    evaluations = {}
    for skill in skills:
        evaluations[skill] = st.selectbox(f"Evalúa tu habilidad en: {skill}", options=levels, index=0)

    if st.button("Enviar autoevaluación"):
        discrepancies = {}
        
        # Establecer el nivel objetivo basado en el nivel del ingeniero
        target_level = 2 if engineer_level == "Ingeniero Asociado" else 3 if engineer_level == "Ingeniero" else 4

        for skill, level in evaluations.items():
            skill_discrepancy = target_level - levels.index(level)
            discrepancies[skill] = skill_discrepancy

        sorted_discrepancies = sorted(discrepancies.items(), key=lambda x: x[1], reverse=True)
        
        st.subheader(f"Resultados de autoevaluación de {engineer_name} ({engineer_level}):")
        for skill, discrepancy in sorted_discrepancies:
            st.write(f"{skill}: {evaluations[skill]} (Diferencia: {discrepancy})")
        
        training_dates = generate_training_schedule(sorted_discrepancies)
        st.subheader("Calendario de entrenamiento:")
        display_calendar(training_dates)

if __name__ == "__main__":
    main()
