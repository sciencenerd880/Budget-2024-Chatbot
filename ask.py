import chromadb
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# setting the environment

DATA_PATH = "data/overall/"
CHROMA_PATH = "chroma_db"

chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)

collection = chroma_client.get_or_create_collection(name="overall")


user_query = input("What do you want to know about the Budget Speech?\n\n")

results = collection.query(
    query_texts=[user_query],
    n_results=2
)

#print(results['documents'])
#print(results['metadatas'])

client = OpenAI()

system_prompt = """
You are a helpful assistant. You answer questions about the Budget Speech 2024. 
But you only answer based on knowledge I'm providing you. You don't use your internal 
knowledge and you don't make things up.
If you don't know the answer, just say: I don't know
--------------------
The data:
"""+str(results['documents'])+"""
"""

print(system_prompt)

response = client.chat.completions.create(
    model="gpt-4o-mini", #gpt-4o
    messages = [
        {"role":"system","content":system_prompt},
        {"role":"user","content":user_query}    
    ]
)

print("\n\n---------------------\n\n")
print(response.choices[0].message.content)