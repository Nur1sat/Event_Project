from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.database import engine, Base
from app.middleware import LoggingMiddleware
from app.routers import auth, users, events, registrations
from app.routers import stats, search, export
from app.models import User, Event, Registration


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="JIHC Clubs Activity API",
    description="""
## JIHC Clubs Activity Management System

A comprehensive API for managing college club activities and student registrations.

### Features:
- 🔐 JWT Authentication with Role-based Access Control
- 📅 Event Management (CRUD)
- 👥 User Registration & Management
- 📊 Statistics & Analytics
- 🔍 Advanced Search
- 📤 CSV Export
- 🏆 Leaderboard

### Roles:
- **Student**: Can view events, register, view personal stats
- **Admin**: Full access including user management, reports, exports
    """,
    version="1.0.0",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allows all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Logging middleware
app.add_middleware(LoggingMiddleware)

# Include routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(events.router)
app.include_router(registrations.router)
app.include_router(stats.router)
app.include_router(search.router)
app.include_router(export.router)


@app.get("/", tags=["Root"])
def root():
    return {
        "message": "JIHC Clubs Activity API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "auth": "/api/auth",
            "users": "/api/users",
            "events": "/api/events",
            "registrations": "/api/registrations",
            "stats": "/api/stats",
            "search": "/api/search",
            "export": "/api/export"
        }
    }


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy", "service": "jihc-clubs-api"}
