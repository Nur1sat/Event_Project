from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta

from app.database import get_db
from app.models.user import User, UserRole
from app.models.event import Event
from app.models.registration import Registration
from app.services.auth import get_current_user, get_current_admin

router = APIRouter(prefix="/api/stats", tags=["Statistics"])


@router.get("/dashboard")
def get_dashboard_stats(
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get dashboard statistics (Admin only)"""
    total_users = db.query(User).count()
    total_students = db.query(User).filter(User.role == UserRole.STUDENT).count()
    total_admins = db.query(User).filter(User.role == UserRole.ADMIN).count()
    total_events = db.query(Event).count()
    total_registrations = db.query(Registration).count()
    
    # Events by status
    now = datetime.utcnow()
    upcoming_events = db.query(Event).filter(Event.date > now).count()
    finished_events = db.query(Event).filter(Event.date <= now).count()
    
    # Recent registrations (last 7 days)
    week_ago = now - timedelta(days=7)
    recent_registrations = db.query(Registration).filter(
        Registration.registered_at >= week_ago
    ).count()
    
    # Most popular events (top 5)
    popular_events = db.query(
        Event.id, Event.title,
        func.count(Registration.id).label('registration_count')
    ).outerjoin(Registration).group_by(Event.id).order_by(
        func.count(Registration.id).desc()
    ).limit(5).all()
    
    # Registrations per day (last 7 days)
    daily_registrations = []
    for i in range(7):
        day = now - timedelta(days=i)
        day_start = day.replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = day_start + timedelta(days=1)
        count = db.query(Registration).filter(
            Registration.registered_at >= day_start,
            Registration.registered_at < day_end
        ).count()
        daily_registrations.append({
            "date": day_start.strftime("%Y-%m-%d"),
            "count": count
        })
    
    return {
        "users": {
            "total": total_users,
            "students": total_students,
            "admins": total_admins
        },
        "events": {
            "total": total_events,
            "upcoming": upcoming_events,
            "finished": finished_events
        },
        "registrations": {
            "total": total_registrations,
            "last_7_days": recent_registrations,
            "daily": daily_registrations
        },
        "popular_events": [
            {"id": e.id, "title": e.title, "registrations": e.registration_count}
            for e in popular_events
        ]
    }


@router.get("/my-stats")
def get_user_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user's statistics"""
    total_registrations = db.query(Registration).filter(
        Registration.user_id == current_user.id
    ).count()
    
    now = datetime.utcnow()
    upcoming_events = db.query(Registration).join(Event).filter(
        Registration.user_id == current_user.id,
        Event.date > now
    ).count()
    
    attended_events = db.query(Registration).join(Event).filter(
        Registration.user_id == current_user.id,
        Event.date <= now
    ).count()
    
    # Recent activity
    recent = db.query(Registration).filter(
        Registration.user_id == current_user.id
    ).order_by(Registration.registered_at.desc()).limit(5).all()
    
    return {
        "total_registrations": total_registrations,
        "upcoming_events": upcoming_events,
        "attended_events": attended_events,
        "recent_registrations": [
            {
                "event_id": r.event_id,
                "event_title": r.event.title,
                "registered_at": r.registered_at
            }
            for r in recent
        ]
    }


@router.get("/events/{event_id}/stats")
def get_event_stats(
    event_id: int,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get statistics for a specific event (Admin only)"""
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        return {"error": "Event not found"}
    
    registrations = db.query(Registration).filter(
        Registration.event_id == event_id
    ).all()
    
    # Group distribution
    groups = {}
    for reg in registrations:
        group = reg.user.group or "No Group"
        groups[group] = groups.get(group, 0) + 1
    
    # Registration timeline
    timeline = {}
    for reg in registrations:
        date = reg.registered_at.strftime("%Y-%m-%d")
        timeline[date] = timeline.get(date, 0) + 1
    
    return {
        "event_id": event_id,
        "title": event.title,
        "total_registrations": len(registrations),
        "capacity": event.max_participants,
        "fill_rate": round(len(registrations) / event.max_participants * 100, 1),
        "group_distribution": groups,
        "registration_timeline": timeline
    }


@router.get("/leaderboard")
def get_leaderboard(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get most active students leaderboard"""
    leaderboard = db.query(
        User.id, User.full_name, User.group,
        func.count(Registration.id).label('event_count')
    ).join(Registration).filter(
        User.role == UserRole.STUDENT
    ).group_by(User.id).order_by(
        func.count(Registration.id).desc()
    ).limit(10).all()
    
    return {
        "leaderboard": [
            {
                "rank": i + 1,
                "user_id": u.id,
                "name": u.full_name,
                "group": u.group,
                "events_attended": u.event_count
            }
            for i, u in enumerate(leaderboard)
        ]
    }

