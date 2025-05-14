import sqlite3

def initialize_db():
    conn = sqlite3.connect('matches.db')
    c = conn.cursor()

    # إنشاء جدول المباريات إذا لم يكن موجودًا
    c.execute('''
    CREATE TABLE IF NOT EXISTS matches (
        match_key TEXT PRIMARY KEY,
        team_a TEXT,
        team_b TEXT,
        score_a TEXT,
        score_b TEXT,
        status TEXT,
        match_time TEXT
    )
    ''')

    conn.commit()
    conn.close()

def addData(match_key, team_a, team_b, score_a, score_b, status, match_time):
    # تأكد من أن score_a و score_b هما أرقام أو قيم فارغة
    try:
        score_a = int(score_a)
    except ValueError:
        score_a = 0  # إذا كانت القيمة النصية غير قابلة للتحويل إلى عدد، ضع 0

    try:
        score_b = int(score_b)
    except ValueError:
        score_b = 0  # إذا كانت القيمة النصية غير قابلة للتحويل إلى عدد، ضع 0

    conn = sqlite3.connect('matches.db')
    c = conn.cursor()

    # إضافة المباراة إلى قاعدة البيانات
    c.execute('''
    INSERT OR REPLACE INTO matches (match_key, team_a, team_b, score_a, score_b, status, match_time)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (match_key, team_a, team_b, score_a, score_b, status, match_time))

    conn.commit()
    conn.close()


def updateData(score_a, score_b, status, match_key):
    conn = sqlite3.connect('matches.db')
    c = conn.cursor()

    # تحديث البيانات للمباراة المعنية باستخدام match_key
    c.execute('''
    UPDATE matches 
    SET score_a = ?, score_b = ?, status = ?
    WHERE match_key = ?
    ''', (score_a, score_b, status, match_key))

    conn.commit()
    conn.close()
def delete_all_data():
    conn = sqlite3.connect('matches.db')
    c = conn.cursor()
    c.execute('DELETE FROM matches')
    conn.commit()
    conn.close()
def getData(match_key):
    conn = sqlite3.connect('matches.db')
    c = conn.cursor()

    # جلب البيانات باستخدام match_key
    c.execute('SELECT * FROM matches WHERE match_key = ?', (match_key,))
    data = c.fetchone()

    conn.close()
    return data
initialize_db()
