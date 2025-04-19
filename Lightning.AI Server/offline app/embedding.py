import os
from sentence_transformers import SentenceTransformer
from huggingface_hub import login


class StellaEmbedding:
    def __init__(self, model_name="dunzhang/stella_en_400M_v5", device="cuda"):
        """Load the model (initialize only once)"""
        login(token=os.getenv("HUGGINGFACE-ACCESS-TOKEN"))

        self.model = SentenceTransformer(model_name, trust_remote_code=True).to(device)
        self.query_prompt_name = "s2p_query"

    def embed_documents(self, texts):
        """Embed multiple documents."""
        return self.model.encode(texts, show_progress_bar=False)

    def embed_query(self, query):
        """Embed a single query."""
        return self.model.encode([query], prompt_name=self.query_prompt_name, show_progress_bar=False)[0]


