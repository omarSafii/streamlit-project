import sqlite3
import os

def create_database():
    # استخدام مسار مطلق لتجنب أخطاء المسار النسبية [[6]]
    DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "new_quran_institute.db"))    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        print("تم الاتصال بقاعدة البيانات بنجاح!")

        # تفعيل المفاتيح الخارجية [[6]]
        cursor.execute("PRAGMA foreign_keys=ON;")

        # =====================================================
        # إنشاء جدول الحلقات (إذا لم يوجد)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS الحلقات (
                رقم_الحلقة INTEGER PRIMARY KEY AUTOINCREMENT,
                اسم_الحلقة TEXT NOT NULL
            )
        ''')
        print("تم إنشاء جدول الحلقات بنجاح.")

        # =====================================================
        # إنشاء جدول الطلاب (إذا لم يوجد)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS الطلاب (
                رقم_الطالب INTEGER PRIMARY KEY AUTOINCREMENT,
                رقم_الحلقة INTEGER,
                اسم_الطالب TEXT NOT NULL,
                الحفظ_السابق TEXT,
                تاريخ_الانضمام DATE,
                الصف_الدراسي TEXT,
                عنوان_السكن TEXT,
                هاتف_الطالب TEXT,
                هاتف_الاهل TEXT,
                FOREIGN KEY (رقم_الحلقة) REFERENCES الحلقات(رقم_الحلقة)
            )
        ''')
        
        print("تم إنشاء جدول الطلاب بنجاح.")




        # =====================================================
        # إنشاء جدول الخطط
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS الخطط (
                رقم_الخطة INTEGER PRIMARY KEY AUTOINCREMENT,
                رقم_الطالب INTEGER UNIQUE,
                الهدف TEXT,
                مدة_الخطة INTEGER,
                تاريخ DATE,
                FOREIGN KEY (رقم_الطالب) REFERENCES الطلاب(رقم_الطالب)
            )
        ''')
        print("تم إنشاء جدول الخطط بنجاح.")

        # =====================================================
        # إنشاء جدول النقاط
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS النقاط (
                رقم_النقطة INTEGER PRIMARY KEY AUTOINCREMENT,
                رقم_الطالب INTEGER,
                القيمة REAL,
                السبب TEXT,
                التاريخ DATE,
                FOREIGN KEY (رقم_الطالب) REFERENCES الطلاب(رقم_الطالب)
            )
        ''')
        print("تم إنشاء جدول النقاط بنجاح.")

        # =====================================================
        # إنشاء جدول نقاط_الضعف
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS نقاط_الضعف (
                رقم_المشكلة INTEGER PRIMARY KEY AUTOINCREMENT,
                رقم_الطالب INTEGER,
                تفصيل_المشكلة TEXT,
                تاريخ_تسجيل_المشكلة DATE,
                FOREIGN KEY (رقم_الطالب) REFERENCES الطلاب(رقم_الطالب)
            )
        ''')
        print("تم إنشاء جدول نقاط_الضعف بنجاح.")

        # =====================================================
        # إنشاء جدول الحضور
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS الحضور (
                رقم_الحضور INTEGER PRIMARY KEY AUTOINCREMENT,
                رقم_الطالب INTEGER,
                رقم_الاستاذ INTEGER,
                تاريخ_الحضور DATE,
                وقت_الجلسة TIME,
                FOREIGN KEY (رقم_الطالب) REFERENCES الطلاب(رقم_الطالب),
                FOREIGN KEY (رقم_الاستاذ) REFERENCES الاساتذة(رقم_الاستاذ)
            )
        ''')
        print("تم إنشاء جدول الحضور بنجاح.")

                # =====================================================
                # إنشاء جدول الاساتذة (إذا لم يوجد)
        cursor.execute('''
                    CREATE TABLE IF NOT EXISTS الاساتذة (
                        رقم_الاستاذ INTEGER PRIMARY KEY AUTOINCREMENT,
                        رقم_الحلقة INTEGER,
                        اسم_الاستاذ TEXT NOT NULL,
                        هاتف_الاستاذ TEXT,
                        المؤهلات_الشرعية TEXT,
                        المؤهلات_الاكاديمية TEXT,
                        العمل TEXT,
                        تاريخ_الانضمام DATE,
                        العمر INTEGER,
                        مستوى_التفرغ TEXT,
                        FOREIGN KEY (رقم_الحلقة) REFERENCES الحلقات(رقم_الحلقة)
                    )
                ''')
        print("تم إنشاء جدول الاساتذة بنجاح.")


                # =====================================================
        # إنشاء الجداول المتبقية (الخطط، النقاط، نقاط_الضعف، الحضور)
        # ... (نفس الكود السابق مع استخدام CREATE TABLE IF NOT EXISTS)

        # حفظ التغييرات [[6]]
        conn.commit()
        print("تم حفظ التغييرات بنجاح.")

    except Exception as e:
        print(f"حدث خطأ: {e}")
        conn.rollback()
    finally:
        if conn:
            conn.close()
            print("تم إغلاق الاتصال.")

if __name__ == "__main__":
    create_database()