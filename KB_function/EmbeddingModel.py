from langchain.embeddings.huggingface import HuggingFaceBgeEmbeddings
import configs

class EmbeddingModel():
    def __init__(self):
        model_path = configs.embedding_model_path
        encode_kwargs = {'normalize_embeddings': True}  # set True to compute cosine similarity
        self.model = HuggingFaceBgeEmbeddings(model_name=model_path, encode_kwargs=encode_kwargs)
    def get_model(self):
        return self.model
