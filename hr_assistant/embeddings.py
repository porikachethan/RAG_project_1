
from openai import OpenAI
from langchain_core.embeddings import Embeddings
from hr_assistant import config


class JinaEmbeddingModel(Embeddings):

    def __init__(self):
        self.client = OpenAI(
            base_url="https://api.jina.ai/v1",
            api_key=config.JINA_API_KEY
        )

    def embed_documents(self, texts):
        response = self.client.embeddings.create(
            model=config.EMBEDDING_MODEL_NAME,
            input=texts,
            extra_body={"task": "retrieval.passage"}
        )

        return [item.embedding for item in response.data]

    def embed_query(self, text):
        response = self.client.embeddings.create(
            model=config.EMBEDDING_MODEL_NAME,
            input=[text],
            extra_body={"task": "retrieval.query"}
        )

        return response.data[0].embedding


def embedding_model():
    return JinaEmbeddingModel()



    
