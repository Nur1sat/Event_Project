from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.user import User
from app.schemas.registration import RegistrationResponse
from app.services.auth import get_current_user
from app.services.registration_service import RegistrationService

router = APIRouter(prefix="/api/registrations", tags=["Registrations"])


@router.post("/{event_id}", response_model=RegistrationResponse, status_code=status.HTTP_201_CREATED)
def register_for_event(
    event_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Register current user for an event"""
    service = RegistrationService(db)
    registration = service.register_for_event(current_user.id, event_id)
    return RegistrationResponse(
        id=registration.id,
        event_id=registration.event_id,
        user_id=registration.user_id,
        registered_at=registration.registered_at
    )


@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
def cancel_registration(
    event_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Cancel registration for an event"""
    service = RegistrationService(db)
    service.cancel_registration(current_user.id, event_id)


@router.get("/my", response_model=List[RegistrationResponse])
def get_my_registrations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all registrations for current user"""
    service = RegistrationService(db)
    registrations = service.get_user_registrations(current_user.id)
    return [
        RegistrationResponse(
            id=r.id,
            event_id=r.event_id,
            user_id=r.user_id,
            registered_at=r.registered_at,
            event={
                "id": r.event.id,
                "title": r.event.title,
                "date": r.event.date,
                "location": r.event.location
            }
        )
        for r in registrations
    ]

