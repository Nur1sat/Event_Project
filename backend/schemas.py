from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date, time, datetime

# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    group: Optional[str] = None

class UserCreate(UserBase):
    password: str
    role: Optional[str] = "student"
    secret_code: Optional[str] = None  # For admin registration

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    group: Optional[str] = None
    photo_url: Optional[str] = None

class UserResponse(UserBase):
    id: int
    role: str
    photo_url: Optional[str] = None

    class Config:
        from_attributes = True

# Event Schemas
class EventBase(BaseModel):
    title: str
    description: str
    date: date
    start_time: time
    location: str
    max_participants: int
    image_url: Optional[str] = None

class EventCreate(EventBase):
    pass

class EventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    date: Optional[str] = None  # Accept string, will be converted to date
    start_time: Optional[str] = None  # Accept string for time
    location: Optional[str] = None
    max_participants: Optional[int] = None
    image_url: Optional[str] = None

class EventResponse(EventBase):
    id: int
    created_by: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Event Registration Schemas
class EventRegistrationCreate(BaseModel):
    event_id: int

class EventRegistrationResponse(BaseModel):
    id: int
    event_id: int
    user_id: int
    registered_at: datetime
    
    class Config:
        from_attributes = True

# Event Request Schemas
class EventRequestCreate(BaseModel):
    title: str
    description: str
    date: date
    start_time: time
    location: str
    max_participants: int

class EventRequestResponse(BaseModel):
    id: int
    user_id: int
    title: str
    description: str
    date: date
    start_time: time
    location: str
    max_participants: int
    status: str
    created_at: datetime
    reviewed_at: Optional[datetime] = None
    reviewed_by: Optional[int] = None
    user: Optional[UserResponse] = None

    class Config:
        from_attributes = True

# Auth Schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[str] = None

# Event Description Generation Schema
class DescriptionGenerateRequest(BaseModel):
    keywords: str
    title: Optional[str] = None
    type: Optional[str] = "workshop"
    audience: Optional[str] = "students"
    date: Optional[str] = None
    location: Optional[str] = None

class DescriptionGenerateResponse(BaseModel):
    description: str

