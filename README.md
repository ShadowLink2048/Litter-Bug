
# 🗑️ Litter-Bug Database Setup and API

**Litter-Bug** is a mobile application inspired by Pokémon GO, designed to encourage users to collect and properly dispose of litter. This backend API server supports user management, trash collection tracking, bin interaction, and leaderboards.

---

## 📂 Project Structure

```
Litter-Bug/
├── database_py_files/
│   ├── api_server.py         # Main Flask API server with user auth, trash collection, bin interaction
│   ├── db_setup.py           # Sets up MongoDB collections and schema validation
│   ├── db_utils.py           # Utility functions for inserting users, bins, trash
│   ├── test_insert_users.py  # Test script to insert showcase-ready test users
├── public/                   # Static assets
├── src/                      # Source code for the app frontend
├── README.md                 # This documentation file
```

---

## ⚙️ Database: MongoDB Structure

### Database Name:
```
litterbug_db
```

### Collections and Schemas:

#### 🟢 Users Collection
- Fields:
  - `username`: string (unique)
  - `password`: string (hashed)
  - `recycle_coins`: int
  - `trash_coins`: int
  - `waste_coins`: int (walk coins)
  - `equipment`: object
    - `hat`, `shirt`, `pants`, `shoes`, `hand_left`, `hand_right`: string or null
  - `steps`: int
  - `created_at`: datetime

#### 🟡 Bins Collection
- Fields:
  - `longitude`: float
  - `latitude`: float
  - `type`: "trash" or "recycle"

#### 🔴 Trash Collection
- Fields:
  - `longitude`: float
  - `latitude`: float
  - `type`: "trash" or "recycle"
  - `dropped_by`: string (optional)
  - `picked_up_by`: string (optional)
  - `is_collected`: bool
  - `timestamp`: datetime

---

## 🌐 API Endpoints Overview

### Authentication and User Management
- **POST /signup** — User registration with password hashing.
- **POST /login** — Login with bcrypt password checking, returns token.
- **POST /userinfo** — Token validation, fetch user info.
- **PATCH /api/users/update/<username>** — Update user coins, steps, or equipment (requires token).

### Trash and Bin Management
- **POST /api/bins/add** — Add a new bin (requires token).
- **POST /api/trash/add** — Add a new trash item (requires token).
- **POST /api/trash/collect** — Mark trash as collected, assign to a user, award trash coins (requires token).

### Location Queries
- **POST /api/bins/nearby** — Get nearby bins based on coordinates and radius.
- **POST /api/trash/nearby** — Get nearby trash items.

### Leaderboard
- **GET /api/users/top-trash-scores** — Returns Top 10 users ranked by trash token score.

---

## 🏗️ Example Payloads

### Signup Example:
```json
{
  "username": "EcoWarrior",
  "passkey": "securepassword123",
  "email": "eco@example.com",
  "firstname": "Eco",
  "lastname": "Warrior"
}
```

### Login Example:
```json
{
  "username": "EcoWarrior",
  "passkey": "securepassword123"
}
```

### Update User Example:
```json
{
  "tokenid": "your_user_token_here",
  "recycle_coins": 10,
  "waste_coins": 5,
  "steps": 1000
}
```

---

## 🧪 Running the Project

1. Ensure MongoDB is running (`localhost:27017`).
2. Run `db_setup.py` to create your collections and apply schema validation:
   ```bash
   python db_setup.py
   ```
3. (Optional) Insert test users:
   ```bash
   python test_insert_users.py
   ```
4. Start your Flask API server:
   ```bash
   python api_server.py
   ```
5. Access the leaderboard or other endpoints via `http://localhost:5000`.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 👥 Authors

- Katherine Rodli  
- Jack Gardner  
- Dominic H-T  
- Morgan  
- Bryan Harris  

> Special thanks to the team for their contributions to the UW 2025 Hackathon "Save the World" project.
