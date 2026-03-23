from app.redis import redis_client
from app.models.ticket import Ticket as TicketModel
from app.schemas.ticket import Ticket as TicketSchema
from app.db import AsyncSessionLocal
from sqlalchemy import select



class TicketNotFound(Exception):
    def __init__(self, case_id:int): 
        self.case_id = case_id
        super().__init__(f"Ticket {case_id} not found")

class QueueError(Exception):
    def __init__(self, ticket_case_id:int | None):
        self.ticket_case_id = ticket_case_id
        super().__init__(f"Failed to push ticket {ticket_case_id} to queue")


async def get_ticket_status(case_id: int) :
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(TicketModel).where(TicketModel.id == case_id))
        ticket = result.scalar_one_or_none()

        if not ticket: 
            raise TicketNotFound(case_id)
        
        return ticket.status
        
async def push_ticket_to_queue(ticket:TicketSchema):
    try:
        await redis_client.rpush("ticket_queue", ticket.model_dump_json())
        print(f"Pushed ticket with case id : {ticket.case_id} to queue")
    except Exception as e:
        raise QueueError(ticket.case_id) from e

   

async def insert_ticket(ticket: TicketSchema):
    async with AsyncSessionLocal() as session:
        try:
            new_ticket = TicketModel(
                title=ticket.case_title,
                owner=ticket.case_owner,
                description=ticket.case_description, 
                status="Pending"
            )
            session.add(new_ticket)
            await session.commit()
            await session.refresh(new_ticket)
            return new_ticket.id
        except Exception:
            await session.rollback()
            raise


async def update_ticket(case_id:int, status:str, ai_resolution:str): 
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(TicketModel).where(TicketModel.id == case_id))
        ticket = result.scalar_one_or_none()

        if not ticket:
            raise TicketNotFound(case_id)
        
        try:
            ticket.status = status
            ticket.ai_resolution = ai_resolution
            await session.commit()
            print(f"Ticket {case_id} updated - status : {status} | resolution : {ai_resolution}")

        except Exception:
            await session.rollback()
            raise

async def get_tickets():
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(TicketModel))
        tickets = result.scalars().all()
        return [
            {
                "case_id": ticket.id,
                "case_title": ticket.title,
                "case_owner": ticket.owner,
                "case_description": ticket.description,
                "case_status": ticket.status,
                "ai_resolution": ticket.ai_resolution,
            }
            
            for ticket in tickets
        ]
