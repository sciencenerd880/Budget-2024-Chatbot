'''
https://tsjohnnychan.medium.com/a-chatgpt-app-with-streamlit-advanced-version-32b4d4a993fb
'''

from openai import OpenAI
import streamlit as st
from dotenv import load_dotenv
import os
import chromadb

import shelve

#Load the environment variable
load_dotenv()

# ChromaDB setup
DATA_PATH = "data/overall/"
CHROMA_PATH = "chroma_db"
chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = chroma_client.get_or_create_collection(name="overall")

#https://graphemica.com/%F0%9F%A6%83
st.title("💰🧧💰 Your Answer from Cai Shen Ye Budget 2024 💰🧧💰")
USER_AVATAR = "🧑‍💻"
BOT_AVATAR = "💰"
client = OpenAI(api_key=st.secrets['OPENAI_API_KEY'])

# Ensure openai_model is initialized in session state
if "openai_model" not in st.session_state:
# available models are ["gpt-4o-mini", "gpt-4o", "gpt-4-turbo", "gpt-4", "gpt-3.5-turbo"]
    st.session_state["openai_model"] = "gpt-4o" 

# Load chat history from shelve file
def load_chat_history():
    with shelve.open("chat_history") as db:
        return db.get("messages", [])

# Save chat history to shelve file
def save_chat_history(messages):
    with shelve.open("chat_history") as db:
        db["messages"] = messages

# Initialize or load chat history
if "messages" not in st.session_state:
    st.session_state.messages = load_chat_history()

# Sidebar with a button to delete chat history
with st.sidebar:
    if st.button("Delete Chat History"):
        st.session_state.messages = []
        save_chat_history([])

# Display chat messages
for message in st.session_state.messages:
    avatar = USER_AVATAR if message["role"] == "user" else BOT_AVATAR
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# Main chat interface
if prompt := st.chat_input("What do you want to know about the Budget Speech 2024?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar=USER_AVATAR):
        st.markdown(prompt)

    # RAG portion: Query ChromaDB and generate system prompt
    results = collection.query(
        query_texts=[prompt],
        n_results=5
    )

    # Format the system prompt with retrieved documents
    system_prompt = """
    You are a helpful assistant focused on answering questions about the Budget Speech 2024. You must only rely on the provided information (retrieved documents) to answer the user’s questions. Do not use your internal knowledge or make up answers.
    Your goal is to extract key details from the chromedb that directly answer the user’s question. If the answer is partially present, summarize the relevant parts of the provided data. If the data doesn't contain enough information, respond with: "I can’t answer based on the available data."
    --------------------
    The retrieved data from chromedb:
    """ + str(results['documents'])
        
    #comment this if i do not want this to appear as part of the Assistant's message
    #st.session_state.messages.append({"role": "assistant", "content": f"System Prompt: {system_prompt}"})

with st.chat_message("assistant", avatar=BOT_AVATAR):
    message_placeholder = st.empty()
    
    # Generate the full response using the OpenAI API without streaming
    response = client.chat.completions.create(
        model=st.session_state["openai_model"],
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
    )

    # Extract the complete response from OpenAI
    full_response = response.choices[0].message.content

    # Display the full response in the UI
    message_placeholder.markdown(full_response)

# Append the assistant's response to the existing chat history
st.session_state.messages.append({"role": "assistant", "content": full_response})

# Save chat history after each interaction
save_chat_history(st.session_state.messages)