import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense
import numpy as np
import matplotlib.pyplot as plt
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import re

# Download NLTK data
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')

# Load IMDB dataset
imdb = tf.keras.datasets.imdb
(X_train, y_train), (X_test, y_test) = imdb.load_data(num_words=10000)

# Get the word index for decoding reviews
word_index = imdb.get_word_index()

# Function to decode a review
def decode_review(encoded_review):
    reverse_word_index = {value: key for (key, value) in word_index.items()}
    return ' '.join([reverse_word_index.get(i - 3, '?') for i in encoded_review])

# Preprocess a review
def preprocess_review(review):
    review = re.sub(r'\W', ' ', review)
    review = review.lower()
    review = word_tokenize(review)
    stop_words = set(stopwords.words('english'))
    review = [word for word in review if word not in stop_words]
    lemmatizer = WordNetLemmatizer()
    review = [lemmatizer.lemmatize(word) for word in review]
    return ' '.join(review)

# Decode and preprocess the reviews
X_train = [preprocess_review(decode_review(review)) for review in X_train]
X_test = [preprocess_review(decode_review(review)) for review in X_test]

# Tokenize and pad sequences
tokenizer = Tokenizer(num_words=10000)
tokenizer.fit_on_texts(X_train)

X_train = tokenizer.texts_to_sequences(X_train)
X_test = tokenizer.texts_to_sequences(X_test)

max_length = 200
X_train = pad_sequences(X_train, maxlen=max_length)
X_test = pad_sequences(X_test, maxlen=max_length)

# Create the model
model = Sequential([
    Embedding(input_dim=10000, output_dim=128, input_length=max_length),
    LSTM(units=128, return_sequences=True),
    LSTM(units=128),
    Dense(units=1, activation='sigmoid')
])

# Compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Train the model
history = model.fit(X_train, y_train, epochs=5, batch_size=64, validation_split=0.2)

# Evaluate the model
loss, accuracy = model.evaluate(X_test, y_test)
print(f"Test Accuracy: {accuracy*100:.2f}%")

# Plot training history
plt.plot(history.history['accuracy'], label='accuracy')
plt.plot(history.history['val_accuracy'], label = 'val_accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.ylim([0, 1])
plt.legend(loc='lower right')
plt.show()

# Predict function
def predict_review(review):
    review = preprocess_review(review)
    encoded_review = tokenizer.texts_to_sequences([review])
    padded_review = pad_sequences(encoded_review, maxlen=max_length)
    prediction = model.predict(padded_review)
    return prediction[0][0]

# Test the predict function
sample_review = "The movie was fantastic! I really enjoyed it."
print(f"Review: {sample_review}")
print(f"Sentiment score: {predict_review(sample_review)}")
