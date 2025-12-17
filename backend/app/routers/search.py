from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from datetime import datetime

from app.database import get_db
from app.models.user import User
from app.models.event import Event
from app.services.auth import get_current_user

router = APIRouter(prefix="/api/search", tags=["Search"])


@router.get("/events")
def search_events(
    q: str = Query(..., min_length=1, description="Search query"),
    location: str = Query(None, description="Filter by location"),
    date_from: str = Query(None, description="Filter from date (YYYY-MM-DD)"),
    date_to: str = Query(None, description="Filter to date (YYYY-MM-DD)"),
    has_spots: bool = Query(None, description="Only show events with available spots"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Advanced event search with multiple filters"""
    query = db.query(Event)
    
    # Text search in title and description
    query = query.filter(
        or_(
            Event.title.ilike(f"%{q}%"),
            Event.description.ilike(f"%{q}%")
        )
    )
    
    # Location filter
    if location:
        query = query.filter(Event.location.ilike(f"%{location}%"))
    
    # Date range filter
    if date_from:
        try:
            from_date = datetime.strptime(date_from, "%Y-%m-%d")
            query = query.filter(Event.date >= from_date)
        except ValueError:
            pass
    
    if date_to:
        try:
            to_date = datetime.strptime(date_to, "%Y-%m-%d")
            query = query.filter(Event.date <= to_date)
        except ValueError:
            pass
    
    events = query.order_by(Event.date).all()
    
    # Filter by available spots (done in Python since it's a computed property)
    if has_spots:
        events = [e for e in events if e.available_spots > 0]
    
    return {
        "query": q,
        "results_count": len(events),
        "events": [
            {
                "id": e.id,
                "title": e.title,
                "description": e.description,
                "date": e.date,
                "location": e.location,
                "available_spots": e.available_spots,
                "max_participants": e.max_participants,
                "status": e.status.value
            }
            for e in events
        ]
    }


@router.get("/suggestions")
def get_suggestions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get event suggestions based on user's group and history"""
    now = datetime.utcnow()
    
    # Get upcoming events user hasn't registered for
    registered_event_ids = [
        r.event_id for r in current_user.registrations
    ]
    
    suggestions = db.query(Event).filter(
        Event.date > now,
        ~Event.id.in_(registered_event_ids) if registered_event_ids else True
    ).order_by(Event.date).limit(5).all()
    
    return {
        "suggestions": [
            {
                "id": e.id,
                "title": e.title,
                "date": e.date,
                "location": e.location,
                "available_spots": e.available_spots,
                "reason": "Upcoming event you haven't joined yet"
            }
            for e in suggestions
        ]
    }

