from dotenv import load_dotenv
import os 
from langchain_core.messages import SystemMessage, HumanMessage


load_dotenv()

LLM_PROVIDER: str = os.getenv("LLM_PROVIDER") or "gemini"

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

def get_llm():

    if LLM_PROVIDER.lower() == "ollama":
        from langchain_ollama import ChatOllama
        return ChatOllama(model=os.getenv("OLLAMA_MODEL", "qwen2.5:7b"),base_url=os.getenv("OLLAMA_HOST", "http://localhost:11434"), temperature=0)

    
    else: 
        GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
        if not GEMINI_API_KEY:
            raise Exception("Gemini API key not set in env")
        from langchain_google_genai import ChatGoogleGenerativeAI
        return ChatGoogleGenerativeAI(model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite"), temperature=0)
    

async def classify_intent(ticket: dict, tools: list) -> dict | str:
    
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=f"Resolve this support ticket: {ticket}")
    ]
    
    llm = get_llm().bind_tools(tools)
    
    response = await llm.ainvoke(messages)
    
    if response.tool_calls: 
        return {
            "tool": response.tool_calls[0]["name"], 
            "arguments": response.tool_calls[0]["args"]
            
        }

    return response.content