import os
import nltk
import random
import torch
from transformers import BertTokenizer, BertModel
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


# Step 1: Read all files from the folder
folder_path = 'firstApp/vsit_data'  # Update with the correct path to your folder
all_text = ""

for filename in os.listdir(folder_path):
    if filename.endswith(".txt"):  # Only process .txt files
        file_path = os.path.join(folder_path, filename)
        with open(file_path, 'r', errors='ignore') as file:
            all_text += file.read().lower() + " "  # Combine all text into one string

# Step 2: Preprocess the combined text (tokenizing sentences)
sentence_tokens = nltk.sent_tokenize(all_text)

# Step 3: Initialize BERT model and tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

# Step 4: Define function to get BERT embeddings
def get_bert_embeddings(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    # Extract the embeddings of the [CLS] token (first token) from the last layer
    embeddings = outputs.last_hidden_state[:, 0, :].numpy()
    return embeddings

# Step 5: Function to get the best response based on BERT embeddings
def response(user_input):
    # Get the embedding for the user input
    user_input_embedding = get_bert_embeddings(user_input)

    # Calculate embeddings for all sentences in the corpus
    sentence_embeddings = np.array([get_bert_embeddings(sentence) for sentence in sentence_tokens])

    # Compute cosine similarity between user input and all sentences
    similarities = cosine_similarity(user_input_embedding, sentence_embeddings)

    # Find the most similar sentence based on cosine similarity
    best_match_idx = np.argmax(similarities)

    # Check if the similarity is above a threshold
    threshold = 0.4  # Adjust this threshold for more or less strict matches
    if similarities[0][best_match_idx] < threshold:
        return "I'm not sure I understand. Can you rephrase?"
    else:
        return sentence_tokens[best_match_idx]

# Chatbot interaction
flag = True
print("Hello, I am your learning bot!")

while flag:
    user_response = input("You: ")
    user_response = user_response.lower()
    if user_response != 'bye':
        if user_response in ['thank you', 'thanks']:
            flag = False
            print("Bot: You are welcome!")
        else:
            print("Bot:", response(user_response))
    else:
        flag = False
        print("Bot: Goodbye!")
