import sqlite3
conn = sqlite3.connect('sql_app.db')
cursor = conn.cursor()
cursor.execute("DELETE FROM users WHERE email='msdmuthu077@gmail.com';")
conn.commit()
print(f"Deleted {cursor.rowcount} rows.")
conn.close()
