from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from PIL import Image
import pytesseract
import os
import requests
import json

from jan import *
from description import *
from answer import *

import sys

app = Flask(__name__)
CORS(app)

# Configure upload folder
UPLOAD_FOLDER = './uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Configure port
app.config['SERVER_PORT'] = 2001


@app.route('/classifygarbage', methods=['POST'])
def classify_garbage():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        print(f"Saving file: {filepath}")  # Debug: Confirm file path
        file.save(filepath)

        # Perform OCR using pytesseract
        image = Image.open(filepath)


        # Generate description
        description = generate_description(image)
        print(f"Generated description: {description}")  # Debug: Log generated description

        garbage = is_garbage(description)
        recyclable = is_recyclable(description) 
        garbage_type = get_type(description)

        points = 0
    
        if garbage:
            if garbage_type == "bottle":
                points = 10
            elif garbage_type == "can":
                points = 20
            elif garbage_type == "wrapper":
                points = 20
            elif garbage_type == "paper":
                points = 20
            elif garbage_type == "plastic":
                points = 15
            elif garbage_type == "glass":
                points = 15
            elif garbage_type == "metal":
                points = 15
            elif garbage_type == "organic":
                points = 10
            else:
                points = 5

        return jsonify({
            'garbage': garbage,
            'description': description,
            'recyclable': recyclable,
            'type': garbage_type,
            'points': points

        }), 200
    
    except Exception as e:
        print(f"Error: {str(e)}")  # Debug: Log errors
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=app.config['SERVER_PORT'])
