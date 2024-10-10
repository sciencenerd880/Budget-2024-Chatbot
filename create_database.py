'''
using recursive character text splitter chunking strategy
'''

from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import chromadb

from utils import read_pdf_to_string
# setting the environment

DATA_PATH = "data/overall/"
CHROMA_PATH = "chroma_db"

chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = chroma_client.get_or_create_collection(name="overall")

# Initiallise Loader object and using .load() method to get raw documents from DATA_PATH's pdf
loader = PyPDFDirectoryLoader(DATA_PATH)
raw_documents = loader.load()
print(raw_documents)

# splitting the document using RC method into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,
    chunk_overlap=100,
    length_function=len,
    is_separator_regex=False,
    )
chunks = text_splitter.split_documents(raw_documents)

# preparing to be added in chromadb
documents = []
metadata = []
ids = []

for i, chunk in enumerate(chunks):
    documents.append(chunk.page_content)
    ids.append("ID"+str(i))
    metadata.append(chunk.metadata)

# adding to chromadb
collection.upsert(
    documents=documents,
    metadatas=metadata,
    ids=ids
    )
print('done')
