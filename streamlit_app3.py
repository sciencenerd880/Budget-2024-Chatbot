import streamlit as st
import random
import time

import chromadb
from openai import OpenAI
from dotenv import load_dotenv
from utils import get_collection, get_response, stream_response_generator, stream_greeting_message
from user_profile import UserProfile, user_profile_form

load_dotenv()
# Function to stream a message
def stream_message(role, message):
    with st.chat_message(role):
        message_placeholder = st.empty()
        streamed_message = ""
        # Simulate a typing effect by adding words one by one
        for word in message.split():
            streamed_message += word + " "
            message_placeholder.markdown(streamed_message)
            time.sleep(0.1)  # Adjust the sleep time to control the speed of the typing effect

# Main application logic
if 'page' not in st.session_state:
    st.session_state['page'] = "form"
    
# Initialize user_profile in session_state if it does not exist
if 'user_profile' not in st.session_state:
    st.session_state['user_profile'] = None

# Switch between form and chat UI based on session state
if st.session_state['page'] == "form":
    user_profile = user_profile_form()
    #st.session_state['user_profile'] = user_profile

elif st.session_state['page'] == "chat":
    # Streamed response emulator
    # Dictionary mapping annexes to their respective link
    annex_links = {
        "Annex A": "https://www.mof.gov.sg/singaporebudget/budget-2024/budget-statement/a-introduction#Introduction",
        "Annex F-2": "https://www.mof.gov.sg/docs/librariesprovider3/budget2024/download/pdf/annexf2.pdf"
    }
    st.title("📊 Budget 2024 Bot")

    # Initialize chat history if it's not already initialized
    if "messages" not in st.session_state:
        st.session_state.messages = []
        # Add the welcome message to the chat history
        welcome_message = "Hello, I’m here to help you navigate the Budget 2024. Ask me anything! "
        stream_message("assistant", welcome_message)
        
    # Display past chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"], unsafe_allow_html=True)

    # Ensure the user_profile is available before accessing it
    if user_query := st.chat_input("Ask what you wanna know from Budget 2024"):
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(user_query)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_query})

        # Process the user query
        collection = get_collection(collection_name='overall_semantic', CHROMA_PATH='chroma_db_semantic')

        if user_query is not None:
            results = collection.query(query_texts=[user_query], n_results=3)

            # Construct the system prompt with user profile
            user_profile = st.session_state['user_profile']  # Access from session_state
            system_prompt = f"""
            You are an AI assistant designed to provide accurate and helpful information about Singapore’s Budget Speech 2024. Your primary role is to help the public understand the details of the budget, answer questions regarding specific policies, schemes (such as the Majulah Package).

            ### The user profile is as follows:
            Age: {user_profile.age} years old
            Citizenship: {user_profile.citizenship}
            Average Monthly Income: {user_profile.avg_income}
            Annual Value of Residence (AV): {user_profile.av_residence}
            Number of Properties Owned: {user_profile.num_properties}
            
            ### Important Guidelines:
            -Based on this user profile and the retrieved chunked information, tailor your responses to answer questions in step by step. Summarize when needed.
            -Ensure it is relevant to the user's circumstances, particularly with respect to eligibility for government schemes and any potential benefits.
            -Ensure the streamlit response is well-formatted, using \n\n for new paragraphs, bullet points for lists, and bold text where appropriate.                   
            
            ### Retrieved chunked information from pdf:
            {results['documents']}
            """  
            print(system_prompt)
            print()
            #print(results)
            response = get_response(client=OpenAI(), 
                                    system_prompt=system_prompt, 
                                    user_query=user_query)
            print()
            print(response)
            annex_ref = list(set([result['which_annex'] for result in results['metadatas'][0]]))
            print(results)
            # Display assistant response in chat message container
            with st.chat_message("assistant"):
                streamed_response = st.write_stream(stream_response_generator(response, annex_ref, annex_links))
            #comment line 93 and line 94 if found a way to format properly with write_stream

            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", 
                                            "content": streamed_response})
