import requests

# Replace with the path to an actual image you want to test with
image_path = 'trashbin.jpg'

url = 'http://localhost:2001/throwgarbage'

# Prepare the payload
data = {
    'id': '1',  # Example player ID
    'points': '10'
}

files = {
    'image': open(image_path, 'rb')
}

# Send POST request
response = requests.post(url, data=data, files=files)

# Print response for testing purposes
print('Status Code:', response.status_code)
print('Response JSON:', response.json())
