from openai import OpenAI
import os
from dotenv import load_dotenv
import yaml

load_dotenv()


# To load the API key and other chatbot relateds settings
def load_config():
    with open("config/config.yaml", "r") as file:
        return yaml.safe_load(file)

config = load_config()

# OpenAI helper function to generate response using GPT4o-mini
def generate_response(prompt):
    # to note later need to replace the model, system messages, max_tokens etc into the 
    # config.yaml file
    client = OpenAI(
        api_key = os.getenv("OPENAI_API_KEY")
        )
    try:
        completion = client.chat.completions.create(
        model=config["chatbot"]["model"],
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Please translate to chinese:{prompt}"}
            ],
        max_tokens=config['chatbot']['max_tokens']
        )
        return completion.choices[0].message.content
    
    except Exception as e:
        print(f"Error calling OpenAI API {e}")
        return "Sorry, something went wrong"


def handle_query(user_input):
    # will integrate RAG to fetch relevant information
    # and provide context to lLM, for now just focus on response generation
    # later priority to settle hallucination too
    
    response = generate_response(user_input)
    return response

if __name__ == "__main__":
    response = handle_query("Am I eligible for the Majulah Package?")
    print("Chatbot response", response)
