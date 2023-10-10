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
    price: float
    total_tickets: int
    location: str
    date_time: datetime


class EventCreate(EventBase):
    pass


class Event(EventBase):
    id: int
    organizer: int
    available_tickets: int

    class Config:
        orm_mode = True


class Ticket(BaseModel):
    id: int
    purchased_date: datetime
    event: Event
    user: User

    class Config:
        orm_mode = True
