from bson import ObjectId
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
import json
import datetime

# MongoDB setup
client = MongoClient('mongodb://localhost:27017/')
db = client['litter_bug_db']
users_collection = db['Users']


# Custom JSON Encoder to handle ObjectId and datetime serialization
class MongoJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)  # Convert ObjectId to string
        elif isinstance(obj, datetime.datetime):
            return obj.isoformat()  # Convert datetime to ISO format string
        return super().default(obj)


# 🟠 Insert a new user into the litter_bug_db Users collection
def insert_user(username):
    # Check if the username already exists
    if db.Users.find_one({"username": username}):
        print(f"⚠️ Username '{username}' already exists. Choose a different username.")
        return

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
        "created_at": datetime.datetime.now(datetime.timezone.utc)  # Timezone-aware datetime
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
        user["created_at"] = user["created_at"].isoformat()  # Ensure datetime is converted
        users_list.append(user)
    return users_list


# Function to export users to JSON
def export_users_to_json():
    users = get_all_users()  # Retrieve all users
    with open('users_export.json', 'w') as f:
        json.dump(users, f, indent=4, cls=MongoJSONEncoder)  # Use custom encoder


# Optional: manual test to export users
if __name__ == "__main__":
    export_users_to_json()
