from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
import datetime
import json

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["litter_bug_db"]  # Correct DB name

# ---------------------------
# Insert a New User (No Password)
# ---------------------------
def insert_user(username):
    user_doc = {
        "username": username,
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
        "created_at": datetime.datetime.utcnow()
    }
    try:
        result = db.Users.insert_one(user_doc)
        print(f"✅ New user '{username}' added with ID: {result.inserted_id}")
    except DuplicateKeyError:
        print(f"⚠️ Username '{username}' already exists. Choose a different username.")

# ---------------------------
# Insert a New Bin
# ---------------------------
def insert_bin(longitude, latitude, bin_type):
    bin_doc = {
        "longitude": float(longitude),
        "latitude": float(latitude),
        "type": str(bin_type)
    }
    result = db.Bins.insert_one(bin_doc)
    print(f"✅ New bin added with ID: {result.inserted_id}")

# ---------------------------
# Insert a New Trash Item
# ---------------------------
def insert_trash(longitude, latitude, trash_type, dropped_by=None):
    trash_doc = {
        "longitude": float(longitude),
        "latitude": float(latitude),
        "type": str(trash_type),
        "dropped_by": dropped_by,
        "picked_up_by": None,
        "is_collected": False,
        "timestamp": datetime.datetime.utcnow()
    }
    result = db.Trash.insert_one(trash_doc)
    print(f"✅ New trash item added with ID: {result.inserted_id}")


def get_all_users():
    users_cursor = db.Users.find()

    # Prepare the data for JSON dumping (convert ObjectId to string)
    users_list = []
    for user in users_cursor:
        user["_id"] = str(user["_id"])  # ObjectId needs to be string for JSON
        users_list.append(user)

    return users_list


def export_users_to_json(filepath="users_export.json"):
    users = get_all_users()

    # Write the users list to a JSON file
    with open(filepath, "w") as f:
        json.dump(users, f, indent=4)

    print(f"✅ All users exported to {filepath}")


# Example usage:
if __name__ == "__main__":
    export_users_to_json()