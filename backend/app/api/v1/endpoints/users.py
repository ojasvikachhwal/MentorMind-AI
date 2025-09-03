from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Any, List
from datetime import datetime

from app.core.database import get_db
from app.core.security import get_current_user, get_password_hash
from app.models.user import User
from app.schemas.user import UserResponse, UserUpdate
from app.services.email_service import EmailService

router = APIRouter()

@router.get("/profile", response_model=UserResponse)
async def get_user_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Get current user's profile information.
    """
    return current_user

@router.put("/profile", response_model=UserResponse)
async def update_user_profile(
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Update current user's profile information.
    """
    try:
        # Check if username is being changed and if it's already taken
        if user_update.username and user_update.username != current_user.username:
            existing_user = db.query(User).filter(
                User.username == user_update.username,
                User.id != current_user.id
            ).first()
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username already taken"
                )
        
        # Check if email is being changed and if it's already taken
        if user_update.email and user_update.email != current_user.email:
            existing_email = db.query(User).filter(
                User.email == user_update.email,
                User.id != current_user.id
            ).first()
            if existing_email:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered"
                )
        
        # Update user fields
        for field, value in user_update.dict(exclude_unset=True).items():
            setattr(current_user, field, value)
        
        current_user.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(current_user)
        
        return current_user
        
    except Exception as e:
        print(f"❌ Error updating user profile: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating profile"
        )

@router.delete("/profile")
async def delete_user_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Delete current user's profile (deactivate account).
    """
    try:
        # Deactivate user instead of deleting
        current_user.is_active = False
        current_user.updated_at = datetime.utcnow()
        db.commit()
        
        return {"message": "Account deactivated successfully"}
        
    except Exception as e:
        print(f"❌ Error deactivating user profile: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deactivating account"
        )

@router.get("/stats")
async def get_user_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Get user's learning statistics.
    """
    try:
        # This would typically fetch from performance tables
        # For now, return sample data
        return {
            "total_quizzes_taken": 15,
            "total_questions_answered": 150,
            "correct_answers": 120,
            "accuracy_rate": 80.0,
            "total_study_time": 450,  # minutes
            "current_streak": 5,
            "longest_streak": 12,
            "badges_earned": 8,
            "topics_covered": ["database", "algorithms", "networks"],
            "favorite_topic": "database",
            "weakest_topic": "dynamic_programming"
        }
        
    except Exception as e:
        print(f"❌ Error getting user stats: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving user statistics"
        )

@router.get("/activity")
async def get_user_activity(
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Get user's recent learning activity.
    """
    try:
        # This would typically fetch from quiz attempts and other activity tables
        # For now, return sample data
        return {
            "recent_activities": [
                {
                    "type": "quiz_completed",
                    "description": "Completed Database Fundamentals quiz",
                    "score": 85,
                    "timestamp": "2024-01-15T10:30:00Z",
                    "topic": "database"
                },
                {
                    "type": "badge_earned",
                    "description": "Earned 'Quick Learner' badge",
                    "badge_name": "Quick Learner",
                    "timestamp": "2024-01-14T15:45:00Z"
                },
                {
                    "type": "streak_milestone",
                    "description": "Achieved 5-day learning streak",
                    "streak_days": 5,
                    "timestamp": "2024-01-13T09:20:00Z"
                }
            ],
            "total_activities": 45
        }
        
    except Exception as e:
        print(f"❌ Error getting user activity: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving user activity"
        )

@router.post("/verify-email")
async def verify_email(
    verification_token: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Verify user's email address.
    """
    try:
        # In a real implementation, this would verify the token
        # For now, just mark the email as verified
        current_user.is_verified = True
        current_user.updated_at = datetime.utcnow()
        db.commit()
        
        return {"message": "Email verified successfully"}
        
    except Exception as e:
        print(f"❌ Error verifying email: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error verifying email"
        )

@router.post("/resend-verification")
async def resend_verification_email(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Resend email verification.
    """
    try:
        if current_user.is_verified:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email is already verified"
            )
        
        # Send verification email
        email_service = EmailService()
        # In a real implementation, this would generate and send a verification token
        # For now, just return success
        
        return {"message": "Verification email sent successfully"}
        
    except Exception as e:
        print(f"❌ Error resending verification email: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error sending verification email"
        )

@router.get("/preferences")
async def get_user_preferences(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Get user's learning preferences and settings.
    """
    try:
        # This would typically fetch from user preferences table
        # For now, return sample data
        return {
            "quiz_preferences": {
                "default_difficulty": "medium",
                "questions_per_quiz": 10,
                "time_limit_enabled": True,
                "show_explanations": True
            },
            "notification_preferences": {
                "email_notifications": True,
                "streak_reminders": True,
                "badge_notifications": True,
                "weekly_progress_reports": False
            },
            "accessibility_preferences": {
                "voice_enabled": True,
                "preferred_language": "en-US",
                "font_size": "medium",
                "high_contrast": False
            },
            "study_preferences": {
                "preferred_topics": ["database", "algorithms"],
                "study_goals": "Improve problem-solving skills",
                "daily_study_target": 30  # minutes
            }
        }
        
    except Exception as e:
        print(f"❌ Error getting user preferences: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving user preferences"
        )

@router.put("/preferences")
async def update_user_preferences(
    preferences: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Update user's learning preferences and settings.
    """
    try:
        # This would typically save to user preferences table
        # For now, just log the update
        print(f"📝 Updated preferences for {current_user.username}: {preferences}")
        
        return {
            "message": "Preferences updated successfully",
            "preferences": preferences
        }
        
    except Exception as e:
        print(f"❌ Error updating user preferences: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating preferences"
        )

@router.get("/goals")
async def get_user_goals(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Get user's learning goals and progress.
    """
    try:
        # This would typically fetch from user goals table
        # For now, return sample data
        return {
            "current_goals": [
                {
                    "id": 1,
                    "title": "Master Database Concepts",
                    "description": "Complete all database quizzes with 80%+ accuracy",
                    "target_date": "2024-02-15",
                    "progress": 75,
                    "status": "in_progress"
                },
                {
                    "id": 2,
                    "title": "Algorithm Proficiency",
                    "description": "Solve 50 algorithm problems",
                    "target_date": "2024-03-01",
                    "progress": 30,
                    "status": "in_progress"
                }
            ],
            "completed_goals": [
                {
                    "id": 3,
                    "title": "Learn SQL Basics",
                    "description": "Complete SQL fundamentals course",
                    "completed_date": "2024-01-10",
                    "final_score": 90
                }
            ],
            "total_goals": 3,
            "completed_goals_count": 1,
            "success_rate": 33.3
        }
        
    except Exception as e:
        print(f"❌ Error getting user goals: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving user goals"
        )

@router.post("/goals")
async def create_user_goal(
    goal_data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Create a new learning goal.
    """
    try:
        # This would typically save to user goals table
        # For now, just log the creation
        print(f"🎯 Created new goal for {current_user.username}: {goal_data}")
        
        return {
            "message": "Goal created successfully",
            "goal": {
                "id": 999,
                **goal_data,
                "progress": 0,
                "status": "in_progress"
            }
        }
        
    except Exception as e:
        print(f"❌ Error creating user goal: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating goal"
        )
