import chromadb
from openai import OpenAI
from dotenv import load_dotenv

import fitz
import re

import time

import streamlit as st

load_dotenv()

def get_collection(collection_name="overall", CHROMA_PATH="chroma_db"):

    chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
    collection = chroma_client.get_or_create_collection(name=collection_name)
    
    return collection

def get_response(client, system_prompt, user_query):
    response = client.chat.completions.create(
    model="gpt-4o", #gpt-4o-mini
    messages = [
        {"role":"system","content":system_prompt},
        {"role":"user","content":user_query}    
    ]
    )
    #print("\n\n---------------------\n\n")
    #print(response.choices[0].message.content)

    return response.choices[0].message.content


def read_pdf_to_string(path):
    """
    Read a PDF document from the specified path and return its content as a string.

    Args:
        path (str): The file path to the PDF document.

    Returns:
        str: The concatenated text content of all pages in the PDF document.

    The function uses the 'fitz' library (PyMuPDF) to open the PDF document, iterate over each page,
    extract the text content from each page, and append it to a single string.
    """
    # Open the PDF document located at the specified path
    doc = fitz.open(path)
    content = ""
    # Iterate over each page in the document
    for page_num in range(len(doc)):
        # Get the current page
        page = doc[page_num]
        # Extract the text content from the current page and append it to the content string
        content += page.get_text()
    return content


# Function to generate the chatbot response with annex links
def stream_response_generator(text, annex_ref, annex_links):    
    def insert_annex_url(response, annex_links):
        # Find the annex reference in the response using regex
        annex_match = re.search(r'Annex ([A-Z]-\d+)', response)

        # If an annex is mentioned in the response
        if annex_match:
            annex_reference = f"Annex {annex_match.group(1)}"
            
            if annex_reference in annex_links:
                annex_url = annex_links[annex_reference]
                # Replace or append the clickable URL using Markdown
                #response = response.replace(,f"[{annex_ref[0]}]({annex_links[annex_ref[0]]})")
                response = response.replace(annex_reference, f"[{annex_reference}]({annex_url})")
                #print(response)
        return response
    
    text = insert_annex_url(text, annex_links)
    # To handle latex issue for $
    text = text.replace("$", "\$")

    # Stream the text word by word
    for word in text.split(" "):
        yield word + " "
        time.sleep(0.015)
        
        
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
