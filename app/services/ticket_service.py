from app.redis import redis_client
from app.schemas.ticket import Ticket

async def push_ticket_to_queue(ticket:Ticket):
    await redis_client.rpush("ticket_queue", ticket.model_dump_json())
   

