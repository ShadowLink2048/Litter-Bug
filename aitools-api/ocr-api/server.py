from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename

import os
import requests
import json

from search import *
from jan import *
from mygoogle import *

app = Flask(__name__)
CORS(app)


# Configure upload folder
UPLOAD_FOLDER = './uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Configure port
app.config['SERVER_PORT'] = 2001


@app.route('/search', methods=['POST'])
def search():
    print("Got request to search for videos")

    data = request.get_json()
    if 'search' not in data or 'violence' not in data or 'last' not in data or 'sexuality' not in data or 'bodynegativity' not in data or 'advertisements' not in data or 'topic' not in data:
        return jsonify({'error': 'Both "message" and "schema" fields are required'}), 400

    search = data['search']
    violence = data['violence']
    sexuality = data['sexuality']
    bodynegativity = data['bodynegativity']
    advertisements = data['advertisements']
    topic = data['topic']
    last = data['last']

    appropriate = True
    distracted = False

    try:
        videos, appropriate, distracted = youtube_search(search, last, topic, violence, sexuality, bodynegativity, advertisements)

        # Convert set to list if videos is a set
        if isinstance(videos, set):
            videos = list(videos)

        try:
            # Convert the response to JSON
            videos_json = jsonify({'videos': videos, 'distracted': distracted, 'appropriate': appropriate})
            return videos_json, 200
        except json.JSONDecodeError as e:
            # Handle JSON decoding errors
            return jsonify({'error': 'Error decoding JSON content', 'details': str(e)}), 500
    except Exception as e:
        # Handle errors while parsing the JAN API response
        return jsonify({'error': 'Error parsing JSON response', 'details': str(e)}), 500



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=app.config['SERVER_PORT'])