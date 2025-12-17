from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class RegistrationCreate(BaseModel):
    event_id: int


class EventInfo(BaseModel):
    id: int
    title: str
    date: datetime
    location: str

    class Config:
        from_attributes = True


class RegistrationResponse(BaseModel):
    id: int
    event_id: int
    user_id: int
    registered_at: datetime
    event: Optional[EventInfo] = None

    class Config:
        from_attributes = True

