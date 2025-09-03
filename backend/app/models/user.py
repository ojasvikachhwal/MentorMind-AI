from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=True)
    bio = Column(Text, nullable=True)
    profile_picture = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    quiz_attempts = relationship("QuizAttempt", back_populates="user")
    performances = relationship("UserPerformance", back_populates="user")
    topic_performances = relationship("TopicPerformance", back_populates="user")
    badges = relationship("UserBadge", back_populates="user")
    streaks = relationship("Streak", back_populates="user")
    chat_sessions = relationship("ChatSession", back_populates="user")
    assessment_sessions = relationship("AssessmentSession", back_populates="user")
    progress_activities = relationship("StudentProgress", back_populates="user")
    progress_analytics = relationship("ProgressAnalytics", back_populates="user")
    ai_feedback = relationship("AIFeedback", back_populates="user")
    coding_practices = relationship("CodingPractice", back_populates="user")
    weekly_reports = relationship("WeeklyReport", back_populates="user")
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"
