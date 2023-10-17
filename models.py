from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    events = relationship("Event")
    tickets = relationship("Ticket", back_populates="user")


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    date_time = Column(DateTime)
    location = Column(String)
    total_tickets = Column(Integer)
    available_tickets = Column(Integer)
    organizer = Column(Integer, ForeignKey("users.id"))
    price = Column(Float)
    # organizer = relationship("User", back_populates="events")


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    event = relationship("Event")
    user = relationship("User", back_populates="tickets")
    purchased_date = Column(DateTime, default=datetime.utcnow)
