# Import necessary libraries
import streamlit as st

def calculate_tax(items):
    """Calculate the subtotal, tax, and total for the provided shopping cart items."""
    subtotal = sum(item['price'] for item in items)
    tax = 0.15 * subtotal
    total = subtotal + tax
    return subtotal, tax, total

# Define the Streamlit app
def main():
    st.title("Shopping Cart Tax Calculator")

    # Number of items in the cart
    n_items = st.number_input("How many items are in your cart?", min_value=1, max_value=10, value=1, step=1)
    cart_items = []

    for i in range(n_items):
        st.subheader(f"Item {i + 1}")
        description = st.text_input(f"Description of item {i + 1}", "")
        price = st.number_input(f"Price of item {i + 1} ($)", min_value=0.01, value=0.01, step=0.01)
        cart_items.append({"description": description, "price": price})

    if st.button("Calculate"):
        subtotal, tax, total = calculate_tax(cart_items)
        st.write(f"Subtotal: ${subtotal:.2f}")
        st.write(f"Tax (15%): ${tax:.2f}")
        st.write(f"Total: ${total:.2f}")

if __name__ == "__main__":
    main()

