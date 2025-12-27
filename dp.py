import mysql.connector

def get_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="mysql",
            database="lost_found",
            charset="utf8"
        )
        return conn
    except mysql.connector.Error as err:
        print(f"❌ Database connection failed: {err}")
        return None

# Test connection when running db.py directly
if __name__ == "__main__":
    conn = get_connection()
    if conn:
        print("✅ Database connected successfully!")
        conn.close()
    else:
        print("❌ Could not connect to database.")
