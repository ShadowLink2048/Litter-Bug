from googleapiclient.discovery import build
import urllib.parse

# Set up your YouTube API key
api_key = "AIzaSyBsPizG5UAxLQ3Gp1YiZS7MicudO9OGebo"  # Replace with your actual API key
backup = "AIzaSyAbRTM291eMwc6DzvNWWsl_zAJcDha4LoY" # Just in case
youtube = build("youtube", "v3", developerKey=api_key)

def extract_video_id(url_path):
    # Parse the query string from the URL
    parsed = urllib.parse.urlparse(url_path)
    query_params = urllib.parse.parse_qs(parsed.query)
    
    # If given just the path (e.g. /watch?v=...), manually extract the query part
    if not parsed.query and '?' in url_path:
        query_string = url_path.split('?', 1)[1]
        query_params = urllib.parse.parse_qs(query_string)
    
    # Get the video ID
    video_id = query_params.get('v', [None])[0]
    return video_id

def get_videos_by_search(query, max_results=2):
    # Perform the search request
    request = youtube.search().list(
        part="snippet",
        q=query,
        type="video",  # We're looking for videos
        maxResults=max_results
    )
    response = request.execute()

    output = []

    # Process the search results
    for item in response.get("items", []):
        video_name = item["snippet"]["title"]
        video_descrip = item["snippet"]["description"]
        video_url = item['id']['videoId']
        img_url = item["snippet"]["thumbnails"]["high"]["url"]  # High quality image thumbnail

        # Create a video dictionary
        video = {
            "name": video_name,
            "description": video_descrip,
            "url": video_url,
            "img": img_url
        }

        output.append(video)

    return output

if __name__ == "__main__":
    # Example usage
    videos = get_videos_by_search("best ai programs for time saving", 3)

    # Print videos found
    print(videos)
