from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from schemas import Event, EventCreate
from controllers import create_event, get_events, get_event

router = APIRouter(prefix="/bookings")

@router.get("/")
def get_bookings(db: Session = Depends(get_db)):
    return get_events(db=db)

@router.get("/{booking_id}")
def get_booking(booking_id: int, db: Session = Depends(get_db)):
    return get_event(db=db, event_id=booking_id)

@router.post("/", response_model=Event)
def create_booking(booking: EventCreate, db: Session = Depends(get_db)):
    return create_event(db=db, event=booking)