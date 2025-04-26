import requests
import json

# URL of the Flask server endpoint
url = "http://localhost:2001/search"

# Sample data to send in the POST request
payload = {
    "search": "python tutorials",
    "violence": False,
    "sexuality": False,
    "bodynegativity": False,
    "advertisements": False,
    "topic": "programming",
    "last": "python basics"
}

# Headers for the request
headers = {
    "Content-Type": "application/json"
}

try:
    # Make the POST request
    response = requests.post(url, data=json.dumps(payload), headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        print("Success! Response from server:")
        print(response.json())
    else:
        print(f"Failed with status code: {response.status_code}")
        print(response.text)

except requests.exceptions.ConnectionError:
    print("Connection Error: Could not connect to the server. Ensure the Flask app is running on http://localhost:2001.")
except Exception as e:
    print(f"An error occurred: {str(e)}")
