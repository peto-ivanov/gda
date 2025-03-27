from locust import HttpUser, task, between
from datasets import load_from_disk
from config.settings import APISettings
from functools import cache
from datasets import Dataset

import random

@cache
def get_dataset():
    """
    Load the test dataset from disk.
    """
    return Dataset.from_parquet("project/tac/data/aclImdb_test.parquet")


class ModelInferenceUser(HttpUser):
    wait_time = between(1, 3)  # Simulate a wait time between requests

    def on_start(self, data=get_dataset()):
        """
        Load the test dataset and initialize API settings when the test starts.
        """
        # Get the conifg
        config = APISettings()
        # Load the test dataset
        self.data = data
        self.api_key = config.TAC_KEY
        self.headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json"
        }
        # self.models = [
        #     {"name": "RoBERTa", "url": config.ROBERTA_URL},
        #     {"name": "TinyBERT", "url": config.TINYBERT_URL}
        # ]

    @task
    def test_model_inference(self):
        """
        Simulate a user sending a request to the model inference API.
        """
        # Randomly select a text sample from the test dataset
        text_sample = random.choice(self.data["text"])

        # # Randomly select a model to test
        # model = random.choice(self.models)

        # Prepare the payload
        payload = {"inputs": text_sample}

        # Send the POST request to the model's API endpoint
        with self.client.post(
            url="/predict",
            headers=self.headers,
            json=payload,
            catch_response=True
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Failed with status code {response.status_code}: {response.text}")