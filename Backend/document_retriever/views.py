import requests
import zipfile
import os
import io
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .logic.doc_splitter import DocumentSplitter
from .logic.collection import add_collection
import re
import uuid
from .utils import clear_directory


class ParseAndStoreCVsView(APIView):
    """
    API View to act as a bridge between the frontend and the cloud parser.
    """

    OUTPUT_DIR = "output_docs"  # Directory to save extracted files
    splitter = DocumentSplitter()

    def sanitize_file_name(self, file_name):
        """
        Sanitize the file name to remove invalid characters for Windows file systems.
        """
        sanitized_name = re.sub(r'[<>:"/\\|?*]', '_', file_name)
        return sanitized_name

    def post(self, request):
        """
        Handle batch upload of PDFs, forward to the cloud parser, and save the results locally.

        Returns:
        - JSON response with the parsing status and the collection name.
        """
        if 'files' not in request.FILES:
            return Response({"error": "No files uploaded."}, status=status.HTTP_400_BAD_REQUEST)

        files = request.FILES.getlist('files')  # Get all uploaded files

        try:
            # Forward the files to the cloud parser
            files_to_upload = [
                ('files', (file.name, file.read(), 'application/pdf')) for file in files
            ]
            response = requests.post(
                f"{os.getenv('LIGHTNING_SERVER_URL')}/parse-pdfs", files=files_to_upload, stream=True
            )

            # If cloud parser returns a ZIP file
            if response.status_code == 200:
                # Ensure output directory exists
                os.makedirs(self.OUTPUT_DIR, exist_ok=True)

                # Extract the ZIP file content while preserving folder structure
                with zipfile.ZipFile(io.BytesIO(response.content)) as z:
                    for file_name in z.namelist():
                        # Process only Markdown files
                        if not file_name.endswith(".md"):
                            continue

                        # Sanitize file paths
                        sanitized_file_name = self.sanitize_file_name(file_name)

                        # Determine the full output path
                        output_file_path = os.path.join(self.OUTPUT_DIR, sanitized_file_name)

                        # Ensure subdirectories exist
                        os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

                        # Save non-empty files
                        with z.open(file_name) as f:
                            file_content = f.read()
                            if not file_content.strip():
                                continue

                            # Write the file to the appropriate path
                            with open(output_file_path, "wb") as output_file:
                                output_file.write(file_content)

                # Split documents and create a new collection
                splitter = DocumentSplitter()
                docs = splitter.load_documents(self.OUTPUT_DIR)
                print("these are the docs: ", docs)
                chunks = splitter.split_documents(docs)
                collection_name = f"collection_{uuid.uuid4().hex}"
                add_collection(collection_name=collection_name, documents=chunks)

                # Return the collection name
                return Response(
                    {
                        "results": "CVs parsed and stored successfully",
                        "collection_name": collection_name
                    },
                    status=status.HTTP_200_OK
                )

            else:
                return Response(
                    {
                        "error": f"Cloud parser returned an error. Status code: {response.status_code}",
                        "details": response.text,
                    },
                    status=response.status_code,
                )

        except requests.exceptions.RequestException as e:
            return Response(
                {"error": f"Request to cloud parser failed: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        except Exception as e:
            return Response(
                {"error": f"An unexpected error occurred: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        finally:
            clear_directory(self.OUTPUT_DIR)
