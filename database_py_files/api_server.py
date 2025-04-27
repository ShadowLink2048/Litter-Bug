# api_server.py (inside database_py_files)

from flask import Flask, jsonify, request
from flask_cors import CORS
from db_utils import export_users_to_json
from geo_utils import get_bins_within_radius, get_trash_within_radius
from login_utils_db import get_user_profile, game_db
from login_utils_db import hash_passkey, check_hash_match, add_logged_in_user, logged_in, collection

app = Flask(__name__)
CORS(app)

# -----------------------------
# General API Health Check
# -----------------------------
@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Litter-Bug API is running!'}), 200

# -----------------------------
# PROFILE CREATION / FETCH
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
@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    print("🟢 Received signup request with data:", data)  # Debug line

    username = data.get('username')
    passkey = data.get('passkey')
    email = data.get('email', '')
    firstname = data.get('firstname', '')
    lastname = data.get('lastname', '')

    if not username or not passkey:
        print("❌ Missing required inputs!")
        return jsonify({'error': 'Missing required inputs'}), 400

    print("🔍 Checking for existing user...")
    print("📂 Collection object being used:", collection)

    user_exists = collection.find_one({'username': username})
    email_exists = collection.find_one({'email': email}) if email else None

    print("🟠 User exists check:", user_exists)
    print("🟠 Email exists check:", email_exists)

    if user_exists or email_exists:
        print("⚠️ Username or email already exists!")
        return jsonify({'error': 'Username or email already exists'}), 409

    if not isinstance(passkey, str) or len(passkey) < 8:
        print("❌ Passkey too short!")
        return jsonify({'error': 'Passkey must be at least 8 characters'}), 401

    hashed_passkey = hash_passkey(passkey).decode('utf-8')
    new_user = {
        'username': username,
        'firstname': firstname,
        'lastname': lastname,
        'passkey': hashed_passkey,
        'email': email
    }

    print("✅ Inserting new user into DB:", new_user)
    result = collection.insert_one(new_user)
    print("🟢 Insert result ID:", result.inserted_id)

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
# Add bins
# -----------------------------
@app.route('/api/bins/add', methods=['POST'])
@app.route('/api/bins/add', methods=['POST'])
def add_bin():
    data = request.get_json()
    username = data.get('username')
    tokenid = data.get('tokenid')
    lon = data.get('longitude')
    lat = data.get('latitude')
    bin_type = data.get('type')

    # Check for missing inputs
    if None in (username, tokenid, lon, lat, bin_type):
        return jsonify({'error': 'Missing required inputs'}), 400

    # Validate token
    if username not in logged_in or logged_in[username]['tokenid'] != tokenid:
        return jsonify({'error': 'Invalid token or user not logged in'}), 401

    # Validate bin type
    if bin_type not in ['recycle', 'trash']:
        return jsonify({'error': 'Invalid type. Must be "recycle" or "trash"'}), 400

    bin_doc = {
        "longitude": lon,  # NOT location!
        "latitude": lat,  # Direct values
        "type": bin_type
    }

    try:
        result = game_db.Bins.insert_one(bin_doc)
        return jsonify({'success': 'Bin added', 'bin_id': str(result.inserted_id)}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# -----------------------------
# Add Trash
# -----------------------------

@app.route('/api/trash/add', methods=['POST'])
@app.route('/api/trash/add', methods=['POST'])
def add_trash():
    data = request.get_json()
    username = data.get('username')
    tokenid = data.get('tokenid')
    lon = data.get('longitude')
    lat = data.get('latitude')
    trash_type = data.get('type')

    if None in (username, tokenid, lon, lat, trash_type):
        return jsonify({'error': 'Missing required inputs'}), 400

    if username not in logged_in or logged_in[username]['tokenid'] != tokenid:
        return jsonify({'error': 'Invalid token or user not logged in'}), 401

    if trash_type not in ['recycle', 'trash']:
        return jsonify({'error': 'Invalid type. Must be "recycle" or "trash"'}), 400

    from datetime import datetime

    trash_doc = {
        "longitude": lon,
        "latitude": lat,
        "type": trash_type,
        "is_collected": False,  # Default value
        "timestamp": datetime.utcnow(),  # Current UTC time
        "dropped_by": username,  # Optional, but helpful!
        "picked_up_by": None  # Not picked up yet
    }

    try:
        result = game_db.Trash.insert_one(trash_doc)
        return jsonify({'success': 'Trash item added', 'trash_id': str(result.inserted_id)}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500



# -----------------------------
# Run the server
# -----------------------------
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3001)
