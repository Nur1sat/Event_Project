from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime
from typing import Optional
from app.models.event import Event
from app.models.registration import Registration
from app.schemas.event import EventCreate, EventUpdate


class EventService:
    def __init__(self, db: Session):
        self.db = db

    def create_event(self, event_data: EventCreate, created_by: int) -> Event:
        event = Event(
            title=event_data.title,
            description=event_data.description,
            date=event_data.date,
            location=event_data.location,
            max_participants=event_data.max_participants,
            created_by=created_by
        )
        self.db.add(event)
        self.db.commit()
        self.db.refresh(event)
        return event

    def get_event(self, event_id: int) -> Event:
        event = self.db.query(Event).filter(Event.id == event_id).first()
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")
        return event

    def get_events(
        self,
        skip: int = 0,
        limit: int = 20,
        status_filter: Optional[str] = None,
        search: Optional[str] = None
    ):
        query = self.db.query(Event)
        
        if search:
            query = query.filter(Event.title.ilike(f"%{search}%"))
        
        total = query.count()
        events = query.order_by(Event.date.desc()).offset(skip).limit(limit).all()
        
        # Filter by status after fetching (since status is computed)
        if status_filter:
            events = [e for e in events if e.status.value == status_filter]
        
        return events, total

    def update_event(self, event_id: int, event_data: EventUpdate) -> Event:
        event = self.get_event(event_id)
        update_data = event_data.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(event, field, value)
        
        self.db.commit()
        self.db.refresh(event)
        return event

    def delete_event(self, event_id: int) -> None:
        event = self.get_event(event_id)
        self.db.delete(event)
        self.db.commit()

    def is_user_registered(self, event_id: int, user_id: int) -> bool:
        return self.db.query(Registration).filter(
            Registration.event_id == event_id,
            Registration.user_id == user_id
        ).first() is not None

    def get_event_participants(self, event_id: int):
        event = self.get_event(event_id)
        return [
            {
                "id": reg.user.id,
                "full_name": reg.user.full_name,
                "email": reg.user.email,
                "group": reg.user.group,
                "registered_at": reg.registered_at
            }
            for reg in event.registrations
        ]

