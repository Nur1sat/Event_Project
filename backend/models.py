from sqlalchemy import Column, Integer, String, Text, Date, Time, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    group = Column(String, nullable=True)
    role = Column(String, default="student")  # "student" or "admin"
    photo_url = Column(Text, nullable=True)  # URL to user's profile photo (or base64 string)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    event_registrations = relationship("EventRegistration", back_populates="user", cascade="all, delete-orphan")
    event_requests = relationship("EventRequest", back_populates="user", cascade="all, delete-orphan", foreign_keys="EventRequest.user_id")

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    location = Column(String, nullable=False)
    max_participants = Column(Integer, nullable=False)
    image_url = Column(Text, nullable=True)  # URL to event image (or base64 string)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    registrations = relationship("EventRegistration", back_populates="event", cascade="all, delete-orphan")

class EventRegistration(Base):
    __tablename__ = "event_registrations"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    registered_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    event = relationship("Event", back_populates="registrations")
    user = relationship("User", back_populates="event_registrations")

class EventRequest(Base):
    __tablename__ = "event_requests"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    location = Column(String, nullable=False)
    max_participants = Column(Integer, nullable=False)
    status = Column(String, default="pending")  # "pending", "approved", "rejected"
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    reviewed_at = Column(DateTime(timezone=True), nullable=True)
    reviewed_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="event_requests", foreign_keys=[user_id])
