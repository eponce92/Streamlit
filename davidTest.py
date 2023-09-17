import streamlit as st
from datetime import datetime, timedelta
from st_aggrid import AgGrid

def display_calendar(training_dates):
    if not training_dates:
        st.write("¡Buenas noticias! No se requieren entrenamientos adicionales.")
        return

    grid_data = [{
        'Fecha': date.strftime('%Y-%m-%d'),
        'Entrenamiento en': training
    } for training, date in training_dates]

    layout = {
        'defaultColDef': {
            'flex': 1,
            'minWidth': 150,
            'sortable': True,
            'resizable': True
        }
    }

    AgGrid(grid_data, gridOptions=layout, height=280, fit_columns_on_grid_load=True)

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

    # ... [resto del código sin cambios] ...

    st.subheader("Calendario de entrenamiento:")
    display_calendar(training_dates)

if __name__ == "__main__":
    main()
