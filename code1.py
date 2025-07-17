import streamlit as st
import pandas as pd
import numpy as np

# ---- App Title and Description ---
st.title("my First streamlit App created by SINDHU")
st.write("This is a simple app to demonstrate the basic functionalities of Streamlit.")

# --Interactive widgets in the sidebar --
st.sidebar.header("User Input Features")

# Text Input
user_name = st.sidebar.text_input("What is your name?", "Streamlit User")

#Slider
age = st.sidebar.slider("Select your age", 0,100,25)

# Selectbox
favorite_color = st.sidebar.selectbox("what is your favorite color?", ["Blue", "Red", "Green", "Yellow"])

# -- Main page content --
st.header(f"Welcome, {user_name}!")
st.write(f"you are {age} years old and your favorite color if {favorite_color}.")

# -- Displaying Data --
st.subheader("Here's some random data:")

# Create a sample Dataframe
data = pd.DataFrame(
    np.random.randn(10, 5),
    columns=('col %d' % i for i in range(5))
)

st.dataframe(data)

#--- Checkbox to show/hide content ---
if st.checkbox("Show raw data"):
    st.subheader("Raw Data")
    st.write(data)

# --- Button to trigger an action ---
if st.button("Say hello"):
    st.write("Hello there!")
else:
    st.write("Goodbye")