# api_server.py (inside database_py_files)
from flask import Flask, jsonify, request
from flask_cors import CORS
from db_utils import export_users_to_json
from geo_utils import get_bins_within_radius, get_trash_within_radius
from login_utils_db import get_user_profile, game_db
from login_utils_db import hash_passkey, check_hash_match, add_logged_in_user, logged_in, collection
from pymongo import MongoClient
from bson import ObjectId
from math import radians, cos, sin, sqrt, atan2
import subprocess
import os
import bcrypt
import datetime

app = Flask(__name__)
CORS(app)

client = MongoClient('mongodb://localhost:27017/')
db = client['litter_bug_db']
users_collection = db['Users']
trash_collection = db['Trash']
bins_collection = db['Bins']

DB_SETUP_FLAG = "DB_SETUP_COMPLETE.flag"

def run_db_setup():
    try:
        print("🔧 Running database setup script...")
        subprocess.run(["python", "setup_all.py"], check=True)
        with open(DB_SETUP_FLAG, "w") as flag_file:
            flag_file.write("Database setup completed.")
        print("✅ Database setup completed successfully.")
    except subprocess.CalledProcessError as e:
        print("❌ Database setup failed:", e)

if not os.path.exists(DB_SETUP_FLAG):
    run_db_setup()

@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Litter-Bug API is running!'}), 200

# -----------------------------
# PROFILE CREATION / FETCH (LOGIN DB ONLY)
# -----------------------------
@app.route('/api/profile', methods=['POST'])
def create_or_get_profile():
    data = request.get_json()
    username = data.get('username')
    if not username:
        return jsonify({'error': 'Missing username'}), 400
    profile = get_user_profile(username)
    if profile:
        return jsonify({'profile': profile}), 200
    else:
        return jsonify({'error': 'User not found in login_db'}), 404

# -----------------------------
# GET FULL USER INFO BY MONGODB _id (GAME DB)
# -----------------------------
@app.route('/api/users/get-by-id', methods=['POST'])
def get_user_by_id():
    data = request.get_json()
    user_id = data.get('user_id')

    if not user_id:
        return jsonify({'error': 'Missing user_id'}), 400

    try:
        user = users_collection.find_one({'_id': ObjectId(user_id)})
        if user:
            user['_id'] = str(user['_id'])
            user.pop('passkey', None)
            return jsonify({'user': user}), 200
        else:
            return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        return jsonify({'error': f'Invalid ID format or server error: {str(e)}'}), 500

# -----------------------------
# EXPORT USERS TO JSON
# -----------------------------
@app.route('/api/users/export', methods=['GET'])
def export_users():
    try:
        export_users_to_json()
        return jsonify({'success': 'Users exported to users_export.json'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# -----------------------------
# GET NEARBY BINS
# -----------------------------
@app.route('/api/bins/nearby', methods=['POST'])
def get_nearby_bins():
    data = request.get_json()
    lon, lat, radius = data.get('longitude'), data.get('latitude'), data.get('radius')
    if None in (lon, lat, radius):
        return jsonify({'error': 'Missing longitude, latitude, or radius'}), 400
    bins = get_bins_within_radius(lon, lat, radius)
    return jsonify({'bins': bins}), 200

# -----------------------------
# GET NEARBY TRASH
# -----------------------------
@app.route('/api/trash/nearby', methods=['POST'])
def get_nearby_trash():
    data = request.get_json()
    lon, lat, radius = data.get('longitude'), data.get('latitude'), data.get('radius')
    if None in (lon, lat, radius):
        return jsonify({'error': 'Missing longitude, latitude, or radius'}), 400
    trash = get_trash_within_radius(lon, lat, radius)
    return jsonify({'trash': trash}), 200

# -----------------------------
# SIGNUP (USER REGISTRATION)
# -----------------------------
@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username, passkey = data.get('username'), data.get('passkey')
    email, firstname, lastname = data.get('email', ''), data.get('firstname', ''), data.get('lastname', '')

    # Check for required fields
    if not username or not passkey:
        return jsonify({'error': 'Missing required inputs'}), 400

    # Check if the username or email already exists
    if collection.find_one({'username': username}) or (email and collection.find_one({'email': email})):
        return jsonify({'error': 'Username or email already exists'}), 409

    # Hash the passkey (password)
    if len(passkey) < 8:
        return jsonify({'error': 'Passkey must be at least 8 characters'}), 401
    hashed_passkey = hash_passkey(passkey).decode('utf-8')

    # Insert into the login DB (first)
    new_login_user = {
        'username': username,
        'firstname': firstname,
        'lastname': lastname,
        'passkey': hashed_passkey,
        'email': email
    }
    login_result = collection.insert_one(new_login_user)  # Insert into login DB
    login_id = login_result.inserted_id  # Retrieve the login ID

    # Insert into the game DB (second), linking the login ID
    new_game_user = {
        "username": username,
        "login_id": login_id,  # Link to login DB
        "recycle_coins": 0,
        "trash_coins": 0,
        "waste_coins": 0,
        "accessories": {
            "hat": None,
            "shirt": None,
            "pants": None,
            "shoes": None,
            "hand_left": None,
            "hand_right": None
        },
        "steps": 0,
        "created_at": datetime.datetime.now(datetime.timezone.utc)
    }
    users_collection.insert_one(new_game_user)  # Insert into game DB

    return jsonify({'success': f"{username} must now log in"}), 201


# -----------------------------
# LOGIN
# -----------------------------
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username, passkey = data.get('username'), data.get('passkey')
    if not username or not passkey:
        return jsonify({'error': 'Missing required inputs'}), 400
    user = collection.find_one({'username': username})
    if not user or not check_hash_match(passkey, user['passkey']):
        return jsonify({'error': 'Invalid username or passkey'}), 401
    add_logged_in_user(username)
    token = logged_in[username]['tokenid']
    get_user_profile(username)
    return jsonify({'success': "User logged in", 'tokenid': token}), 201

# -----------------------------
# USERINFO (TOKEN CHECK)
# -----------------------------
@app.route('/userinfo', methods=['POST'])
def userinfo():
    data = request.get_json()
    username, tokenid = data.get('username'), data.get('tokenid')
    if not username or not tokenid:
        return jsonify({'error': 'Missing required inputs'}), 400
    if username not in logged_in or logged_in[username]['tokenid'] != tokenid:
        return jsonify({'error': 'Invalid token or user not logged in'}), 401
    user = collection.find_one({'username': username})
    if user:
        user.pop('_id', None)
        user.pop('passkey', None)
        return jsonify(user), 200
    return jsonify({'error': 'User not found'}), 404

# -----------------------------
# USER UPDATE (PATCH user data)
# -----------------------------
@app.route('/api/users/update/<username>', methods=['PATCH'])
def update_user(username):
    data = request.get_json()
    tokenid = data.get('tokenid')
    if username not in logged_in or logged_in[username]['tokenid'] != tokenid:
        return jsonify({'error': 'Invalid token or user not logged in'}), 401
    update_fields = {field: data[field] for field in ['recycle_coins', 'trash_coins', 'waste_coins', 'steps', 'equipment'] if field in data}
    if not update_fields:
        return jsonify({'error': 'No valid fields provided for update.'}), 400
    result = users_collection.update_one({'username': username}, {'$set': update_fields})
    if result.matched_count == 0:
        return jsonify({'error': 'User not found.'}), 404
    return jsonify({'success': f'User {username} updated successfully.'}), 200

# -----------------------------
# TRASH COLLECTION (pick up trash)
# -----------------------------
@app.route('/api/trash/collect', methods=['POST'])
def collect_trash():
    data = request.get_json()
    username, tokenid, trash_id = data.get('username'), data.get('tokenid'), data.get('trash_id')
    if username not in logged_in or logged_in[username]['tokenid'] != tokenid:
        return jsonify({'error': 'Invalid token or user not logged in'}), 401
    if not trash_id:
        return jsonify({'error': 'Missing trash_id.'}), 400
    trash_item = game_db.Trash.find_one({'_id': ObjectId(trash_id)})
    if not trash_item:
        return jsonify({'error': 'Trash item not found.'}), 404
    if trash_item.get('is_collected'):
        return jsonify({'error': 'Trash has already been collected.'}), 409
    game_db.Trash.update_one({'_id': ObjectId(trash_id)}, {'$set': {'is_collected': True, 'picked_up_by': username}})
    users_collection.update_one({'username': username}, {'$inc': {'trash_coins': 10}})
    return jsonify({'success': f'Trash {trash_id} collected by {username}. 10 trash coins awarded!'}), 200

# -----------------------------
# LEADERBOARD
# -----------------------------
@app.route('/api/users/top-trash-scores', methods=['GET'])
def get_top_trash_scores():
    try:
        top_users = users_collection.find({}, {'username': 1, 'trash_coins': 1, '_id': 0}).sort('trash_coins', -1).limit(10)
        result = [{'username': user.get('username'), 'trash_coins': user.get('trash_coins', 0)} for user in top_users]
        return jsonify({'leaderboard': result, 'message': 'Top 10 trash token scores'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

#score board info
#http://localhost:5000/api/users/top-trash-scores