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
        instructions = f': question: should i recycle a {description}. Return a boolean in the "decision" key. No extra json'
        schema = '{"decision": boolean}'
        result = get_most_common_response(instructions, schema)
        return result['json']['decision'] if result else None
    
    except Exception as e:
        print(f"Error in generate_related_query: {e}")
        return None
    
    finally:
        print("Finished processing generate_related_query")

def get_type(description):
    try:
        instructions = f': question: classify {str(description)} as either bottle, can, wrapper, paper, or "other". Return a string in the "type" key of one of those five. If unknown, type other. No extra json.'
        schema = '{"type": string}'
        result = get_most_common_response(instructions, schema)
        return result['json']['type'] if result else None
    
    except Exception as e:
        print(f"Error in generate_related_query: {e}")
        return None
    
    finally:
        print("Finished processing generate_related_query")

def get_brand(description):
    while(1):
        try:
            instructions = f': Return a string in the "brand" key. If no brand, set to "none". No extra json. question: determine brand of {str(description)}.'
            schema = '{"brand": string}'
            result = get_most_common_response(instructions, schema)
            
            if result['json']['brand'].lower() == 'none':
                pass
            else:
                return result['json']['brand']
        
        except Exception as e:
            print(f"Error in generate_related_query: {e}")
            return None
        
        finally:
            print("Finished processing generate_related_query")

def get_product_name(description):
    while(1):
        try:
            instructions = f'Product name. Return a string in the "name" key. No extra json. : question: determine the product name from {str(description)}'
            schema = '{"name": string}'
            result = get_most_common_response(instructions, schema)
            if result['json']['name'] != None:
                return result['json']['name']
            else:
                pass # keep looping, until not None
        
        except Exception as e:
            print(f"Error in generate_related_query: {e}")
            return None
        
        finally:
            print("Finished processing generate_related_query")


def is_can_present(description):
    try:
        instructions = f': question: is something being thrown away in the sentence : {str(description)} : anything thrown away? : Return a string in the "can" key.'
        schema = '{"bin": true/false}'
        result = get_most_common_response(instructions, schema)
        if result['json']['bin'] != None:
            return result['json']['bin']
        else:
            pass # keep looping, until not None
    
    except Exception as e:
        print(f"Error in generate_related_query: {e}")
        return None
    
    finally:
        print("Finished processing generate_related_query")

def get_thrown_away(description):
    while(1):
        try:
            instructions = f': question:  what  is being thrown away in the sentence : what brand being thrown away? Return a string in the "brand" and "type" keys. Type should be bottle, can, paper, or other. No extra json. {str(description)} '
            schema = '{"brand": string}'
            result = get_most_common_response(instructions, schema)
            if result['json']['thrownaway'] != None:
                return result['json']['thrownaway']
            else:
                pass # keep looping, until not None
        
        except Exception as e:
            print(f"Error in generate_related_query: {e}")
            return None
        
        finally:
            print("Finished processing generate_related_query")

# Example usage
if __name__ == "__main__":
    query = "a person throwing away a mountain dew bottle in a blue recepticle"

    name = get_product_name(query)
    brand = get_brand(query)
    recycle = is_recyclable(query)
    type = get_type(query)

    can = is_can_present(query)
    throw = get_thrown_away(query)

    print(name, brand, type, can, throw)
    


