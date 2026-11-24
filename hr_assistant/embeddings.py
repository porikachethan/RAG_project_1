import os
import requests
from openai import OpenAI
from langchain_core.embeddings import Embeddings
from hr_assistant import config
from hr_assistant.document_loader import load_document


def embedding_model():
    """Returns Jina embedding model and reads JINA_API_KEY from environment."""

    client = OpenAI(
        base_url="https://api.jina.ai/v1",
        api_key=config.JINA_API_KEY
    )

    return client.embeddings.create( model=config.EMBEDDING_MODEL_NAME)



    
