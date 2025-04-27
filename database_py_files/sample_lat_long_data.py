from pymongo import MongoClient
import random
import datetime

# MongoDB setup
client = MongoClient('mongodb://localhost:27017/')
db = client['litter_bug_db']
bins_collection = db['Bins']
trash_collection = db['Trash']

# Function to generate random lat/lon values within a specific range
def generate_random_lat_lon():
    lat = random.uniform(47.5, 47.8)  # Example latitude range (Seattle area)
    lon = random.uniform(-122.4, -122.2)  # Example longitude range (Seattle area)
    return lat, lon

# Function to add sample bins to MongoDB
def add_sample_bins(n=10):
    print(f"Adding {n} sample bins to MongoDB...")
    for _ in range(n):
        lat, lon = generate_random_lat_lon()
        bin_doc = {
            "location": {
                "type": "Point",  # GeoJSON format
                "coordinates": [lon, lat]  # [longitude, latitude]
            },
            "type": random.choice(["recycle", "trash"]),  # Example bin types
            "latitude": lat,  # Explicit latitude field
            "longitude": lon,  # Explicit longitude field
            "created_at": datetime.datetime.utcnow()
        }
        bins_collection.insert_one(bin_doc)
    print(f"{n} bins added successfully.")

# Function to add sample trash items to MongoDB
def add_sample_trash(n=10):
    print(f"Adding {n} sample trash items to MongoDB...")
    for _ in range(n):
        lat, lon = generate_random_lat_lon()
        trash_doc = {
            "location": {
                "type": "Point",  # GeoJSON format
                "coordinates": [lon, lat]  # [longitude, latitude]
            },
            "latitude": lat,  # Explicit latitude field
            "longitude": lon,  # Explicit longitude field
            "type": random.choice(["recycle", "trash"]),  # Random type (recycle/trash)
            "is_collected": False,
            "timestamp": datetime.datetime.utcnow(),  # Required timestamp field
            "created_at": datetime.datetime.utcnow()
        }
        trash_collection.insert_one(trash_doc)
    print(f"{n} trash items added successfully.")

# Add sample data
add_sample_bins(10)  # Add 10 sample bins
add_sample_trash(10)  # Add 10 sample trash items
