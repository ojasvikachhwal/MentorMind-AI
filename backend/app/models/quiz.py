from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Float, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    topic = Column(String(100), nullable=False)
    difficulty_level = Column(String(20), nullable=False)  # easy, medium, hard
    time_limit = Column(Integer, nullable=True)  # in minutes
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    questions = relationship("Question", back_populates="quiz")
    attempts = relationship("QuizAttempt", back_populates="quiz")
    
    def __repr__(self):
        return f"<Quiz(id={self.id}, title='{self.title}', topic='{self.topic}')>"

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"), nullable=False)
    question_text = Column(Text, nullable=False)
    question_type = Column(String(20), nullable=False)  # mcq, flashcard, coding
    options = Column(JSON, nullable=True)  # For MCQ questions
    correct_answer = Column(Text, nullable=False)
    explanation = Column(Text, nullable=True)
    difficulty_score = Column(Float, nullable=False)  # 1.0 to 10.0
    topic_tags = Column(JSON, nullable=True)  # Array of related topics
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    quiz = relationship("Quiz", back_populates="questions")
    answers = relationship("QuizAnswer", back_populates="question")
    
    def __repr__(self):
        return f"<Question(id={self.id}, quiz_id={self.quiz_id}, type='{self.question_type}')>"

class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"), nullable=False)
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    score = Column(Float, nullable=True)
    total_questions = Column(Integer, nullable=False)
    correct_answers = Column(Integer, nullable=True)
    time_taken = Column(Integer, nullable=True)  # in seconds
    difficulty_adjustment = Column(Float, default=1.0)  # AI adaptive factor
    
    # Relationships
    user = relationship("User", back_populates="quiz_attempts")
    quiz = relationship("Quiz", back_populates="attempts")
    answers = relationship("QuizAnswer", back_populates="attempt")
    
    def __repr__(self):
        return f"<QuizAttempt(id={self.id}, user_id={self.user_id}, quiz_id={self.quiz_id})>"

class QuizAnswer(Base):
    __tablename__ = "quiz_answers"

    id = Column(Integer, primary_key=True, index=True)
    attempt_id = Column(Integer, ForeignKey("quiz_attempts.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    user_answer = Column(Text, nullable=False)
    is_correct = Column(Boolean, nullable=False)
    time_taken = Column(Integer, nullable=True)  # in seconds
    confidence_score = Column(Float, nullable=True)  # User's confidence (1-10)
    answered_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    attempt = relationship("QuizAttempt", back_populates="answers")
    question = relationship("Question", back_populates="answers")
    
    def __repr__(self):
        return f"<QuizAnswer(id={self.id}, attempt_id={self.attempt_id}, question_id={self.question_id})>"
