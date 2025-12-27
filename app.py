from auth import register, login
from items import add_item, search_items
from claims import claim_item, get_claims_for_user, update_claim_status


current_user_id = None  # store logged-in user ID

print("=== Lost & Found Backend ===")
print("1. Register")
print("2. Login")
choice = input("Enter choice: ")

if choice == "1":
    name = input("Enter your name: ")
    email = input("Enter email: ")
    password = input("Enter password: ")
    register(name, email, password)

elif choice == "2":
    email = input("Enter email: ")
    password = input("Enter password: ")

    # Modified login() so it returns user_id if login successful
    from auth import login
    user_id = login(email, password)

    if user_id:
        current_user_id = user_id
        while True:
            print("\n=== MENU ===")
            print("1. Add Lost Item")
            print("2. Search Items")
            print("3. Claim an Item")
            print("4. View & Manage Claims (For Your Items)")
            print("5. Logout")
            option = input("Enter choice: ")

            if option == "1":
                title = input("Enter item title: ")
                description = input("Enter description: ")
                location = input("Enter location: ")
                add_item(current_user_id, title, description, location)

            elif option == "2":
                keyword = input("Enter search keyword: ")
                results = search_items(keyword)
                if results:
                    print("\n Search Results:")
                    for r in results:
                        print(f"ID: {r['item_id']} | Title: {r['title']} | Location: {r['location']} | Status: {r['status']}")
                else:
                    print("No matching items found.")

            elif option == "3":
                item_id = input("Enter item ID to claim: ")
                message = input("Describe proof (e.g., color, marks, serial number): ")
                claim_item(item_id, current_user_id, message)

            elif option == "4":
                claims = get_claims_for_user(current_user_id)
                if not claims:
                    print(" No claims for your items.")
                else:
                    print("\n Claims for your items:")
                    for c in claims:
                        print(f"Claim ID: {c['claim_id']} | Item: {c['title']} | Claimer: {c['claimant_name']} | Proof: {c['claim_message']} | Status: {c['status']}")

                    claim_id = input("Enter Claim ID to approve/reject (or press Enter to skip): ")
                    if claim_id:
                        decision = input("Approve (a) or Reject (r): ").lower()
                        if decision == "a":
                            update_claim_status(claim_id, "approved")
                        elif decision == "r":
                            update_claim_status(claim_id, "rejected")
                        else:
                            print("❌ Invalid choice.")


            elif option == "5":
                print(" Logged out.")
                break
    else:
        print("❌ Invalid choice.")

