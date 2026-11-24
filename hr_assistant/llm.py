from langchain_groq import ChatGroq
from hr_assistant import config

def get_llm():
    """ return a groq llm chat model which reads the GROQ_API_KEY from env """
    return ChatGroq(model = config.LLM_MODEL_NAME,temperature = 0 )