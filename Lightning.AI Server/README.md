# Lightning.AI Server

The Lightning.AI Server is the computational backbone of the Talent Acquisition Hub, handling resource-intensive tasks such as document parsing, embedding generation, and conversational AI processing. This server operates with a modular design, split into offline and online components, to optimize efficiency and scalability.

## Modules

- `/offline_app`: Handles offline tasks like parsing resumes, and storing data in the vector database.
  - `embedding.py`: Implements the **dunzhang/stella_en_400M_v5** model to generate dense vector embeddings for resumes.
  - `parser.py`: Extracts structured data from uploaded PDF resumes.
  - `vectordb.py`: Manages connections and operations with the **Milvus** vector database, including storing and retrieving document embeddings.
  - `__init__.py`: An empty file used to mark this directory as a Python package.

- `/online_app`: Processes real-time user queries and manages the conversational AI pipeline.
  - `chatbot.py`: Orchestrates the RAG pipeline, including context retrieval and response generation.
  - `model.py`: Loads and manages the **meta-llama/Llama-3.2-3B-Instruct** model, tokenizer, and prompt template.
  - `utils.py`: Provides utility functions for online operations, such as formatting retrieved documents.
  - `__init__.py`: An empty file used to mark this directory as a Python package.

- `main.py`: Entry point for the Lightning.AI server, initializing and running both offline and online components.

- `requirements.txt`: Lists the Python dependencies required for the server.

- `install_marker.sh`: A shell script for setting up marker-pdf library.

- `.env`: Stores environment variables, such as database URIs, authentication tokens, and model configurations.

## Setup

### Prerequisite

- Python 3.10.0

### Setup your own lightning.ai server

- Go to [lightning.ai](https://lightning.ai/).
- Set up your own vscode studion
- transfer the lighning.ai server files there
- create your own server url using api builder
- replace the LIGHTNING_SERVER_URL env variable in the django backend env file with your server

### Install required dependencies

``` bash
pip install -r requirements.txt
chmod +x install_marker.sh
./install_marker.sh
```

### Run server

``` bash
python main.py
```
