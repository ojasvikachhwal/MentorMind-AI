from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.quiz import QuizAttempt, QuizAnswer
from app.models.performance import UserPerformance, TopicPerformance
from app.schemas.performance import PerformanceResponse, TopicPerformanceResponse

router = APIRouter()

@router.get("/stats", response_model=dict)
async def get_user_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user performance statistics."""
    try:
        # Get all quiz attempts for the user
        attempts = db.query(QuizAttempt).filter(
            QuizAttempt.user_id == current_user.id,
            QuizAttempt.completed_at.isnot(None)
        ).all()
        
        if not attempts:
            return {
                "total_quizzes_taken": 0,
                "average_score": 0.0,
                "total_questions_answered": 0,
                "total_correct_answers": 0,
                "overall_accuracy": 0.0,
                "current_streak": 0,
                "rank": 0
            }
        
        # Calculate basic stats
        total_quizzes = len(attempts)
        total_score = sum(attempt.score or 0 for attempt in attempts)
        average_score = total_score / total_quizzes if total_quizzes > 0 else 0
        
        total_questions = sum(attempt.total_questions or 0 for attempt in attempts)
        total_correct = sum(attempt.correct_answers or 0 for attempt in attempts)
        overall_accuracy = total_correct / total_questions if total_questions > 0 else 0
        
        # Calculate current streak
        current_streak = 0
        today = datetime.utcnow().date()
        
        for attempt in sorted(attempts, key=lambda x: x.completed_at, reverse=True):
            if attempt.completed_at and attempt.completed_at.date() == today - timedelta(days=current_streak):
                current_streak += 1
            else:
                break
        
        # Calculate rank (simplified - would need more complex logic in production)
        all_users = db.query(User).count()
        rank = max(1, all_users - current_streak)  # Simplified ranking
        
        return {
            "total_quizzes_taken": total_quizzes,
            "average_score": average_score,
            "total_questions_answered": total_questions,
            "total_correct_answers": total_correct,
            "overall_accuracy": overall_accuracy,
            "current_streak": current_streak,
            "rank": rank
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching user stats: {str(e)}"
        )

@router.get("/weak-areas", response_model=List[str])
async def get_weak_areas(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's weak areas based on quiz performance."""
    try:
        # Get all quiz attempts with quiz information
        attempts = db.query(QuizAttempt).join(QuizAttempt.quiz).filter(
            QuizAttempt.user_id == current_user.id,
            QuizAttempt.completed_at.isnot(None)
        ).all()
        
        if not attempts:
            return ["No quiz data available"]
        
        # Calculate performance by topic
        topic_performance = {}
        
        for attempt in attempts:
            topic = attempt.quiz.topic
            if topic not in topic_performance:
                topic_performance[topic] = {
                    'total_questions': 0,
                    'correct_answers': 0,
                    'attempts': 0
                }
            
            topic_performance[topic]['total_questions'] += attempt.total_questions or 0
            topic_performance[topic]['correct_answers'] += attempt.correct_answers or 0
            topic_performance[topic]['attempts'] += 1
        
        # Identify weak areas (topics with accuracy < 70%)
        weak_areas = []
        for topic, perf in topic_performance.items():
            accuracy = perf['correct_answers'] / perf['total_questions'] if perf['total_questions'] > 0 else 0
            if accuracy < 0.7:
                weak_areas.append(topic)
        
        # If no weak areas, suggest improvement areas
        if not weak_areas:
            weak_areas = ["Consider practicing more to identify specific weak areas"]
        
        return weak_areas[:5]  # Return top 5 weak areas
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching weak areas: {str(e)}"
        )

@router.get("/progress", response_model=dict)
async def get_progress_data(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user progress data for charts."""
    try:
        # Get quiz attempts from the last 4 weeks
        four_weeks_ago = datetime.utcnow() - timedelta(weeks=4)
        
        attempts = db.query(QuizAttempt).filter(
            QuizAttempt.user_id == current_user.id,
            QuizAttempt.completed_at >= four_weeks_ago
        ).order_by(QuizAttempt.completed_at).all()
        
        # Group by week
        weekly_data = {}
        for attempt in attempts:
            week_start = attempt.completed_at.date() - timedelta(days=attempt.completed_at.weekday())
            week_key = week_start.strftime('%Y-%m-%d')
            
            if week_key not in weekly_data:
                weekly_data[week_key] = {
                    'scores': [],
                    'total_questions': 0,
                    'correct_answers': 0
                }
            
            weekly_data[week_key]['scores'].append(attempt.score or 0)
            weekly_data[week_key]['total_questions'] += attempt.total_questions or 0
            weekly_data[week_key]['correct_answers'] += attempt.correct_answers or 0
        
        # Calculate weekly averages
        weeks = []
        averages = []
        
        for i in range(4):
            week_date = datetime.utcnow().date() - timedelta(weeks=3-i)
            week_key = week_date.strftime('%Y-%m-%d')
            
            weeks.append(f"Week {i+1}")
            
            if week_key in weekly_data:
                week_scores = weekly_data[week_key]['scores']
                avg_score = sum(week_scores) / len(week_scores) if week_scores else 0
                averages.append(round(avg_score * 100, 1))
            else:
                averages.append(0)
        
        return {
            "weeks": weeks,
            "averages": averages
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching progress data: {str(e)}"
        )

@router.get("/topic-performance", response_model=List[TopicPerformanceResponse])
async def get_topic_performance(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user performance by topic."""
    try:
        # Get all quiz attempts with quiz information
        attempts = db.query(QuizAttempt).join(QuizAttempt.quiz).filter(
            QuizAttempt.user_id == current_user.id,
            QuizAttempt.completed_at.isnot(None)
        ).all()
        
        if not attempts:
            return []
        
        # Calculate performance by topic
        topic_performance = {}
        
        for attempt in attempts:
            topic = attempt.quiz.topic
            if topic not in topic_performance:
                topic_performance[topic] = {
                    'total_questions': 0,
                    'correct_answers': 0,
                    'attempts': 0,
                    'last_attempt': None
                }
            
            topic_performance[topic]['total_questions'] += attempt.total_questions or 0
            topic_performance[topic]['correct_answers'] += attempt.correct_answers or 0
            topic_performance[topic]['attempts'] += 1
            
            if not topic_performance[topic]['last_attempt'] or attempt.completed_at > topic_performance[topic]['last_attempt']:
                topic_performance[topic]['last_attempt'] = attempt.completed_at
        
        # Convert to response format
        result = []
        for topic, perf in topic_performance.items():
            accuracy = perf['correct_answers'] / perf['total_questions'] if perf['total_questions'] > 0 else 0
            
            result.append(TopicPerformanceResponse(
                topic=topic,
                total_questions=perf['total_questions'],
                correct_answers=perf['correct_answers'],
                accuracy=accuracy,
                last_attempt=perf['last_attempt']
            ))
        
        return result
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching topic performance: {str(e)}"
        )
