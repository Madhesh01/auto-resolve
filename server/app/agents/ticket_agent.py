from langchain.agents import create_agent
from app.tools.order_tools import TOOLS
from app.llm import get_llm
from langchain_core.prompts import ChatPromptTemplate
import asyncio

SYSTEM_PROMPT = """You are an AI customer support agent for an e-commerce platform.

You will receive a support ticket with a case_title, case_description, and case_owner.

Your job:
1. Extract the order number from the description. If none is mentioned, ask for clarification and do not call any tool.
2. When your action depends on the current order state, call get_order_status first and use the result to decide what to do next.
3. Call the most appropriate tool to resolve the issue.

Important:
- case_id is an internal ticket identifier — never treat it as an order number.
- Always respond in a clear, empathetic, and professional tone.
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




