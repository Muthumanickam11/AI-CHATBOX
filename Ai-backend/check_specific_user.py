import sqlite3
conn = sqlite3.connect('sql_app.db')
cursor = conn.cursor()
cursor.execute("SELECT id, email FROM users WHERE email='msdmuthu077@gmail.com';")
rows = cursor.fetchall()
print(f"Match found: {len(rows)}")
for row in rows:
    print(row)
conn.close()
