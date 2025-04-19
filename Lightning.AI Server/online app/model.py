from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from langchain_core.prompts import PromptTemplate
from langchain_huggingface.llms import HuggingFacePipeline
import torch

class ModelManager:
    def __init__(self, model_id: str, torch_dtype=torch.bfloat16, device_map="auto"):
        """
        Initialize the ModelManager with a specified model ID.

        Args:
            model_id (str): Hugging Face model ID.
            torch_dtype: Torch data type for the model (default: torch.bfloat16).
            device_map: Device map for model loading (default: "auto").
        """
        self.model_id = model_id
        self.torch_dtype = torch_dtype
        self.device_map = device_map
        self.tokenizer = None
        self.model = None
        self.pipeline = None

    def load_model(self):
        """
        Load the tokenizer and model for the specified model ID.
        """
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_id)
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_id, 
            torch_dtype=self.torch_dtype, 
            device_map=self.device_map
        )

    def get_pipeline(self, max_new_tokens=2024):
        """
        Create a Hugging Face pipeline for text generation using the loaded model and tokenizer.

        Args:
            max_new_tokens (int): Maximum number of tokens for generation (default: 2024).
        
        Returns:
            HuggingFacePipeline: A LangChain-compatible pipeline for text generation.
        """
        if self.model is None or self.tokenizer is None:
            raise ValueError("Model and tokenizer must be loaded before creating a pipeline.")
        
        pipe = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            torch_dtype=self.torch_dtype,
            device_map=self.device_map,
            max_new_tokens=max_new_tokens
        )
        self.pipeline = HuggingFacePipeline(pipeline=pipe)
        return self.pipeline

    def get_prompt(self, messages):
        """
        Generate a prompt template based on the provided messages.

        Args:
            messages (list[dict]): A list of messages for the prompt template.

        Returns:
            PromptTemplate: A LangChain-compatible prompt template.
        """
        if self.tokenizer is None:
            raise ValueError("Tokenizer must be loaded before creating a prompt.")

        # Apply the chat template using the tokenizer
        formatted_prompt_template = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
            return_tensors=None,  # Ensure this returns a string, not tensors
        )

        # Define the prompt template with the correct input variable
        prompt_template = PromptTemplate(
            input_variables=["history", "context", "question"],  # Align this with the variable used in the chain
            template=formatted_prompt_template ,
        )
        return prompt_template
