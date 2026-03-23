from fastapi import APIRouter, status
from app.schemas.ticket import Ticket
from app.services.ticket_service import push_ticket_to_queue, insert_ticket, get_ticket_status, get_tickets


router = APIRouter()

 
@router.post('/ticket', status_code=202)
async def push_ticket(ticket: Ticket):
    case_id = await insert_ticket(ticket)
    ticket.case_id = case_id
    await push_ticket_to_queue(ticket)
    return {"case_id" : case_id}


@router.get('/ticket/{id}/status')
async def get_ticket(id: int):
    ticket_status = await get_ticket_status(id)
    return {"status": ticket_status} 

@router.get('/tickets')
async def get_all_tickets():
    tickets = await get_tickets()
    return tickets
