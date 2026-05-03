from langchain_core.prompts import ChatPromptTemplate
from app.llm import get_llm
from pydantic import BaseModel
from typing import Literal


# STILL IN PROGRESS

system_instruction = """Classify this customer support agent resolution into exactly one category:
- NEEDS_INFO: The agent is asking the customer a question or requesting more details
- RESOLVED: The agent has provided a complete answer or taken a conclusive action
- ESCALATED: The agent has escalated to a human"""

class ClassifierResponse(BaseModel):
    response: Literal["NEEDS_INFO", "RESOLVED", "ESCALATED"]

model = get_llm().with_structured_output(ClassifierResponse)

prompt = ChatPromptTemplate.from_messages([
    ("system", system_instruction),
    ("human", "{response}")
])

chain = prompt | model

async def classify_response(resolution: str) -> str:
    result = await chain.ainvoke({"response": resolution})
    return result.response