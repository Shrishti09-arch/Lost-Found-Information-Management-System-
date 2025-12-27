import hashlib
from db import get_connection

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register(name, email, password):
    conn = get_connection()
    cur = conn.cursor()

    hashed_pw = hash_password(password)
    query = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
    cur.execute(query, (name, email, hashed_pw))
    conn.commit()

    cur.close()
    conn.close()
    print("✅ User registered successfully!")

def login(email, password):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    query = "SELECT * FROM users WHERE email=%s"
    cur.execute(query, (email,))
    user = cur.fetchone()

    cur.close()
    conn.close()

    if user:
        hashed_pw = hash_password(password)
        if user["password"] == hashed_pw:
            print(f"✅ Welcome, {user['name']}!")
            return user["user_id"]  # Return user_id instead of just True
        else:
            print("❌ Incorrect password.")
            return None
    else:
        print("❌ No user found with this email.")
        return None
