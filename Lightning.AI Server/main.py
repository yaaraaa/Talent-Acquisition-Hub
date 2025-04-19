import os
import shutil
from dotenv import load_dotenv
from flask import Flask, request, jsonify, send_file
from langchain.schema import Document
from offline_app.embedding import StellaEmbedding
from offline_app.vectordb import RetrieverManager
from offline_app.parser import parse_pdf
from online_app.model import ModelManager
from online_app.chatbot import Chatbot
from langchain.memory import ConversationBufferWindowMemory
from langchain.retrievers.document_compressors.listwise_rerank import LLMListwiseRerank
from langchain.retrievers import ContextualCompressionRetriever
from langchain_openai import ChatOpenAI
from flask_cors import CORS


load_dotenv()

app = Flask(__name__)
CORS(app)


# Set the base directory for temporary file storage
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


stella_embedding_model = StellaEmbedding()

retriever_manager = RetrieverManager(
    uri=os.getenv("MILVUS-URI"), 
    token=os.getenv("MILVUS-TOKEN"), 
    embedding_model=stella_embedding_model
)

retriever_manager.get_all_retrievers()

model_manager = ModelManager(model_id="meta-llama/Llama-3.2-3B-Instruct")
model_manager.load_model()
pipeline = model_manager.get_pipeline(max_new_tokens=1024)

prompt_template = [
{"role": "system", "content": '''You are an intelligent talent acquisition assistant chatbot. 
Your primary role is to assist recruiters by analyzing candidates' resumes, understanding their qualifications, 
and answering questions about their suitability for specific roles. Provide detailed, professional, and context-aware responses.
this is the previous question and answer history if needed: {history}
Relevant Candidates Information:
{context}
'''},
{"role": "user", "content": '''
Recruiter's Question:
{question}'''},
]
formatted_prompt_template = model_manager.get_prompt(prompt_template)
print(formatted_prompt_template)

memory = ConversationBufferWindowMemory(k=10)

chatbot = Chatbot(memory, formatted_prompt_template, pipeline)

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
_filter = LLMListwiseRerank.from_llm(llm, top_n=6)



@app.route('/parse-pdfs', methods=['POST'])
def parse_pdfs():
    """
    Flask endpoint to handle batch PDF uploads, parse them, and return the output folder as a ZIP file.
    """
    try:
        if 'files' not in request.files:
            return jsonify({"error": "No files uploaded."}), 400

        files = request.files.getlist('files')  # Get all uploaded files

        # Define temporary input and output directories
        input_folder = os.path.join(MEDIA_ROOT, "input_docs")
        output_folder = os.path.join(MEDIA_ROOT, "output_docs")
        os.makedirs(input_folder, exist_ok=True)
        os.makedirs(output_folder, exist_ok=True)

        # Save uploaded files to the input folder
        for file in files:
            if not file.filename or not file.filename.endswith('.pdf'):
                return jsonify({"error": f"File '{file.filename}' is not a PDF. Skipping."}), 400

            file_path = os.path.join(input_folder, file.filename)
            file.save(file_path)

        # Call the parse_pdf function
        parse_pdf(input_folder, output_folder)

        # Create a ZIP file of the output folder
        output_zip_path = os.path.join(MEDIA_ROOT, "output_docs.zip")
        shutil.make_archive(output_zip_path.replace(".zip", ""), 'zip', output_folder)

        # Return the ZIP file as a response
        return send_file(output_zip_path, as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        # Clean up temporary folders
        for folder in [input_folder, output_folder]:
            if os.path.exists(folder):
                shutil.rmtree(folder)

        # Clean up the ZIP file
        if 'output_zip_path' in locals() and os.path.exists(output_zip_path):
            os.remove(output_zip_path)



@app.route('/add-collection', methods=['POST'])
def add_collection():
    try:
        data = request.get_json()

        collection_name = data.get('collection_name')
        documents_data = data.get('documents', [])

        if not collection_name or not documents_data:
            return jsonify({"error": "collection_name and documents are required"}), 400

        # Convert documents data to Document objects
        documents = [Document(**doc) for doc in documents_data]

        retriever_manager.add_collection(collection_name, documents)

        retriever_manager.get_all_retrievers()

        # Clear LangChain memory after creating a new collection
        memory.clear()

        return jsonify({"message": f"Collection '{collection_name}' added successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/send-message', methods=['POST'])
def send_message():
    try:
        # Parse input JSON
        data = request.get_json()

        # Retrieve the collection name and user message
        collection_name = data.get('collection_name')
        message = data.get('message')
        print(message)

        # Validate input
        if not collection_name or not message:
            return jsonify({"error": "Both 'collection_name' and 'message' are required."}), 400

        # Set up retriever for the chatbot
        retriever = retriever_manager.get_retriever(collection_name)
        compression_retriever = ContextualCompressionRetriever(base_compressor=_filter, base_retriever=retriever)

        chatbot.retriever = compression_retriever

        # Generate the chatbot's response
        response = chatbot.send_message(message)

        # Return the response to the user
        return jsonify({"response": response}), 200

    except KeyError as e:
        # Handle missing keys in input
        return jsonify({"error": f"Missing key: {str(e)}"}), 400

    except Exception as e:
        # Handle other unexpected exceptions
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

        response = chatbot.send_message(message)


def send_message_to_chatbot(collection_name, message):
    """
    Send a message to the chatbot and retrieve a response.

    Args:
        collection_name (str): The name of the collection to retrieve context from.
        message (str): The user's message.

    Returns:
        dict: A dictionary containing the chatbot's response or an error message.
    """
    try:
        # Validate input
        if not collection_name or not message:
            return {"error": "Both 'collection_name' and 'message' are required."}, 400

        # Set up retriever for the chatbot
        retriever = retriever_manager.get_retriever(collection_name)
        chatbot.retriever = retriever

        # Generate the chatbot's response
        response = chatbot.send_message(message)

        # Return the response
        return {"response": response}, 200

    except KeyError as e:
        # Handle missing keys in input
        return {"error": f"Missing key: {str(e)}"}, 400

    except Exception as e:
        # Handle other unexpected exceptions
        return {"error": f"An unexpected error occurred: {str(e)}"}, 500




if __name__ == '__main__':
    app.run(debug=True)
    #response = send_message_to_chatbot("collection_90a4fe791a87471da71e09daf767265e", "what are the names of the people in the resumes")
    #print(response)
