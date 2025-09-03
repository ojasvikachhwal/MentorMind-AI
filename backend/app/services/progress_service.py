"""
Progress Tracking Service with AI Analysis
Handles student progress tracking, analytics, and AI-powered feedback generation.
"""

import json
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, desc

from app.models.progress import (
    StudentProgress, ProgressAnalytics, AIFeedback, 
    CodingPractice, WeeklyReport, ActivityType, FeedbackType
)
from app.models.assessment import Course, Subject
from app.models.quiz import QuizAttempt
from app.models.user import User
from app.services.ai_feedback_service import AIFeedbackService

logger = logging.getLogger(__name__)

class ProgressService:
    """Service for tracking and analyzing student progress."""
    
    def __init__(self, db: Session):
        self.db = db
        self.ai_service = AIFeedbackService()
    
    def track_activity(
        self,
        user_id: int,
        activity_type: ActivityType,
        activity_name: str,
        subject: Optional[str] = None,
        score: Optional[float] = None,
        time_spent: int = 0,
        difficulty_level: Optional[str] = None,
        activity_id: Optional[int] = None,
        metadata: Optional[Dict] = None
    ) -> StudentProgress:
        """Track a student activity."""
        try:
            progress = StudentProgress(
                user_id=user_id,
                activity_type=activity_type,
                activity_name=activity_name,
                subject=subject,
                score=score,
                time_spent=time_spent,
                difficulty_level=difficulty_level,
                activity_id=activity_id,
                activity_metadata=metadata
            )
            
            self.db.add(progress)
            self.db.commit()
            self.db.refresh(progress)
            
            logger.info(f"Tracked activity for user {user_id}: {activity_name}")
            return progress
            
        except Exception as e:
            logger.error(f"Error tracking activity: {e}")
            self.db.rollback()
            raise
    
    def track_coding_practice(
        self,
        user_id: int,
        problem_title: str,
        problem_difficulty: str,
        language: str,
        solution_code: str,
        test_cases_passed: int,
        total_test_cases: int,
        execution_time: Optional[float] = None,
        memory_usage: Optional[float] = None,
        time_spent: int = 0
    ) -> CodingPractice:
        """Track coding practice session with AI analysis."""
        try:
            # Calculate score
            score = (test_cases_passed / total_test_cases) * 100 if total_test_cases > 0 else 0
            
            # Generate AI feedback
            ai_feedback, optimization_suggestions = self.ai_service.analyze_code_quality(
                solution_code, language, execution_time, memory_usage
            )
            
            coding_practice = CodingPractice(
                user_id=user_id,
                problem_title=problem_title,
                problem_difficulty=problem_difficulty,
                language=language,
                solution_code=solution_code,
                test_cases_passed=test_cases_passed,
                total_test_cases=total_test_cases,
                execution_time=execution_time,
                memory_usage=memory_usage,
                ai_feedback=ai_feedback,
                optimization_suggestions=optimization_suggestions,
                score=score,
                time_spent=time_spent
            )
            
            self.db.add(coding_practice)
            self.db.commit()
            self.db.refresh(coding_practice)
            
            # Track as progress activity
            self.track_activity(
                user_id=user_id,
                activity_type=ActivityType.CODING_PRACTICE,
                activity_name=problem_title,
                subject="Coding",
                score=score,
                time_spent=time_spent,
                difficulty_level=problem_difficulty,
                activity_id=coding_practice.id,
                metadata={
                    "language": language,
                    "test_cases_passed": test_cases_passed,
                    "total_test_cases": total_test_cases,
                    "execution_time": execution_time,
                    "memory_usage": memory_usage
                }
            )
            
            logger.info(f"Tracked coding practice for user {user_id}: {problem_title}")
            return coding_practice
            
        except Exception as e:
            logger.error(f"Error tracking coding practice: {e}")
            self.db.rollback()
            raise
    
    def get_weekly_analytics(self, user_id: int, week_start: Optional[datetime] = None) -> ProgressAnalytics:
        """Generate weekly analytics for a user."""
        if week_start is None:
            week_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            week_start = week_start - timedelta(days=week_start.weekday())
        
        week_end = week_start + timedelta(days=7)
        
        # Check if analytics already exist for this week
        existing_analytics = self.db.query(ProgressAnalytics).filter(
            and_(
                ProgressAnalytics.user_id == user_id,
                ProgressAnalytics.week_start == week_start
            )
        ).first()
        
        if existing_analytics:
            return existing_analytics
        
        # Get activities for the week
        activities = self.db.query(StudentProgress).filter(
            and_(
                StudentProgress.user_id == user_id,
                StudentProgress.created_at >= week_start,
                StudentProgress.created_at < week_end
            )
        ).all()
        
        # Calculate metrics
        total_study_time = sum(activity.time_spent for activity in activities)
        courses_completed = len([a for a in activities if a.activity_type == ActivityType.COURSE_COMPLETION])
        quizzes_taken = len([a for a in activities if a.activity_type == ActivityType.QUIZ_ATTEMPT])
        coding_sessions = len([a for a in activities if a.activity_type == ActivityType.CODING_PRACTICE])
        
        # Calculate average scores
        quiz_scores = [a.score for a in activities if a.activity_type == ActivityType.QUIZ_ATTEMPT and a.score is not None]
        coding_scores = [a.score for a in activities if a.activity_type == ActivityType.CODING_PRACTICE and a.score is not None]
        
        average_quiz_score = sum(quiz_scores) / len(quiz_scores) if quiz_scores else 0.0
        average_coding_score = sum(coding_scores) / len(coding_scores) if coding_scores else 0.0
        
        # Analyze subject performance
        subject_performance = {}
        for activity in activities:
            if activity.subject:
                if activity.subject not in subject_performance:
                    subject_performance[activity.subject] = {
                        "activities": 0,
                        "total_time": 0,
                        "scores": [],
                        "average_score": 0.0
                    }
                
                subject_performance[activity.subject]["activities"] += 1
                subject_performance[activity.subject]["total_time"] += activity.time_spent
                if activity.score is not None:
                    subject_performance[activity.subject]["scores"].append(activity.score)
        
        # Calculate average scores per subject
        for subject, data in subject_performance.items():
            if data["scores"]:
                data["average_score"] = sum(data["scores"]) / len(data["scores"])
        
        # Generate AI insights
        strengths, weaknesses, recommendations = self.ai_service.generate_weekly_insights(
            subject_performance, activities
        )
        
        # Create analytics record
        analytics = ProgressAnalytics(
            user_id=user_id,
            week_start=week_start,
            week_end=week_end,
            total_study_time=total_study_time,
            courses_completed=courses_completed,
            quizzes_taken=quizzes_taken,
            coding_sessions=coding_sessions,
            average_quiz_score=average_quiz_score,
            average_coding_score=average_coding_score,
            subject_performance=subject_performance,
            strengths=strengths,
            weaknesses=weaknesses,
            recommendations=recommendations
        )
        
        self.db.add(analytics)
        self.db.commit()
        self.db.refresh(analytics)
        
        return analytics
    
    def generate_weekly_report(self, user_id: int, week_start: Optional[datetime] = None) -> WeeklyReport:
        """Generate a comprehensive weekly report for a user."""
        if week_start is None:
            week_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            week_start = week_start - timedelta(days=week_start.weekday())
        
        week_end = week_start + timedelta(days=7)
        
        # Check if report already exists
        existing_report = self.db.query(WeeklyReport).filter(
            and_(
                WeeklyReport.user_id == user_id,
                WeeklyReport.week_start == week_start
            )
        ).first()
        
        if existing_report:
            return existing_report
        
        # Get weekly analytics
        analytics = self.get_weekly_analytics(user_id, week_start)
        
        # Get user info
        user = self.db.query(User).filter(User.id == user_id).first()
        
        # Generate AI-powered report content
        report_content = self.ai_service.generate_weekly_report_content(
            user, analytics, week_start, week_end
        )
        
        # Get recommended courses and coding problems
        recommended_courses = self._get_recommended_courses(user_id, analytics.weaknesses or [])
        recommended_coding_problems = self._get_recommended_coding_problems(
            user_id, analytics.weaknesses or []
        )
        
        # Create weekly report
        report = WeeklyReport(
            user_id=user_id,
            week_start=week_start,
            week_end=week_end,
            summary=report_content["summary"],
            achievements=report_content["achievements"],
            areas_for_improvement=report_content["areas_for_improvement"],
            next_week_goals=report_content["next_week_goals"],
            recommended_courses=recommended_courses,
            recommended_coding_problems=recommended_coding_problems
        )
        
        self.db.add(report)
        self.db.commit()
        self.db.refresh(report)
        
        return report
    
    def get_progress_dashboard_data(self, user_id: int, days: int = 30) -> Dict[str, Any]:
        """Get comprehensive progress data for dashboard."""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # Get activities
        activities = self.db.query(StudentProgress).filter(
            and_(
                StudentProgress.user_id == user_id,
                StudentProgress.created_at >= start_date,
                StudentProgress.created_at <= end_date
            )
        ).order_by(StudentProgress.created_at).all()
        
        # Get coding practices
        coding_practices = self.db.query(CodingPractice).filter(
            and_(
                CodingPractice.user_id == user_id,
                CodingPractice.created_at >= start_date,
                CodingPractice.created_at <= end_date
            )
        ).order_by(CodingPractice.created_at).all()
        
        # Get recent AI feedback
        recent_feedback = self.db.query(AIFeedback).filter(
            AIFeedback.user_id == user_id
        ).order_by(desc(AIFeedback.created_at)).limit(5).all()
        
        # Get weekly analytics for the period
        weekly_analytics = self.db.query(ProgressAnalytics).filter(
            and_(
                ProgressAnalytics.user_id == user_id,
                ProgressAnalytics.week_start >= start_date
            )
        ).order_by(ProgressAnalytics.week_start).all()
        
        # Process data for charts
        daily_activity = self._process_daily_activity_data(activities, start_date, end_date)
        subject_performance = self._process_subject_performance_data(activities)
        coding_progress = self._process_coding_progress_data(coding_practices)
        
        return {
            "daily_activity": daily_activity,
            "subject_performance": subject_performance,
            "coding_progress": coding_progress,
            "recent_feedback": [
                {
                    "id": feedback.id,
                    "type": feedback.feedback_type,
                    "title": feedback.title,
                    "message": feedback.message,
                    "subject": feedback.subject,
                    "created_at": feedback.created_at.isoformat(),
                    "is_read": feedback.is_read
                }
                for feedback in recent_feedback
            ],
            "weekly_analytics": [
                {
                    "week_start": analytics.week_start.isoformat(),
                    "total_study_time": analytics.total_study_time,
                    "courses_completed": analytics.courses_completed,
                    "quizzes_taken": analytics.quizzes_taken,
                    "coding_sessions": analytics.coding_sessions,
                    "average_quiz_score": analytics.average_quiz_score,
                    "average_coding_score": analytics.average_coding_score
                }
                for analytics in weekly_analytics
            ],
            "summary": {
                "total_activities": len(activities),
                "total_coding_sessions": len(coding_practices),
                "total_study_time": sum(activity.time_spent for activity in activities),
                "average_quiz_score": self._calculate_average_score(
                    [a for a in activities if a.activity_type == ActivityType.QUIZ_ATTEMPT]
                ),
                "average_coding_score": self._calculate_average_score(
                    [a for a in activities if a.activity_type == ActivityType.CODING_PRACTICE]
                )
            }
        }
    
    def _process_daily_activity_data(self, activities: List[StudentProgress], start_date: datetime, end_date: datetime) -> List[Dict]:
        """Process activities into daily data for charts."""
        daily_data = {}
        current_date = start_date
        
        while current_date <= end_date:
            date_str = current_date.strftime("%Y-%m-%d")
            daily_data[date_str] = {
                "date": date_str,
                "study_time": 0,
                "activities": 0,
                "quiz_score": 0,
                "coding_score": 0
            }
            current_date += timedelta(days=1)
        
        for activity in activities:
            date_str = activity.created_at.strftime("%Y-%m-%d")
            if date_str in daily_data:
                daily_data[date_str]["study_time"] += activity.time_spent
                daily_data[date_str]["activities"] += 1
                
                if activity.activity_type == ActivityType.QUIZ_ATTEMPT and activity.score:
                    daily_data[date_str]["quiz_score"] = activity.score
                elif activity.activity_type == ActivityType.CODING_PRACTICE and activity.score:
                    daily_data[date_str]["coding_score"] = activity.score
        
        return list(daily_data.values())
    
    def _process_subject_performance_data(self, activities: List[StudentProgress]) -> List[Dict]:
        """Process activities into subject performance data."""
        subject_data = {}
        
        for activity in activities:
            if activity.subject:
                if activity.subject not in subject_data:
                    subject_data[activity.subject] = {
                        "subject": activity.subject,
                        "activities": 0,
                        "total_time": 0,
                        "scores": [],
                        "average_score": 0.0
                    }
                
                subject_data[activity.subject]["activities"] += 1
                subject_data[activity.subject]["total_time"] += activity.time_spent
                if activity.score is not None:
                    subject_data[activity.subject]["scores"].append(activity.score)
        
        # Calculate average scores
        for subject, data in subject_data.items():
            if data["scores"]:
                data["average_score"] = sum(data["scores"]) / len(data["scores"])
        
        return list(subject_data.values())
    
    def _process_coding_progress_data(self, coding_practices: List[CodingPractice]) -> List[Dict]:
        """Process coding practices into progress data."""
        return [
            {
                "date": practice.created_at.strftime("%Y-%m-%d"),
                "problem": practice.problem_title,
                "difficulty": practice.problem_difficulty,
                "language": practice.language,
                "score": practice.score,
                "execution_time": practice.execution_time,
                "test_cases_passed": practice.test_cases_passed,
                "total_test_cases": practice.total_test_cases
            }
            for practice in coding_practices
        ]
    
    def _calculate_average_score(self, activities: List[StudentProgress]) -> float:
        """Calculate average score from activities."""
        scores = [activity.score for activity in activities if activity.score is not None]
        return sum(scores) / len(scores) if scores else 0.0
    
    def _get_recommended_courses(self, user_id: int, weaknesses: List[str]) -> List[Dict]:
        """Get recommended courses based on weaknesses."""
        if not weaknesses:
            return []
        
        # Get courses for weak subjects
        courses = self.db.query(Course).join(Subject).filter(
            Subject.name.in_(weaknesses)
        ).limit(5).all()
        
        return [
            {
                "id": course.id,
                "title": course.title,
                "level": course.level,
                "subject": course.subject.name if course.subject else None,
                "url": course.url
            }
            for course in courses
        ]
    
    def _get_recommended_coding_problems(self, user_id: int, weaknesses: List[str]) -> List[Dict]:
        """Get recommended coding problems based on weaknesses."""
        # This would typically come from an external coding platform API
        # For now, return mock data
        return [
            {
                "title": "Two Sum",
                "difficulty": "Easy",
                "topic": "Array",
                "url": "https://leetcode.com/problems/two-sum/"
            },
            {
                "title": "Binary Tree Inorder Traversal",
                "difficulty": "Medium",
                "topic": "Tree",
                "url": "https://leetcode.com/problems/binary-tree-inorder-traversal/"
            }
        ]
