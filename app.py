import streamlit as st
import pandas as pd
import numpy as np

#Set page title
st.title("My Streamlit App")

#Display the data
st.write("Here is our first sample data")
df=pd.DataFrame({
    "first column":[1,2,3,4],
    "second column":[10,20,30,40]
}
)
st.write(df)

st.line_chart(df)