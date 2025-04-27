
# 🗑️ Litter-Bug Database Setup and API

This project is the backend database and API layer for the **Litter-Bug mobile app**, a game similar to Pokémon GO but focused on cleaning up trash and recycling in the real world.

This README documents the MongoDB setup, utilities, test scripts, and API endpoints used in the project.

---

## 📂 Project Structure
Litter-Bug/
├── database_py_files/
│   ├── db_setup.py           # Sets up database collections and schema validation
│   ├── db_utils.py           # Utility functions for inserting users, bins, trash
│   ├── server.py             # Flask API server with endpoints (including leaderboard)
│   ├── test_insert_users.py  # Test script to insert showcase-ready test users
├── README.md                 # This documentation file

---

## ⚙️ Database: MongoDB Structure

### Database Name:
litterbug_db

### Collections and Schemas:

#### 🟢 Users Collection
- Fields:
  - username: string (unique)
  - password: string (hashed)
  - recycle_coins: int
  - trash_coins: int (used for leaderboard ranking)
  - waste_coins: int
  - equipment: object
    - hat, shirt, pants, shoes, hand_left, hand_right: string or null
  - steps: int
  - created_at: datetime

Unique index on username to prevent duplicate accounts.

---

#### 🟡 Bins Collection
- Fields:
  - longitude: float
  - latitude: float
  - type: "trash" or "recycle"

---

#### 🔴 Trash Collection
- Fields:
  - longitude: float
  - latitude: float
  - type: "trash" or "recycle"
  - dropped_by: string (optional)
  - picked_up_by: string (optional)
  - is_collected: bool
  - timestamp: datetime

---

## 🚀 Files and Their Purposes

### 📌 db_setup.py
- Creates the MongoDB collections.
- Applies JSON schema validation to enforce field types.
- Adds a unique index on username in the Users collection.
- Run this file once at the start to prepare the database:
  python db_setup.py

---

### ⚒️ db_utils.py
- Contains utility functions:
  - insert_user(username, password_plaintext)
  - insert_bin(longitude, latitude, bin_type)
  - insert_trash(longitude, latitude, trash_type, dropped_by=None)
- Handles duplicate prevention for user insertion.

---

### 🧩 test_insert_users.py
- Inserts 10 showcase-ready test users into the Users collection.
- Uses a pool of 100 realistic and gamer-style names.
- Randomizes:
  - trash_coins
  - recycle_coins
  - waste_coins
  - steps
- Run this separately:
  python test_insert_users.py

---

### 🌐 server.py (Flask API Server)
- Hosts the REST API for the project.
- Current Endpoint:
  - GET /api/users/top-trash-scores
    Returns the Top 10 users sorted by trash_coins (leaderboard).
- Example Response:
  {
    "leaderboard": [
      {"username": "NeonTiger", "trash_coins": 985},
      {"username": "Hannah", "trash_coins": 920}
    ],
    "message": "Top 10 trash token scores"
  }

---

## ✅ How to Run the Project

1. Ensure MongoDB is running (localhost:27017).
2. Run db_setup.py to create your collections and apply schema validation:
   python db_setup.py
3. (Optional) Insert test users:
   python test_insert_users.py
4. Start your Flask API server:
   python server.py
5. Access the leaderboard:
   http://localhost:<your-port>/api/users/top-trash-scores

---

## 🛡️ Future Improvements
- Add login/authentication endpoints (with bcrypt password checks).
- Add endpoints for user updates, trash collection, and bin interaction.
- Include cleanup scripts for test data.
- Expand leaderboard to support dynamic sorting/filtering.

---

## 🏆 Hackathon Showcase Ready!
This setup is designed for rapid testing and demonstration at the UW 2025 Hackathon "Save the World" event.
