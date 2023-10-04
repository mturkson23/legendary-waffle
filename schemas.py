from pydantic import BaseModel
from datetime import date, datetime


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    events: list = []

    class Config:
        orm_mode = True


class EventBase(BaseModel):
    title: str
    description: str
    total_tickets: int


class EventCreate(EventBase):
    user_id: int
    booking_date: date


class Event(EventBase):
    id: int
    # organizer: User
    available_tickets: int
    booking_date: datetime

    class Config:
        orm_mode = True


class TicketBase(BaseModel):
    price: int


class TicketCreate(TicketBase):
    user_id: int
    event_id: int


class Ticket(TicketBase):
    id: int
    purchased_date: str
    event: Event
    user: User

    class Config:
        orm_mode = True
