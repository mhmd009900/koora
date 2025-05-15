import psycopg2

# الاتصال بقاعدة بيانات Railway
conn = psycopg2.connect(
    dbname="railway",
    user="postgres",
    password="pblEwDbdOflfRWGdxQffBexQzuIrtjUR",
    host="caboose.proxy.rlwy.net",
    port="26944"
)

cursor = conn.cursor()

# إنشاء الجدول إن لم يكن موجودًا
cursor.execute("""
CREATE TABLE IF NOT EXISTS matches (
    match_key TEXT PRIMARY KEY,
    team_a TEXT,
    team_b TEXT,
    score_a TEXT,
    score_b TEXT,
    status TEXT,
    match_time TEXT
);
""")
conn.commit()


def addData(match_key, team_a, team_b, score_a, score_b, status, match_time):
    cursor.execute("""
    INSERT INTO matches (match_key, team_a, team_b, score_a, score_b, status, match_time)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (match_key) DO NOTHING;
    """, (match_key, team_a, team_b, score_a, score_b, status, match_time))
    conn.commit()


def updateData(score_a, score_b, status, match_key):
    cursor.execute("""
    UPDATE matches
    SET score_a = %s, score_b = %s, status = %s
    WHERE match_key = %s;
    """, (score_a, score_b, status, match_key))
    conn.commit()


def getData(match_key):
    cursor.execute("SELECT * FROM matches WHERE match_key = %s;", (match_key,))
    return cursor.fetchone()


def delete_all_data():
    cursor.execute("DELETE FROM matches;")
    conn.commit()
