import sqlite3
import pandas as pd
import streamlit as st

# تحميل البيانات من ملف Excel
df = pd.read_excel(r"C:\Users\1\Desktop\mo\data1.xlsx")

# إعادة تسمية واستخراج الأعمدة
df = df[['اسم الطالب الثلاثي','تاريخ الميلاد','مستوى الحفظ(في اي جزء)','رقم والدة الطالب','رقم الطالب(ان وجد)']]
df.columns = ['name','birth_date','previous_memorization','parent_phone','phone']
df['birth_date'] = pd.to_datetime(df['birth_date'], errors='coerce').dt.strftime('%Y-%m-%d')

# اتصال بقاعدة البيانات
conn = sqlite3.connect('new_quran_institute.db')
cursor = conn.cursor()

# تأكد من وجود الأعمدة (مرة واحدة)
for col in ['parent_phone','phone']:
    try:
        cursor.execute(f"ALTER TABLE students ADD COLUMN {col} TEXT")
    except sqlite3.OperationalError:
        pass

# 1️⃣ مسح كل البيانات القديمة
cursor.execute("DELETE FROM students")

# 2️⃣ إدخال البيانات الجديدة
for _, row in df.iterrows():
    cursor.execute('''
        INSERT INTO students (name, birth_date, previous_memorization, parent_phone, phone)
        VALUES (?, ?, ?, ?, ?)
    ''', (row['name'], row['birth_date'], row['previous_memorization'], row['parent_phone'], row['phone']))

conn.commit()

# عرض البيانات في Streamlit
st.title("📚 جدول الطلاب")
df_db = pd.read_sql_query("SELECT * FROM students", conn)
st.dataframe(df_db)

conn.close()
