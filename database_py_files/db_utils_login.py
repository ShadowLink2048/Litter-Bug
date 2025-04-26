from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["login_db"]

def insert_user(user_id, passkey):
    user_doc = {
        "id": user_id,         # Can be string or int, depending on your system
        "passkey": passkey     # Stored directly as given
    }

    try:
        result = db.Users.insert_one(user_doc)
        print(f"✅ New user with ID '{user_id}' added successfully (Mongo _id: {result.inserted_id})")
    except DuplicateKeyError:
        print(f"⚠️ User ID '{user_id}' already exists. Choose a different ID.")

# Example usage:
if __name__ == "__main__":
    insert_user("player1", "generated_passkey_here")
