from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .api.v1.api import api_router

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title="FastAPI with JWT Authentication and RBAC",
    description="A FastAPI application with PostgreSQL, JWT authentication, and Role-based Access Control (RBAC)",
    version="2.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI with JWT Authentication and RBAC!"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "MentorMind Backend", "version": "2.0.0"}
