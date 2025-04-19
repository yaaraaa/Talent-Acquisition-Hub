from .model import ModelManager
from langchain_core.runnables import RunnablePassthrough
from .utils import format_docs


class Chatbot:
    """
    A chatbot class designed for talent acquisition and recruitment use cases.
    It processes user queries, retrieves relevant contextual information, and generates responses using a pipeline.

    Attributes:
        memory: A memory object for managing chat history and state.
        prompt_template: A string template for formatting prompts dynamically.
        pipeline: A pipeline object responsible for generating responses.
        retriever: (Optional) A retriever object for fetching relevant documents.
    """
    
    def __init__(self, memory, prompt_template, pipeline, retriever=None):
        """
        Initializes the Chatbot class with memory, a prompt template, a pipeline, and an optional retriever.

        Args:
            memory: The memory object used to manage chat history.
            prompt_template: A template string for dynamically formatting prompts.
            pipeline: The pipeline object that generates responses from the formatted prompt.
            retriever: (Optional) An object to retrieve relevant documents for context.
        """
        self.memory = memory
        self.prompt_template = prompt_template
        self.pipeline = pipeline
        self.retriever = retriever

    def send_message(self, message):
        """
        Processes a user query, retrieves context, generates a response, and updates chat history.

        Args:
            message (str): The user's query.

        Returns:
            str: The generated response, extracted to include only content after <|start_header_id|>assistant<|end_header_id|>.
        """
        try:
            # Load memory and retrieve context
            memory_data = self.memory.load_memory_variables({})
            context_data = self.retriever.invoke(message) if self.retriever else []

            # Format the retrieved context into a readable string
            formatted_context = format_docs(context_data)

            # Dynamically format the prompt
            formatted_prompt = self.prompt_template.format(
                history=memory_data,
                context=formatted_context,
                question=message
            )

            # Generate the response
            full_response = self.pipeline.invoke(formatted_prompt)

            # Extract content after <|start_header_id|>assistant<|end_header_id|>
            extracted_response = full_response.split("<|start_header_id|>assistant<|end_header_id|>", 1)[-1].strip()

            # Save the interaction in memory
            self.memory.save_context({"input": message}, {"output": extracted_response})

            return extracted_response
        except Exception as e:
            print(f"Error in send_message: {e}")
            return "An error occurred while processing your request."
