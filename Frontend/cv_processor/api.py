import requests


class APIClient:
    """
    A client for interacting with the local Django REST API.
    """
    def __init__(self, api_base_url, headers=None):
        """
        Initialize the API client.
        Args:
        - api_base_url (str): Base URL of the Django REST API.
        - headers (dict): Optional headers for the requests (e.g., authentication).
        """
        self.api_base_url = api_base_url
        self.headers = headers or {}

    def upload_pdfs(self, files):
        """
        Upload multiple PDF files to the local Django REST API.

        Args:
        - files: List of Streamlit UploadedFile objects.

        Returns:
        - dict: A dictionary with the API response or an error message.
        """
        endpoint = f"{self.api_base_url}/parse-store-cvs/"
        try:
            # Prepare files for upload
            files_to_upload = [
                ('files', (file.name, file, 'application/pdf')) for file in files
            ]
            response = requests.post(endpoint, files=files_to_upload, headers=self.headers)

            if response.status_code == 200:
                return {"success": True, "data": response.json()}
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