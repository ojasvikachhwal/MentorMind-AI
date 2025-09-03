"""
Test service layer functionality
"""
import pytest
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.services.progress_service import ProgressService
from app.services.ai_feedback_service import AIFeedbackService
from app.services.recommendation_engine import RecommendationEngine
from app.models.progress import ActivityType, FeedbackType
from app.models.user import User

class TestProgressService:
    """Test ProgressService functionality."""
    
    def test_track_activity(self, db_session: Session, test_user: User):
        """Test tracking a new activity."""
        service = ProgressService(db_session)
        
        activity_data = {
            "user_id": test_user.id,
            "activity_type": ActivityType.COURSE_COMPLETION,
            "activity_name": "Test Course",
            "subject": "Computer Science",
            "score": 85.0,
            "time_spent": 120,
            "difficulty_level": "INTERMEDIATE",
            "metadata": {"course_id": 1}
        }
        
        result = service.track_activity(**activity_data)
        assert result is not None
        assert result.activity_name == activity_data["activity_name"]
        assert result.score == activity_data["score"]
        assert result.user_id == test_user.id
    
    def test_generate_weekly_report(self, db_session: Session, test_user: User):
        """Test weekly report generation."""
        service = ProgressService(db_session)
        
        # First track some activities
        service.track_activity(
            user_id=test_user.id,
            activity_type=ActivityType.COURSE_COMPLETION,
            activity_name="Course 1",
            subject="Computer Science",
            score=85.0,
            time_spent=120,
            difficulty_level="INTERMEDIATE",
            metadata={"course_id": 1}
        )
        
        service.track_activity(
            user_id=test_user.id,
            activity_type=ActivityType.QUIZ_ATTEMPT,
            activity_name="Quiz 1",
            subject="Computer Science",
            score=90.0,
            time_spent=30,
            difficulty_level="INTERMEDIATE",
            metadata={"quiz_id": 1}
        )
        
        # Generate weekly report
        report = service.generate_weekly_report(test_user.id)
        assert report is not None
        assert report.user_id == test_user.id
        assert "summary" in report.__dict__
        assert "achievements" in report.__dict__
    
    def test_get_progress_dashboard_data(self, db_session: Session, test_user: User):
        """Test dashboard data retrieval."""
        service = ProgressService(db_session)
        
        # Track some activities
        service.track_activity(
            user_id=test_user.id,
            activity_type=ActivityType.COURSE_COMPLETION,
            activity_name="Course 1",
            subject="Computer Science",
            score=85.0,
            time_spent=120,
            difficulty_level="INTERMEDIATE",
            metadata={"course_id": 1}
        )
        
        # Get dashboard data
        dashboard_data = service.get_progress_dashboard_data(test_user.id)
        assert dashboard_data is not None
        assert "recent_activities" in dashboard_data
        assert "subject_performance" in dashboard_data
        assert "coding_progress" in dashboard_data

class TestAIFeedbackService:
    """Test AIFeedbackService functionality."""
    
    def test_generate_personalized_feedback(self, test_user: User):
        """Test AI feedback generation."""
        service = AIFeedbackService()
        
        # Test strength feedback
        strength_feedback = service.generate_personalized_feedback(
            test_user.id,
            FeedbackType.STRENGTH,
            "Computer Science"
        )
        assert strength_feedback is not None
        assert isinstance(strength_feedback, str)
        assert len(strength_feedback) > 0
        
        # Test weakness feedback
        weakness_feedback = service.generate_personalized_feedback(
            test_user.id,
            FeedbackType.WEAKNESS,
            "Study consistency"
        )
        assert weakness_feedback is not None
        assert isinstance(weakness_feedback, str)
        assert len(weakness_feedback) > 0
    
    def test_generate_coding_feedback(self, test_user: User):
        """Test coding-specific feedback generation."""
        service = AIFeedbackService()
        
        code = "def two_sum(nums, target):\n    return [0, 1]"
        feedback = service.generate_coding_feedback(
            test_user.id,
            code,
            "Python",
            "Two Sum"
        )
        assert feedback is not None
        assert isinstance(feedback, str)
        assert len(feedback) > 0

class TestRecommendationEngine:
    """Test RecommendationEngine functionality."""
    
    def test_generate_course_recommendations(self, db_session: Session, test_user: User):
        """Test course recommendation generation."""
        engine = RecommendationEngine()
        
        # Mock user preferences and history
        user_preferences = {
            "subjects": ["Computer Science", "Mathematics"],
            "difficulty_level": "INTERMEDIATE",
            "learning_style": "visual"
        }
        
        recommendations = engine.generate_course_recommendations(
            test_user.id,
            user_preferences
        )
        assert recommendations is not None
        assert isinstance(recommendations, list)
        assert len(recommendations) > 0
        
        # Check recommendation structure
        for rec in recommendations:
            assert "course_id" in rec
            assert "title" in rec
            assert "subject" in rec
            assert "difficulty_level" in rec
            assert "confidence_score" in rec
    
    def test_generate_coding_problem_recommendations(self, db_session: Session, test_user: User):
        """Test coding problem recommendation generation."""
        engine = RecommendationEngine()
        
        # Mock user coding history
        coding_history = {
            "solved_problems": ["Two Sum", "Valid Parentheses"],
            "preferred_languages": ["Python", "JavaScript"],
            "difficulty_preference": "EASY"
        }
        
        recommendations = engine.generate_coding_problem_recommendations(
            test_user.id,
            coding_history
        )
        assert recommendations is not None
        assert isinstance(recommendations, list)
        assert len(recommendations) > 0
        
        # Check recommendation structure
        for rec in recommendations:
            assert "problem_id" in rec
            assert "title" in rec
            assert "difficulty" in rec
            assert "language" in rec
            assert "confidence_score" in rec
