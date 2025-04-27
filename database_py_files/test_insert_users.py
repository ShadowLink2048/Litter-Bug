from pymongo import MongoClient
import random
import datetime
from datetime import timezone

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['litter_bug_db']
users_collection = db['Users']

# 🎯 Use a list of real names in game names and fantasy names for showcase/demo
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



def insert_test_users():
    """Inserts 10 test users with random real first names and random trash_coins values."""
    test_users = []
    selected_names = random.sample(name_pool, 10)  # Pick 10 unique names

    for name in selected_names:
        trash_coins = random.randint(0, 1000)
        test_user = {
            "username": name,
            "password": "testpassword",  # Dummy password (would be hashed in real cases)
            "recycle_coins": random.randint(0, 500),
            "trash_coins": trash_coins,
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
        test_users.append(test_user)

    users_collection.insert_many(test_users)
    print("✅ Inserted 10 showcase-ready test users with real names and random trash token scores.")


if __name__ == "__main__":
    insert_test_users()
