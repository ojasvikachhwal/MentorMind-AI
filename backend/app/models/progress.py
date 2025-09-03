from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON, Text, Boolean, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum

class ActivityType(str, enum.Enum):
    COURSE_COMPLETION = "course_completion"
    QUIZ_ATTEMPT = "quiz_attempt"
    CODING_PRACTICE = "coding_practice"
    ASSESSMENT = "assessment"
    STUDY_TIME = "study_time"

class FeedbackType(str, enum.Enum):
    STRENGTH = "strength"
    WEAKNESS = "weakness"
    RECOMMENDATION = "recommendation"
    ENCOURAGEMENT = "encouragement"
    WARNING = "warning"

class StudentProgress(Base):
    __tablename__ = "student_progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    activity_type = Column(Enum(ActivityType), nullable=False)
    activity_id = Column(Integer, nullable=True)  # ID of the specific activity (course, quiz, etc.)
    activity_name = Column(String(200), nullable=False)
    subject = Column(String(100), nullable=True)
    score = Column(Float, nullable=True)  # Score for the activity
    time_spent = Column(Integer, default=0)  # Time spent in minutes
    difficulty_level = Column(String(20), nullable=True)  # beginner, intermediate, advanced
    activity_metadata = Column(JSON, nullable=True)  # Additional activity-specific data
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="progress_activities")
    
    def __repr__(self):
        return f"<StudentProgress(id={self.id}, user_id={self.user_id}, activity='{self.activity_name}')>"

class ProgressAnalytics(Base):
    __tablename__ = "progress_analytics"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    week_start = Column(DateTime(timezone=True), nullable=False)
    week_end = Column(DateTime(timezone=True), nullable=False)
    
    # Weekly metrics
    total_study_time = Column(Integer, default=0)  # in minutes
    courses_completed = Column(Integer, default=0)
    quizzes_taken = Column(Integer, default=0)
    coding_sessions = Column(Integer, default=0)
    average_quiz_score = Column(Float, default=0.0)
    average_coding_score = Column(Float, default=0.0)
    
    # Subject-wise performance
    subject_performance = Column(JSON, nullable=True)  # {subject: {score, time_spent, activities}}
    
    # AI-generated insights
    strengths = Column(JSON, nullable=True)  # Array of strength areas
    weaknesses = Column(JSON, nullable=True)  # Array of weakness areas
    recommendations = Column(JSON, nullable=True)  # Array of recommendations
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="progress_analytics")
    
    def __repr__(self):
        return f"<ProgressAnalytics(id={self.id}, user_id={self.user_id}, week_start='{self.week_start}')>"

class AIFeedback(Base):
    __tablename__ = "ai_feedback"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    feedback_type = Column(Enum(FeedbackType), nullable=False)
    subject = Column(String(100), nullable=True)
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    confidence_score = Column(Float, default=0.0)  # AI confidence in the feedback
    feedback_metadata = Column(JSON, nullable=True)  # Additional context data
    is_read = Column(Boolean, default=False)
    is_archived = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="ai_feedback")
    
    def __repr__(self):
        return f"<AIFeedback(id={self.id}, user_id={self.user_id}, type='{self.feedback_type}')>"

class CodingPractice(Base):
    __tablename__ = "coding_practice"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    problem_title = Column(String(200), nullable=False)
    problem_difficulty = Column(String(20), nullable=False)  # easy, medium, hard
    language = Column(String(50), nullable=False)  # python, java, cpp, etc.
    solution_code = Column(Text, nullable=False)
    test_cases_passed = Column(Integer, default=0)
    total_test_cases = Column(Integer, default=0)
    execution_time = Column(Float, nullable=True)  # in seconds
    memory_usage = Column(Float, nullable=True)  # in MB
    ai_feedback = Column(Text, nullable=True)  # AI analysis of code quality
    optimization_suggestions = Column(JSON, nullable=True)  # AI suggestions for improvement
    score = Column(Float, nullable=True)  # Overall score for the solution
    time_spent = Column(Integer, default=0)  # Time spent in minutes
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="coding_practices")
    
    def __repr__(self):
        return f"<CodingPractice(id={self.id}, user_id={self.user_id}, problem='{self.problem_title}')>"

class WeeklyReport(Base):
    __tablename__ = "weekly_reports"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    week_start = Column(DateTime(timezone=True), nullable=False)
    week_end = Column(DateTime(timezone=True), nullable=False)
    
    # Report content
    summary = Column(Text, nullable=False)
    achievements = Column(JSON, nullable=True)  # Array of achievements
    areas_for_improvement = Column(JSON, nullable=True)  # Array of improvement areas
    next_week_goals = Column(JSON, nullable=True)  # Array of goals
    recommended_courses = Column(JSON, nullable=True)  # Array of course recommendations
    recommended_coding_problems = Column(JSON, nullable=True)  # Array of coding problems
    
    # Email tracking
    email_sent = Column(Boolean, default=False)
    email_sent_at = Column(DateTime(timezone=True), nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="weekly_reports")
    
    def __repr__(self):
        return f"<WeeklyReport(id={self.id}, user_id={self.user_id}, week_start='{self.week_start}')>"
