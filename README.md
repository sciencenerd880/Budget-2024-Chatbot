# HTX Budget-2024-Chatbot

This is a chatbot application built using a Large Language Model (LLM) and Retrieval-Augmented Generation (RAG) to answer queries related to Singapore’s Finance Minister’s Budget 2024.

## Project Structure

├── app/                    # Main application code
│   ├── __init__.py         # Initialize the app package (optional for a package)
│   ├── chatbot.py          # Core chatbot logic (retrieval, generation, LLM interaction)
│   ├── prompts.py          # Script for prompts design and management
│   └── streamlit_app.py    # Streamlit front-end code for user interaction
│
├── models/                 # Model-related logic
│   ├── embeddings.py       # Document embeddings and chunking logic
│   ├── retriever.py        # RAG retrieval logic
│   └── response_generator.py # Response generation using LLM
│
├── config/                 # Configuration files
│   └── config.yaml         # Store the configuration settings here
│
├── docs/                   # Documentation files
│   ├── architecture.png    # Architecture diagram of the RAG model
│   └── prompts.md          # List of prompts tested for the chatbot
│
├── Dockerfile              # Dockerfile to set up the environment
├── requirements.txt        # Python dependencies for the project
├── README.md               # Project setup and instructions
└── .gitignore              # Ignoring unnecessary files
