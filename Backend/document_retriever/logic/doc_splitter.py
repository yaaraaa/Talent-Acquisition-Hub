import os
import uuid
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from openai import OpenAI

class DocumentSplitter:
    """
    Handles splitting of parsed documents into smaller chunks with metadata.
    """

    def __init__(self, chunk_size=500, chunk_overlap=50):
        """
        Initialize the DocumentSplitter with chunking configuration.

        Args:
        - chunk_size (int): Size of each chunk (default: 500).
        - chunk_overlap (int): Overlap between chunks (default: 50).
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap
        )
        self.client = OpenAI()

    def extract_name_from_content(self, content):
        """
        Extract the candidate's name from the resume's content using OpenAI.

        Args:
        - content (str): The content of the resume.

        Returns:
        - str: Extracted candidate name.
        """
        try:
            # Prompt to instruct OpenAI to extract the name
            prompt = (
                "Extract the candidate's full name from the following text:\n\n"
                f"{content}\n\n"
                "Return only the name, nothing else."
            )

            response = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": f"{prompt}",
                    }
                ],
                model="gpt-4o",
            )

            # Extract the name from the response
            name = response.choices[0].message.content.strip()
            return name.lower()
        except Exception as e:
            print(f"Error extracting name with OpenAI: {e}")
            return "Unknown"  # Default name if extraction fails


    def load_documents(self, path):
        """
        Load resumes into LangChain documents with metadata.

        Args:
        - path (str): Path to the directory containing markdown resumes.

        Returns:
        - list: A list of LangChain document objects.
        """
        documents = []
        if not os.path.isdir(path):
            raise ValueError(f"The provided path '{path}' is not a valid directory.")

        for root, _, files in os.walk(path):
            for file in files:
                if file.endswith('.md'):  # Only process markdown files
                    file_path = os.path.join(root, file)

                    try:
                        loader = UnstructuredMarkdownLoader(file_path)
                        data = loader.load()

                        # Extract metadata
                        extracted_name = self.extract_name_from_content(data[0].page_content)   
                        candidate_id = str(uuid.uuid4())[:8]

                        # Add metadata to the first document
                        data[0].metadata["name"] = extracted_name
                        data[0].metadata["candidate_id"] = candidate_id

                        documents.append(data)
                    except Exception as e:
                        print(f"Error loading file '{file}': {e}")

        return documents


    def split_documents(self, documents):
        """
        Split documents into smaller chunks using the RecursiveCharacterTextSplitter.

        Args:
        - documents (list): List of LangChain document objects.

        Returns:
        - list: A list of chunked document objects.
        """
        chunks = []
        for doc in documents:
            try:
                splits = self.text_splitter.split_documents(doc)
                chunks.extend(splits)
            except Exception as e:
                print(f"Error splitting document: {e}")

        return chunks
