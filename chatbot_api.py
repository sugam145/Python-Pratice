from flask import Flask, request, jsonify
import spacy
import numpy as np
import json
import random
from sklearn.neural_network import MLPClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
import logging
from flask_cors import CORS
import mysql.connector
import uuid
import os
from datetime import datetime
import re

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Setup logging
logging.basicConfig(level=logging.INFO)

# Load the SpaCy model once to avoid multiple loads
nlp = spacy.load('en_core_web_sm')

def preprocess(text):
    doc = nlp(text)
    lemmatized = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
    return ' '.join(lemmatized)

def extract_numbers(text):
    return [int(s) for s in re.findall(r'\b\d+\b', text)]

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # Replace with your MySQL password
        database="roomsewa"
    )

def get_room_details(room_number):
    conn = get_db_connection()
    cursor = conn.cursor(buffered=True)
    try:
        query = "SELECT ROOMID, ROOMDESC, PRICE, AMENITIES, NUMPERSON FROM tblroom WHERE ROOMID = %s"
        cursor.execute(query, (room_number,))
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()

def list_available_rooms():
    conn = get_db_connection()
    cursor = conn.cursor(buffered=True)
    try:
        cursor.execute("SELECT ROOMID,ROOM, PRICE FROM tblroom ORDER BY ROOMNUM ASC")
        rooms = cursor.fetchall()
        room_list = ""
        for room_id,room, price, in rooms:
            room_list += (f"Room {room_id}:{room} Price: {price:.2f}\n")
        return room_list
    finally:
        cursor.close()
        conn.close()

def is_valid_room_number(room_number):
    room_details = get_room_details(room_number)
    return room_details is not None

def is_room_available(room_id, check_in, check_out):
    conn = get_db_connection()
    cursor = conn.cursor(buffered=True)
    try:
        query = """
        SELECT * FROM tblreservation
        WHERE ROOMID = %s
        AND STATUS = 'Confirmed'
        AND (
            (ARRIVAL <= %s AND DEPARTURE >= %s) OR
            (ARRIVAL <= %s AND DEPARTURE >= %s) OR
            (ARRIVAL >= %s AND DEPARTURE <= %s)
        )
        """
        cursor.execute(query, (room_id, check_in, check_in, check_out, check_out, check_in, check_out))
        return cursor.rowcount == 0
    finally:
        cursor.close()
        conn.close()

def book_room(room_id, guest_id, check_in, check_out, price, purpose):
    if is_room_available(room_id, check_in, check_out):
        conn = get_db_connection()
        cursor = conn.cursor(buffered=True)
        try:
            confirmation_code = str(uuid.uuid4())[:8]
            cursor.execute("""
                INSERT INTO tblreservation (CONFIRMATIONCODE, TRANSDATE, ROOMID, ARRIVAL, DEPARTURE, RPRICE, GUESTID, PRORPOSE, STATUS, BOOKDATE)
                VALUES (%s, NOW(), %s, %s, %s, %s, %s, %s, 'Pending', NOW())
            """, (confirmation_code, room_id, check_in, check_out, price, guest_id, purpose))
            conn.commit()
            return confirmation_code
        finally:
            cursor.close()
            conn.close()
    else:
        return None

def cancel_booking(confirmation_code):
    conn = get_db_connection()
    cursor = conn.cursor(buffered=True)
    try:
        cursor.execute("UPDATE tblreservation SET STATUS = 'Cancelled' WHERE CONFIRMATIONCODE = %s", (confirmation_code,))
        if cursor.rowcount > 0:
            conn.commit()
            return "Your booking has been successfully cancelled."
        else:
            return "Confirmation code not found. Please check the code and try again."
    finally:
        cursor.close()
        conn.close()

def parse_date(date_str):
    try:
        # Parse as datetime and then return just the date part
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return None


# Load intents from the JSON file
try:
    with open('intents.json', 'r') as file:
        data = json.load(file)
except FileNotFoundError:
    logging.error("Intents file not found.")
    data = {'intents': []}

patterns = []
tags = []
responses = {}

for intent in data['intents']:
    for pattern in intent['patterns']:
        pattern = preprocess(pattern)
        patterns.append(pattern)
        tags.append(intent['tag'])
    responses[intent['tag']] = intent['responses']

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(patterns)

tag_to_code = {tag: i for i, tag in enumerate(set(tags))}
code_to_tag = {i: tag for i, tag in enumerate(set(tags))}
y = np.array([tag_to_code[tag] for tag in tags])

model = MLPClassifier(hidden_layer_sizes=(50, 50), max_iter=1000, random_state=42, alpha=0.01)
model.fit(X, y)

def get_response(user_input, user_context):
    try:
        logging.info(f"User input: {user_input}")

        processed_input = preprocess(user_input)
        X_test = vectorizer.transform([processed_input])
        tag_code = model.predict(X_test)[0]
        tag = code_to_tag[tag_code]

        if user_context.get("state") == "booking":
            if "awaiting_room_id" in user_context:
                room_number = extract_numbers(user_input)
                if room_number and is_valid_room_number(room_number[0]):
                    user_context["room_id"] = room_number[0]
                    user_context.pop("awaiting_room_id", None)
                    user_context["awaiting_check_in"] = True
                    return "Please provide the check-in date (YYYY-MM-DD).", "booking"
                else:
                    return "Invalid room number. Please provide a valid room number.", "booking"
            elif "awaiting_check_in" in user_context:
                check_in_date = parse_date(user_input)
                if check_in_date:
                    # Check if the check-in date is in the past
                    if check_in_date < datetime.now().date():
                        return "Check-in date cannot be in the past. Please provide a valid check-in date (YYYY-MM-DD).", "booking"
                    user_context["check_in"] = check_in_date
                    user_context.pop("awaiting_check_in", None)
                    user_context["awaiting_check_out"] = True
                    return "Please provide the check-out date (YYYY-MM-DD).", "booking"
                else:
                    return "Invalid check-in date. Please provide a valid date in the format YYYY-MM-DD.", "booking"
            elif "awaiting_check_out" in user_context:
                check_out_date = parse_date(user_input)
                if check_out_date:
                    # Check if the check-out date is before the check-in date
                    if check_out_date <= user_context.get("check_in"):
                        return "Check-out date must be after check-in date. Please provide a valid check-out date (YYYY-MM-DD).", "booking"
                    
                    user_context["check_out"] = check_out_date
                    user_context.pop("awaiting_check_out", None)
                    
                    # Calculate the total price based on room rate and the number of nights
                    check_in = user_context["check_in"]
                    nights = (check_out_date - check_in).days
                    room_id = user_context.get("room_id")
                    room_details = get_room_details(room_id)
                    if room_details:
                        price_per_night = room_details[2]  # Assuming the 3rd column is price
                        total_price = price_per_night * nights
                        user_context["total_price"] = total_price
                    
                    user_context["awaiting_purpose"] = True
                    return f"Your total price for {nights} nights is {total_price:.2f}. Please provide the purpose of your stay.", "booking"
                else:
                    return "Invalid check-out date. Please provide a valid date in the format YYYY-MM-DD.", "booking"
            elif "awaiting_purpose" in user_context:
                user_context["purpose"] = user_input.strip()
                user_context.pop("awaiting_purpose", None)
                
                room_id = user_context.get("room_id")
                check_in = user_context.get("check_in")
                check_out = user_context.get("check_out")
                price = user_context.get("total_price")
                guest_id = user_context.get("guest_id")
                purpose = user_context.get("purpose")

                confirmation_code = book_room(room_id, guest_id, check_in, check_out, price, purpose)
                if confirmation_code:
                    user_context.clear()  # Clear context after booking
                    return f"Room successfully booked! Your confirmation code is {confirmation_code}.", None
                else:
                    return "Sorry, the room is not available for the selected dates. Please try a different room or date.", "booking"

        if tag == "book_room":
            user_context["state"] = "booking"
            user_context["awaiting_room_id"] = True
            return "Please provide the room number you'd like to book.", "booking"

        elif tag == "cancel_booking":
            user_context["awaiting_confirmation_code"] = True
            return "Please provide your confirmation code to cancel the booking.", "cancel_booking"

        elif tag == "check_availability":
            available_rooms = list_available_rooms()
            return (f"Please select a room from the following list:\n{available_rooms}\n", "booking")

        elif tag == "thank_you":
            return "You're welcome! If you need any further assistance, feel free to ask.", None

        # Handle confirmation code cancellation
        if user_context.get("awaiting_confirmation_code"):
            confirmation_code = user_input.strip()
            cancellation_message = cancel_booking(confirmation_code)
            user_context["awaiting_confirmation_code"] = False
            return cancellation_message, None

        # Default response
        response = responses.get(tag, ["I'm not sure how to respond to that."])
        return random.choice(response), None

    except Exception as e:
        logging.error(f"Error processing input: {e}")
        return "Sorry, there was an error processing your request.", None


user_context = {}  # Initialize user context at the start

@app.route('/chat', methods=['POST'])
def chat():
    global user_context
    data = request.json
    user_message = data.get('message', '')
    guest_id = data.get('user_id')
    user_context['guest_id'] = guest_id
    response, context = get_response(user_message, user_context)
    if context:
        user_context["state"] = context  # Store the context for future messages
    
    return jsonify({'response': response})


if __name__ == "__main__":
    app.run(debug=True)
