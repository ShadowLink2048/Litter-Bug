import requests
import json






def send_request_to_chat_with_schema(instructions, schema):
    url = "http://127.0.0.1:2000/chat/json"  # Replace with the actual server URL if different
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "instructions": instructions,
        "schema": schema
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()  # Raise an exception for HTTP errors
        #print("Response JSON:", response.json())
        return response.json()
    
    except requests.exceptions.RequestException as e:
        print("Request failed:", e)
    except json.JSONDecodeError as e:
        print("Failed to decode JSON response:", e)


def get_most_common_response(instructions, schema, num_attempts=1):
    responses = []
    for _ in range(num_attempts):
        result = send_request_to_chat_with_schema(instructions, schema)
        if result is not None:
            responses.append(json.dumps(result))
    
    if not responses:
        return None
    
    # Count occurrences of each response
    response_counts = {}
    try:
        for response in responses:
            response_counts[response] = response_counts.get(response, 0) + 1
    except Exception as e:
        print(f"Error counting responses: {e}")
        response_counts = {}
    
    # Find the response with highest count
    most_common = max(response_counts.items(), key=lambda x: x[1])[0]
    
    return json.loads(most_common)

def result_appropriate(age, result):
    try:
        instructions = ': question: is the search result appropriate for the age? : age: ' + str(age) + ' and result: ' + str(result) + 'answer the question boolean true or false. "appropriate" key should coorespond to that.' 
        schema = '{"appropriate": boolean}'
        return get_most_common_response(instructions, schema)['json']['appropriate']
    except Exception as e:
        print(f"Error in result_appropriate: {e}")
        return False
    finally:
        print("Finished processing result_appropriate")

def result_is_any(any, result):
    try:
        instructions = ': question: is the search result' + str(any) +' : search result is: ' + str(result) + 'answer the question boolean true or false. "'+ str(any) +'" key should coorespond to that.' 
        schema = '{"' + str(any) + '": boolean}'
        return get_most_common_response(instructions, schema)['json'][str(any)]
    
    except Exception as e:
        print(f"Error in result_appropriate: {e}")
        return False
    finally:
        print("Finished processing result_appropriate")

def result_match(query, result):
    try:
        instructions = ': question: is search result reasonable for query ? : search: ' + str(query) + ' and result: ' + str(result) + 'answer the question boolean true or false. "reasonable" key should coorespond to that.'
        schema = '{"reasonable": boolean}'
        return get_most_common_response(instructions, schema)['json']['reasonable']
    except Exception as e:
        print(f"Error in result_match: {e}")
        return False
    finally:
        print("Finished processing result_match")


def query_offtrack(first, last):
    try:
        instructions = ': question:  is search within given topic? : topic: ' + str(first) + '.  search: ' + str(last) + '. answer the question boolean true or false. "offtopic" key should coorespond to that.'
        schema = '{"offtopic": boolean}'
        return get_most_common_response(instructions, schema)['json']['offtopic']
    except Exception as e:
        print(f"Error in getting_offtrack: {e}")
        return False
    finally:
        print("Finished processing getting_offtrack")

'''

def generate_topic_title(search):
    try:
        instructions = f': question: what overall topic is being researched based on this search? : search: {str(search)}. limit to one or two words, no more. Return a short title in the "topic" key.'
        schema = '{"topic": string}'
        result = get_most_common_response(instructions, schema)
        return result['json']['topic'] if result else "Unknown Topic"
    except Exception as e:
        print(f"Error in generate_topic_title: {e}")
        return "Unknown Topic"
    finally:
        print("Finished processing generate_topic_title")
'''

def generate_related_query(search, last_search, current_topic):
    try:
        instructions = f': question: generate a search query that will get results in matching  last search was {str(last_search)} and current topic is {str(current_topic)} with newest search : {str(search)}:. Newest search should hold highest weight. Return a short search query in the "query" key, 4-6 words. No extra json'
        schema = '{"query": string}'
        result = get_most_common_response(instructions, schema)
        return result['json']['query'] if result else f"more about {current_topic}"
    except Exception as e:
        print(f"Error in generate_related_query: {e}")
        return f"more about {current_topic}"
    finally:
        print("Finished processing generate_related_query")

def is_recyclable(description):
    try:
        instructions = f': question: determine whether  {str(description)}  is recyclable. Return a boolean in the "recycle" key. No extra json'
        schema = '{"recycle": boolean}'
        result = get_most_common_response(instructions, schema)
        return result['json']['recycle'] if result else None
    
    except Exception as e:
        print(f"Error in generate_related_query: {e}")
        return None
    
    finally:
        print("Finished processing generate_related_query")

def get_type(description):
    try:
        instructions = f': question: classify {str(description)} as either plastic, metal, glass, organic, or other. Return a string in the "type" key of one of those five. No extra json, no more information than exactly requested.'
        schema = '{"type": string}'
        result = get_most_common_response(instructions, schema)
        return result['json']['type'] if result else None
    
    except Exception as e:
        print(f"Error in generate_related_query: {e}")
        return None
    
    finally:
        print("Finished processing generate_related_query")

def get_product_name(description):
    try:
        instructions = f': question: determine the product name from {str(description)}  is. Return a string in the "product" key. No extra json'
        schema = '{"product": string}'
        result = get_most_common_response(instructions, schema)
        return result['json']['product'] if result else None
    
    except Exception as e:
        print(f"Error in generate_related_query: {e}")
        return None
    
    finally:
        print("Finished processing generate_related_query")

# Example usage
if __name__ == "__main__":
    query = "Keloggs cereal treat Nutrition Facts blah blah blah "
    print(get_product_name(query))
    print(get_type(query))
    print(is_recyclable(query))

