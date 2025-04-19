from langchain_community.vectorstores import Milvus
from langchain.schema import Document
from langchain_core.runnables import Runnable
from pymilvus import connections, utility


class RetrieverManager:
    def __init__(self, uri: str | None, token: str | None, embedding_model):
        """
        Initialize the MilvusManager with connection details and embedding model.

        Args:
            uri (str): The URI of the Milvus instance.
            token (str): The token of the Milvus instance.
            embedding_model: The embedding model to use for document storage and queries.
        """
        self.uri = uri
        self.token = token
        self.embedding_model = embedding_model
        self.retrievers = {}


    def add_collection(self, collection_name: str, documents: list[Document]):
        """
        Add a Milvus collection.

        Args:
            collection_name (str): Name of the Milvus collection.
            documents (list[Document], optional): List of documents to initialize the collection. Defaults to None.
        """
        Milvus.from_documents(
            documents,
            self.embedding_model,
            collection_name=collection_name,
            connection_args={"uri": self.uri, "token": self.token},
        )

    def get_all_retrievers(self):
        """
        Retrieve all retrievers for previously stored collections in the database.

        Returns:
            dict: A dictionary of collection names and their corresponding retrievers.
        """
        try:
            # Establish connection to Milvus using pymilvus.connections
            connections.connect(
                alias="default",
                uri=self.uri,
                token=self.token
            )

            # Use pymilvus utility to list all collections
            collection_names = utility.list_collections()

            # Initialize retrievers for all collections
            for collection_name in collection_names:
                if collection_name not in self.retrievers:  # Avoid reinitializing existing retrievers
                    retriever = Milvus(
                        self.embedding_model,
                        collection_name=collection_name,
                        connection_args={"uri": self.uri, "token": self.token},
                    ).as_retriever()
                    self.retrievers[collection_name] = retriever

            return self.retrievers
        except Exception as e:
            raise RuntimeError(f"Failed to retrieve collections or initialize retrievers: {e}")


    def get_retriever(self, collection_name: str) -> Runnable:
        """
        Retrieve the retriever for a specific collection.

        Args:
            collection_name (str): Name of the Milvus collection.

        Returns:
            Runnable: The retriever for the specified collection.
        """
        if collection_name not in self.retrievers:
            raise ValueError(f"Collection '{collection_name}' not found.")
        return self.retrievers[collection_name]

