from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
import datetime

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
        "type": bin_type
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
        "type": trash_type,
        "dropped_by": dropped_by,
        "picked_up_by": None,
        "is_collected": False,
        "timestamp": datetime.datetime.utcnow()
    }
    result = db.Trash.insert_one(trash_doc)
    print(f"✅ New trash item added with ID: {result.inserted_id}")
