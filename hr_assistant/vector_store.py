
from langchain_chroma import Chroma

from hr_assistant import config
from hr_assistant.embeddings import get_embeddings_model

# build_vector_store

def build_vector_store(chunks):
    """Embed every chunk and store it in a local ChromaDB collection."""
    embeddings_model = get_embeddings_model()

    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings_model,
        collection_name=config.CHROMA_COLLECTION_NAME,
        persist_directory=config.CHROMA_PERSIST_DIRECTORY,
    )


    return vector_store

# load_vector_store

def load_vector_store():
    """Connect to an existing ChromaDB collection."""

    embeddings_model = get_embeddings_model()

    return Chroma(
        collection_name=config.CHROMA_COLLECTION_NAME,
        embedding_function=embeddings_model,
        persist_directory=config.CHROMA_PERSIST_DIRECTORY,
    )

# save vector store
def save_vector_store(vector_store):
    """ChromaDB automatically saves data to disk."""
    return vector_store
    
    
# vector_store_exists

def vector_store_exists() -> bool:
    """Check whether the ChromaDB collection already exists."""

    client = Chroma(
        collection_name=config.CHROMA_COLLECTION_NAME,
        embedding_function=get_embeddings_model(),
        persist_directory=config.CHROMA_PERSIST_DIRECTORY,
    )

    return client._collection.count() > 0

# get_retriever

def get_retriever(vector_store, k: int = config.TOP_K_RESULTS):
    """Return a retriever that fetches the top-k matching chunks."""

    return vector_store.as_retriever(search_kwargs={"k": k})
