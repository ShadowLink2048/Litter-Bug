# test_geo_queries.py
# --------------------------------------
# Test script for the geo_utils.py functions
# Allows manual input of longitude, latitude, and radius (in miles)
# Returns matching Bins and Trash from the litter_bug_db
# --------------------------------------

from geo_utils import get_bins_within_radius, get_trash_within_radius

def main():
    print("=== Geo Query Test: Find Bins and Trash Within Radius ===")

    try:
        # Get input from user
        longitude = float(input("Enter longitude (e.g., -122.335167): ").strip())
        latitude = float(input("Enter latitude (e.g., 47.608013): ").strip())
        radius_miles = float(input("Enter search radius in miles (e.g., 1): ").strip())
    except ValueError:
        print("❌ Invalid input. Please enter numeric values for longitude, latitude, and radius.")
        return

    print("\n🔎 Searching for Bins...")
    bins = get_bins_within_radius(longitude, latitude, radius_miles)
    print(f"Found {len(bins)} bins:")
    for bin_doc in bins:
        print(bin_doc)

    print("\n🔎 Searching for Trash...")
    trash = get_trash_within_radius(longitude, latitude, radius_miles)
    print(f"Found {len(trash)} trash items:")
    for trash_doc in trash:
        print(trash_doc)

if __name__ == "__main__":
    main()
