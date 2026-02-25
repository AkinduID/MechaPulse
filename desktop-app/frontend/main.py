import streamlit as st

st.set_page_config(page_title="MechaPulse ML App", layout="wide")

st.title("MechaPulse Machine Learning Platform")
st.sidebar.title("Navigation")

st.sidebar.info("Select a page to get started.")

# Streamlit's multipage support will automatically show pages in the 'pages' folder.
st.write("Use the sidebar to navigate to Train, Test, Validate, or Predict.")
