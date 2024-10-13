'''
create_database2 uses semantic chunking 
and will save into chroma_db semantic overall collection seperately

reference on semantic chunking: https://github.com/NirDiamant/RAG_Techniques/blob/main/all_rag_techniques/semantic_chunking.ipynb
'''
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFDirectoryLoader
import chromadb

from utils import read_pdf_to_string

import os
from dotenv import load_dotenv

from tqdm import tqdm


# Step 1: Load environment variables for API key
load_dotenv()

print('Please wait to process')

#pdf_filename = 'overall', 'majulah
pdf_filename = 'majulah'
content = read_pdf_to_string('data/overall/{}.pdf'.format(pdf_filename))
#print(content)
text_splitter = SemanticChunker(OpenAIEmbeddings(openai_api_key =os.getenv("OPENAI_API_KEY")), 
                                breakpoint_threshold_type='percentile', 
                                breakpoint_threshold_amount=90) # chose which embeddings and breakpoint type and threshold to use

# Split original text to semantic chunks
chunks = text_splitter.create_documents([content])
#print(chunks)

# Step 5: Initialize ChromaDB client
CHROMA_PATH = "chroma_db_semantic"
chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)

# Create a new collection in ChromaDB (name it 'semantic_overall' for semantic chunks)
collection = chroma_client.get_or_create_collection(name="overall_semantic")

# Step 6: Prepare the data for insertion into ChromaDB
documents = []
metadata = []
ids = []

# Step 7: Process each chunked document and prepare for ChromaDB
for i, chunk in enumerate(tqdm(chunks)):
    # Extract the content and metadata of each chunk
    documents.append(chunk.page_content)  # Get the chunked content (text)
    ids.append(f"ID_{i}")               # Generate a unique ID for each chunk
    chunk_meta = chunk.metadata
    chunk_meta['which_annex']  = 'Annex F-2'
    metadata.append(chunk_meta)
    #print(type(chunk.metadata)) 
# Step 8: Insert the documents, metadata, and IDs into ChromaDB collection
collection.upsert(
    documents=documents,  # List of chunked content
    metadatas=metadata,   # List of metadata corresponding to each chunk
    ids=ids               # List of unique IDs for each chunk
)

print('Semantic chunking complete and added to ChromaDB Collection (overall_semantic)')