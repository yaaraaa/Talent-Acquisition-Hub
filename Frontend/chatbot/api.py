import requests

class ChatbotAPIClient:
    """
    A client for interacting with the Chatbot Django REST API.
    """
    
    def __init__(self, api_base_url, headers=None):
        """
        Initialize the API client.
        Args:
        - headers (dict): Optional headers for the requests (e.g., authentication).
        """
        self.api_base_url = api_base_url
        self.headers = headers or {}

    def send_message(self, collection_name, message):
        """
        Send a message to the chatbot and receive a response.

        Args:
        - collection_name (str): The collection name for the chatbot retriever.
        - message (str): The user's message.

        Returns:
        - dict: A dictionary with the API response or an error message.
        """
        endpoint = f"{self.api_base_url}/send-message/"
        payload = {
            "collection_name": collection_name,
            "message": message
        }
        try:
            response = requests.post(endpoint, json=payload, headers=self.headers)
            if response.status_code == 200:
                return {"success": True, "response": response.json()}
            else:
                return {
                    "success": False,
                    "error": f"API returned an error. Status code: {response.status_code}",
                    "details": response.text,
                }
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": f"Request failed: {e}"}
        except Exception as e:
            return {"success": False, "error": f"An unexpected error occurred: {e}"}
