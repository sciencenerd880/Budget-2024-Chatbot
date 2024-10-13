import streamlit as st
import random
import time

import chromadb
from openai import OpenAI
from dotenv import load_dotenv
from utils import get_collection, get_response, stream_response_generator, stream_message

load_dotenv()

# Initialize session state variables
if 'name' not in st.session_state:
    st.session_state.name = ""
if 'age' not in st.session_state:
    st.session_state.age = 0
if 'income' not in st.session_state:
    st.session_state.income = ""
if 'avresidence' not in st.session_state:
    st.session_state.avresidence = ""
if 'numproperty' not in st.session_state:
    st.session_state.avresidence = ""
if 'page' not in st.session_state:
    st.session_state.page = "form" 
    

def submit_form():
    st.session_state.name = st.session_state.form_name
    st.session_state.age = st.session_state.form_age
    st.session_state.income = st.session_state.form_income
    st.session_state.avresidence = st.session_state.form_av_residence
    st.session_state.numproperty = st.session_state.form_num_property

    st.session_state.page = "chat"  # Switch to chat page after form submission

def form_page():
    st.title("Enter Your Details")
    # Create a form to input name and age
    with st.form("name_age_form"):
        st.text_input("Enter your name", 
                      key="form_name")
        st.number_input("Enter your age",
                        min_value=1, max_value=120, value=68,
                        key="form_age",
                        help="Please enter your current age as of birthdate. Age must be between 1 and 120.")
        st.selectbox("Average Monthly Income", 
                    ("$500-$2,500", "$2,500-$3,500", "$3,500-$6,000"),
                    key="form_income",
                     help="Please enter your average monthly income in SGD before taxes. Include bonuses or allowances if applicable.")        
        st.selectbox("Annual Value (AV) of Residence", 
                    ("Less than $25,000", "More than $25,000"),
                    key="form_av_residence",
                    help='Please enter the Annual Value of your residence as stated in the property tax notice. This is used for government-related schemes.')
        st.selectbox("Number of Properties Owned", 
                     ("1", "2 or more"),
                    key="form_num_property",
                    help='Please input only local/Singapore Properties owned including commercial properties under yourself.')
        submit_button = st.form_submit_button("Submit", on_click=submit_form)

#Initialize all the session state variables
if 'page' not in st.session_state:
    st.session_state['page'] = "form"

# Page Navigation part
if st.session_state['page'] == "form":
    form_page()
    #st.session_state['user_profile'] = user_profile

elif st.session_state['page'] == "chat":
    # Streamed response emulator
    # Dictionary mapping annexes to their respective link
    annex_links = {
        "Annex F-2": "https://www.mof.gov.sg/docs/librariesprovider3/budget2024/download/pdf/annexf2.pdf",
        "Annex F-3": "https://www.mof.gov.sg/docs/librariesprovider3/budget2024/download/pdf/annexf3.pdf",
        "Annex B-1": "https://www.mof.gov.sg/docs/librariesprovider3/budget2024/download/pdf/annexb1.pdf",
        "":"s"
    }
    st.title("📊 Budget 2024 Bot")

    # Initialize chat history if it's not already initialized
    if "messages" not in st.session_state:
        st.session_state.messages = []
        # Add the welcome message to the chat history
        welcome_message = f"Hello {st.session_state.name}, I’m here to help you navigate the Budget 2024. Ask me anything! "
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
            #user_profile = st.session_state['user_profile']  # Access from session_state
            system_prompt = f"""
            You are an AI assistant designed to provide accurate and helpful information about Singapore’s Budget Speech 2024. Your primary role is to help the public understand the details of the budget, answer questions regarding specific policies, schemes (such as the Majulah Package and Medisave Bonus). Provide the annex that was referenced if and only if confident and accurately factual.

            ### The user profile is as follows:
            Age: {st.session_state.age} years old
            Average Monthly Income: {st.session_state.income}
            Annual Value of Residence (AV): {st.session_state.avresidence}
            Number of Properties Owned: {st.session_state.numproperty}
            
            ### Important Guidelines:
            -Based on this user profile and the retrieved chunked information, answer the user query step by step.
            -Include the Annex reference if and only if when highly confident about addressing the user query and the retrieved information.
            -Ensure it is relevant to the user's circumstances, particularly with respect to eligibility for government schemes and any potential benefits.
            -Ensure the streamlit response is well-formatted, using \n\n for new paragraphs, bullet points for lists, and bold text where appropriate.                   
            
            ### Retrieved chunked information from pdf:
            {results['documents']}
            
            ### Sample Outputs Formatting to Adhere:
            "One line conclusion + Reasoning" 
            Reference from: Annex F-3
            
            "One line conclusion + Reasoninge" 
            Referfence from: Annex B-2
            
            "One line conclusion + Reasoning" 
            Reference from: Annex C-5
            
            "One line conclusion + Reasoning" 
            Reference from: Annex A-1
            
            """  
            print(system_prompt)
            print()
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
                print(streamed_response)

            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", 
                                            "content": streamed_response})
