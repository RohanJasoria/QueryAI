# embedding.py

from sentence_transformers import SentenceTransformer

class EmbeddingGenerator:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

    def generate_embedding(self, text: str):
        # Generate the embedding for the given text
        return self.model.encode(text).tolist()
