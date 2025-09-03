from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class UserPerformance(Base):
    __tablename__ = "user_performances"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    total_quizzes_taken = Column(Integer, default=0)
    total_questions_answered = Column(Integer, default=0)
    total_correct_answers = Column(Integer, default=0)
    overall_score = Column(Float, default=0.0)
    average_time_per_question = Column(Float, default=0.0)
    longest_streak = Column(Integer, default=0)
    current_streak = Column(Integer, default=0)
    total_study_time = Column(Integer, default=0)  # in minutes
    last_activity = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="performances")
    topic_performances = relationship("TopicPerformance", back_populates="user_performance")
    
    def __repr__(self):
        return f"<UserPerformance(id={self.id}, user_id={self.user_id}, score={self.overall_score})>"

class TopicPerformance(Base):
    __tablename__ = "topic_performances"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user_performance_id = Column(Integer, ForeignKey("user_performances.id"), nullable=False)
    topic = Column(String(100), nullable=False)
    questions_attempted = Column(Integer, default=0)
    correct_answers = Column(Integer, default=0)
    accuracy_rate = Column(Float, default=0.0)
    average_difficulty = Column(Float, default=1.0)
    time_spent = Column(Integer, default=0)  # in minutes
    last_attempt = Column(DateTime(timezone=True), nullable=True)
    strength_score = Column(Float, default=0.0)  # AI-calculated strength
    weakness_score = Column(Float, default=0.0)  # AI-calculated weakness
    recommended_next_topics = Column(JSON, nullable=True)  # Array of topic suggestions
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="topic_performances")
    user_performance = relationship("UserPerformance", back_populates="topic_performances")
    
    def __repr__(self):
        return f"<TopicPerformance(id={self.id}, user_id={self.user_id}, topic='{self.topic}')>"
