# login_utils_db.py

from pymongo import MongoClient
import datetime

# Connect to both databases
client = MongoClient("mongodb://localhost:27017/")
login_db = client["login_db"]
game_db = client["litter_bug_db"]

def create_profile_if_missing(user_id):
    """
    Checks if the user has a profile in litter_bug_db.
    If not, auto-creates one with default values.
    """
    existing_profile = game_db.Users.find_one({"username": user_id})

    if existing_profile:
        print(f"✅ Profile for '{user_id}' already exists.")
        return existing_profile

    # Create new profile with default values
    new_profile = {
        "username": user_id,
        "recycle_coins": 0,
        "trash_coins": 0,
        "waste_coins": 0,
        "accessories": {
            "hat": None,
            "shirt": None,
            "pants": None,
            "shoes": None,
            "hand_left": None,
            "hand_right": None
        },
        "steps": 0,
        "created_at": datetime.datetime.now(datetime.UTC)

    }

    result = game_db.Users.insert_one(new_profile)
    new_profile["_id"] = str(result.inserted_id)  # Convert ObjectId to string
    print(f"🟢 Auto-created new profile for '{user_id}'.")
    return new_profile

def get_user_profile(user_id):
    """
    Verifies the user exists in login_db and ensures a game profile exists in litter_bug_db.
    """
    login_user = login_db.Users.find_one({"id": user_id})

    if not login_user:
        print(f"❌ Login failed: user '{user_id}' not found in login_db.")
        return None

    print(f"✅ User '{user_id}' authenticated.")
    return create_profile_if_missing(user_id)

# Optional: Manual test run
if __name__ == "__main__":
    user_id = input("Enter login ID: ").strip()
    profile = get_user_profile(user_id)
    if profile:
        print("User Profile Data:")
        print(profile)
