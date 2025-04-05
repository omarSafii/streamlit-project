import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import sqlite3

# ------ التنقل عبر الصفحات ------
page = st.sidebar.selectbox("اختر الصفحة", ["الرئيسية", "عرض الجداول"])

# ------ الصفحة الرئيسية ------
if page == "الرئيسية":
    st.title("📖 منصة معهد التحفيظ")
    st.write("مرحباً بك في الصفحة الرئيسية للتطبيق.")
    
    # محتوى الصفحة الرئيسية فقط يظهر هنا
    with st.form(key="my_form"):
        name = st.text_input("Enter your name")
        age = st.number_input("Enter your age")
        st.form_submit_button()

    st.sidebar.header("Options")
    st.sidebar.selectbox("Select a page", ["Home", "About", "Contact"])
    
    tab1, tab2, tab3 = st.tabs(["Tab 1", "Tab 2", "Tab 3"])
    with tab1:
        st.write("This is the content of tab 1.")
    with tab2:
        st.write("This is the content of tab 2.")
    with tab3:
        st.write("This is the content of tab 3.")

    with st.container(border=True):
        st.write("This is a container with a border.")
        with st.expander("Expand me"):
            st.write("This is a container with an expander.")

    st.write("This is a container with a border.")
    st.button("Click me", help="This is a button")
    st.slider('Select a value', min_value=0, max_value=100, value=25)

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

    st.image(os.path.join(os.getcwd(), "static", "night.jpg"), width=500)

# ------ صفحة عرض الجداول ------
elif page == "عرض الجداول":
    st.title("📊 عرض جميع جداول قاعدة البيانات")

    # الاتصال بقاعدة البيانات
    conn = sqlite3.connect("quran_institute.db")
    cursor = conn.cursor()

    # جلب أسماء الجداول
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [table[0] for table in cursor.fetchall()]

    # إنشاء التبويبات لكل جدول
    tabs = st.tabs(tables)

    for i, table in enumerate(tables):
        with tabs[i]:
            st.subheader(f"📋 محتوى جدول: {table}")
            try:
                df = pd.read_sql_query(f"SELECT * FROM {table}", conn)
                st.dataframe(df)
            except Exception as e:
                st.error(f"❌ خطأ في عرض الجدول {table}: {e}")

    conn.close()
