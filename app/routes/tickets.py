from fastapi import APIRouter, status
from app.schemas.ticket import Ticket
from app.services.ticket_service import push_ticket_to_queue  


router = APIRouter()

 
@router.post('/ticket', status_code=202)
async def push_ticket(ticket: Ticket):
    await push_ticket_to_queue(ticket)


@router.get('/ticket/{id}/status')
async def get_ticket(id: int):
    pass 

