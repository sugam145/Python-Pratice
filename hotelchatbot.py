import spacy
import numpy as np
import json
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
import random
import re
from datetime import datetime

# Load and preprocess text using spaCy
def preprocess(pattern):
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(pattern)
    lemmatized = []
    for token in doc:
        if not token.is_stop and not token.is_punct:
            lemmatized.append(token.lemma_.lower())
    return ' '.join(lemmatized)

# Load intents from JSON file
with open('hotelintents.json', 'r') as file:
    data = json.load(file)

# Prepare data for training
patterns = []
tags = []

for intent in data['intents']:
    for pattern in intent['patterns']:
        processed_pattern = preprocess(pattern)
        patterns.append(processed_pattern)
        tags.append(intent['tag'])

# Transform patterns to TF-IDF vectors
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(patterns)

# Encode tags
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(tags)

# Split the dataset into training and testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model Training using Logistic Regression
model = LogisticRegression(max_iter=500)
model.fit(X_train, y_train)

# Function to extract dates in YYYY-MM-DD format
def extract_dates(text):
    date_pattern = r'\b(\d{4}-\d{2}-\d{2})\b'
    dates = re.findall(date_pattern, text)
    return dates if len(dates) == 2 else None

# Function to extract room type from user input
def extract_room_type(text):
    room_types = ['single', 'double', 'suite', 'deluxe', 'executive', 'family']
    for room_type in room_types:
        if room_type in text.lower():
            return room_type
    return None

# Function to extract number of persons from user input
def extract_number_of_persons(text):
    number_pattern = r'\b(\d+)\b'
    numbers = re.findall(number_pattern, text)
    return int(numbers[0]) if numbers else None

# Function to handle responses based on user input and state
def get_response(user_input, state):
    user_input_processed = preprocess(user_input)
    user_input_vectorized = vectorizer.transform([user_input_processed])
    predicted_tag_index = model.predict(user_input_vectorized)[0]
    predicted_tag = label_encoder.inverse_transform([predicted_tag_index])[0]

    # State management
    if state['booking']:
        if not state['check_in_date'] or not state['check_out_date']:
            if predicted_tag == 'room_availability':
                dates = extract_dates(user_input)
                if dates:
                    check_in_date, check_out_date = dates
                    try:
                        check_in = datetime.strptime(check_in_date, '%Y-%m-%d')
                        check_out = datetime.strptime(check_out_date, '%Y-%m-%d')
                        if check_out > check_in:
                            state['check_in_date'] = check_in_date
                            state['check_out_date'] = check_out_date
                            state['room_type'] = None
                            state['number_of_persons'] = None
                            return "Booking dates confirmed. Now, please specify the room type you prefer."
                        else:
                            return "Check-out date must be after check-in date. Please provide valid dates."
                    except ValueError:
                        return "Invalid date format. Please use YYYY-MM-DD format."
                else:
                    return "Please provide both check-in and check-out dates in YYYY-MM-DD format."

        if not state['room_type']:
            room_type = extract_room_type(user_input)
            if room_type:
                state['room_type'] = room_type
                return f"Room type '{room_type}' selected. Please let me know the number of persons."
            else:
                return "Please specify a valid room type."

        if not state['number_of_persons']:
            number_of_persons = extract_number_of_persons(user_input)
            if number_of_persons:
                state['number_of_persons'] = number_of_persons
                return (f"Number of persons set to {number_of_persons}. Your booking details are as follows:\n"
                        f"Check-in date: {state['check_in_date']}\n"
                        f"Check-out date: {state['check_out_date']}\n"
                        f"Room type: {state['room_type']}\n"
                        f"Number of persons: {state['number_of_persons']}\n"
                        f"Thank you for your booking!")
            else:
                return "Please specify the number of persons."

    # Generic responses
    for intent in data['intents']:
        if intent['tag'] == predicted_tag:
            if predicted_tag == 'booking':
                state['booking'] = True
                state['check_in_date'] = None
                state['check_out_date'] = None
                state['room_type'] = None
                state['number_of_persons'] = None
                return "Let's get you booked! Please provide your check-in and check-out dates."
            return random.choice(intent['responses'])

    return "I'm sorry, I didn't understand that. Can you please rephrase?"

# Chat loop with state management
state = {'booking': False, 'check_in_date': None, 'check_out_date': None, 'room_type': None, 'number_of_persons': None}
print("Hello! Welcome to Hotel Lux. How can I assist you today?")
while True:
    user_input = input("You: ")
    if user_input.lower() in ['exit', 'quit', 'bye']:
        print("Chatbot: Goodbye! Have a great day!")
        break

    response = get_response(user_input, state)
    print("Chatbot:", response)
