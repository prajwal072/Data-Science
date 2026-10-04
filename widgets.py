import streamlit as st
import pandas as pd
import numpy as np

st.title("streamlit text input widget")
name=st.text_input("Enter your name","Type Here...")
age=st.slider("Enter your age",1,100,25)
options=["javascript","python","c++","java"]
choice=st.selectbox("Select your favourite programming language",options)
st.write("your choice is",choice)

if name:
    st.write(f"Hello {name}!")
file_uploaded=st.file_uploader("Upload a file",type="csv")
if file_uploaded is not None:
    data=pd.read_csv(file_uploaded)
    st.write(data)