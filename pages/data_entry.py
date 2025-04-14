import sqlite3
import os
import pandas as pd
import streamlit as st

# ---------- دالة اكتشاف التغييرات ----------
def detect_changes(original_df, edited_df, pk):
    orig = original_df.set_index(pk)
    edit = edited_df.set_index(pk)

    deleted = orig.loc[~orig.index.isin(edit.index)].reset_index()
    added = edit.loc[~edit.index.isin(orig.index)].reset_index()

    common = orig.index.intersection(edit.index)
    modified_mask = (edit.loc[common] != orig.loc[common]).any(axis=1)
    modified = edit.loc[common][modified_mask].reset_index()

    return added, deleted, modified

# ---------------------- الكود الرئيسي ----------------------
DB_FILE = "new_quran_institute.db"

if not os.path.exists(DB_FILE):
    st.error("لم يتم العثور على قاعدة البيانات! تأكد من تشغيل create_database.py أولاً")
    st.stop()

with sqlite3.connect(DB_FILE) as conn:
    tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table';", conn)['name'].tolist()

selected_table = st.selectbox(
    "اختر جدول:", tables,
    format_func=lambda x: {
        "الحلقات": "حلقات التحفيظ",
        "الطلاب": "بيانات الطلاب",
        "الاساتذة": "هيئة التدريس",
        "الخطط": "خطط التحفيظ",
        "النقاط": "نقاط التقييم",
        "نقاط_الضعف": "نقاط الضعف",
        "الحضور": "سجلات الحضور"
    }.get(x, x)
)

# جلب البيانات الأصلية
with sqlite3.connect(DB_FILE) as conn:
    df_original = pd.read_sql(f"SELECT * FROM [{selected_table}]", conn)

# تكوين الأعمدة القابل للتعديل
column_config = {}
if selected_table == "الطلاب":
    # مثال: حلقة باستخدام اسم الحلقة ثم سنحول لاحقاً للأرقام
    sessions = pd.read_sql("SELECT رقم_الحلقة, اسم_الحلقة FROM الحلقات", conn)
    session_map = dict(zip(sessions["اسم_الحلقة"], sessions["رقم_الحلقة"]))

    column_config = {
        "رقم_الطالب": st.column_config.NumberColumn("المعرف", disabled=True),
        "اسم_الطالب": st.column_config.TextColumn("الاسم", width="large"),
        "رقم_الحلقة": st.column_config.SelectboxColumn(
            "الحلقة", options=sessions["اسم_الحلقة"].tolist()
        ),
        "الحفظ_السابق": st.column_config.TextColumn("الحفظ السابق"),
        "تاريخ_الانضمام": st.column_config.DateColumn("تاريخ الانضمام"),
        "العمر": st.column_config.NumberColumn("العمر"),
        "هاتف_الطالب": st.column_config.TextColumn("هاتف الطالب"),
    }
elif selected_table == "الاساتذة":
    column_config = {
        "رقم_الاستاذ": st.column_config.NumberColumn("المعرف", disabled=True),
        "اسم_الاستاذ": st.column_config.TextColumn("الاسم"),
        "المؤهلات_الشرعية": st.column_config.TextColumn("المؤهلات الشرعية"),
        "مستوى_التفرغ": st.column_config.SelectboxColumn(
            "مستوى التفرغ", options=["كامل", "جزئي", "مؤقت"]
        )
    }

# عرض المحرر
edited_df = st.data_editor(
    df_original,
    column_config=column_config,
    hide_index=True,
    num_rows="dynamic",
    use_container_width=True,
    key=f"{selected_table}_editor"
)

# زر الحفظ
if st.button("حفظ التعديلات", key=f"save_{selected_table}"):
    if selected_table == "الطلاب":
        # حفظ آمن باستخدام INSERT/UPDATE/DELETE
        added, deleted, modified = detect_changes(df_original, edited_df, pk="رقم_الطالب")

        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()

            # حذف
            for _, row in deleted.iterrows():
                cursor.execute("DELETE FROM الطلاب WHERE رقم_الطالب = ?", (row["رقم_الطالب"],))

            # إضافة
            for _, row in added.iterrows():
                cols = [c for c in row.index if c != "رقم_الطالب"]
                vals = []
                for c in cols:
                    if c == "رقم_الحلقة":
                        vals.append(session_map[row[c]])
                    else:
                        vals.append(row[c])
                placeholders = ", ".join("?" for _ in cols)
                cursor.execute(
                    f"INSERT INTO الطلاب ({', '.join(cols)}) VALUES ({placeholders})",
                    vals
                )

            # تعديل
            for _, row in modified.iterrows():
                cols = [c for c in row.index if c != "رقم_الطالب"]
                set_clause = ", ".join(f"{c} = ?" for c in cols)
                vals = []
                for c in cols:
                    if c == "رقم_الحلقة":
                        vals.append(session_map[row[c]])
                    else:
                        vals.append(row[c])
                vals.append(row["رقم_الطالب"])
                cursor.execute(
                    f"UPDATE الطلاب SET {set_clause} WHERE رقم_الطالب = ?",
                    vals
                )

            conn.commit()

        st.success(f"✅ تمت معالجة التغييرات: +{len(added)} إضافة, -{len(deleted)} حذف, ✎{len(modified)} تعديل.")
    else:
        # السلوك الافتراضي: استبدال الجدول بالكامل
        with sqlite3.connect(DB_FILE) as conn:
            edited_df.to_sql(selected_table, conn, if_exists='replace', index=False)
        st.success("✅ تم حفظ التعديلات بنجاح (استبدال كامل الجدول).")
