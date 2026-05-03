import redis.asyncio as aioredis
from dotenv import load_dotenv
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import json
import logging
import time
from langchain_core.messages import ToolMessage
from app.services.ticket_service import update_ticket, TicketNotFound
from app.agents.ticket_agent import execute_agent

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

file_handler = logging.FileHandler("worker.log")

formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

file_handler.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(file_handler)

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL")

if not REDIS_URL:
    raise ValueError("REDIS_URL not set in .env")

assert REDIS_URL

async def main():
    async with aioredis.from_url(REDIS_URL) as redis_client:
        logger.info("Worker started, waiting for tickets...")
        while True:
            case_id = None
            try:
                res = await redis_client.blpop("ticket_queue", timeout=0)

                ticket_data = res[1]
                ticket = json.loads(ticket_data.decode())
                case_id = ticket.get("case_id")
                logger.info(f"Received ticket: {case_id}")

                if not case_id:
                    raise ValueError("Missing case_id")

                llm_ticket = {k: v for k, v in ticket.items() if k != "case_id"}

                llm_start = time.monotonic()
                agent_response = await execute_agent(llm_ticket)
                llm_elapsed = time.monotonic() - llm_start
                logger.info(f"Agent inference for ticket {case_id} took {llm_elapsed:.2f}s")

                messages = agent_response["messages"]
                ai_resolution = messages[-1].content
                tool_messages = [m for m in messages if isinstance(m, ToolMessage)]

                if not tool_messages:
                    new_status = "Needs Info"
                else:
                    tool_result = json.loads(str(tool_messages[-1].content))
                    new_status = "Flagged" if tool_result.get("error") else "Resolved"

                logger.info(f"Ticket {case_id} → {new_status}")

                try:
                    await update_ticket(case_id, new_status, ai_resolution)
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
