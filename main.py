import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime
import os
# ---------------------------- الإعدادات الأساسية ----------------------------
st.set_page_config(
    page_title="معهد قباء",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------- CSS مخصص مع تحسينات ----------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&display=swap');

body {
    font-family: 'Amiri', serif !important;
    background-color: #f0f8ff;
}

.header {
    background: linear-gradient(45deg, #1a4d2e, #2d6a4f);
    padding: 2rem;
    border-radius: 15px;
    text-align: center;
    box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    color: white;
    font-size: 2.5rem;
    margin-bottom: 2rem;
    position: relative;
}

.login-btn {
    position: absolute;
    top: 50%;
    right: 2rem;
    transform: translateY(-50%);
    background: #9b2226 !important;
    color: white !important;
    border: none;
    padding: 1rem 2rem;
    border-radius: 30px;
    font-size: 1.2rem;
    transition: all 0.3s;
    box-shadow: 0 3px 6px rgba(0,0,0,0.2);
}

.login-btn:hover {
    background: #7f1d1d !important;
    transform: translateY(-50%) scale(1.05);
}

.stForm {
    background: #fff;
    border-radius: 15px;
    padding: 2rem;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    border: 1px solid #e0e0e0;
}

.stButton > button {
    border-radius: 10px !important;
    padding: 0.8rem 1.5rem !important;
    background: #1a5d2e !important;
    color: white !important;
    font-weight: bold !important;
    transition: transform 0.2s !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 3px 6px rgba(0,0,0,0.2) !important;
}

.data-table {
    background: #fff;
    border-radius: 15px;
    padding: 1.5rem;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    border: 1px solid #e0e0e0;
}

.metric-card {
    background: #fff;
    border-radius: 15px;
    padding: 1.5rem;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    border-left: 5px solid #1a5d2e;
    transition: transform 0.2s;
}

.metric-card:hover {
    transform: translateY(-2px);
}
</style>
""", unsafe_allow_html=True)

# ---------------------------- الهيكل الرئيسي مع تحسينات ----------------------------
# الهيدر مع زر الدخول
st.markdown("""
<div class="header">
    معهد قباء لتحفيظ القرآن الكريم
    <button class="login-btn" onclick="alert('قيد التطوير')">دخول النظام</button>
</div>
""", unsafe_allow_html=True)

# تبويبات الصفحة مع تحسينات التصميم
main_tab, data_tab, reports_tab = st.tabs([
    "الرئيسية 🕌",
    "إدارة البيانات 📊",
    "التقارير 📈"
])

# ---------------------------- صفحة الرئيسية ----------------------------
with main_tab:
    # قسم الصورة الرئيسية مع تأثيرات
    img_col, text_col = st.columns([3, 4])
    with img_col:
        st.image("static/qubaa.jpg", use_column_width=True, caption="مبنى المعهد الرئيسي")
    
    with text_col:
        st.markdown("""
        ## 🌟 نبذة عن المعهد
        معهد قباء مؤسسة تعليمية متخصصة في:
        - تحفيظ القرآن الكريم بالقراءات العشر
        - تعليم العلوم الشرعية والتفسير
        - دورات التجويد والتلاوة
        - برامج الإجازات القرآنية
        
        **الرؤية:** تخريج حفظة متقنين لكتاب الله مع فهم عميق لأحكامه
        """)
    
    # نموذج التسجيل المحسن
    with st.expander("📝 تسجيل طالب جديد", expanded=True):
        with st.form("student_registration"):
            col1, col2 = st.columns(2)
            
            # تحميل الحلقات من قاعدة البيانات
            with sqlite3.connect("new_quran_institute.db") as conn:
                df_sessions = pd.read_sql("SELECT رقم_الحلقة, اسم_الحلقة FROM الحلقات", conn)
            
            with col1:
                student_name = st.text_input("اسم الطالب الكامل", placeholder="أدخل الاسم الثلاثي")
                student_age = st.number_input("العمر", min_value=5, max_value=60, step=1)
                session_choice = st.selectbox("اختر الحلقة", df_sessions["اسم_الحلقة"], index=None)
                
            with col2:
                previous_hifz = st.text_input("الحفظ السابق", placeholder="مثال: ختم 3 أجزاء")
                enrollment_date = st.date_input("تاريخ الانضمام", datetime.today())
                student_phone = st.text_input("هاتف الطالب", placeholder="05XXXXXXXX")
                
            submitted = st.form_submit_button("تسجيل الطالب", type="primary")
            
            if submitted:
                if not student_name or not session_choice:
                    st.error("الرجاء إدخال الاسم واختيار الحلقة")
                else:
                    try:
                        session_id = df_sessions[df_sessions["اسم_الحلقة"] == session_choice]["رقم_الحلقة"].values[0]
                        with sqlite3.connect("new_quran_institute.db") as conn:
                            conn.execute("""
                                INSERT INTO الطلاب 
                                (اسم_الطالب, رقم_الحلقة, الحفظ_السابق, تاريخ_الانضمام, العمر, هاتف_الطالب)
                                VALUES (?, ?, ?, ?, ?, ?)
                            """, (student_name, session_id, previous_hifz, enrollment_date, student_age, student_phone))
                        st.success("تم تسجيل الطالب بنجاح ✅")
                    except Exception as e:
                        st.error(f"حدث خطأ: {str(e)}")

    # أقسام إحصائية مطورة
    st.markdown("---")
    st.subheader("📊 مؤشرات الأداء")
    
    metric_cols = st.columns(4)
    metrics = [
        {"title": "الطلاب المسجلين", "value": "250", "delta": "+15 هذا الشهر"},
        {"title": "المعدل العام", "value": "87%", "delta": "▲ 4% عن العام الماضي"},
        {"title": "الحضور اليومي", "value": "180 طالب", "delta": "▼ 2% عن الأسبوع الماضي"},
        {"title": "الاختبارات الناجحة", "value": "120 امتحان", "delta": "تطور 92%"}
    ]
    
    for i, metric in enumerate(metrics):
        with metric_cols[i%4]:
            st.markdown(f"""
            <div class="metric-card">
                <h4>{metric['title']}</h4>
                <h2 style="color: #1a5d2e;">{metric['value']}</h2>
                <p style="color: {'#16a34a' if '▲' in metric['delta'] else '#dc2626'};">
                    {metric['delta']}
                </p>
            </div>
            """, unsafe_allow_html=True)

    # رسم بياني تفاعلي محسن
    st.markdown("---")
    st.subheader("📈 توزيع الطلاب حسب الحلقات")
    
    with sqlite3.connect("new_quran_institute.db") as conn:
        df = pd.read_sql("""
            SELECT الحلقات.اسم_الحلقة, COUNT(الطلاب.رقم_الطالب) AS عدد_الطلاب
            FROM الحلقات
            LEFT JOIN الطلاب ON الحلقات.رقم_الحلقة = الطلاب.رقم_الحلقة
            GROUP BY الحلقات.رقم_الحلقة
        """, conn)
    
    if not df.empty:
        st.bar_chart(df.set_index("اسم_الحلقة"))
    else:
        st.warning("لا توجد بيانات متاحة")

# ---------------------------- صفحة إدارة البيانات ----------------------------
with data_tab:
    st.subheader("📦 استكشاف وتعديل البيانات")
    
    if os.path.exists("new_quran_institute.db"):
        with sqlite3.connect("new_quran_institute.db") as conn:
            tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table';", conn)['name'].tolist()
            
            # تحسين واجهة عرض الجداول
            selected_table = st.selectbox("اختر جدول:", tables, 
                                         format_func=lambda x: {
                                             "الحلقات": "حلقات التحفيظ",
                                             "الطلاب": " بيانات الطلاب",
                                             "الاساتذة": "هيئة التدريس",
                                             "الخطط": "خطط التحفيظ",
                                             "النقاط": " نقاط التقييم",
                                             "نقاط_الضعف": " نقاط الضعف",
                                             "الحضور": "سجلات الحضور"
                                         }.get(x, x))
            
            if selected_table:
                # تكوين خاص لكل جدول
                column_config = {}
                if selected_table == "الطلاب":
                    column_config = {
                        "رقم_الطالب": st.column_config.NumberColumn("المعرف", format="%d"),
                        "رقم_الحلقة": st.column_config.SelectboxColumn(
                            "الحلقة",
                            help="الحلقة التي ينتمي إليها الطالب",
                            options=pd.read_sql("SELECT رقم_الحلقة, اسم_الحلقة FROM الحلقات", conn)["اسم_الحلقة"].tolist(),
                            required=True
                        ),
                        "اسم_الطالب": st.column_config.TextColumn("الاسم", width="large"),
                        "الحفظ_السابق": st.column_config.TextColumn("الحفظ السابق"),
                        "تاريخ_الانضمام": st.column_config.DateColumn("تاريخ الانضمام"),
                        "هاتف_الطالب": st.column_config.TextColumn("هاتف الطالب")
                    }
                
                elif selected_table == "الاساتذة":
                    column_config = {
                        "رقم_الاستاذ": st.column_config.NumberColumn("المعرف"),
                        "اسم_الاستاذ": st.column_config.TextColumn("الاسم"),
                        "المؤهلات_الشرعية": st.column_config.TextColumn("المؤهلات الشرعية"),
                        "مستوى_التفرغ": st.column_config.SelectboxColumn(
                            "مستوى التفرغ",
                            options=["كامل", "جزئي", "مؤقت"]
                        )
                    }
                
                df = pd.read_sql(f"SELECT * FROM {selected_table}", conn)
                
                edited_df = st.data_editor(
                    df,
                    column_config=column_config,
                    hide_index=True,
                    num_rows="dynamic",
                    use_container_width=True,
                    key=f"{selected_table}_editor"
                )
                
                # زر حفظ التعديلات
                if st.button("حفظ التعديلات", key=f"save_{selected_table}"):
                    try:
                        edited_df.to_sql(selected_table, conn, if_exists='replace', index=False)
                        st.success("تم حفظ التعديلات بنجاح!")
                    except Exception as e:
                        st.error(f"فشل الحفظ: {str(e)}")
    
    else:
        st.error("لم يتم العثور على قاعدة البيانات! تأكد من تشغيل create_database.py أولاً")

# ---------------------------- صفحة التقارير ----------------------------
with reports_tab:
    st.subheader("📄 تقارير المعهد")
    
    report_type = st.selectbox("اختر نوع التقرير", [
        "تقرير الحضور الشهري",
        "تقرير تقدم الطلاب",
        "تقرير تقييم الأساتذة"
    ])
    
    if report_type == "تقرير الحضور الشهري":
        with sqlite3.connect("new_quran_institute.db") as conn:
            df_attendance = pd.read_sql("""
                SELECT 
                    الطلاب.اسم_الطالب,
                    COUNT(الحضور.رقم_الحضور) AS عدد_الجلسات,
                    MAX(الحضور.تاريخ_الحضور) AS آخر_حضور
                FROM الحضور
                JOIN الطلاب ON الحضور.رقم_الطالب = الطلاب.رقم_الطالب
                GROUP BY الطلاب.رقم_الطالب
            """, conn)
            
            if not df_attendance.empty:
                st.dataframe(df_attendance, use_container_width=True)
            else:
                st.warning("لا توجد بيانات حضور")

# ---------------------------- القائمة الجانبية المطورة ----------------------------
#with st.sidebar:
#    st.image("static/qubaa.png", width=100)
#    st.title("لوحة التحكم")
    
    menu_choice = st.radio("القائمة", [
        "الرئيسية",
        "إضافة حلقة جديدة",
        "إدارة الأساتذة",
        "إعدادات النظام"
    ], index=0)
    
    if menu_choice == "إضافة حلقة جديدة":
        with st.form("add_session"):
            session_name = st.text_input("اسم الحلقة")
            max_students = st.number_input("الحد الأقصى للطلاب", min_value=5, max_value=50)
            
            if st.form_submit_button("إضافة الحلقة"):
                if session_name:
                    try:
                        with sqlite3.connect("new_quran_institute.db") as conn:
                            conn.execute("INSERT INTO الحلقات (اسم_الحلقة) VALUES (?)", (session_name,))
                        st.success("تمت إضافة الحلقة بنجاح!")
                    except Exception as e:
                        st.error(f"خطأ: {str(e)}")
                else:
                    st.warning("الرجاء إدخال اسم الحلقة")

    # إضافة المزيد من الخيارات الإدارية هنا

# ---------------------------- تحسينات إضافية ----------------------------
# 1. إضافة ميزة التحميل التلقائي عند التعديل
# 2. إضافة رسائل تأكيد للعمليات الحساسة
# 3. تحسين معالجة الأخطاء
# 4. إضافة ميزة البحث والتصفية في الجداول