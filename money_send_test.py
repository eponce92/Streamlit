# Importar las bibliotecas necesarias
import streamlit as st

def calculate_tax(items):
    """Calculate the subtotal, tax, and total for the provided shopping cart items."""
    subtotal = sum(item['price'] for item in items)
    tax = 0.15 * subtotal
    total = subtotal + tax
    return subtotal, tax, total

# Define la aplicación Streamlit
def main():
    st.title("Calculadora de Impuestos para el Carrito de Compras")

    # Crear dos columnas: col1 para los inputs y col2 para los resultados
    col1, col2 = st.beta_columns(2)

    with col1:
        # Número de artículos en el carrito
        n_items = st.number_input("¿Cuántos artículos hay en tu carrito?", min_value=1, max_value=10, value=1, step=1)
        cart_items = []

        for i in range(n_items):
            st.subheader(f"Artículo {i + 1}")
            description = st.text_input(f"Descripción del artículo {i + 1}", "")
            price = st.number_input(f"Precio del artículo {i + 1} ($)", min_value=0.01, value=0.01, step=0.01)
            cart_items.append({"description": description, "price": price})

    if st.button("Calcular"):
        subtotal, tax, total = calculate_tax(cart_items)
        with col2:
            st.write(f"Subtotal: ${subtotal:.2f}")
            st.write(f"Impuesto (15%): ${tax:.2f}")
            st.write(f"Total: ${total:.2f}")
    else:
        with col2:
            st.write("Tus resultados aparecerán aquí.")

if __name__ == "__main__":
    main()
