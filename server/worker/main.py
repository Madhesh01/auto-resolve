import redis.asyncio as aioredis
from dotenv import load_dotenv
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import json
import logging
from app.services.ticket_service import update_ticket, TicketNotFound

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

file_handler = logging.FileHandler("worker.log")

formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

file_handler.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(file_handler)

from app.tools.order_tools import TOOLS
from app.gemini import classify_intent

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL")

tool_map = {fn.__name__:fn for fn in TOOLS}

if not REDIS_URL:
    raise ValueError("REDIS_URL not set in .env")


async def main():
    async with aioredis.from_url(REDIS_URL) as redis_client:
        logger.info("Worker started, waiting for tickets...")
        while True:
            case_id = None
            try:
                res = await redis_client.blpop("ticket_queue", timeout=5)
                # Setting timeout returns None. Need to continue loop if None is returned
                if res is None:
                    logger.info("Worker alive, queue is empty")
                    continue

                ticket_data = res[1]
                ticket = json.loads(ticket_data.decode())
                logger.info(f"Received ticket : {ticket.get('case_id')}")
                gemini_ticket = {k: v for k, v in ticket.items() if k != "case_id"}
                case_id  = ticket.get('case_id')

                if not case_id:
                    raise ValueError("Missing case_id")

                intent_result = await classify_intent(gemini_ticket, TOOLS)
                # Using below as hardcoded values, not to get ratelimitted by gemini ;)
                # intent_result = {"tool": "update_shipping_address", "arguments": {"new_address": "23 Washington", "order_no": 23}}
                # intent_result = {"tool": "cancel_order", "arguments": {"order_no": 23}}
                logger.info(f"Gemini Result : {intent_result}")
                
                # Check whether request does not have enough info for gemini to process.
                # If so, the type of intent_result will be not be dict

                if isinstance(intent_result, dict):
                    tool_name = intent_result["tool"]
                    tool_args = intent_result["arguments"]
                    if tool_name not in tool_map:
                        raise ValueError(f"Unknown tool : {tool_name}")
                    
                    
                    tool_result = await tool_map[tool_name](**tool_args)

                    new_status = "Flagged" if tool_result.get("error") else "Resolved"
                    try:
                        await update_ticket(case_id, new_status, tool_result["message"])

                    except TicketNotFound:
                        logger.error("Ticket %s not found — skipping update", case_id)
                    
                    except Exception: 
                        logger.exception("DB commit failed for ticket %s — requeueing", case_id)
                        await redis_client.rpush("ticket_queue", ticket_data)

                # Gemini has requested for additonal response. Do not call tools. 
                else:
                    try:
                        await update_ticket(case_id, "Needs Info", intent_result)
                    except TicketNotFound:
                        logger.error("Ticket %s not found — skipping update", case_id)

                    except Exception:
                        logger.exception("DB commit failed for ticket %s — requeueing", case_id)
                        await redis_client.rpush("ticket_queue", ticket_data)



            except json.JSONDecodeError:
                logger.exception("Failed to decode JSON from queue")

            except Exception:
                logger.exception("Unexpected error processing ticket: %s", case_id)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())