import openai
import json
from llama_index import download_loader, GPTSimpleVectorIndex
from pathlib import Path
from decouple import config
import os

# Documentation:  https://llamahub.ai/
# Reference: Liam Ottley https://www.youtube.com/watch?v=sUSw9MaPm2M


# llama index requires the os.environ variable called OPENAI_API_KEY:
os.environ['OPENAI_API_KEY'] = config('OPENAI_API_KEY')

class Chatbot:
    def __init__(self, index):
        self.index = index
        # openai.api_key = api_key
        self.chat_history = []

    def generate_response(self, user_input):
        prompt = "\n".join([f"{message['role']}: {message['content']}" for message in self.chat_history[-5:]])
        prompt += f"\nUser: {user_input}"
        response = index.query(user_input)

        message = {"role": "assistant", "content": response.response}
        self.chat_history.append({"role": "user", "content": user_input})
        self.chat_history.append(message)
        return message
    
    def load_chat_history(self, filename):
        try:
            with open(filename, 'r') as f:
                self.chat_history = json.load(f)
        except FileNotFoundError:
            pass

    def save_chat_history(self, filename):
        with open(filename, 'w') as f:
            json.dump(self.chat_history, f)


# ==========WIKIPEDIA PAGE 


# WikipediaReader = download_loader("WikipediaReader")

# loader = WikipediaReader()
# wikidocs = loader.load_data(pages=['Cyclone Freddy'])
# index = GPTSimpleVectorIndex(wikidocs)


# ======GOOGLE DOCS 
# GoogleDocsReader = download_loader('GoogleDocsReader')

# gdoc_ids = ['1wf-y2pd9C878Oh-FmLH7Q_BQkljdm6TQal-c1pUfrec']
# loader = GoogleDocsReader()
# documents = loader.load_data(document_ids=gdoc_ids)

# index = GPTSimpleVectorIndex(documents)


# =====PDF====
PDFReader = download_loader("PDFReader")

loader = PDFReader()
documents = loader.load_data(file=Path('./data/data.pdf'))
index = GPTSimpleVectorIndex(documents)





# Swap out your index below for whatever knowledge base you want
bot = Chatbot(index=index)
bot.load_chat_history("chat_history.json")

while True:
    user_input = input("You: ")
    if user_input.lower() in ["bye", "goodbye"]:
        print("Bot: Goodbye!")
        bot.save_chat_history("chat_history.json")
        break
    response = bot.generate_response(user_input)
    print(f"Bot: {response['content']}")