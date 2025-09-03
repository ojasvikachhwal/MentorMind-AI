from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import uvicorn
from sqlalchemy import create_engine
import os
from fastapi import APIRouter
from app.core.config import settings
from app.core.database import engine, Base
from app.api.v1.api import api_router
from app.core.security import get_current_user
from app.models import user, quiz, performance, gamification

# Create database tables
Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🚀 Starting MentorMind AI Learning Platform...")
    yield
    # Shutdown
    print("🛑 Shutting down MentorMind...")

app = FastAPI(
    title="MentorMind AI Learning Platform",
    description="An AI-powered learning platform with adaptive quizzes, AI tutoring, and gamification",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api/v1")

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "MentorMind Backend",
        "version": "1.0.0"
    }



engine = create_engine("postgresql://postgres:170404@localhost:5432/student_learning")
conn = engine.connect()
print("✅ Connected to PostgreSQL!")
conn.close()

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Welcome to MentorMind AI Learning Platform",
        "docs": "/docs",
        "health": "/health"
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

router=APIRouter(
    prefix="/api/v1",
    tags=["v1"],
)
@router.post("/register")
async def register_user():
    return {"msg": "user registered"}