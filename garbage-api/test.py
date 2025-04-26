import requests

# Replace with your actual server URL if needed
SERVER_URL = 'http://localhost:2001/classifygarbage'

# Replace with the path to your image
IMAGE_PATH = 'test.png'

def send_image(image_path):
    with open(image_path, 'rb') as img_file:
        files = {'image': img_file}
        try:
            response = requests.post(SERVER_URL, files=files)
            response.raise_for_status()
            data = response.json()
            print("Server Response:")
            for key, value in data.items():
                print(f"{key}: {value}")
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")

if __name__ == "__main__":
    send_image(IMAGE_PATH)