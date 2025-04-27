from pymongo import MongoClient
import random
import datetime
from datetime import timezone
from login_utils_db import hash_passkey  # Password hasher

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
game_db = client['litter_bug_db']
login_db = client['login_db']

game_users_collection = game_db['Users']
login_users_collection = login_db['Users']

name_pool = [
    "Alice", "Bob", "Charlie", "Diana", "Ethan", "Fiona", "George", "Hannah", "Ian", "Julia",
    "Kevin", "Lily", "Mason", "Nina", "Oscar", "Paula", "Quinn", "Riley", "Sophia", "Thomas",
    "Axel", "Zara", "Kai", "Nova", "Leo", "Orion", "Sage", "Vega", "Ivy", "Jett",
    "ShadowWolf", "PixelNinja", "CyberKnight", "GhostRider", "EpicPenguin", "DarkFalcon",
    "LoneDragon", "StarBlaster", "IronFist", "VenomViper", "NebulaQueen", "Frostbite",
    "BlazeStorm", "QuantumKid", "PlasmaDuck", "HyperNova", "SilentArrow", "ThunderBolt",
    "RapidFire", "CrazyKoala", "TurboTiger", "SilentBlade", "DragonSoul", "StormBreaker",
    "OmegaByte", "ToxicVenom", "MoonRider", "CrystalMage", "FirePhoenix", "NightShade",
    "SavageBear", "ArcticFox", "CyberHawk", "SkySniper", "StealthCat", "FlashGator",
    "RebelRogue", "TwilightFox", "TsunamiSamurai", "InfernoX", "IronWarden", "Spectre",
    "Wraith", "ReaperX", "MysticWolf", "AshenOne", "RogueRaptor", "DuskWalker", "Blizzard",
    "DarkMatter", "PulseRanger", "ByteBandit", "CircuitBreaker", "NeonTiger", "LaserBlade",
    "CosmicDancer", "GravityGlitch", "TitanSlayer", "Oblivion", "NightCrawler",
    "EclipseHunter", "VoltSurge", "SonicBoom", "AtomicRhino", "BladeRunner", "CrimsonWolf"
]

# ----------------------------
# ✅ Index Safety Check & Cleanup
# ----------------------------
def check_and_fix_indexes():
    indexes = login_users_collection.index_information()
    if "id_1" in indexes:
        print("⚠️ Removing old 'id' index from login_db.Users...")
        login_users_collection.drop_index("id_1")
        print("✅ 'id' index removed.")

    # Ensure 'username' has a unique index
    existing_indexes = login_users_collection.index_information()
    if not any(index.get("key") == [('username', 1)] for index in existing_indexes.values()):
        print("🔧 Creating unique index on 'username' field...")
        login_users_collection.create_index([("username", 1)], unique=True)
        print("✅ Unique index on 'username' created.")
    else:
        print("✅ Unique index on 'username' already exists.")

# ----------------------------
# Insert Test Users Function
# ----------------------------
def insert_test_users():
    check_and_fix_indexes()  # Ensure login DB indexes are correct before inserting

    selected_names = random.sample(name_pool, 10)

    for name in selected_names:
        # Check if user already exists in either login DB OR game DB:
        login_exists = login_users_collection.find_one({"username": name})
        game_exists = game_users_collection.find_one({"username": name})

        if login_exists or game_exists:
            print(f"⚠️ User '{name}' already exists (login or game DB), skipping.")
            continue

        # -----------------------------
        # Insert into login DB first (get the login ID)
        login_user = {
            "username": name,
            "passkey": hash_passkey("testpassword").decode('utf-8')
        }
        login_result = login_users_collection.insert_one(login_user)
        login_id = login_result.inserted_id  # <--- Grab the login ID!
        print(f"🔗 Created login user '{name}' with login_id: {login_id}")

        # -----------------------------
        # Insert into game DB and link login_id
        game_user = {
            "username": name,
            "login_id": login_id,  # <-- LINK HERE!
            "password": "testpassword",  # Dummy field for testing/demo purposes
            "recycle_coins": random.randint(0, 500),
            "trash_coins": random.randint(0, 1000),
            "waste_coins": random.randint(0, 500),
            "accessories": {
                "hat": None,
                "shirt": None,
                "pants": None,
                "shoes": None,
                "hand_left": None,
                "hand_right": None
            },
            "steps": random.randint(0, 10000),
            "created_at": datetime.datetime.now(timezone.utc)
        }
        game_users_collection.insert_one(game_user)

        print(f"✅ Linked game user '{name}' to login_id '{login_id}'.")

# ----------------------------
if __name__ == "__main__":
    insert_test_users()
