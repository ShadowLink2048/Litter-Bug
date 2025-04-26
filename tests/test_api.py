import requests

BASE_URL = "http://localhost:3001"

def signup_user():
    payload = {
        "username": "testuser",
        "passkey": "strongpassword",
        "firstname": "Test",
        "lastname": "User",
        "email": "test@example.com"
    }
    response = requests.post(f"{BASE_URL}/signup", json=payload)
    print("Signup Response:", response.json())

def login_user():
    payload = {
        "username": "testuser",
        "passkey": "strongpassword"
    }
    response = requests.post(f"{BASE_URL}/login", json=payload)
    print("Login Response:", response.json())
    return response.json().get("tokenid")

def get_user_info(token):
    payload = {
        "username": "testuser",
        "tokenid": token
    }
    response = requests.post(f"{BASE_URL}/userinfo", json=payload)
    print("User Info Response:", response.json())

if __name__ == "__main__":
    signup_user()  # Only run once; comment out if user already exists!
    token = login_user()
    if token:
        get_user_info(token)
