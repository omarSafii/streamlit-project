import pandas as pd
import streamlit as st

# جرّب تحديد الفاصل المناسب
data = pd.read_csv(r"C:\Users\1\Desktop\mo\omar.csv", delimiter=';', encoding='utf-8-sig')

st.write(data)
