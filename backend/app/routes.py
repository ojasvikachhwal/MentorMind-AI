from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from . import models, schemas, auth, rbac
from .models import UserRole
from .database import get_db

router = APIRouter()

@router.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Register a new user."""
    # Check if username already exists
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Check if email already exists
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user with role (defaults to student if not provided)
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        password=hashed_password,
        role=user.role or UserRole.STUDENT
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Login and get access token."""
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me", response_model=schemas.UserResponse)
def read_users_me(current_user: models.User = Depends(auth.get_current_user)):
    """Get current user information."""
    return current_user

# Role-based access control endpoints
@router.get("/admin/dashboard")
def admin_dashboard(current_user: models.User = Depends(rbac.admin_required)):
    """Admin dashboard - accessible only to admin users."""
    return {
        "message": "Welcome to Admin Dashboard",
        "user": current_user.username,
        "role": current_user.role.value,
        "features": ["User Management", "System Settings", "Analytics", "All Access"]
    }

@router.get("/teacher/dashboard")
def teacher_dashboard(current_user: models.User = Depends(rbac.teacher_or_admin_required)):
    """Teacher dashboard - accessible to teacher and admin users."""
    return {
        "message": "Welcome to Teacher Dashboard",
        "user": current_user.username,
        "role": current_user.role.value,
        "features": ["Student Management", "Course Creation", "Grading", "Analytics"]
    }

@router.get("/student/dashboard")
def student_dashboard(current_user: models.User = Depends(rbac.any_authenticated_user)):
    """Student dashboard - accessible to all authenticated users."""
    return {
        "message": "Welcome to Student Dashboard",
        "user": current_user.username,
        "role": current_user.role.value,
        "features": ["Course Enrollment", "Assignments", "Grades", "Progress Tracking"]
    }

# Example of using the flexible role_required function
@router.get("/admin/analytics")
def admin_analytics(current_user: models.User = Depends(rbac.role_required([UserRole.ADMIN]))):
    """Admin analytics - using the flexible role_required function."""
    return {
        "message": "Admin Analytics Dashboard",
        "user": current_user.username,
        "role": current_user.role.value,
        "analytics": {
            "total_users": 150,
            "active_courses": 25,
            "system_health": "Excellent"
        }
    }

@router.get("/")
def read_root():
    """Root endpoint."""
    return {"message": "Welcome to FastAPI with JWT Authentication and RBAC!"}
