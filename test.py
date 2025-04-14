import streamlit as st
import sqlite3
import pandas as pd
import os

# تحديد المسار الكامل لقاعدة البيانات
DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "new_quran_institute.db"))

# دالة لإحضار أسماء الجداول الموجودة
def get_table_names():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [table[0] for table in cursor.fetchall()]
    conn.close()
    return tables

# دالة لجلب البيانات من جدول معين
def get_table_data(table_name):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(f"SELECT * FROM '{table_name}'", conn)
    conn.close()
    return df

# =================== Streamlit ===================
st.title("📊 عرض بيانات قاعدة التحفيظ")

# الحصول على أسماء جميع الجداول
tables = get_table_names()

# عرض الجداول
for table_name in tables:
    st.subheader(f"📁 جدول: {table_name}")
    try:
        df = get_table_data(table_name)
        if not df.empty:
            st.dataframe(df, use_container_width=True)
        else:
            st.info("لا توجد بيانات في هذا الجدول.")
    except Exception as e:
        st.error(f"حدث خطأ أثناء تحميل الجدول {table_name}: {e}")
