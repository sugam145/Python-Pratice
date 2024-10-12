import spacy
import numpy as np
import json
import random
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.neural_network import MLPClassifier
from sklearn.feature_extraction.text import TfidfVectorizer

# Load the SpaCy model once to avoid multiple loads
nlp = spacy.load('en_core_web_sm')

def preprocess(pattern):
    """
    Preprocesses the input text by lemmatizing and removing stop words and punctuation.
    """
    doc = nlp(pattern)
    lemmatized = []
    for token in doc:
        if not token.is_stop and not token.is_punct:
            lemmatized.append(token.lemma_)
    return ' '.join(lemmatized)

# Load intents from the JSON file
with open('intents.json', 'r') as file:
    data = json.load(file)
    
patterns = []
tags = []
responses = {}

# Extract patterns, tags, and responses from the JSON data
for intent in data['intents']:
    for pattern in intent['patterns']:
        pattern = preprocess(pattern)
        patterns.append(pattern)
        tags.append(intent['tag'])
    
    # Store responses for each tag
    responses[intent['tag']] = intent['responses']

# Transform patterns to TF-IDF vectors
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(patterns)

# Encode tags into numerical codes
tag_to_code = {tag: i for i, tag in enumerate(set(tags))}
code_to_tag = {i: tag for tag, i in tag_to_code.items()}
y = np.array([tag_to_code[tag] for tag in tags])

# Check class distribution
print("Class distribution:", {tag: list(tags).count(tag) for tag in set(tags)})

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Train the model
model = MLPClassifier(hidden_layer_sizes=(10, 10), max_iter=900, random_state=20)
model.fit(X_train, y_train)

# Evaluate the model
y_test_pred = model.predict(X_test)

# Use zero_division to handle warnings
print(classification_report(y_test, y_test_pred, zero_division=0))

def get_response(user_input):
    """
    Predicts the intent of the user input and returns an appropriate response.
    """
    # Preprocess the input and transform it into a TF-IDF vector
    preprocessed_input = preprocess(user_input)
    input_vector = vectorizer.transform([preprocessed_input])

    # Predict the class of the input
    predicted_code = model.predict(input_vector)[0]
    predicted_tag = code_to_tag.get(predicted_code, None)

    if predicted_tag:
        # Select a random response from the predicted intent's responses
        response = random.choice(responses[predicted_tag])
    else:
        # Fallback response for unknown inputs
        response = "I'm not sure I understand. Can you please rephrase?"

    return response

def chat():
    """
    Main function to handle conversation with the user.
    """
    print("Hello! I am your friendly chatbot. How can I assist you today?")
    
    # Conversation loop
    while True:
        user_input = input("You: ")
        
        # Exit the chat if the user types 'exit' or 'quit'
        if user_input.lower() in ['exit', 'quit']:
            print("Chatbot: Goodbye! Have a great day!")
            break
        
        # Get response from the chatbot
        response = get_response(user_input)
        print(f"Chatbot: {response}")

# Start the chatbot conversation
chat()
