from db import get_connection

def add_item(user_id, title, description, location):
    conn = get_connection()
    if not conn:
        print("❌ Cannot connect to database.")
        return

    cur = conn.cursor()
    query = "INSERT INTO items (user_id, title, description, location) VALUES (%s, %s, %s, %s)"
    cur.execute(query, (user_id, title, description, location))
    conn.commit()

    cur.close()
    conn.close()
    print("✅ Item added successfully!")

def search_items(keyword):
    conn = get_connection()
    if not conn:
        print("❌ Cannot connect to database.")
        return []

    cur = conn.cursor(dictionary=True)
    query = "SELECT * FROM items WHERE title LIKE %s OR location LIKE %s"
    search_term = f"%{keyword}%"
    cur.execute(query, (search_term, search_term))
    results = cur.fetchall()

    cur.close()
    conn.close()
    return results
