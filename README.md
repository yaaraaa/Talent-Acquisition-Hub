# **TA-Chatbot: Talent Acquisition Hub**

The **Talent Acquisition Hub** project is an intelligent system designed to streamline the recruitment process by parsing resumes, retrieving relevant candidate information, and enabling conversational interactions with recruiters. It leverages cutting-edge technologies like **RAG pipelines**, **Milvus vector databases**, and **Hugging Face models** for efficient document processing and natural language understanding.

![image](https://github.com/user-attachments/assets/f67c6e91-f9fd-444a-a2e6-aacf7bd121f2)

## Features

- **Resume Parsing**: Processes PDF resumes, extracts structured data, and stores embeddings in a vector database.
- **RAG Pipeline**: Combines document retrieval with large language models for conversational AI.
- **Context-Aware Chatbot**: Maintains conversation history for follow-up questions and dynamic context handling.
- **Scalable Backend**: Implements a modular architecture using Django for APIs and Lightning.AI for GPU-accelerated tasks.
- **Interactive Frontend**: Built with Streamlit for resume uploads and chatbot interactions.

## Setup

### Prerequisite

- Python 3.10.0
- Docker and Docker Compose
- Git

### Clone the Reposository

``` bash
git clone https://github.com/yaaraaa/TA-Chatbot.git
cd TA-Chatbot
```

### Build and start the services using Docker Compose:

``` bash
docker compose build
docker compose up -d
```

### Access the system

- Access frontnd at `http://localhost:8501`
- Access backend at `http://localhost:8000`
