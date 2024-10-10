import chromadb
from openai import OpenAI
from dotenv import load_dotenv

import fitz

load_dotenv()

def get_collection(collection_name="overall", CHROMA_PATH="chroma_db"):

    chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
    collection = chroma_client.get_or_create_collection(name=collection_name)
    
    return collection

def get_response(client, system_prompt, user_query):
    response = client.chat.completions.create(
    model="gpt-4o-mini", #gpt-4o
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