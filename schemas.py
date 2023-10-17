from pydantic import BaseModel
from datetime import date, datetime


class UserBase(BaseModel):
    username: str


class UserCreateRequest(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    events: list = []

    class Config:
        orm_mode = True


class EventRequest(BaseModel):
    title: str
    description: str
    price: float
    total_tickets: int
    location: str
    date_time: datetime


class EventResponse(EventRequest):
    id: int
    organizer: int
    available_tickets: int

    class Config:
        orm_mode = True


class TicketRequest(BaseModel):
    id: int
    purchased_date: datetime
    event: EventResponse
    user: UserResponse

    class Config:
        orm_mode = True
