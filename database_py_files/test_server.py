import requests

BASE_URL = "http://localhost:3001"

# Test account info
username = "testuser"
passkey = "strongpassword"
email = "testuser@example.com"
firstname = "Test"
lastname = "User"


# -------------------------
# 1. Signup (Optional if user exists)
# -------------------------
def signup():
    print("📩 Testing signup...")
    payload = {
        "username": username,
        "passkey": passkey,
        "firstname": firstname,
        "lastname": lastname,
        "email": email
    }
    response = requests.post(f"{BASE_URL}/signup", json=payload)
    print("Signup Response:", response.status_code, response.json())


# -------------------------
# 2. Login
# -------------------------
def login():
    print("\n🔐 Testing login...")
    payload = {"username": username, "passkey": passkey}
    response = requests.post(f"{BASE_URL}/login", json=payload)
    print("Login Response:", response.status_code, response.json())
    return response.json().get("tokenid")


# -------------------------
# 3. Check user info (token test)
# -------------------------
def check_userinfo(token):
    print("\n👤 Testing userinfo...")
    payload = {"username": username, "tokenid": token}
    response = requests.post(f"{BASE_URL}/userinfo", json=payload)
    print("User Info Response:", response.status_code, response.json())


# -------------------------
# 4. Test adding a bin
# -------------------------
def add_bin(token):
    print("\n🗑️ Testing add_bin...")
    payload = {
        "username": username,
        "tokenid": token,
        "longitude": -122.335167,
        "latitude": 47.608013,
        "type": "recycle"
    }
    response = requests.post(f"{BASE_URL}/api/bins/add", json=payload)
    print("Add Bin Response:", response.status_code, response.json())


# -------------------------
# 5. Test adding trash
# -------------------------
def add_trash(token):
    print("\n🚮 Testing add_trash...")
    payload = {
        "username": username,
        "tokenid": token,
        "longitude": -122.334567,
        "latitude": 47.609123,
        "type": "trash"
    }
    response = requests.post(f"{BASE_URL}/api/trash/add", json=payload)
    print("Add Trash Response:", response.status_code, response.json())


# -------------------------
# Run Tests
# -------------------------
if __name__ == "__main__":
    try:
        signup()  # Comment out if user already exists
    except Exception as e:
        print("⚠️ Signup may have failed (user may already exist):", e)

    token = login()
    if token:
        check_userinfo(token)
        add_bin(token)
        add_trash(token)
    else:
        print("❌ Login failed, cannot proceed with token-based tests.")
