from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.exceptions import HTTPException
from database import get_db
from schemas import TicketRequest
from controllers import get_ticket, get_tickets

router = APIRouter(prefix="/tickets")


@router.get("/{ticket_id}", response_model=TicketRequest)
def read_ticket(ticket_id: int, db: Session = Depends(get_db)):
    ticket = get_ticket(db=db, ticket_id=ticket_id)
    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket


@router.get("/", response_model=list[TicketRequest])
def read_tickets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tickets = get_tickets(db=db, skip=skip, limit=limit)
    return tickets


# To be checked out later
# @router.get("/{ticket_id}/receipt")
# def get_ticket_receipt(ticket_id: int, db: Session = Depends(get_db)):
#     ticket = get_ticket(db=db, ticket_id=ticket_id)
#     if ticket is None:
#         raise HTTPException(status_code=404, detail="Ticket not found")
#
