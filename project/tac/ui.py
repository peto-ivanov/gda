import streamlit as st
import requests

from config.settings import APISettings

api_settings = APISettings()
headers = {
    "x-api-key": api_settings.TAC_KEY,
    "Content-Type": "application/json"
}

# Streamlit UI
st.title("REST API Client")

# Input text field
user_input = st.text_input("Enter your text:")

# Submit button
if st.button("Submit"):
    if user_input:
        try:
            # REST API request
            payload = {"inputs": user_input}
            print(f"Using API Key: {api_settings.TAC_KEY}")  # Debugging
            print(f"Using API URL: {api_settings.ROBERTA_URL}")  # Debugging
            print(f"Headers: {headers}")
            print(f"Payload: {payload}")  # Debugging
            response = requests.post(url=api_settings.ROBERTA_URL, headers=headers, json=payload)

            # Display response
            if response.status_code == 200:
                st.markdown(f"### API Response:\n{response.json()}")
            else:
                st.error(f"Error: {response.status_code} - {response.text}")
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter some text before submitting.")