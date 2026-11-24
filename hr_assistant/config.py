# load env file 

import os 
from dotenv import load_dotenv
load_dotenv()

# loading api keys 

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
JINA_API_KEY = os.getenv("JINA_API_KEY")

# define path data/vectorstore 
DATA_FILE_PATH = os.path.join("data","hr_policy.txt")

# vector store
VECTOR_STORE_PATH = os.path.join("data","faiss_index")
CHROMA_PERSIST_DIRECTORY = "./chroma_db"
CHROMA_COLLECTION_NAME = "hr_policy"



#chunking strategies 
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

# llm models and embedding models 
LLM_MODEL_NAME = "openai/gpt-oss-120b"
EMBEDDING_MODEL_NAME = "jina-embeddings-v3" 

# retrival results 
TOP_K_RESULTS = 3

#system instructions

SYSTEM_PROMPT = ("you are a friendly    HR_Policy assistant you have to look up for"

"search_hr_policy tool to answer the query. you didnt find the answer simply say"
" answer not found please check your query ones")

def clear_api_key ()->None:
    """ stop early if you did't find API key"""
  
    if not GROQ_API_KEY:
        raise ValueError("missing GROQ_API_KEY ")
    if not JINA_API_KEY:
        raise ValueError("missing JINA_API_KEY ")    


