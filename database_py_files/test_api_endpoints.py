import requests
import random
import string

from database_py_files.api_server import trash_collection

# API URLs
API_URL_SIGNUP = "http://127.0.0.1:5000/signup"
API_URL_LOGIN = "http://127.0.0.1:5000/login"
API_URL_PROFILE = "http://127.0.0.1:5000/api/profile"
API_URL_USER_INFO = "http://127.0.0.1:5000/userinfo"
API_URL_UPDATE_USER = "http://127.0.0.1:5000/api/users/update/"
API_URL_TRASH_COLLECTION = "http://127.0.0.1:5000/api/trash/collect"

# Helper functions
def random_string(length=8):
    """Generate a random string of given length."""
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))


def handle_response(response, action):
    """Handles the response for the tests, prints status code and JSON data."""
    print(f"{action} response status code: {response.status_code}")
    try:
        response_json = response.json()
        print(f"{action} response JSON: {response_json}")
        return response_json
    except ValueError:
        print(f"{action} response is not in JSON format. Response text: {response.text}")
        return None


def test_signup():
    """Test signup functionality by creating a new user."""
    username = random_string(10)
    passkey = random_string(12)  # Ensure it's at least 8 characters long
    new_user_data = {
        "username": username,
        "passkey": passkey,
        "email": f"{username}@example.com",
        "firstname": "Test",
        "lastname": "User"
    }

    print(f"\nTesting Signup with username: {username} and passkey: {passkey}...")
    response_signup = requests.post(API_URL_SIGNUP, json=new_user_data)
    response_json = handle_response(response_signup, "Signup")

    if response_signup.status_code == 201:
        print(f"User created successfully! User ID: {response_json.get('user_id')}")
        return username, passkey  # Return username and passkey for login
    else:
        print(f"Signup failed: {response_signup.status_code} - {response_json}")
        return None, None


def test_login():
    """Test login functionality after signup."""
    username, passkey = test_signup()  # Get username and passkey from signup
    if not username or not passkey:
        print("Skipping login due to failed signup.")
        return None, None

    login_data = {
        "username": username,
        "passkey": passkey
    }

    print("\nTesting Login...")
    response_login = requests.post(API_URL_LOGIN, json=login_data)
    response_json = handle_response(response_login, "Login")

    if response_login.status_code == 201:
        print("Login successful!")
        tokenid = response_json.get("tokenid")
        return tokenid, username  # Return token and username
    else:
        print(f"Login failed: {response_login.status_code} - {response_json}")
        return None, None


def test_create_or_get_profile(username, tokenid):
    """Test fetching user profile."""
    if not username or not tokenid:
        print("Skipping profile fetch due to login failure.")
        return

    profile_data = {"username": username}
    headers = {"Authorization": f"Bearer {tokenid}"}

    print(f"\nTesting profile fetch for username: {username}")
    response_profile = requests.post(API_URL_PROFILE, json=profile_data, headers=headers)
    response_json = handle_response(response_profile, "Profile fetch")

    if response_profile.status_code == 200:
        print("Profile fetch successful!")
    else:
        print(f"Profile fetch failed: {response_profile.status_code} - {response_json}")


def test_user_info(username, tokenid):
    """Test fetching user info."""
    if not username or not tokenid:
        print("Skipping user info fetch due to login failure.")
        return

    user_info_data = {"username": username, "tokenid": tokenid}
    headers = {"Authorization": f"Bearer {tokenid}"}

    print("\nTesting User Info fetch...")
    response_user_info = requests.post(API_URL_USER_INFO, json=user_info_data, headers=headers)
    response_json = handle_response(response_user_info, "User Info fetch")

    if response_user_info.status_code == 200:
        print("User info fetched successfully!")
    else:
        print(f"User info fetch failed: {response_user_info.status_code} - {response_json}")


def test_update_user(username, tokenid):
    """Test updating user information."""
    if not username or not tokenid:
        print("Skipping user update due to login failure.")
        return

    update_data = {
        "tokenid": tokenid,
        "recycle_coins": 100,
        "trash_coins": 200,
        "waste_coins": 50,
        "steps": 5000
    }
    headers = {"Authorization": f"Bearer {tokenid}"}

    print(f"\nTesting User update for username: {username}...")
    response_update = requests.patch(f"{API_URL_UPDATE_USER}{username}", json=update_data, headers=headers)
    response_json = handle_response(response_update, "User update")

    if response_update.status_code == 200:
        print(f"User {username} updated successfully!")
    else:
        print(f"User update failed: {response_update.status_code} - {response_json}")


def create_new_trash_item():
    """Create a new trash item with is_collected set to False."""
    new_trash = {
        "location": {"type": "Point", "coordinates": [random.uniform(-180, 180), random.uniform(-90, 90)]},  # Random geolocation
        "type": "recycle",  # Or "trash"
        "is_collected": False,
        "collected_by": None
    }
    result = trash_collection.insert_one(new_trash)
    return str(result.inserted_id)  # Return the ID of the newly created trash item

def get_uncollected_trash_item():
    """Get an uncollected trash item from the database."""
    trash_item = trash_collection.find_one({"is_collected": False})  # Find an uncollected trash item
    if trash_item:
        return str(trash_item["_id"])  # Return the ID of the uncollected trash item
    else:
        return None  # No uncollected trash item found


def test_trash_collection(username, tokenid):
    # Get an uncollected trash item from the database
    trash_id = get_uncollected_trash_item()

    if not trash_id:
        print("No uncollected trash items found in the database.")
        return

    data = {
        'username': username,
        'tokenid': tokenid,
        'trash_id': trash_id
    }

    response = requests.post(API_URL_TRASH_COLLECTION, json=data)

    try:
        response_json = response.json()  # Parse response into JSON
        print(f"Trash collection response status code: {response.status_code}")
        print(f"Trash collection response JSON: {response_json}")
    except ValueError:
        print(f"Error parsing JSON response: {response.text}")

    if response.status_code == 200:
        print("Trash collected successfully!")
    else:
        print(f"Trash collection failed: {response.status_code} - {response_json}")


def test_leaderboard():
    """Test the leaderboard functionality (Top Trash Scores)."""
    print("\nTesting Leaderboard (Top Trash Scores)...")

    response_leaderboard = requests.get("http://127.0.0.1:5000/api/users/top-trash-scores")

    # Handle response
    response_json = handle_response(response_leaderboard, "Leaderboard")

    if response_leaderboard.status_code == 200:
        print("Leaderboard fetched successfully!")
        print("Top 10 users:")
        for rank, user in enumerate(response_json['leaderboard'], 1):
            print(f"{rank}. {user['username']} - {user['trash_coins']} trash coins")
    else:
        print(f"Leaderboard fetch failed: {response_leaderboard.status_code} - {response_json}")


def run_tests():
    """Run all tests in sequence."""
    print("Starting tests...\n")

    # Test Signup and Login
    username, passkey = test_signup()  # Username and passkey from signup

    # Test Login
    if username and passkey:
        tokenid, username = test_login()  # No arguments required
        if tokenid:
            print("Login successful!")
        else:
            print("Login failed.")

    # Test Profile Fetch
    if username and tokenid:
        test_create_or_get_profile(username, tokenid)

    # Test User Info Fetch
    if username and tokenid:
        test_user_info(username, tokenid)

    # Test Update User
    if username and tokenid:
        test_update_user(username, tokenid)

    # Test Trash Collection (fetching an uncollected trash item from the DB)
    if username and tokenid:
        test_trash_collection(username, tokenid)

    # Test Leaderboard (Top Trash Scores)
    test_leaderboard()  # Fetch and print top 10 leaderboard

if __name__ == "__main__":
    run_tests()

