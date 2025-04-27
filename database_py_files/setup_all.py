# setup_all.py

from pymongo import MongoClient
from pymongo.errors import CollectionInvalid

# -----------------------------
# Connection Setup
# -----------------------------
client = MongoClient("mongodb://localhost:27017/")
login_db = client["login_db"]
game_db = client["litter_bug_db"]

# -----------------------------
# Configurable Options
# -----------------------------
DROP_EXISTING_COLLECTIONS = True  # Toggle this OFF in production!

# -----------------------------
# Schema Definitions
# -----------------------------

# Login DB Users Schema
login_users_schema = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["username", "passkey"],
        "properties": {
            "username": {"bsonType": "string"},
            "passkey": {"bsonType": "string"},
            "email": {"bsonType": "string"},
            "firstname": {"bsonType": "string"},
            "lastname": {"bsonType": "string"}
        }
    }
}

# Game DB Users Schema
game_users_schema = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["username", "recycle_coins", "trash_coins", "waste_coins", "accessories", "steps"],
        "properties": {
            "username": {"bsonType": "string"},
            "recycle_coins": {"bsonType": "int"},
            "trash_coins": {"bsonType": "int"},
            "waste_coins": {"bsonType": "int"},
            "accessories": {
                "bsonType": "object",
                "required": ["hat", "shirt", "pants", "shoes", "hand_left", "hand_right"],
                "properties": {
                    "hat": {"bsonType": ["string", "null"]},
                    "shirt": {"bsonType": ["string", "null"]},
                    "pants": {"bsonType": ["string", "null"]},
                    "shoes": {"bsonType": ["string", "null"]},
                    "hand_left": {"bsonType": ["string", "null"]},
                    "hand_right": {"bsonType": ["string", "null"]}
                }
            },
            "steps": {"bsonType": "int"},
            "created_at": {"bsonType": "date"}
        }
    }
}

# Bins Schema
bins_schema = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["longitude", "latitude", "type"],
        "properties": {
            "longitude": {"bsonType": "double"},
            "latitude": {"bsonType": "double"},
            "type": {"enum": ["trash", "recycle"]}
        }
    }
}

# Trash Schema
trash_schema = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["longitude", "latitude", "type", "is_collected", "timestamp"],
        "properties": {
            "longitude": {"bsonType": "double"},
            "latitude": {"bsonType": "double"},
            "type": {"enum": ["trash", "recycle"]},
            "dropped_by": {"bsonType": ["string", "null"]},
            "picked_up_by": {"bsonType": ["string", "null"]},
            "is_collected": {"bsonType": "bool"},
            "timestamp": {"bsonType": "date"}
        }
    }
}

# -----------------------------
# Utility Function to Create Collections
# -----------------------------
def create_collection_with_schema(db, collection_name, schema):
    if DROP_EXISTING_COLLECTIONS:
        db[collection_name].drop()
        print(f"⚠️ Dropped existing collection '{collection_name}'.")

    try:
        db.create_collection(collection_name)
        print(f"✅ Created collection '{collection_name}'.")
    except CollectionInvalid:
        print(f"⚠️ Collection '{collection_name}' already exists.")

    db.command("collMod", collection_name, validator=schema)
    print(f"🛠️ Applied schema validation for '{collection_name}'.")

# -----------------------------
# Setup Login DB
# -----------------------------
print("\n🔐 Setting up login_db.Users...")
create_collection_with_schema(login_db, "Users", login_users_schema)
login_db.Users.create_index("username", unique=True)
print("✅ Unique index on 'username' (login_db.Users).\n")

# -----------------------------
# Setup Game DB
# -----------------------------
print("🎮 Setting up litter_bug_db...")
create_collection_with_schema(game_db, "Users", game_users_schema)
game_db.Users.create_index("username", unique=True)
print("✅ Unique index on 'username' (game profile Users).")

create_collection_with_schema(game_db, "Bins", bins_schema)
game_db.Bins.create_index([("longitude", 1), ("latitude", 1)])
game_db.Bins.create_index([("location", "2dsphere")])
print("✅ 2dsphere index on Bins.location.")

create_collection_with_schema(game_db, "Trash", trash_schema)
game_db.Trash.create_index([("longitude", 1), ("latitude", 1)])
game_db.Trash.create_index([("location", "2dsphere")])
print("✅ 2dsphere index on Trash.location.\n")

print("🚀 Database setup complete!")
