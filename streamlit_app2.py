import streamlit as st
import random
import time

import chromadb
from openai import OpenAI
from dotenv import load_dotenv
from utils import get_collection, get_response, stream_response_generator

load_dotenv()

'''
1) chunking evaluation https://github.com/brandonstarxel/chunking_evaluation / https://zilliz.com/learn/guide-to-chunking-strategies-for-rag
2) embed age profile, household income, income level, gender etc (simulation of singpass)
3) citation and metadata extraction https://www.youtube.com/watch?v=JjSCezpZbI0&ab_channel=DataScienceBasics
4) need to process by annex for create_database2/3
5) create more prompts for unit testing besides just what is the main takeaway, how much is the cdc voucher
6) user profile and context of what year isit right nows
7) docker simple deployment - ensure all links is not hardcoded use os.path whenever possible
'''

    
# Streamed response emulator
# Dictionary mapping annexes to their respective links
annex_links = {
    "Annex A": "https://www.mof.gov.sg/singaporebudget/budget-2024/budget-statement/a-introduction#Introduction",
    "Annex B": "https://www.mof.gov.sg/singaporebudget/budget-2024/budget-statement/b-tackling-immediate-challenges#Tackling-Immediate-Challenges",
    "Annex C": "https://www.mof.gov.sg/singaporebudget/budget-2024/budget-statement/c-pursuing-better-growth-and-jobs#Pursuing-Better-Growth-and-Jobs",
}


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
    print()
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
    The user's age is: 52 years old. household income of $1000.
    
    The data:
    """+str(results['documents'])

    print('----')
    response = get_response(client = OpenAI(), system_prompt = system_prompt, user_query = user_query)
    annex_ref = list(set([result['which_annex'] for result in results['metadatas'][0]]))
    print('Which Annexes', annex_ref)
    print('GPT4o response ->',response)
    print('Retrieved  context ->',results['ids'],results['documents'])
    # https://www.gov.sg/features/budget-2024

    # Display assistant response in chat message container
    with st.chat_message("assistant",avatar=BOT_AVATAR):
        # Replace this line with GPT4o response
        streamed_response = st.write_stream(stream_response_generator(response, annex_ref, annex_links))
    # Add assistant response to chat history, and dont forget to replace
    st.session_state.messages.append({"role": "assistant", 
                                    "content": streamed_response
                                    })
