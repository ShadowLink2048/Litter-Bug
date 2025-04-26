from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
import json
import datetime

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["litter_bug_db"]

# 🟢 Custom JSON Encoder to handle datetime objects
class MongoJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()  # Convert datetime to ISO 8601 string
        return super().default(obj)

# 🟠 Insert a new user into the litter_bug_db Users collection
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
        "created_at": datetime.datetime.now(datetime.UTC)  # Timezone-aware datetime
    }

    try:
        result = db.Users.insert_one(user_doc)
        print(f"✅ New user '{username}' added with ID: {result.inserted_id}")
    except DuplicateKeyError:
        print(f"⚠️ Username '{username}' already exists. Choose a different username.")

# 🟣 Retrieve all users from the Users collection
def get_all_users():
    users_cursor = db.Users.find()
    users_list = []
    for user in users_cursor:
        user["_id"] = str(user["_id"])  # Convert ObjectId to string for JSON safety
        users_list.append(user)
    return users_list

# 🟡 Export all users to a JSON file (fixed datetime issue)
def export_users_to_json(filepath="users_export.json"):
    users = get_all_users()

    with open(filepath, "w") as f:
        json.dump(users, f, indent=4, cls=MongoJSONEncoder)

    print(f"✅ All users exported to {filepath}")

# Optional: manual test to export users
if __name__ == "__main__":
    export_users_to_json()
