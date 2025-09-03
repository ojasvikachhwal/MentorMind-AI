"""
Progress Tracking API Endpoints
Handles student progress tracking, analytics, and AI-powered feedback.
"""

import logging
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.progress import ActivityType, FeedbackType
from app.services.progress_service import ProgressService
from app.schemas.progress import (
    ProgressActivityCreate, ProgressActivityResponse,
    CodingPracticeCreate, CodingPracticeResponse,
    WeeklyAnalyticsResponse, WeeklyReportResponse,
    ProgressDashboardResponse, AIFeedbackResponse
)

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/track-activity", response_model=ProgressActivityResponse)
async def track_activity(
    activity_data: ProgressActivityCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Track a student activity."""
    try:
        progress_service = ProgressService(db)
        
        progress = progress_service.track_activity(
            user_id=current_user.id,
            activity_type=ActivityType(activity_data.activity_type),
            activity_name=activity_data.activity_name,
            subject=activity_data.subject,
            score=activity_data.score,
            time_spent=activity_data.time_spent,
            difficulty_level=activity_data.difficulty_level,
            activity_id=activity_data.activity_id,
            metadata=activity_data.metadata
        )
        
        return ProgressActivityResponse(
            id=progress.id,
            user_id=progress.user_id,
            activity_type=progress.activity_type,
            activity_name=progress.activity_name,
            subject=progress.subject,
            score=progress.score,
            time_spent=progress.time_spent,
            difficulty_level=progress.difficulty_level,
            created_at=progress.created_at
        )
        
    except Exception as e:
        logger.error(f"Error tracking activity: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to track activity"
        )

@router.post("/track-coding-practice", response_model=CodingPracticeResponse)
async def track_coding_practice(
    coding_data: CodingPracticeCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Track coding practice session with AI analysis."""
    try:
        progress_service = ProgressService(db)
        
        coding_practice = progress_service.track_coding_practice(
            user_id=current_user.id,
            problem_title=coding_data.problem_title,
            problem_difficulty=coding_data.problem_difficulty,
            language=coding_data.language,
            solution_code=coding_data.solution_code,
            test_cases_passed=coding_data.test_cases_passed,
            total_test_cases=coding_data.total_test_cases,
            execution_time=coding_data.execution_time,
            memory_usage=coding_data.memory_usage,
            time_spent=coding_data.time_spent
        )
        
        return CodingPracticeResponse(
            id=coding_practice.id,
            user_id=coding_practice.user_id,
            problem_title=coding_practice.problem_title,
            problem_difficulty=coding_practice.problem_difficulty,
            language=coding_practice.language,
            test_cases_passed=coding_practice.test_cases_passed,
            total_test_cases=coding_practice.total_test_cases,
            execution_time=coding_practice.execution_time,
            memory_usage=coding_practice.memory_usage,
            ai_feedback=coding_practice.ai_feedback,
            optimization_suggestions=coding_practice.optimization_suggestions,
            score=coding_practice.score,
            time_spent=coding_practice.time_spent,
            created_at=coding_practice.created_at
        )
        
    except Exception as e:
        logger.error(f"Error tracking coding practice: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to track coding practice"
        )

@router.get("/weekly-analytics", response_model=WeeklyAnalyticsResponse)
async def get_weekly_analytics(
    week_start: Optional[datetime] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get weekly analytics for the current user."""
    try:
        progress_service = ProgressService(db)
        
        analytics = progress_service.get_weekly_analytics(
            user_id=current_user.id,
            week_start=week_start
        )
        
        return WeeklyAnalyticsResponse(
            id=analytics.id,
            user_id=analytics.user_id,
            week_start=analytics.week_start,
            week_end=analytics.week_end,
            total_study_time=analytics.total_study_time,
            courses_completed=analytics.courses_completed,
            quizzes_taken=analytics.quizzes_taken,
            coding_sessions=analytics.coding_sessions,
            average_quiz_score=analytics.average_quiz_score,
            average_coding_score=analytics.average_coding_score,
            subject_performance=analytics.subject_performance,
            strengths=analytics.strengths,
            weaknesses=analytics.weaknesses,
            recommendations=analytics.recommendations,
            created_at=analytics.created_at
        )
        
    except Exception as e:
        logger.error(f"Error getting weekly analytics: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get weekly analytics"
        )

@router.get("/weekly-report", response_model=WeeklyReportResponse)
async def get_weekly_report(
    week_start: Optional[datetime] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate and get weekly report for the current user."""
    try:
        progress_service = ProgressService(db)
        
        report = progress_service.generate_weekly_report(
            user_id=current_user.id,
            week_start=week_start
        )
        
        return WeeklyReportResponse(
            id=report.id,
            user_id=report.user_id,
            week_start=report.week_start,
            week_end=report.week_end,
            summary=report.summary,
            achievements=report.achievements,
            areas_for_improvement=report.areas_for_improvement,
            next_week_goals=report.next_week_goals,
            recommended_courses=report.recommended_courses,
            recommended_coding_problems=report.recommended_coding_problems,
            email_sent=report.email_sent,
            created_at=report.created_at
        )
        
    except Exception as e:
        logger.error(f"Error generating weekly report: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate weekly report"
        )

@router.get("/dashboard", response_model=ProgressDashboardResponse)
async def get_progress_dashboard(
    days: int = 30,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get comprehensive progress data for dashboard."""
    try:
        progress_service = ProgressService(db)
        
        dashboard_data = progress_service.get_progress_dashboard_data(
            user_id=current_user.id,
            days=days
        )
        
        return ProgressDashboardResponse(**dashboard_data)
        
    except Exception as e:
        logger.error(f"Error getting dashboard data: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get dashboard data"
        )

@router.get("/feedback", response_model=List[AIFeedbackResponse])
async def get_ai_feedback(
    limit: int = 10,
    feedback_type: Optional[FeedbackType] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get AI-generated feedback for the current user."""
    try:
        from app.models.progress import AIFeedback
        from sqlalchemy import desc
        
        query = db.query(AIFeedback).filter(AIFeedback.user_id == current_user.id)
        
        if feedback_type:
            query = query.filter(AIFeedback.feedback_type == feedback_type)
        
        feedback_list = query.order_by(desc(AIFeedback.created_at)).limit(limit).all()
        
        return [
            AIFeedbackResponse(
                id=feedback.id,
                user_id=feedback.user_id,
                feedback_type=feedback.feedback_type,
                subject=feedback.subject,
                title=feedback.title,
                message=feedback.message,
                confidence_score=feedback.confidence_score,
                is_read=feedback.is_read,
                is_archived=feedback.is_archived,
                created_at=feedback.created_at
            )
            for feedback in feedback_list
        ]
        
    except Exception as e:
        logger.error(f"Error getting AI feedback: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get AI feedback"
        )

@router.put("/feedback/{feedback_id}/read")
async def mark_feedback_as_read(
    feedback_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Mark AI feedback as read."""
    try:
        from app.models.progress import AIFeedback
        
        feedback = db.query(AIFeedback).filter(
            AIFeedback.id == feedback_id,
            AIFeedback.user_id == current_user.id
        ).first()
        
        if not feedback:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Feedback not found"
            )
        
        feedback.is_read = True
        db.commit()
        
        return {"message": "Feedback marked as read"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error marking feedback as read: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to mark feedback as read"
        )

@router.get("/activities", response_model=List[ProgressActivityResponse])
async def get_recent_activities(
    limit: int = 20,
    activity_type: Optional[ActivityType] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get recent activities for the current user."""
    try:
        from app.models.progress import StudentProgress
        from sqlalchemy import desc
        
        query = db.query(StudentProgress).filter(StudentProgress.user_id == current_user.id)
        
        if activity_type:
            query = query.filter(StudentProgress.activity_type == activity_type)
        
        activities = query.order_by(desc(StudentProgress.created_at)).limit(limit).all()
        
        return [
            ProgressActivityResponse(
                id=activity.id,
                user_id=activity.user_id,
                activity_type=activity.activity_type,
                activity_name=activity.activity_name,
                subject=activity.subject,
                score=activity.score,
                time_spent=activity.time_spent,
                difficulty_level=activity.difficulty_level,
                created_at=activity.created_at
            )
            for activity in activities
        ]
        
    except Exception as e:
        logger.error(f"Error getting recent activities: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get recent activities"
        )

@router.get("/coding-practices", response_model=List[CodingPracticeResponse])
async def get_coding_practices(
    limit: int = 20,
    language: Optional[str] = None,
    difficulty: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get coding practice sessions for the current user."""
    try:
        from app.models.progress import CodingPractice
        from sqlalchemy import desc
        
        query = db.query(CodingPractice).filter(CodingPractice.user_id == current_user.id)
        
        if language:
            query = query.filter(CodingPractice.language == language)
        
        if difficulty:
            query = query.filter(CodingPractice.problem_difficulty == difficulty)
        
        practices = query.order_by(desc(CodingPractice.created_at)).limit(limit).all()
        
        return [
            CodingPracticeResponse(
                id=practice.id,
                user_id=practice.user_id,
                problem_title=practice.problem_title,
                problem_difficulty=practice.problem_difficulty,
                language=practice.language,
                test_cases_passed=practice.test_cases_passed,
                total_test_cases=practice.total_test_cases,
                execution_time=practice.execution_time,
                memory_usage=practice.memory_usage,
                ai_feedback=practice.ai_feedback,
                optimization_suggestions=practice.optimization_suggestions,
                score=practice.score,
                time_spent=practice.time_spent,
                created_at=practice.created_at
            )
            for practice in practices
        ]
        
    except Exception as e:
        logger.error(f"Error getting coding practices: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get coding practices"
        )
