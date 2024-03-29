
from llama_index.core import Settings, VectorStoreIndex, SimpleDirectoryReader
from llama_index.llms.openai import OpenAI
import json
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
        response = self.index.query(user_input)

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


# =====PDF====
# define LLM
# llm = OpenAI(temperature=0.1, model="gpt-4")
reader = SimpleDirectoryReader(
    input_files=["./data/joel.pdf"]
)
documents = reader.load_data()
Settings.llm = OpenAI(temperature=0, model="gpt-4")
index=VectorStoreIndex.from_documents(documents,show_progress=True)
query_engine=index.as_query_engine()




# Swap out your index below for whatever knowledge base you want
bot = Chatbot(index=query_engine)
bot.load_chat_history("chat_history.json")

while True:
    user_input = input("You: ")
    if user_input.lower() in ["bye", "goodbye", exit]:
        print("Didi: Goodbye!")
        bot.save_chat_history("chat_history.json")
        break
    response = bot.generate_response(user_input)
    print(f"Didi: {response['content']}")