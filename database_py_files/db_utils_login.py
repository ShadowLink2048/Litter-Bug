from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["login_db"]

def insert_user(username, passkey):
    user_doc = {
        "username": username,
        "passkey": passkey,
        # Add any other required fields here
    }

    try:
        result = db.Users.insert_one(user_doc)
        print(f"✅ New user '{username}' added successfully (Mongo _id: {result.inserted_id})")
    except DuplicateKeyError:
        print(f"⚠️ User '{username}' already exists. Choose a different username.")

# Example usage:
if __name__ == "__main__":
    insert_user("player1", "generated_passkey_here")
