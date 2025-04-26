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


app = Flask(__name__)
CORS(app)

# Configure upload folder
UPLOAD_FOLDER = './uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Configure port
app.config['SERVER_PORT'] = 2001


@app.route('/classifygarbage', methods=['POST'])
def ocr_text():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Perform OCR using pytesseract
        image = Image.open(filepath)
        text = pytesseract.image_to_string(image)

        # Clean up the uploaded file
        os.remove(filepath)

        # Use the OCR text to classify garbage
        is_garbage = jan.is_garbage(text)
        
        garbage_type = None
        product_name = None
        is_recyclable = None
        points = 0

        if is_garbage:
            garbage_type = jan.get_type(text)
            product_name = jan.get_product_name(text)
            is_recyclable = False
            points = 0

            if garbage_type == 'plastic':
                is_recyclable = True
                points = 5
            elif garbage_type == 'metal':
                is_recyclable = True
                points = 8
            elif garbage_type == 'glass':
                is_recyclable = True
            elif garbage_type == 'organic':
                is_recyclable = False
            elif garbage_type == 'wrapper':
                is_recyclable = False
            elif garbage_type == 'paper':
                is_recyclable = True
            elif garbage_type == 'other':
                is_recyclable = False
            else :
                is_recyclable = False
                garbage_type = 'other'

        elif is_garbage == False:
            garbage_type = False
            product_name = None
            is_recyclable = None

            points = 0
        

        return jsonify({'garbage': is_garbage, 
                        'recyclable': is_recyclable, 
                        'type': garbage_type, 
                        'name': product_name, 
                        'points':points}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=app.config['SERVER_PORT'])