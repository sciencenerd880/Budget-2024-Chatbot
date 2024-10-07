# HTX Budget-2024-Chatbot

This is a chatbot application built using a Large Language Model (LLM) and Retrieval-Augmented Generation (RAG) to answer queries related to Singapore’s Finance Minister’s Budget 2024.

## Project Structure
├── streamlit_app.py        # Streamlit front-end code for user interaction
├── create_database.py      # Creates the database
├── chroma_db/              # Store the embeddings / sql-lite3
├── data/                   # Store your budget document or any text you need for retrieval
│   └── budget_2024.txt     # The document for RAG (text files, PDFs, etc.)
│
├── config/                 # Configuration files (optional)
│   └── config.yaml         # Store the configuration settings here
│
├── Dockerfile              # Dockerfile to set up the environment
├── requirements.txt        # Python dependencies for the project
├── README.md               # Project setup and instructions
└── .gitignore              # Ignoring unnecessary files
