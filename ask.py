'''
Uses command line terminal for backend testing
testing of getting top-k retrieved query from db as context to system prompt
before getting the final response from LLM

Ensure things are good to go before integration to streamlit frontend
'''

import chromadb
from openai import OpenAI
from dotenv import load_dotenv
from utils import get_collection, get_response

load_dotenv()

user_query = input("What do you want to know about the Budget Speech?\n\n")
#collection = get_collection(collection_name='overall_semantic', CHROMA_PATH='chroma_db_semantic')
collection = get_collection(collection_name='overall',CHROMA_PATH='chroma_db')

results = collection.query(
    query_texts=[user_query],
    n_results=3
    )

print('----')
print('Retrieved  context ->',results['ids'],results['documents'])
print('Retrieved metadatas ->',results['ids'],results['metadatas'])

system_prompt = """
You are a helpful assistant. You answer questions about the Budget Speech 2024. 
But you only answer based on knowledge I'm providing you. You don't use your internal 
knowledge and you don't make things up.
If you don't know the answer, just say: I don't know
--------------------
The data:
"""+str(results['documents'])

print('----')
print('GPT4o response ->', get_response(client = OpenAI(), system_prompt = system_prompt, user_query = user_query))
