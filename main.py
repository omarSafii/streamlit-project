import streamlit as st
import pandas as pd
import numpy as np
import os
import sqlite3
st.set_page_config(
    page_title="معهد قباء",
    page_icon="📖",
    layout="wide"
)

# إعداد CSS
# إعداد CSS
st.markdown("""
<style>
/* الشريط العلوي */
.header {
    background-color: #4CAF50;
    padding: 10px;
    border-radius: 5px;
    text-align: center;
    color: white;
    font-size: 28px;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    position: relative;
}
/* زر الدخول */
.login-button {
    position: absolute;
    top: 10px;
    right: 20px;
    background-color: #f44336;
    border: none;
    color: white;
    padding: 8px 16px;
    font-size: 16px;
    border-radius: 4px;
    cursor: pointer;
}
.login-button:hover {
    background-color: #d32f2f;
}

/* تأثير Parallax لصورة الغلاف */
.parallax {
    background-image: url("static/qubaa.jpg");
    min-height: 500px; 
    background-attachment: fixed;
    background-position: center;
    background-repeat: no-repeat;
    background-size: cover;
}
</style>
""", unsafe_allow_html=True)

# عرض الصورة من مجلد static
if os.path.exists("static/qubaa.jpg"):
    st.image("static/qubaa.jpg", use_column_width=True)
else:
    st.error("❌ ملف الصورة 'qubaa.jpg' غير موجود.")
# Tabs رئيسية
tab1, tab2 = st.tabs(["الرئيسية", "عرض الجداول"])

########################################### TAB(1) #####################################################
with tab1:
    # الشريط العلوي
    st.markdown("""
    <div class="header">
        <span>معهد قباء</span>
        <button class="login-button" onclick="alert('تم الضغط على زر تسجيل الدخول/الخروج');">دخول/خروج</button>
    </div>
    """, unsafe_allow_html=True)

    # صورة الغلاف بتأثير Scroll Parallax
    st.markdown('<div class="parallax"></div>', unsafe_allow_html=True)

    # محتوى الصفحة
    st.title("📖 معهد قباء")
    st.write("مرحباً بك في منصة معهد قباء الإلكترونية.")

    with st.form(key="my_form"):
        name = st.text_input("الاسم")
        age = st.number_input("العمر", min_value=0)
        st.form_submit_button("إرسال")

    # مكونات إضافية
    st.button("اضغط هنا")
    st.slider("اختر القيمة", 0, 100, 25)

    # الرسوم البيانية
    data = pd.DataFrame(np.random.randn(30, 3), columns=["a", "b", "c"])
    st.subheader("📈 رسم بياني خطي")
    st.line_chart(data)

    st.subheader("📊 رسم بياني عمودي")
    st.bar_chart(data)

    st.subheader("🗺️ خريطة")
    map_data = pd.DataFrame(
        np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
        columns=["lat", "lon"]
    )
    st.map(map_data)

########################################### TAB(2) #####################################################
with tab2:
    st.title("📊 عرض جداول قاعدة البيانات")

    db_path = "new_quran_institute.db"
    if os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [table[0] for table in cursor.fetchall()]

        if not tables:
            st.error("❌ لا توجد جداول.")
        else:
            table_tabs = st.tabs(tables)
            for i, table in enumerate(tables):
                with table_tabs[i]:
                    st.subheader(f"📋 جدول: {table}")
                    try:
                        df = pd.read_sql_query(f"SELECT * FROM {table}", conn)
                        st.dataframe(df.style.set_properties(**{
                            'background-color': 'lightblue',
                            'color': 'black'
                        }).set_table_styles([{
                            'selector': 'th',
                            'props': [('background-color', 'darkblue'), ('color', 'white')]
                        }]))
                    except Exception as e:
                        st.error(f"خطأ في الجدول {table}: {e}")
        conn.close()
    else:
        st.error("❌ ملف قاعدة البيانات غير موجود.")
