from langchain_text_splitters import RecursiveCharacterTextSplitter
from hr_assistant import config

def spliting_into_chunks (documents):
    """ split documents into small overlap chunks """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = config.CHUNK_SIZE,
        chunk_overlap = config.CHUNK_OVERLAP
    )

    return splitter.split_documents([documents])