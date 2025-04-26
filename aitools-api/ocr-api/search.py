from jan import *
from mygoogle import *

def youtube_search(search, last, topic, violence, sexuality, bodynegativity, advertisements):

    print("Got request to search for videos")

    query_appropriate = True
    query_distracted = False

    videos = []

    print("Getting videos")

    # Generate ai optimized query
    new_query = generate_related_query(search, last, topic)


    # Parse the response from the JAN API
    videos = get_videos_by_search(new_query, 13)
    print("Got videos: " + str(videos))

    # Check if the search is appropriate for the user's criteria, if so, empty the videos list
    if (violence and result_is_any("violent", search)) or (sexuality and result_is_any("sexual", search)) or (bodynegativity and result_is_any("bodynegativety", search)) or (advertisements and result_is_any("advertisement", search)):
        videos = []

    print("Search appropriate: " + str(query_appropriate))

    if query_offtrack(topic, search):
        query_distracted = True


    print("Query distracted: " + str(query_distracted))


    # Filter videos based on age appropriateness and relevance to topic
    print(videos)
    for video in videos:
        if (violence and result_is_any("violent", video["name"])) or (sexuality and result_is_any("sexual", video["name"])) or (bodynegativity and result_is_any("bodynegativety", video["name"])) or (advertisements and result_is_any("advertisement", video["name"])):
            videos.remove(video)
            print("Filtered out video: " + video["name"])
        else : 
            print("Kept video: " + video["name"])

    # Convert the response to JSON
    print("Videos JSON: " + str(videos))
    

    return videos, query_appropriate, query_distracted

if __name__ == "__main__":
    print(youtube_search("how to do woodworking", "what is woodworking", "woodworking", False, False, False, False))
