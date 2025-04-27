from pymongo import MongoClient
from pymongo.errors import CollectionInvalid
import uuid

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["login_db"]  # Your new login database

# Define schema (no encryption, just structure)
users_schema = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["username", "passkey"],
        "properties": {
            "id": {"bsonType": "string"},  # Change to "int" if IDs are numeric
            "passkey": {"bsonType": "string"}  # Stored exactly as provided
        }
    }
}

def create_collection_with_schema(collection_name, schema):
    try:
        db.create_collection(collection_name)
        db.command("collMod", collection_name, validator=schema)
        print(f"✅ Collection '{collection_name}' created with schema validation.")
    except CollectionInvalid:
        print(f"⚠️ Collection '{collection_name}' already exists. Updating schema validation...")
        db.command("collMod", collection_name, validator=schema)

# Create the Users collection with schema validation
create_collection_with_schema("Users", users_schema)

# Remove documents with null 'id' values
db.Users.delete_many({"id": None})
print("✅ Removed documents with null 'id' values.")

# Update documents with missing or null 'id' values by assigning a unique identifier (UUID)
db.Users.update_many({"id": {"$exists": False}}, {"$set": {"id": str(uuid.uuid4())}})
print("✅ Updated documents with missing 'id' values.")

# Add unique index on ID (prevents duplicate user IDs)
db.Users.create_index("id", unique=True)
print("✅ Unique index on 'id' created.")
