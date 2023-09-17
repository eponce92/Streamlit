import streamlit as st

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
                st.write(f"{skill}: {levels[rating]} (Diferencia: {discrepancy})")
        else:
            st.warning("Por favor, ingresa tu nombre.")

if __name__ == "__main__":
    main()
