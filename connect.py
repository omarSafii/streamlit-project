import sqlite3
import os
print(os.path.abspath('quran_institute.db'))

# إنشاء الاتصال بقاعدة البيانات
conn = sqlite3.connect('quran_institute.db')
cursor = conn.cursor()

# جدول الأساتذة
cursor.execute('''
CREATE TABLE IF NOT EXISTS teachers (
    teacher_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    phone TEXT,
    qualification TEXT,
    join_date DATE,
    memorization_amount TEXT
)
''')

# جدول الحلقات
cursor.execute('''
CREATE TABLE IF NOT EXISTS study_circles (
    circle_id INTEGER PRIMARY KEY,
    teacher_id INTEGER,
    name TEXT NOT NULL,
    students_count INTEGER,
    FOREIGN KEY (teacher_id) REFERENCES teachers(teacher_id)
)
''')

# جدول الطلاب
cursor.execute('''
CREATE TABLE IF NOT EXISTS students (
    student_id INTEGER PRIMARY KEY,
    circle_id INTEGER,
    name TEXT NOT NULL,
    phone TEXT,
    parent_phone TEXT,
    join_date DATE,
    previous_memorization TEXT,
    birth_date DATE,
    FOREIGN KEY (circle_id) REFERENCES study_circles(circle_id)
)
''')

# جدول النقاط
cursor.execute('''
CREATE TABLE IF NOT EXISTS points (
    point_id INTEGER PRIMARY KEY,
    student_id INTEGER,
    points_count INTEGER,
    reason TEXT,
    date DATE,
    FOREIGN KEY (student_id) REFERENCES students(student_id)
)
''')

# جدول خطة الحفظ
cursor.execute('''
CREATE TABLE IF NOT EXISTS memorization_plans (
    plan_id INTEGER PRIMARY KEY,
    student_id INTEGER,
    goal TEXT,
    set_date DATE,
    FOREIGN KEY (student_id) REFERENCES students(student_id)
)
''')

# جدول الأخطاء ونقاط الضعف
cursor.execute('''
CREATE TABLE IF NOT EXISTS weakness_points (
    error_id INTEGER PRIMARY KEY,
    student_id INTEGER,
    weakness_point TEXT,
    date DATE,
    FOREIGN KEY (student_id) REFERENCES students(student_id)
)
''')

# جدول التسميع اليومي
cursor.execute('''
CREATE TABLE IF NOT EXISTS daily_recitation (
    recitation_id INTEGER PRIMARY KEY,
    student_id INTEGER,
    date DATE,
    surah TEXT,
    verses TEXT,
    evaluation TEXT,
    notes TEXT,
    FOREIGN KEY (student_id) REFERENCES students(student_id)
)
''')

# جدول الحضور والغياب
cursor.execute('''
CREATE TABLE IF NOT EXISTS attendance (
    attendance_id INTEGER PRIMARY KEY,
    student_id INTEGER,
    date DATE,
    status TEXT,
    FOREIGN KEY (student_id) REFERENCES students(student_id)
)
''')

# حفظ التغييرات وإغلاق الاتصال
conn.commit()
conn.close()