# login_utils_db.py

from pymongo import MongoClient
import bcrypt
from datetime import datetime, timedelta
import random
import string

# ------------------------
# Database Connections
# ------------------------
client = MongoClient("mongodb://localhost:27017/")
login_db = client["login_db"]
collection = login_db["Users"]  # This is what your api_server.py was expecting

game_db = client["litter_bug_db"]

# ------------------------
# Logged-In Users Dictionary
# ------------------------
logged_in = {}

# ------------------------
# Hash Password / Passkey
# ------------------------
def hash_passkey(passkey):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(passkey.encode('utf-8'), salt)

# ------------------------
# Check Password Match
# ------------------------
def check_hash_match(passkey, stored_hash):
    if isinstance(stored_hash, str):
        stored_hash = stored_hash.encode('utf-8')  # Ensure bytes
    return bcrypt.checkpw(passkey.encode('utf-8'), stored_hash)

# ------------------------
# Generate Login Token
# ------------------------
def generate_token():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=16))

# ------------------------
# Add User to Logged-In Dictionary
# ------------------------
def add_logged_in_user(username):
    logged_in[username] = {
        'tokenid': generate_token(),
        'token_expiry': datetime.now() + timedelta(hours=24)
    }

# ------------------------
# Profile Creation / Linking
# ------------------------
def create_profile_if_missing(user_id):
    """
    Checks if the user has a profile in litter_bug_db.
    If not, auto-creates one with default values.
    """
    existing_profile = game_db.Users.find_one({"username": user_id})
    if existing_profile:
        print(f"✅ Profile for '{user_id}' already exists.")
        return existing_profile

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
        "created_at": datetime.now().astimezone()  # Timezone-aware datetime
    }

    result = game_db.Users.insert_one(new_profile)
    new_profile["_id"] = str(result.inserted_id)
    print(f"🟢 Auto-created new profile for '{user_id}'.")
    return new_profile

# ------------------------
# Get User Profile and Link It
# ------------------------
def get_user_profile(user_id):
    """
    Verifies the user exists in login_db and ensures a game profile exists in litter_bug_db.
    """
    login_user = collection.find_one({"id": user_id})  # Uses the collection alias here
    if not login_user:
        print(f"❌ Login failed: user '{user_id}' not found in login_db.")
        return None

    print(f"✅ User '{user_id}' authenticated.")
    return create_profile_if_missing(user_id)

# ------------------------
# Optional Manual Test
# ------------------------
if __name__ == "__main__":
    user_id = input("Enter login ID: ").strip()
    profile = get_user_profile(user_id)
    if profile:
        print("User Profile Data:")
        print(profile)
