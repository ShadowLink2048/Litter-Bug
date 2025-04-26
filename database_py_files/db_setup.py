from pymongo import MongoClient
from pymongo.errors import CollectionInvalid

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["litter_bug_db"]  # Correct DB name

# ---------------------------
# Define Collection Schemas
# ---------------------------

# Users Schema (No password, uses 'accessories')
users_schema = {
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

# ---------------------------
# Create Collections with Validation
# ---------------------------
def create_collection_with_schema(collection_name, schema):
    try:
        db.create_collection(collection_name)
        db.command("collMod", collection_name, validator=schema)
        print(f"✅ Collection '{collection_name}' created with schema validation.")
    except CollectionInvalid:
        print(f"⚠️ Collection '{collection_name}' already exists. Updating schema validation...")
        db.command("collMod", collection_name, validator=schema)

# Apply schemas
create_collection_with_schema("Users", users_schema)
create_collection_with_schema("Bins", bins_schema)
create_collection_with_schema("Trash", trash_schema)

# Unique index for username (duplicate prevention)
db.Users.create_index("username", unique=True)
print("✅ Unique index on 'username' created.")


# Ensure Users collection exists
create_collection_with_schema("Users", users_schema)

# 🟢 Create 2dsphere indexes for geospatial queries
db.Bins.create_index([("location", "2dsphere")])
print("✅ 2dsphere index created on Bins.location")

db.Trash.create_index([("location", "2dsphere")])
print("✅ 2dsphere index created on Trash.location")


