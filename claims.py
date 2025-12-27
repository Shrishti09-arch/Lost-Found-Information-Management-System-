from db import get_connection

def claim_item(item_id, claimant_user_id, claim_message):
    conn = get_connection()
    if not conn:
        print("❌ Cannot connect to database.")
        return

    cur = conn.cursor()
    query = "INSERT INTO claims (item_id, claimant_user_id, claim_message) VALUES (%s, %s, %s)"
    cur.execute(query, (item_id, claimant_user_id, claim_message))
    conn.commit()

    cur.close()
    conn.close()
    print("✅ Claim request submitted. Waiting for owner's approval.")

def get_claims_for_user(user_id):
    """Get all claims for items that belong to a specific user (owner)."""
    conn = get_connection()
    if not conn:
        print("❌ Cannot connect to database.")
        return []

    cur = conn.cursor(dictionary=True)
    query = """
    SELECT c.claim_id, c.item_id, c.claim_message, c.status,
           i.title, i.location, u.name AS claimant_name
    FROM claims c
    JOIN items i ON c.item_id = i.item_id
    JOIN users u ON c.claimant_user_id = u.user_id
    WHERE i.user_id = %s
    """
    cur.execute(query, (user_id,))
    claims = cur.fetchall()

    cur.close()
    conn.close()
    return claims

def update_claim_status(claim_id, new_status):
    conn = get_connection()
    if not conn:
        print("❌ Cannot connect to database.")
        return

    cur = conn.cursor()

    # First, get the item_id for this claim
    cur.execute("SELECT item_id FROM claims WHERE claim_id = %s", (claim_id,))
    result = cur.fetchone()
    if not result:
        print("❌ Claim not found.")
        cur.close()
        conn.close()
        return

    item_id = result[0]

    # Update claim status
    cur.execute("UPDATE claims SET status = %s WHERE claim_id = %s", (new_status, claim_id))

    # If claim is approved, mark item as found
    if new_status == "approved":
        cur.execute("UPDATE items SET status = 'claimed' WHERE item_id = %s", (item_id,))

    conn.commit()
    cur.close()
    conn.close()
    print(f"✅ Claim {claim_id} updated to {new_status}.")
