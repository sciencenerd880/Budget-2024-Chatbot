# HTX Budget-2024-Chatbot

This is a chatbot application built using a Large Language Model (LLM) and Retrieval-Augmented Generation (RAG) to answer queries related to Singapore’s Finance Minister’s Budget 2024.

## 1.0 Proposed Main Components & Architecture Diagram
- chroma_db / sql-lite
- semantic chunking using text-embedding-ada-002 embedding model || default breakpoint threshold type: percentile
- openai api
- streamlit
- Curated designed system prompt
<image here>

## 2.0 Rationale of RAG Implementation
In the context of a Budget 2024 use-case, implementing a Retrieval Augmented Generation (RAG) approach is essential to overcome the limitations of pre-trained language models. While these models possess vast amounts of general knowledge from their pre-training, they lack the ability to access or generate responses based on real-time or highly specific data, such as the details from the Budget 2024 speech. RAG combines the strengths of retrieval-based systems and generative models by:
Retrieval: Fetching up-to-date information to retrieve the most relevant information ensuring that the responses are accurate and aligned with the source data.
Generation: After retrieval, RAG leverages the generative capabilities to generate contextually appropriate responses which are both factually accurate and contextually appropriate. This is important because public users may ask very nuanced type of questions about eligibility, policy changes etc.

## 3.0 List of Prompts to Interact with LLM
This chatbot is designed to handle a variety of queries related to Singapore's Budget 2024. Below is a list of sample prompts that the chatbot is expected to address:

- ○ **Am I eligible for the Majulah Package?**
- ○ **What are the payouts I can expect to receive in December 2024?**
- ○ **What are the key reasons for high inflation over the last two years?**
- ○ **How can I apply for the Earn and Save Bonus?**
- ○ **What is the qualifying criteria for the Workfare Income Supplement (WIS)?**
- ○ **When will the next GST Voucher payouts be distributed?**

## 4.0 Add the OpenAI API Key to the .env File
To allow the app to access OpenAI's services, you'll need to add your API key to an environment file in the same working directory. Here's how you can do that:

-Create a .env file in the same directory where your Dockerfile and requirements.txt are located (if the file doesn't already exist).

-Open the .env file with any text editor.

-Add the following line to the .env file, replacing the example key with your actual OpenAI API key:
```bash
  OPENAI_API_KEY=my-api-key-here
```

## 5.0 Build & Run the Docker Image

To build the Docker image for this Streamlit app, navigate to the directory containing the `Dockerfile` and run the following command:

```bash
docker build -t my-streamlit-app . --no-cache --progress=plain
```

To run & open the Docker image for this Streamlit app, and run the following commands:

```bash
docker run -p 8501:8501 my-streamlit-app
```

Open the streamlit url using your local browser via:

```bash
http://localhost:8501
```

## Bonus Features (Planned/Completed)
- ✅ **Chunking Strategies**: Comparison of various Chunking Strategies + Rationale for selecting final Approach
- ✅ **Streaming effect on chat**: Chat Streaming Effect


