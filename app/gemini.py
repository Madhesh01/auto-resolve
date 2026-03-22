from google import genai
from google.genai import Client, types
from dotenv import load_dotenv
import os

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
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

async def classify_intent(ticket: dict, available_tools: list) -> str | dict:

    print(f"Payload to Gemini. Ticket : {ticket}")
    async with Client().aio as aclient:
        response = await aclient.models.generate_content(
            model="gemini-2.5-flash-lite", 
            contents=f"Resolve this support ticket : {ticket}",
            config=types.GenerateContentConfig(
                tools=available_tools,
                temperature=0.0, 
                tool_config=types.ToolConfig(
                    function_calling_config=types.FunctionCallingConfig(
                        mode=types.FunctionCallingConfigMode.AUTO
                    )
                ),
                system_instruction=SYSTEM_PROMPT,
                # GeminiSDK calls the function being sent by default. This is to prevent that from happening.
                automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True)
            ) 
        )
    
    
    # Use the built-in helper property to return which function to call
    if response.function_calls:
        fc = response.function_calls[0]
        return {
            "tool": fc.name,
            "arguments": fc.args
        }
    
    # Fallback
    if response.text:
        print("Printing from Fallback")
        return response.text
    
    # Fallback
    if response.candidates:
        print("Printing from fallback")
        finish_reason = response.candidates[0].finish_reason
        print(f"DEBUG - Content was empty. Finish Reason : {finish_reason}")

        
    
    return "No tools matched and no text returned"
