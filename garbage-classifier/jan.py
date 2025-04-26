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

def recycle_can(description):
    try:
        instructions = f': question: determine whether phrase "{str(description)}" has a recycling can. Return a boolean in the "recycle" key. No extra json'
        schema = '{"recycle": boolean}'
        result = get_most_common_response(instructions, schema)
        return result['json']['recycle'] if result else None
    
    except Exception as e:
        print(f"Error in generate_related_query: {e}")
        return None
    
    finally:
        print("Finished processing generate_related_query")

def garbage_can(description):
    try:
        instructions = f': question: determine whether phrase "{str(description)}" has a garbage can. Return a boolean in the "garbage" key. No extra json'
        schema = '{"garbage": boolean}'
        result = get_most_common_response(instructions, schema)
        return result['json']['garbage'] if result else None
    
    except Exception as e:
        print(f"Error in generate_related_query: {e}")
        return None
    
    finally:
        print("Finished processing generate_related_query")

def is_garbage(description):
    try:
        instructions = f': question: I found {description} on the street, should i throw it away? Return a boolean in the "decision" key.'
        schema = '{"decision": boolean}'
        result = get_most_common_response(instructions, schema)
        return result['json']['decision'] if result else None
    
    except Exception as e:
        print(f"Error in generate_related_query: {e}")
        return None
    
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
    name = get_product_name(query)
    type = get_type(query)
    


