
from langchain_chroma import Chroma

from hr_assistant import config
from hr_assistant.embeddings import embedding_model


# Build vector store
def build_vector_store(chunks):
    """Embed chunks and store them in ChromaDB."""

    embeddings_model = embedding_model()

    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings_model,
        collection_name=config.CHROMA_COLLECTION_NAME,
        persist_directory=config.CHROMA_PERSIST_DIRECTORY,
    )

    return vector_store


# Load vector store
def load_vector_store():
    """Load an existing ChromaDB collection."""

    embeddings_model = embedding_model()

    vector_store = Chroma(
        collection_name=config.CHROMA_COLLECTION_NAME,
        embedding_function=embeddings_model,
        persist_directory=config.CHROMA_PERSIST_DIRECTORY,
    )

    return vector_store


# Save vector store
def save_vector_store(vector_store):
    """ChromaDB automatically persists data to disk."""
    return vector_store


# Check vector store
def vector_store_exists() -> bool:
    """Check whether the ChromaDB collection contains documents."""

    client = Chroma(
        collection_name=config.CHROMA_COLLECTION_NAME,
        embedding_function=embedding_model(),
        persist_directory=config.CHROMA_PERSIST_DIRECTORY,
    )

    return client._collection.count() > 0


# Get retriever
def get_retriever(vector_store, k: int = config.TOP_K_RESULTS):
    """Return a retriever with top-k matching chunks."""

    return vector_store.as_retriever(
        search_kwargs={"k": k}
    )

