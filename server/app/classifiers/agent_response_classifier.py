from langchain_core.prompts import ChatPromptTemplate
from app.llm import get_llm
from dataclasses import dataclass
from pydantic import BaseModel
from typing import Literal
from langchain_core.output_parsers import PydanticOutputParser

system_instruction = """Classify this customer support agent resolution into exactly one category:
- NEEDS_INFO: The agent is asking the customer a question or requesting more details
- RESOLVED: The agent has provided a complete answer or taken a conclusive action
- ESCALATED: The agent has escalated to a human"""

class ClassifierResponse(BaseModel): 
    response: Literal["NEEDS_INFO", "RESOLVED", "ESCALATED"]
    

model = get_llm().with_structured_output(ClassifierResponse)
prompt = ChatPromptTemplate.from_messages(messages=(
    ("system", f"{system_instruction}"), 
    ("human", "{response}")
))

output_parser = PydanticOutputParser(pydantic_object=ClassifierResponse)

chain = prompt | model | output_parser
async def classify_response(resolution: str) -> str: 
    
    response = await chain.ainvoke({"response": resolution})
    
    return response
    
    
    
    
    
    
    