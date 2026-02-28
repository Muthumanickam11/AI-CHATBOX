import asyncio
import sqlite3
from app.core import security

def check_db():
    conn = sqlite3.connect('sql_app.db')
    cursor = conn.cursor()
    cursor.execute("SELECT email, hashed_password FROM users WHERE email='msdmuthu077@gmail.com';")
    row = cursor.fetchone()
    if row:
        email, hashed_pw = row
        print(f"User found: {email}")
        print(f"Stored Hash: {hashed_pw}")
        
        # Test verification
        test_pass = "password123"
        match = security.verify_password(test_pass, hashed_pw)
        print(f"Verification with 'password123': {match}")
        
        if not match:
            print("Password mismatch detected! Updating to known hash...")
            new_hash = security.get_password_hash(test_pass)
            cursor.execute("UPDATE users SET hashed_password=? WHERE email=?", (new_hash, email))
            conn.commit()
            print("Database updated with fresh hash.")
    else:
        print("User 'msdmuthu077@gmail.com' not found in database!")
    conn.close()

if __name__ == "__main__":
    check_db()
