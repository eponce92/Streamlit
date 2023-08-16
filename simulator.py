import streamlit as st

st.title("Graphviz Test")
dot_string = st.text_area("Enter Graphviz Dot String:")
if dot_string:
    st.graphviz_chart(dot_string)
