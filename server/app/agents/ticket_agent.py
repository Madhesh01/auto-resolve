from langchain.agents import create_agent
from app.tools.order_tools import TOOLS
from app.llm import get_llm
from langchain_core.prompts import ChatPromptTemplate
import asyncio

SYSTEM_PROMPT = """You are an AI customer support agent for an e-commerce platform.
    You will receive a support ticket as a JSON object with these fields:
    - case_title: brief summary of the customer's issue
    - case_description: the customer's full message
    - case_owner: the customer's name

    Your job:
    1. Read case_title and case_description to understand what the customer needs
    2. Extract any order number mentioned in the description (look for phrases like "order #1234", "order number 1234", "my order 1234")
    3. Call the most appropriate tool to resolve the issue

    Important:
    - case_id is an internal ticket number — never use it as an order number
    - If no order number is mentioned in the description, ask for clarification by returning a text response
    - Always prefer the most specific tool (e.g. if customer wants to cancel, use cancel_order, not get_order_status)
    """



model = get_llm()



agent = create_agent(model=model, tools= TOOLS, system_prompt= SYSTEM_PROMPT)


async def execute_agent(ticket: dict):
    return await agent.ainvoke({
        "messages": [
            {"role": "user", "content": f"Resolve this support ticket {ticket}"}
        ]
    })


if __name__ == "__main__": 
    ticket = {"id": 25, "description": "Where is my order? Order number : 1001"}
    answer  = asyncio.run(execute_agent(ticket))




