import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

with st.form(key="my_form"):
    name = st.text_input("Enter your name")
    age = st.number_input("Enter your age")
    st.form_submit_button()

    
        








chart_data = pd.DataFrame(
    np.random.randn(30, 3),
    columns=['a', 'b', 'c']
)

st.subheader('A line chart')
st.line_chart(chart_data)

st.subheader('A bar chart')
st.bar_chart(chart_data)


st.subheader('Map')
map_data = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    columns=['lat', 'lon']
)
st.map(map_data)




















st.image(os.path.join(os.getcwd(),"static","night.jpg"),width=500)



