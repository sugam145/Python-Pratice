from flask import Flask, request, jsonify, session
import spacy
import numpy as np
import json
import random
from sklearn.neural_network import MLPClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from flask_session import Session
import os

# Initialize Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your_secret_key')
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Load SpaCy model
nlp = spacy.load('en_core_web_sm')

def preprocess(message):
    doc = nlp(message)
    lemmatized_message = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
    return ' '.join(lemmatized_message)

# Load intents from JSON file
with open('intents.json', 'r') as file:
    data = json.load(file)

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

model = MLPClassifier(hidden_layer_sizes=(50, 50), max_iter=1000, random_state=21, alpha=0.01)
model.fit(X, y)

def predict(message):
    processed_input = preprocess(message)
    vectorized_message = vectorizer.transform([processed_input])
    tag_code = model.predict(vectorized_message)[0]
    tag = code_to_tag[tag_code]
    return tag

def chat_response(user_intent):
    if user_intent != 'book_room':
        response_list = responses[user_intent]
        return random.choice(response_list)
    else:
        room_details = book_room()
        return f'''Your request has been successfully completed.
Room has been booked. Booking Details:
Room Number: {room_details['room_number']}
Date: {room_details['checkin_date']}
'''

def book_room():
    room_details = {}
    print('Chatbot: Sure! Please provide the check-in date.')
    room_details['checkin_date'] = input('Me: ')
    print('Chatbot: Which Room would you like to book?')
    room_details['room_number'] = input('Me: ')
    return room_details

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    user_intent = predict(user_input)
    response = chat_response(user_intent)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
