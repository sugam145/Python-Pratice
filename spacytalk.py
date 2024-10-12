import spacy
import nltk
from nltk import word_tokenize, sent_tokenize

# text='''
# Hi, I am Sakriya Maharjan. I teach Python, Distributed System, Computer Network etc to BCA.
# I am consulting with Er. Roshan Chitrakar for ML. 9810288250
# '''
# nlp=spacy.load('en_core_web_sm')
# doc=nlp(text)
# print(doc)
# for sentence in doc.sents:
#     for token in sentence:
#         if token.like_num:
#          print (token)
    

with open('students.txt','r') as file:
    text=file.read()
    
print(text)

nlp=spacy.load('en_core_web_sm')
doc=nlp(text)
number=[]
email=[]
print(doc)
for sentence in doc.sents:
    for token in sentence:
        if token.like_num:
            number.append(token)
            
        if token.like_email:
            email.append(token)

print(number)
print(email)