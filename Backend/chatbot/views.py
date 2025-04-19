import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import os


class SendMessageView(APIView):
    """
    API View to act as a bridge between the frontend and the cloud chatbot API.
    """

    def post(self, request):
        """
        Forward the user message to the cloud chatbot API and return its response.

        Request:
        - JSON body with 'collection_name' and 'message' keys.

        Response:
        - JSON response from the chatbot API.
        """
        try:
            # Parse input JSON
            data = request.data

            # Retrieve the collection name and user message
            collection_name = data.get('collection_name')
            message = data.get('message')

            # Validate input
            if not collection_name or not message:
                return Response(
                    {"error": "Both 'collection_name' and 'message' are required."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Prepare the payload to forward to the cloud API
            payload = {
                "collection_name": collection_name,
                "message": message
            }

            # Send the request to the cloud chatbot API
            cloud_api_url = f"{os.getenv('LIGHTNING_SERVER_URL')}/send-message"
            response = requests.post(cloud_api_url, json=payload)

            # If the cloud API returns success
            if response.status_code == 200:
                return Response(response.json(), status=status.HTTP_200_OK)

            # If the cloud API returns an error
            return Response(
                {
                    "error": f"Cloud API returned an error. Status code: {response.status_code}",
                    "details": response.text,
                },
                status=response.status_code,
            )

        except requests.exceptions.RequestException as e:
            # Handle request exceptions
            return Response(
                {"error": f"Request to cloud API failed: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        except Exception as e:
            # Handle unexpected exceptions
            return Response(
                {"error": f"An unexpected error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
