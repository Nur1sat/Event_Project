from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.models.event import EventStatus


class EventCreate(BaseModel):
    title: str
    description: Optional[str] = None
    date: datetime
    location: str
    max_participants: int = 20


class EventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    date: Optional[datetime] = None
    location: Optional[str] = None
    max_participants: Optional[int] = None


class ParticipantInfo(BaseModel):
    id: int
    full_name: str
    email: str
    group: Optional[str]
    registered_at: datetime

    class Config:
        from_attributes = True


class EventResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    date: datetime
    location: str
    max_participants: int
    current_participants: int
    available_spots: int
    status: EventStatus
    created_by: int
    created_at: datetime
    is_registered: bool = False
    participants: Optional[List[ParticipantInfo]] = None

    class Config:
        from_attributes = True


class EventListResponse(BaseModel):
    events: List[EventResponse]
    total: int
    page: int
    per_page: int

