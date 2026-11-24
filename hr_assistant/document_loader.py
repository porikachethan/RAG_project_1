from langchain_core.documents import Document
from hr_assistant import config

def load_document(file_path: str = config.DATA_FILE_PATH):
    """Load a .txt file and return a LangChain Document object."""

    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()

    documents = Document(
        page_content=text,
        metadata={"source": file_path}
    )

    return documents
