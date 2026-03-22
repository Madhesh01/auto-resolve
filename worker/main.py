import redis.asyncio as aioredis
from dotenv import load_dotenv
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import json

from pprint import pprint
from app.services.ticket_service import update_ticket




from app.tools.order_tools import TOOLS
from app.gemini import classify_intent

load_dotenv()

TOOLS = TOOLS
REDIS_URL = os.getenv("REDIS_URL")

tool_map = {fn.__name__:fn for fn in TOOLS}

if not REDIS_URL:
    raise ValueError("REDIS_URL not set in .env")

redis_client = aioredis.from_url(REDIS_URL)

async def main():

    while True:
        try:
            res = await redis_client.blpop("ticket_queue")
            ticket_data = res[1]

            ticket = json.loads(ticket_data)
            print(f"\n Received ticket : {ticket.get('case_id', 'Unknown ID')}")
            gemini_ticket = {k: v for k, v in ticket.items() if k != "case_id"}
            case_id  = ticket.get('case_id', 'UnkownID')

            intent_result = await classify_intent(gemini_ticket, TOOLS)
            # Using below as hardcoded values, not to get ratelimitted by gemini ;)
            # intent_result = {"tool": "update_shipping_address", "arguments": {"new_address": "23 Washington", "order_no": 23}}
            # intent_result = {"tool": "cancel_order", "arguments": {"order_no": 23}}
            print(f"Gemini Result : {intent_result}")
            
            # Check whether request does not have enough info for gemini to process.
            # If so, the type of intent_result will be not be dict

            if isinstance(intent_result, dict):
                tool_name = intent_result["tool"]
                tool_args = intent_result["arguments"]
                tool_result = await tool_map[tool_name](**tool_args)
                if tool_result["error"]:
                    await update_ticket(case_id, "Flagged", tool_result["message"])
                else:   
                    await update_ticket(case_id, "Resolved", tool_result["message"])

            # Gemini has requested for additonal response. Do not call tools. 
            else:
                await update_ticket(case_id, "Needs Info", intent_result)



        except json.JSONDecodeError:
            print(f"Error: Failed to decode JSON from queue: {res[1]}")

        except Exception as e:
            print(f"Unexpected error processing ticket: {e}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())