import requests

# Replace with your actual server URL if needed
SERVER_URL = 'http://localhost:2001/grabgarbage'

# Replace with the path to your image
IMAGE_PATH = 'test.png'

def send_image(image_path, player_id, player_lat, player_lon):
    # Open the image file in binary mode
    with open(image_path, 'rb') as img_file:
        # Prepare the file and form data
        files = {'image': img_file}
        data = {'id': player_id}
        
        try:
            # Send the POST request with the file and data
            response = requests.post(SERVER_URL, files=files, data=data)
            
            # Raise an exception for bad status codes
            response.raise_for_status()
            
            # Parse the JSON response
            data = response.json()
            print("Server Response:")
            
            # Print the response from the server
            for key, value in data.items():
                print(f"{key}: {value}")
        
        except requests.exceptions.RequestException as e:
            # Handle any request errors (e.g., network issues, timeouts)
            print(f"Request failed: {e}")

if __name__ == "__main__":
    # Example player details
    player_id = 1  # Example player ID
    player_lat = 37.7749  # Example latitude
    player_lon = -122.4194  # Example longitude
    
    # Send the image with player data to the server
    send_image(IMAGE_PATH, player_id, player_lat, player_lon)
