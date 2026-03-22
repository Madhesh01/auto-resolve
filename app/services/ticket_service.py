from app.redis import redis_client
from app.models.ticket import Ticket as TicketModel
from app.schemas.ticket import Ticket as TicketSchema
from app.db import AsyncSessionLocal
from sqlalchemy import select

async def get_ticket_status(case_id: int) :
    try: 
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(TicketModel).where(TicketModel.id == case_id))
            ticket = result.scalar_one_or_none()

            if not ticket: 
                return(f"Ticket {case_id} not found")
  
            
            return ticket.status
    
    except Exception as e:
        print(f"Error when getting ticket : {e}")
        raise

async def push_ticket_to_queue(ticket:TicketSchema):
    await redis_client.rpush("ticket_queue", ticket.model_dump_json())
    print(f"Pushed ticket with case id : {ticket.case_id} to queue")
   

async def insert_ticket(ticket: TicketSchema):
    try:
        async with AsyncSessionLocal() as session:
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
    except Exception as e:
        print(f"Error when inserting ticket : {e}")
        raise

async def update_ticket(case_id:int, status:str, ai_resolution:str): 
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(TicketModel).where(TicketModel.id == case_id))
        ticket = result.scalar_one_or_none()

        if not ticket:
            print(f"Ticket {case_id} not found")
            return 
        
        ticket.status = status
        ticket.ai_resolution = ai_resolution
        await session.commit()

        print(f"Ticket {case_id} updated - status : {status} | resolution : {ai_resolution}")