import requests
import json

# URL of your local API server
API_URL = 'http://127.0.0.1:5000/signup'

# Test data for creating a user
user_data = {
    "username": "testuser1",
    "passkey": "testpassword123",
    "email": "testuser1@example.com",
    "firstname": "Test",
    "lastname": "User"
}

# Make the POST request to create the user
response = requests.post(API_URL, json=user_data)

# Check the response status code
if response.status_code == 201:
    print("User created successfully!")
else:
    print(f"Error: {response.status_code} - {response.text}")
