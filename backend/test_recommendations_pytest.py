#!/usr/bin/env python3
"""
Pytest test suite for the recommendation engine.
Run with: pytest test_recommendations_pytest.py -v
"""

import pytest
from unittest.mock import Mock, patch
from sqlalchemy.orm import Session
from app.services.recommendation_engine import RecommendationEngine
from app.models.assessment import (
    Subject, Course, Question, AssessmentSession, AssessmentAnswer,
    CourseLevel, QuestionDifficulty, AssessmentStatus
)
from app.models.user import User

class TestRecommendationEngine:
    """Test cases for the RecommendationEngine class."""
    
    @pytest.fixture
    def mock_db(self):
        """Create a mock database session."""
        return Mock(spec=Session)
    
    @pytest.fixture
    def mock_user(self):
        """Create a mock user."""
        user = Mock(spec=User)
        user.id = 1
        user.username = "teststudent"
        return user
    
    @pytest.fixture
    def mock_subject(self):
        """Create a mock subject."""
        subject = Mock(spec=Subject)
        subject.id = 1
        subject.name = "Mathematics"
        return subject
    
    @pytest.fixture
    def mock_course_beginner(self):
        """Create a mock beginner course."""
        course = Mock(spec=Course)
        course.id = 1
        course.title = "Intro to Algebra"
        course.level = CourseLevel.BEGINNER
        course.description = "Basic algebra concepts"
        return course
    
    @pytest.fixture
    def mock_course_intermediate(self):
        """Create a mock intermediate course."""
        course = Mock(spec=Course)
        course.id = 2
        course.title = "Algebra Problem Solving"
        course.level = CourseLevel.INTERMEDIATE
        course.description = "Intermediate algebra problems"
        return course
    
    @pytest.fixture
    def mock_assessment_session(self):
        """Create a mock assessment session."""
        session = Mock(spec=AssessmentSession)
        session.id = 1
        session.user_id = 1
        session.selected_subject_ids = [1]
        session.status = AssessmentStatus.SUBMITTED
        return session
    
    @pytest.fixture
    def mock_answers(self):
        """Create mock assessment answers."""
        answers = []
        
        # Easy questions - mostly correct
        for i in range(8):
            answer = Mock(spec=AssessmentAnswer)
            answer.is_correct = True
            answer.question.difficulty = QuestionDifficulty.EASY
            answers.append(answer)
        
        # Medium questions - mixed results
        for i in range(6):
            answer = Mock(spec=AssessmentAnswer)
            answer.is_correct = i < 3  # 3 correct, 3 incorrect
            answer.question.difficulty = QuestionDifficulty.MEDIUM
            answers.append(answer)
        
        # Hard questions - mostly incorrect
        for i in range(6):
            answer = Mock(spec=AssessmentAnswer)
            answer.is_correct = i < 2  # 2 correct, 4 incorrect
            answer.question.difficulty = QuestionDifficulty.HARD
            answers.append(answer)
        
        return answers
    
    def test_init(self):
        """Test RecommendationEngine initialization."""
        engine = RecommendationEngine()
        assert engine.scaler is not None
    
    def test_get_course_recommendations_success(self, mock_db, mock_user, mock_subject, 
                                              mock_course_beginner, mock_assessment_session, mock_answers):
        """Test successful course recommendations generation."""
        # Mock database queries
        mock_db.query.return_value.filter.return_value.first.return_value = mock_user
        mock_db.query.return_value.filter.return_value.order_by.return_value.first.return_value = mock_assessment_session
        
        # Mock subject query
        subject_query = Mock()
        subject_query.filter.return_value.first.return_value = mock_subject
        mock_db.query.return_value = subject_query
        
        # Mock answers query
        answers_query = Mock()
        answers_query.join.return_value.filter.return_value.all.return_value = mock_answers
        mock_db.query.return_value = answers_query
        
        # Mock courses query
        courses_query = Mock()
        courses_query.filter.return_value.limit.return_value.all.return_value = [mock_course_beginner]
        mock_db.query.return_value = courses_query
        
        engine = RecommendationEngine()
        result = engine.get_course_recommendations(mock_db, 1, 3)
        
        assert result is not None
        assert "student_id" in result
        assert "student_name" in result
        assert "recommendations" in result
        assert len(result["recommendations"]) > 0
    
    def test_get_course_recommendations_no_student(self, mock_db):
        """Test recommendations when student is not found."""
        mock_db.query.return_value.filter.return_value.first.return_value = None
        
        engine = RecommendationEngine()
        result = engine.get_course_recommendations(mock_db, 999, 3)
        
        # Should return fallback recommendations
        assert result is not None
        assert "student_id" in result
        assert result["student_id"] is None
    
    def test_get_course_recommendations_no_assessment(self, mock_db, mock_user):
        """Test recommendations when no assessment data is available."""
        mock_db.query.return_value.filter.return_value.first.return_value = mock_user
        mock_db.query.return_value.filter.return_value.order_by.return_value.first.return_value = None
        
        # Mock subjects query for fallback
        subjects_query = Mock()
        subjects_query.all.return_value = []
        mock_db.query.return_value = subjects_query
        
        engine = RecommendationEngine()
        result = engine.get_course_recommendations(mock_db, 1, 3)
        
        # Should return fallback recommendations
        assert result is not None
        assert "student_id" in result
        assert result["student_id"] is None
    
    def test_analyze_subject_performance(self, mock_db, mock_subject, mock_answers):
        """Test subject performance analysis."""
        # Mock database queries
        subject_query = Mock()
        subject_query.filter.return_value.first.return_value = mock_subject
        mock_db.query.return_value = subject_query
        
        answers_query = Mock()
        answers_query.join.return_value.filter.return_value.all.return_value = mock_answers
        mock_db.query.return_value = answers_query
        
        engine = RecommendationEngine()
        session = Mock(spec=AssessmentSession)
        session.selected_subject_ids = [1]
        
        result = engine._analyze_subject_performance(mock_db, session)
        
        assert 1 in result
        subject_data = result[1]
        assert "subject_name" in subject_data
        assert "percent_correct" in subject_data
        assert "performance_level" in subject_data
        assert "recommended_level" in subject_data
        assert "weaknesses" in subject_data
    
    def test_identify_weaknesses(self, mock_answers):
        """Test weakness identification logic."""
        engine = RecommendationEngine()
        
        # Create difficulty breakdown
        difficulty_breakdown = {"easy": 8, "medium": 6, "hard": 6}
        
        result = engine._identify_weaknesses(mock_answers, difficulty_breakdown)
        
        assert isinstance(result, list)
        assert len(result) > 0
        # Should identify weaknesses based on incorrect answers
        assert any("Basic concepts" in weakness or "Intermediate problem solving" in weakness or "Advanced concepts" in weakness for weakness in result)
    
    def test_generate_recommendations(self, mock_db, mock_course_beginner, mock_course_intermediate):
        """Test course recommendation generation."""
        # Mock database queries
        courses_query = Mock()
        courses_query.filter.return_value.limit.return_value.all.return_value = [mock_course_beginner]
        mock_db.query.return_value = courses_query
        
        engine = RecommendationEngine()
        
        subject_performance = {
            1: {
                "subject_name": "Mathematics",
                "recommended_level": CourseLevel.BEGINNER,
                "weaknesses": ["Basic concepts"],
                "performance_level": "weak",
                "percent_correct": 35.0,
                "weighted_score": 15
            }
        }
        
        result = engine._generate_recommendations(mock_db, subject_performance, 3)
        
        assert isinstance(result, list)
        assert len(result) > 0
        
        recommendation = result[0]
        assert "subject" in recommendation
        assert "weakness" in recommendation
        assert "recommended_courses" in recommendation
        assert len(recommendation["recommended_courses"]) > 0
    
    def test_get_fallback_recommendations(self, mock_db):
        """Test fallback recommendations when no assessment data is available."""
        # Mock subjects query
        mock_subject = Mock(spec=Subject)
        mock_subject.id = 1
        mock_subject.name = "Mathematics"
        
        subjects_query = Mock()
        subjects_query.all.return_value = [mock_subject]
        mock_db.query.return_value = subjects_query
        
        # Mock courses query
        mock_course = Mock(spec=Course)
        mock_course.id = 1
        mock_course.title = "Basic Math"
        mock_course.level = CourseLevel.BEGINNER
        mock_course.description = "Fundamental mathematics"
        
        courses_query = Mock()
        courses_query.filter.return_value.limit.return_value.all.return_value = [mock_course]
        mock_db.query.return_value = courses_query
        
        engine = RecommendationEngine()
        result = engine._get_fallback_recommendations(mock_db, 3)
        
        assert result is not None
        assert "student_id" in result
        assert result["student_id"] is None
        assert "recommendations" in result
        assert len(result["recommendations"]) > 0
    
    def test_ml_recommendations(self, mock_db, mock_user, mock_subject, 
                               mock_course_beginner, mock_assessment_session, mock_answers):
        """Test ML recommendations endpoint (currently returns same as regular)."""
        # Mock database queries similar to regular recommendations
        mock_db.query.return_value.filter.return_value.first.return_value = mock_user
        mock_db.query.return_value.filter.return_value.order_by.return_value.first.return_value = mock_assessment_session
        
        subject_query = Mock()
        subject_query.filter.return_value.first.return_value = mock_subject
        mock_db.query.return_value = subject_query
        
        answers_query = Mock()
        answers_query.join.return_value.filter.return_value.all.return_value = mock_answers
        mock_db.query.return_value = answers_query
        
        courses_query = Mock()
        courses_query.filter.return_value.limit.return_value.all.return_value = [mock_course_beginner]
        mock_db.query.return_value = courses_query
        
        engine = RecommendationEngine()
        result = engine.get_ml_recommendations(mock_db, 1, 3)
        
        assert result is not None
        assert "student_id" in result
        assert "student_name" in result
        assert "recommendations" in result

def test_performance_level_calculation():
    """Test performance level calculation logic."""
    engine = RecommendationEngine()
    
    # Test weak performance
    assert engine._calculate_performance_level(35.0) == "weak"
    
    # Test moderate performance
    assert engine._calculate_performance_level(65.0) == "moderate"
    
    # Test strong performance
    assert engine._calculate_performance_level(85.0) == "strong"

def test_course_level_mapping():
    """Test course level mapping based on performance."""
    engine = RecommendationEngine()
    
    # Test beginner level recommendation
    assert engine._get_recommended_level(35.0) == CourseLevel.BEGINNER
    
    # Test intermediate level recommendation
    assert engine._get_recommended_level(65.0) == CourseLevel.INTERMEDIATE
    
    # Test advanced level recommendation
    assert engine._get_recommended_level(85.0) == CourseLevel.ADVANCED

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
