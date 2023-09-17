import streamlit as st
from datetime import datetime, timedelta
import calendar

# Definición de skills y niveles
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

levels = {
    0: "No tiene conocimiento",
    1: "Tiene el conocimiento pero no tiene la práctica",
    2: "Lo puede hacer pero con ayuda",
    3: "Lo puede hacer solo sin ayuda",
    4: "Puede entrenar a otros"
}

targets = {
    "ingeniero asociado": 2,
    "ingeniero": 3,
    "ingeniero senior": 4
}

def generate_training_schedule(sorted_discrepancies):
    start_date = datetime.now() + timedelta(weeks=1)
    
    # Aquí debemos filtrar las habilidades con discrepancia >= 1, no sólo las que son exactamente 1.
    trainings = [skill for skill, discrepancy in sorted_discrepancies if discrepancy >= 1]
    
    training_dates = []
    for i, training in enumerate(trainings):
        training_date = start_date + timedelta(weeks=i*4)  # Sumamos 4 semanas para cada siguiente entrenamiento
        training_dates.append((training, training_date))

    return training_dates


def display_calendar(training_dates):
    current_month = training_dates[0][1].month
    current_year = training_dates[0][1].year

    cal = calendar.TextCalendar(calendar.SUNDAY)
    for training, date in training_dates:
        if date.month != current_month:
            current_month = date.month
            st.text(cal.formatmonth(current_year, current_month))
        st.write(f"{date.strftime('%Y-%m-%d')} - Entrenamiento en: {training}")

def main():
    st.title('Autoevaluación para Ingenieros de Tesla')
    st.write("Por favor, rellena el formulario a continuación:")

    # Capturar datos del formulario
    name = st.text_input("Nombre:")
    position = st.selectbox("Selecciona tu posición:", list(targets.keys()))
    user_ratings = {}
    for skill in skills:
        rating = st.selectbox(f"Califica tu habilidad en {skill}", list(levels.keys()), format_func=lambda x: levels[x])
        user_ratings[skill] = rating

    if st.button("Enviar"):
        if name:
            # Procesar los resultados
            discrepancies = {}
            for skill, rating in user_ratings.items():
                discrepancy = rating - targets[position]
                discrepancies[skill] = discrepancy

            # Ordenar por criticidad
            sorted_discrepancies = sorted(discrepancies.items(), key=lambda x: x[1], reverse=True)

            # Mostrar resultados
            st.subheader(f"Resultados de autoevaluación de {name} ({position}):")
            for skill, discrepancy in sorted_discrepancies:
                st.write(f"{skill}: {levels[user_ratings[skill]]} (Diferencia: {discrepancy})")

            # Generar el calendario de entrenamiento
            training_dates = generate_training_schedule(sorted_discrepancies)
            display_calendar(training_dates)
            
        else:
            st.warning("Por favor, ingresa tu nombre.")

if __name__ == "__main__":
    main()
