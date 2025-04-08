import sqlite3
import os

# اسم قاعدة البيانات الجديدة
db_name = 'new_quran_institute.db'
print("مسار قاعدة البيانات الجديدة:", os.path.abspath(db_name))

# إنشاء الاتصال بقاعدة البيانات الجديدة
conn = sqlite3.connect(db_name)
cursor = conn.cursor()

# إنشاء الجداول
cursor.execute("DROP TABLE IF EXISTS attendance")
cursor.execute("DROP TABLE IF EXISTS daily_recitation")
cursor.execute("DROP TABLE IF EXISTS weakness_points")
cursor.execute("DROP TABLE IF EXISTS memorization_plans")
cursor.execute("DROP TABLE IF EXISTS points")
cursor.execute("DROP TABLE IF EXISTS students")
cursor.execute("DROP TABLE IF EXISTS study_circles")
cursor.execute("DROP TABLE IF EXISTS teachers")

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

# تجربة: إدخال بيانات مبدئية للأساتذة
teachers_data = [
    ("أحمد علي", "123456789", "ماجستير", "2023-10-01", "نصف القرآن"),
    ("محمد سعيد", "987654321", "بكالوريوس", "2023-10-02", "القرآن كاملاً"),
    ("فاطمة الزهراء", "456789123", "دكتوراه", "2023-10-03", "نصف القرآن"),
    ("علي حسن", "321654987", "بكالوريوس", "2023-10-04", "القرآن كاملاً"),
    ("سارة محمد", "654321789", "ماجستير", "2023-10-05", "نصف القرآن"),
]

cursor.executemany('''
INSERT INTO teachers (name, phone, qualification, join_date, memorization_amount)
VALUES (?, ?, ?, ?, ?)
''', teachers_data)

# عرض الجداول الموجودة
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
print("\nالجداول الموجودة حالياً:")
for table in cursor.fetchall():
    print("-", table[0])

# عرض بيانات الأساتذة
cursor.execute('SELECT * FROM teachers')
rows = cursor.fetchall()
print("\nالبيانات في جدول الأساتذة:")
for row in rows:
    print(row)

# حفظ وإغلاق
conn.commit()
conn.close()
