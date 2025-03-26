import streamlit as st
import plotly.graph_objects as go
import requests

from config.settings import APISettings

api_settings = APISettings()
headers = {
    "x-api-key": api_settings.TAC_KEY,
    "Content-Type": "application/json"
}

models = [
    {
        "name": "RoBERTa",
        "url": api_settings.ROBERTA_URL,
        },
    {
        "name": "TinyBERT",
        "url": api_settings.TINYBERT_URL,
    },
]

# Streamlit UI
st.title("Sentiment Analysis with Transformers")

# Input text field
user_input = st.text_area("Enter your textual review:")

if user_input:
    # Create columns for displaying gauges side by side
    cols = st.columns(len(models))

    for idx, model in enumerate(models):
        try:
            # REST API request
            payload = {"inputs": user_input}
            print(f"Using API Key: {api_settings.TAC_KEY}")  # Debugging
            print(f"Using API URL: {model['url']}")  # Debugging
            print(f"Headers: {headers}")
            print(f"Payload: {payload}")  # Debugging
            response = requests.post(url=model['url'], headers=headers, json=payload)

            # Display response
            if response.status_code == 200:
                result = response.json()[0]
                # Set the value for the gauge (between 0 and 1)
                score = result["score"]
                label = result["label"]
                # cols[idx].markdown(f"### {model['name']}: Prediction: {label} ({score})")

                # Determine gauge color based on label
                color = "green" if label == "positive" else "red"

                # Create the gauge figure
                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=score,
                    title={'text': f"{model['name']} Score [{label}]"},
                    gauge={'axis': {'range': [0, 1]},
                           'bar': {'color': color}}
                ))

                # Display the gauge in the respective column
                cols[idx].plotly_chart(fig)
            else:
                cols[idx].error(f"Error: {response.status_code} - {response.text}")
        except Exception as e:
            cols[idx].error(f"An error occurred: {e}")
else:
    st.warning("Please enter some text before submitting.")