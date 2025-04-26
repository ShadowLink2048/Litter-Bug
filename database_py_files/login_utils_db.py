from pymongo import MongoClient

# Connect to both databases
client = MongoClient("mongodb://localhost:27017/")
login_db = client["login_db"]
game_db = client["litter_bug_db"]

def get_user_profile(user_id):
    """
    Verify the user exists in login_db and return their game profile from litter_bug_db.
    No auto-profile creation; assumes frontend handles that.
    """
    login_user = login_db.Users.find_one({"id": user_id})

    if not login_user:
        print(f"❌ Login failed: user '{user_id}' not found in login_db.")
        return None

    print(f"✅ User '{user_id}' authenticated (passkey validation handled externally).")

    # Check for the matching game profile
    game_user = game_db.Users.find_one({"username": user_id})

    if game_user:
        game_user["_id"] = str(game_user["_id"])  # Convert ObjectId for JSON compatibility
        return game_user
    else:
        print(f"⚠️ User '{user_id}' has no profile in litter_bug_db (handled by frontend).")
        return None

# Example test run
if __name__ == "__main__":
    user_id = input("Enter login ID: ").strip()
    profile = get_user_profile(user_id)
    if profile:
        print("User Profile Data:")
        print(profile)
