import nltk
from nltk.tokenize import word_tokenize
nltk.download('punkt')
text = "Natural Language Processing is a subfield of artificial intelligence that focuses on the interaction between humans and computers using natural language."
tokens = word_tokenize(text)
print(tokens)