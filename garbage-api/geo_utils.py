# geo_utils.py

from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["litter_bug_db"]

EARTH_RADIUS_MILES = 3963.2  # Radius of the Earth in miles

def get_bins_within_radius(longitude, latitude, radius_miles):
    query = {
        "location": {
            "$geoWithin": {
                "$centerSphere": [[longitude, latitude], radius_miles / EARTH_RADIUS_MILES]
            }
        }
    }
    bins_list = list(db.Bins.find(query))
    for bin in bins_list:
        bin["_id"] = str(bin["_id"])  # Convert ObjectId to string for safe output
    return bins_list

def get_trash_within_radius(longitude, latitude, radius_miles):
    query = {
        "location": {
            "$geoWithin": {
                "$centerSphere": [[longitude, latitude], radius_miles / EARTH_RADIUS_MILES]
            }
        }
    }
    trash_list = list(db.Trash.find(query))
    for trash in trash_list:
        trash["_id"] = str(trash["_id"])
    return trash_list

# Optional: test run
if __name__ == "__main__":
    # Example: Find within 1 mile of Seattle (approx. coordinates)
    longitude = -122.335167
    latitude = 47.608013
    radius_miles = 1

    print("Bins near this location:")
    print(get_bins_within_radius(longitude, latitude, radius_miles))

    print("Trash near this location:")
    print(get_trash_within_radius(longitude, latitude, radius_miles))
