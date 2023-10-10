from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.exceptions import HTTPException
from fastapi.encoders import jsonable_encoder
from database import get_db
from schemas import Event, EventCreate, User
from controllers import (
    create_event,
    get_events,
    get_event,
    get_event_organizer,
    update_event,
    create_ticket,
)
from .auth import get_current_user

router = APIRouter(prefix="/events")


@router.get("/")
def get_event_bookings(db: Session = Depends(get_db)):
    return get_events(db=db)


@router.get("/{booking_id}")
def get_event_booking(booking_id: int, db: Session = Depends(get_db)):
    event = get_event(db=db, event_id=booking_id)
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return event


@router.post("/", response_model=Event)
def create_event_booking(
    booking: EventCreate,
    db: Session = Depends(get_db),
    token: str = Depends(get_current_user),
):
    return create_event(db=db, event=booking, user_id=token.id)


@router.get("/{booking_id}/organizer")
def get_event_booking_organizer(booking_id: int, db: Session = Depends(get_db)):
    organizer = get_event_organizer(db=db, event_id=booking_id)
    if organizer is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return User(username=organizer.username, id=organizer.id)


@router.patch("/{booking_id}")
def update_event_booking(
    booking: dict,
    booking_id: int,
    db: Session = Depends(get_db),
    token: str = Depends(get_current_user),
):
    event_item = get_event(db=db, event_id=booking_id)
    if event_item is None:
        raise HTTPException(status_code=404, detail="Event not found")
    if event_item.organizer != token.id:
        raise HTTPException(
            status_code=401, detail="You are not authorized to update this event"
        )
    updated_event = update_event(db=db, event_data=booking, event_id=booking_id)
    return updated_event


@router.delete("/{booking_id}")
def delete_event_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    token: str = Depends(get_current_user),
):
    event_item = get_event(db=db, event_id=booking_id)
    if event_item is None:
        raise HTTPException(status_code=404, detail="Event not found")
    if event_item.organizer_id != token.id:
        raise HTTPException(
            status_code=401, detail="You are not authorized to delete this event"
        )
    db.delete(event_item)
    db.commit()
    return {"message": "Event deleted successfully"}


@router.post("/{booking_id}/buy")
def buy_event_ticket(
    booking_id: int,
    db: Session = Depends(get_db),
    token: str = Depends(get_current_user),
):
    event_item = get_event(db=db, event_id=booking_id)
    if event_item is None:
        raise HTTPException(status_code=404, detail="Event not found")
    ticket = create_ticket(db=db, user_id=token.id, event_id=booking_id)
    if ticket is None:
        raise HTTPException(status_code=400, detail="No tickets available")
    return ticket
