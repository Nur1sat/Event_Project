from fastapi import APIRouter, Depends
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
import csv
import io

from app.database import get_db
from app.models.user import User, UserRole
from app.models.event import Event
from app.models.registration import Registration
from app.services.auth import get_current_admin

router = APIRouter(prefix="/api/export", tags=["Export"])


@router.get("/events/csv", response_class=PlainTextResponse)
def export_events_csv(
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Export all events to CSV (Admin only)"""
    events = db.query(Event).all()
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    writer.writerow([
        "ID", "Title", "Description", "Date", "Location",
        "Max Participants", "Current Participants", "Status", "Created At"
    ])
    
    for e in events:
        writer.writerow([
            e.id, e.title, e.description or "", e.date.isoformat(),
            e.location, e.max_participants, e.current_participants,
            e.status.value, e.created_at.isoformat()
        ])
    
    return PlainTextResponse(
        content=output.getvalue(),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=events.csv"}
    )


@router.get("/events/{event_id}/participants/csv", response_class=PlainTextResponse)
def export_participants_csv(
    event_id: int,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Export event participants to CSV (Admin only)"""
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        return PlainTextResponse("Event not found", status_code=404)
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    writer.writerow(["ID", "Full Name", "Email", "Group", "Registered At"])
    
    for reg in event.registrations:
        writer.writerow([
            reg.user.id, reg.user.full_name, reg.user.email,
            reg.user.group or "", reg.registered_at.isoformat()
        ])
    
    return PlainTextResponse(
        content=output.getvalue(),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=event_{event_id}_participants.csv"}
    )


@router.get("/users/csv", response_class=PlainTextResponse)
def export_users_csv(
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Export all users to CSV (Admin only)"""
    users = db.query(User).all()
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    writer.writerow(["ID", "Full Name", "Email", "Group", "Role", "Created At"])
    
    for u in users:
        writer.writerow([
            u.id, u.full_name, u.email, u.group or "",
            u.role.value, u.created_at.isoformat()
        ])
    
    return PlainTextResponse(
        content=output.getvalue(),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=users.csv"}
    )


@router.get("/report")
def get_full_report(
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get comprehensive system report (Admin only)"""
    now = datetime.utcnow()
    month_ago = now - timedelta(days=30)
    
    # User stats
    total_users = db.query(User).count()
    new_users_month = db.query(User).filter(User.created_at >= month_ago).count()
    
    # Event stats
    total_events = db.query(Event).count()
    upcoming_events = db.query(Event).filter(Event.date > now).count()
    
    # Registration stats
    total_registrations = db.query(Registration).count()
    registrations_month = db.query(Registration).filter(
        Registration.registered_at >= month_ago
    ).count()
    
    # Average registrations per event
    if total_events > 0:
        avg_registrations = total_registrations / total_events
    else:
        avg_registrations = 0
    
    # Most active group
    group_stats = db.query(
        User.group, func.count(Registration.id).label('count')
    ).join(Registration).filter(User.group.isnot(None)).group_by(
        User.group
    ).order_by(func.count(Registration.id).desc()).first()
    
    return {
        "report_date": now.isoformat(),
        "period": "Last 30 days",
        "users": {
            "total": total_users,
            "new_this_month": new_users_month,
            "growth_rate": round(new_users_month / max(total_users - new_users_month, 1) * 100, 1)
        },
        "events": {
            "total": total_events,
            "upcoming": upcoming_events,
            "average_registrations": round(avg_registrations, 1)
        },
        "registrations": {
            "total": total_registrations,
            "this_month": registrations_month
        },
        "insights": {
            "most_active_group": group_stats[0] if group_stats else None,
            "most_active_group_registrations": group_stats[1] if group_stats else 0
        }
    }
