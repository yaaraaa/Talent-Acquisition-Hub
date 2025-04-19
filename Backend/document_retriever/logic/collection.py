from langchain.schema import Document
import requests
from typing import List
import os
import logging

def add_collection(collection_name: str, documents: List[Document]):
    """
    Call the Flask endpoint to add a Milvus collection.
    """
    try:
        # Prepare the payload
        documents = [{"page_content": doc.page_content, "metadata": doc.metadata} for doc in documents]
        #print(documents)
        payload = {
            "collection_name": collection_name,
            "documents": documents,
        }
        logging.info(f"Sending payload to Flask API: {payload}")

        # Make the POST request
        response = requests.post(f"{os.getenv('LIGHTNING_SERVER_URL')}/add-collection", json=payload)

        # Log the response
        logging.info(f"Response status: {response.status_code}, Response body: {response.text}")

        # Raise an exception if the request fails
        response.raise_for_status()

        # Parse and return the response
        return response.json()

    except requests.exceptions.RequestException as e:
        error_message = e.response.text if e.response else "No response body"
        logging.error(f"Request failed: {error_message}")
        raise Exception(f"Failed to add collection: {error_message}")
