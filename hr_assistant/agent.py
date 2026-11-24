from langchain.agents import create_agent
from hr_assistant import config 

def create_hr_agent(llm,tools):
 """ return a langchain agent which calls tools answer question """
         
 return create_agent(
    model = llm,
    tools = tools,
    system_prompt= config.SYSTEM_PROMPT
 )  
