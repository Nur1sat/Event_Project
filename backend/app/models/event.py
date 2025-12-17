from sqlalchemy import Column, Integer, String, Text, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.database import Base


class EventStatus(str, enum.Enum):
    UPCOMING = "upcoming"
    FULL = "full"
    FINISHED = "finished"


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    date = Column(DateTime, nullable=False)
    location = Column(String(255), nullable=False)
    max_participants = Column(Integer, nullable=False, default=20)
    created_by = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    registrations = relationship("Registration", back_populates="event", cascade="all, delete-orphan")

    @property
    def current_participants(self):
        return len(self.registrations) if self.registrations else 0

    @property
    def status(self):
        if self.date < datetime.utcnow():
            return EventStatus.FINISHED
        if self.current_participants >= self.max_participants:
            return EventStatus.FULL
        return EventStatus.UPCOMING

    @property
    def available_spots(self):
        return max(0, self.max_participants - self.current_participants)

