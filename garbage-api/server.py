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




# Dictionary to store players by their ID
players = {}

# Function to add a player by ID
def add_player(player_id):
    # If the player doesn't exist, create a new entry
    if player_id not in players:
        players[player_id] = []
    

# Function to check if a player already has an item with the same type and brand
def has_item(player_id, type, brand):
    # If the player exists
    if player_id in players:
        # First check if the player has an item with the same brand
        for item in players[player_id]:
            if item['brand'] == brand:
                return True  # Player already has the item with the same brand
        # If no brand match, check if the player has an item with the same type
        for item in players[player_id]:
            if item['type'] == type:
                return True  # Player already has the item with the same type
    return False  # Player doesn't have the item


# Function to get if a player already has an item with the same type and brand
def get_item(player_id, type, brand):
    # If the player exists
    if player_id in players:
        # Loop through the player's items
        for item in players[player_id]:
            # First check if the item brand matches
            if item['brand'] == brand:
                return item  # Return the item if the brand matches
        # If no brand match, check if the type matches
        for item in players[player_id]:
            if item['type'] == type:
                return item  # Return the item if the type matches
    return None  # If not found, return None

# Function to delete if a player already has an item with the same type and brand
def delete_item(player_id, type, brand):
    # If the player exists
    if player_id in players:
        # First, attempt to delete an item with the matching brand
        for i, item in enumerate(players[player_id]):
            if item['brand'] == brand:
                del players[player_id][i]  # Delete the item if the brand matches
                return True
        # If no brand match, attempt to delete an item with the matching type
        for i, item in enumerate(players[player_id]):
            if item['type'] == type:
                del players[player_id][i]  # Delete the item if the type matches
                return True
    return False  # Return False if no matching item is found

def add_item_to_player(player_id, type, brand, points):
    # If the player exists, add the new item
    if player_id in players:
        players[player_id].append({'type': type, 'brand': brand, 'points': points})
    else:
        add_player(player_id)
        players[player_id].append({'type': type, 'brand': brand, 'points': points})

def add_item_to_player(player_id, type, brand, points):
    # If the player exists, add the new item
    if player_id in players:
        players[player_id].append({'type': type, 'brand': brand, 'points': points})
    else:
        add_player(player_id)
        players[player_id].append({'type': type, 'brand': brand, 'points': points})

        

# Example Usage
# add_player(1, 37.7749, -122.4194, 'Bike', 'BrandA')
# add_player(1, 37.7749, -122.4194, 'Car', 'BrandB')

@app.route('/grabgarbage', methods=['POST'])
def grab_garbage():

    # Handle the image file
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    pid = request.form.get('id', 'No argument provided')

    try:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Perform OCR using pytesseract
        image = Image.open(filepath)
        ocr_info = pytesseract.image_to_string(image)

        # Generate description (custom function you may have defined elsewhere)
        description = generate_description(image)

        



        points = 0

        garbage = answer_yes_no(generate_answer(image, "what type of garbage is this?"))

        garbage_type = generate_answer(image, "what type of garbage is this?")
        garbage_brand = generate_answer(image, "what brand is the product in the image")


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
                points = 10


        # checking if player already has the item
        if not has_item(pid, garbage_type, garbage_brand):
            add_item_to_player(pid, garbage_type, garbage_brand, points)
        else: 
            return jsonify({"error": "Oops! You already took a photo of that one, make sure to throw it away to earn points!"})        

        
        return jsonify({
            'pid': pid,
            'player_items': players[pid],
            'garbage': garbage,
            'description': description,
            'brand': garbage_brand,
            'type': garbage_type,
            'points': points,
            'ocr': ocr_info
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

@app.route('/throwgarbage', methods=['POST'])
def throw_garbage():

    # Handle the image file
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    pid = request.form.get('id', 'No argument provided')
    #lon = request.form.get('lon', 'No lon argument')
    #lat = request.form.get('lat', "No lat argument")
    points = int(request.form.get('points', "No points argument"))

    try:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Perform OCR using pytesseract
        image = Image.open(filepath)
        ocr_info = pytesseract.image_to_string(image)

        # Generate description (custom function you may have defined elsewhere)
        thrown_away = answer_yes_no(generate_answer(image, "is something being thrown away?"))

        garbage_type = generate_answer(image, "what type of garbage is being thrown away?")
        garbage_brand = generate_answer(image, "what brand of garbage is being thrown away")

        item = {}

        if thrown_away == True:
            if has_item(pid, garbage_type, garbage_brand):
                item = get_item(pid, garbage_type, garbage_brand)
                points = points + item['points']
                
                delete_item(pid, garbage_type, garbage_brand)
                
            else:
                points = points + 3
                return jsonify({'error': "Oops! Looks like you forgot to take a photo before you through it out. Don't worry, we'll give you a couple points just for trying, but remember next time!", 'points':str(points)}), 200
        
        
        return jsonify({
            'pid': pid,
            'player_items': players[pid],
            'brand': garbage_brand,
            'type': garbage_type,
            'points': points,
            'item': item,
            'throwaway' : thrown_away
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=app.config['SERVER_PORT'])
