from flask import Flask, jsonify, request



from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId

from pymongo.errors import OperationFailure, ServerSelectionTimeoutError
import threading
import time
from datetime import datetime, timedelta
import random
import string

import bcrypt

# Method to hash a password
def hash_passkey(passkey):
    salt = bcrypt.gensalt()  # Generate a salt
    hashed_passkey = bcrypt.hashpw(passkey.encode('utf-8'), salt)  # Hash the password and return as bytes
    return hashed_passkey

# Method to check if a password matches the hash
def check_hash_match(passkey, stored_hash):
    # Convert passkey to bytes
    passkey_bytes = passkey.encode('utf-8')  # Convert passkey (string) to bytes
    
    # Ensure the stored hash is already in bytes, it should be by default
    if isinstance(stored_hash, str):  # If stored_hash is a string, convert it to bytes
        stored_hash = stored_hash.encode('utf-8')
    
    # Check if the hashed passkey matches the stored hash
    if bcrypt.checkpw(passkey_bytes, stored_hash):  # stored_hash is in bytes
        print("Password matches!", flush=True)
        return True
    
    print("Password not a match", flush=True)
    return False

# Instantiate Flask app
app = Flask(__name__)
CORS(app)

# Set the port for the Flask server
app.config['SERVER_PORT'] = 3001

print("Instantiated flask app.")  

# MongoDB connection
client = MongoClient('mongodb://account-db:3000/')
db = client['account-db']
collection = db['users']

print("Connected to MongoDB server.")  

# Logged in users
logged_in = {}

# Generates random token for user login
def generate_token():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=16))

# Add user to logged in dictionary
def add_logged_in_user(username):
    logged_in[username] = { 'tokenid': generate_token(), 'token_expiry': datetime.now() + timedelta(hours=24) }

def check_logged_in_user(username):
    return username in logged_in

# Function to check for expired tokens
def check_expired_token(username):
    current_time = datetime.now()
    print(f"Checking for expired tokens...{datetime.now()}")  # Debug statement to show the function is running
    user = logged_in[username]

    if user['token_expiry'] < current_time:
        logged_in.remove(user)
        print(f"Token for user {username} has expired. Removing from logged in users.")
        return True
    return False

def check_user_by_token(token):
    #find username with the associated token from logged_in
    for username, info in logged_in.items():
        if info['tokenid'] == token:
            # Check if the token has expired
            if check_expired_token(username):
                return None
            
            #Fetch user from the database
            user = collection.find_one({'username': username})
            if user:
                user.pop('_id', None)
                user.pop('passkey', None)
                return user
    return None



@app.route('/userinfo', methods=['POST'])
def userinfo():
    data = request.get_json()
    print(data)

    if not data or not data.get('tokenid') or not data.get('username'):
        return jsonify({'error': 'Missing required inputs'}), 400

    if check_expired_token(data['username']):
        return jsonify({'error': 'Token expired, please log in again'}), 401

    try:
        # Check if the token is expired or invalid
        if logged_in[data['username']]['tokenid'] != data['tokenid']:
            return jsonify({'error': 'Invalid token, need to log in again'}), 401
        
        # Retrieve user information from the database
        user = collection.find_one({'username': data['username']})
        
        # If user not found, return an error message
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Delete the _id field from the user dictionary to avoid exposing it in the API response
        del user["_id"]
        del user['passkey']
        
        return jsonify(user), 201
    except (OperationFailure, ServerSelectionTimeoutError) as e:
        return jsonify({'error': str(e)}), 500

# Log in user
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    print(data, flush=True)

    # Check if required inputs are provided
    if not data or not data.get('username') or not data.get('passkey'):
        return jsonify({'error': 'Missing required inputs'}), 400

    try:
        # Check if a user exists
        user = collection.find_one({'username': data['username']})
        print(user, flush=True)

        # Check if a passkey is correct
        print(data['passkey'], user['passkey'], flush=True)  # Debug statement to check passkey and stored hash

        if not check_hash_match(data['passkey'], user['passkey']):
            return jsonify({'error': 'Invalid username or passkey'}), 401

        # Add user to logged-in dictionary
        add_logged_in_user(data['username'])

        # Retrieve generated token
        generated_token = logged_in[data['username']]['tokenid']
        
        # Return a success message to a user
        return jsonify({'success': "User will be logged in for 24 hours", 'tokenid': generated_token}), 201
    except (OperationFailure, ServerSelectionTimeoutError) as e:
        return jsonify({'error': str(e)}), 500

# Log in user
@app.route('/signup', methods=['POST'])
def signup():
    
    data = request.get_json()
    print(data, flush=True)

    # Check if required inputs are provided
    if not data or not data.get('username') or not data.get('passkey'):
        return jsonify({'error': 'Missing required inputs'}), 400

    try:
        # Check if user/email exists
        user_exists = collection.find_one({'username': data['username']}) if 'username' in data else None
        email_exists = collection.find_one({'email': data['email']}) if 'email' in data else None
        
        if user_exists or email_exists:
            # If a user exists, return an error message
            return jsonify({'error': 'Username already exists'}), 409
        
        # Check if the passkey qualifies
        if not isinstance(data['passkey'], str) or len(data['passkey']) < 8:
            return jsonify({'error': 'Passkey does not qualify. It must be a string with a minimum length of 8 characters'}), 401

        # hash the passcode
        hashed_passkey = hash_passkey(data['passkey'])

        # Insert a new user into the database
        new_user = {
            'username': data['username'],
            'firstname': data.get('firstname', ''),  # Optional field, default to empty string if not provided
            'lastname': data.get('lastname', ''),    # Optional field, default to empty string if not provided
            'passkey': hashed_passkey.decode('utf-8'),
            'email': data.get('email', '')           # Optional field, default to empty string if not provided
        }
        collection.insert_one(new_user)
        
        # Return a success message to user
        return jsonify({'success': f"{data['username']} must now log in"}), 201
    except (OperationFailure, ServerSelectionTimeoutError) as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=app.config['SERVER_PORT'])

 