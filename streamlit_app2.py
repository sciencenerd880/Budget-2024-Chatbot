import streamlit as st
import random
import time

import chromadb
from openai import OpenAI
from dotenv import load_dotenv
from utils import get_collection, get_response

load_dotenv()

'''
[user_query] got issue causing encode problems
response got class related issue, says need string???
'''

    
# Streamed response emulator
# Dictionary mapping annexes to their respective links
annex_links = {
    "Annex A": "https://www.mof.gov.sg/singaporebudget/budget-2024/budget-statement/a-introduction#Introduction",
    "Annex B": "https://www.mof.gov.sg/singaporebudget/budget-2024/budget-statement/b-tackling-immediate-challenges#Tackling-Immediate-Challenges",
    "Annex C": "https://www.mof.gov.sg/singaporebudget/budget-2024/budget-statement/c-pursuing-better-growth-and-jobs#Pursuing-Better-Growth-and-Jobs",
}

# Function to generate the chatbot response with annex links
def stream_response_generator(text, annex_ref):
    text += "\nBudget 2024 Annex Reference:\n"
    
    annex_text = f"You can check out [{annex_ref[0]}]({annex_links[annex_ref[0]]}) for more information.\n"
    text += annex_text

    # Stream the text word by word
    for word in text.split():
        yield word + " "
        time.sleep(0.05)


st.title("💰🧧💰 Your Answer from Cai Shen Ye Budget 2024 💰🧧💰")
USER_AVATAR = "🧑‍💻"
BOT_AVATAR = "💰"
# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

### PAST
# Display past chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

### PRESENT
# Accept user input
if user_query := st.chat_input("Ask what you wanna know from Budget 2024"):
    # Display user message in chat message container
    with st.chat_message("user", avatar=USER_AVATAR):
        st.markdown(user_query)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", 
                                      "content": user_query})
    # Display assistant message in chat message container

collection = get_collection(collection_name='overall_semantic',CHROMA_PATH='chroma_db_semantic')
if user_query != None: 
    print('this is users query',user_query)

    results = collection.query(
        query_texts=[user_query],
        n_results=3
        )

    system_prompt = """
    You are a helpful assistant. You answer questions about the Budget Speech 2024. 
    But you only answer based on knowledge I'm providing you. You don't use your internal 
    knowledge and you don't make things up.
    If you don't know the answer, just say: I don't know
    --------------------
    The data:
    """+str(results['documents'])

    print('----')
    response = get_response(client = OpenAI(), system_prompt = system_prompt, user_query = user_query)
    annex_ref = list(set([result['which_annex'] for result in results['metadatas'][0]]))
    print('Which Annexes', annex_ref)
    print('GPT4o response ->',response)
    # https://www.gov.sg/features/budget-2024

    # Display assistant response in chat message container
    with st.chat_message("assistant",avatar=BOT_AVATAR):
        # Replace this line with GPT4o response
        streamed_response = st.write_stream(stream_response_generator(response, annex_ref))
    # Add assistant response to chat history, and dont forget to replace
    st.session_state.messages.append({"role": "assistant", 
                                    "content": streamed_response
                                    })
