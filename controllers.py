from sqlalchemy.orm import Session
import bcrypt
from datetime import datetime

import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreateRequest):
    hashed_password = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt())
    db_user = models.User(username=user.username, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_events(db: Session, user_id: int):
    return db.query(models.Event).filter(models.Event.organizer == user_id).all()


def get_event(db: Session, event_id: int):
    return db.query(models.Event).filter(models.Event.id == event_id).first()


def get_event_organizer(db: Session, event_id: int):
    organizer = (
        db.query(models.Event).filter(models.Event.id == event_id).first().organizer
    )
    return get_user(db, organizer)


def get_events(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Event).offset(skip).limit(limit).all()


def create_event(db: Session, event: schemas.EventRequest, user_id: int):
    db_event = models.Event(
        title=event.title,
        description=event.description,
        date_time=event.date_time,
        total_tickets=event.total_tickets,
        available_tickets=event.total_tickets,
        organizer=user_id,
        price=event.price,
        location=event.location,
    )
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


def update_event(db: Session, event_data: dict, event_id: int):
    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    for key, value in event_data.items():
        setattr(event, key, value)
    db.commit()
    db.refresh(event)
    return event


def delete_event(db: Session, event_id: int):
    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    db.delete(event)
    db.commit()
    return event


def create_ticket(db: Session, user_id: int, event_id: int):
    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if event.available_tickets == 0:
        return None
    event.available_tickets -= 1
    db_ticket = models.Ticket(
        user_id=user_id,
        event_id=event_id,
        purchased_date=datetime.utcnow(),
    )
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket


def get_ticket(db: Session, ticket_id: int):
    return db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()


def get_tickets(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Ticket).offset(skip).limit(limit).all()
