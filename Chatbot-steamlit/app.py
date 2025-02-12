import streamlit as st
import requests
from dotenv import load_dotenv
import _pickle
import time

# Define the query function
def query(payload, api_key):
    headers = {"Authorization": api_key}
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

# Define the chat function
def chat_with_gpt(question, context, api_key):
    try:
        output = query({
            "inputs": {
                "question": question,
                "context": context,
            },
        }, api_key)
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

    if 'estimated_time' in output:
        st.info(f"Model loading, {output['estimated_time']} sec")
        time.sleep(output['estimated_time'])
        output = query({
            "inputs": {
                "question": question,
                "context": context,
            },
        }, api_key)
    return output

# Load the context data
with open("Web-Chatbot/data.pkl", "rb") as f:
    loaded_data = _pickle.load(f)
context = loaded_data.get('context', None)

# Show title and description
st.title("💬 Chatbot")
st.write(
    "This is a simple chatbot that uses an AI model to generate answers. "
    "To use this app, you need to provide a HuggingFace API key, which you can get [here](https://huggingface.co/settings/tokens)."
)

api_key = st.text_input("HuggingFace API Key", type="password")
if not api_key:
    st.info("Please add your HuggingFace API key to continue.", icon="🗝️")

# Define the API URL
API_URL = "https://api-inference.huggingface.co/models/consciousAI/question-answering-roberta-base-s-v2"

question = st.text_input("Your question", "")

if st.button("Ask"):
    if question:
        output = chat_with_gpt(question, context, api_key)
        if output:
            st.write(f"Question: {question}")
            st.write(f"Answer: {output['answer']}")
    else:
        st.warning("Please enter a question.")

# Option to exit the chat
if st.button("Exit"):
    st.stop()