from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.registration import Registration
from app.models.event import Event, EventStatus


class RegistrationService:
    def __init__(self, db: Session):
        self.db = db

    def register_for_event(self, user_id: int, event_id: int) -> Registration:
        # Check event exists
        event = self.db.query(Event).filter(Event.id == event_id).first()
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")
        
        # Check if event is finished
        if event.status == EventStatus.FINISHED:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot register for finished event"
            )
        
        # Check if event is full
        if event.status == EventStatus.FULL:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No available spots"
            )
        
        # Check if already registered
        existing = self.db.query(Registration).filter(
            Registration.user_id == user_id,
            Registration.event_id == event_id
        ).first()
        
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You are already registered"
            )
        
        registration = Registration(user_id=user_id, event_id=event_id)
        self.db.add(registration)
        self.db.commit()
        self.db.refresh(registration)
        return registration

    def cancel_registration(self, user_id: int, event_id: int) -> None:
        registration = self.db.query(Registration).filter(
            Registration.user_id == user_id,
            Registration.event_id == event_id
        ).first()
        
        if not registration:
            raise HTTPException(
                status_code=404,
                detail="Registration not found"
            )
        
        self.db.delete(registration)
        self.db.commit()

    def get_user_registrations(self, user_id: int):
        registrations = self.db.query(Registration).filter(
            Registration.user_id == user_id
        ).all()
        return registrations

