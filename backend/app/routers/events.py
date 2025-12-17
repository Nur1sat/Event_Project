from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models.user import User
from app.schemas.event import EventCreate, EventUpdate, EventResponse, EventListResponse
from app.services.auth import get_current_user, get_current_admin
from app.services.event_service import EventService

router = APIRouter(prefix="/api/events", tags=["Events"])


def event_to_response(event, user_id: int = None, include_participants: bool = False, service: EventService = None):
    response = {
        "id": event.id,
        "title": event.title,
        "description": event.description,
        "date": event.date,
        "location": event.location,
        "max_participants": event.max_participants,
        "current_participants": event.current_participants,
        "available_spots": event.available_spots,
        "status": event.status,
        "created_by": event.created_by,
        "created_at": event.created_at,
        "is_registered": service.is_user_registered(event.id, user_id) if user_id and service else False,
        "participants": service.get_event_participants(event.id) if include_participants and service else None
    }
    return EventResponse(**response)


@router.get("/", response_model=EventListResponse)
def get_events(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    status: Optional[str] = None,
    search: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all events with pagination and filtering"""
    service = EventService(db)
    skip = (page - 1) * per_page
    events, total = service.get_events(skip, per_page, status, search)
    
    return EventListResponse(
        events=[event_to_response(e, current_user.id, False, service) for e in events],
        total=total,
        page=page,
        per_page=per_page
    )


@router.get("/{event_id}", response_model=EventResponse)
def get_event(
    event_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get event details"""
    service = EventService(db)
    event = service.get_event(event_id)
    return event_to_response(event, current_user.id, False, service)


@router.post("/", response_model=EventResponse, status_code=status.HTTP_201_CREATED)
def create_event(
    event_data: EventCreate,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Create a new event (Admin only)"""
    service = EventService(db)
    event = service.create_event(event_data, current_user.id)
    return event_to_response(event, current_user.id, False, service)


@router.put("/{event_id}", response_model=EventResponse)
def update_event(
    event_id: int,
    event_data: EventUpdate,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Update an event (Admin only)"""
    service = EventService(db)
    event = service.update_event(event_id, event_data)
    return event_to_response(event, current_user.id, False, service)


@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_event(
    event_id: int,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Delete an event (Admin only)"""
    service = EventService(db)
    service.delete_event(event_id)


@router.get("/{event_id}/participants")
def get_event_participants(
    event_id: int,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get list of participants for an event (Admin only)"""
    service = EventService(db)
    return service.get_event_participants(event_id)

