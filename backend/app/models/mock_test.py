from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Enum, Index, JSON, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum

class MockTestStatus(str, enum.Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    INACTIVE = "inactive"

class MockTestSessionStatus(str, enum.Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    SUBMITTED = "submitted"

class MockTest(Base):
    """
    Mock Test model for creating and managing mock tests
    """
    __tablename__ = "mock_tests"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    instructor_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    total_marks = Column(Integer, default=0, nullable=False)
    time_limit_minutes = Column(Integer, default=60, nullable=False)  # Time limit in minutes
    status = Column(Enum(MockTestStatus), default=MockTestStatus.DRAFT, nullable=False)
    is_public = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    subject = relationship("Subject")
    instructor = relationship("User")
    questions = relationship("MockTestQuestion", back_populates="mock_test", cascade="all, delete-orphan")
    sessions = relationship("MockTestSession", back_populates="mock_test", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<MockTest(id={self.id}, title='{self.title}', status='{self.status}')>"

class MockTestQuestion(Base):
    """
    Questions for mock tests with 4 options each
    """
    __tablename__ = "mock_test_questions"

    id = Column(Integer, primary_key=True, index=True)
    mock_test_id = Column(Integer, ForeignKey("mock_tests.id"), nullable=False)
    question_text = Column(Text, nullable=False)
    option_a = Column(Text, nullable=False)
    option_b = Column(Text, nullable=False)
    option_c = Column(Text, nullable=False)
    option_d = Column(Text, nullable=False)
    correct_option = Column(Enum('A', 'B', 'C', 'D'), nullable=False)
    marks = Column(Integer, default=1, nullable=False)
    explanation = Column(Text, nullable=True)
    difficulty = Column(Enum('easy', 'medium', 'hard'), default='medium', nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    mock_test = relationship("MockTest", back_populates="questions")
    answers = relationship("MockTestAnswer", back_populates="question", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<MockTestQuestion(id={self.id}, mock_test_id={self.mock_test_id})>"

class MockTestSession(Base):
    """
    Student session for taking a mock test
    """
    __tablename__ = "mock_test_sessions"

    id = Column(Integer, primary_key=True, index=True)
    mock_test_id = Column(Integer, ForeignKey("mock_tests.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(Enum(MockTestSessionStatus), default=MockTestSessionStatus.NOT_STARTED, nullable=False)
    started_at = Column(DateTime(timezone=True), nullable=True)
    submitted_at = Column(DateTime(timezone=True), nullable=True)
    total_score = Column(Float, default=0.0, nullable=False)
    total_marks = Column(Integer, default=0, nullable=False)
    percentage = Column(Float, default=0.0, nullable=False)
    time_taken_minutes = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    mock_test = relationship("MockTest", back_populates="sessions")
    student = relationship("User")
    answers = relationship("MockTestAnswer", back_populates="session", cascade="all, delete-orphan")

    # Indexes
    __table_args__ = (
        Index('idx_session_student_test', 'student_id', 'mock_test_id'),
        {'extend_existing': True}
    )

    def __repr__(self):
        return f"<MockTestSession(id={self.id}, student_id={self.student_id}, status='{self.status}')>"

class MockTestAnswer(Base):
    """
    Student answers for mock test questions
    """
    __tablename__ = "mock_test_answers"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("mock_test_sessions.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("mock_test_questions.id"), nullable=False)
    selected_option = Column(Enum('A', 'B', 'C', 'D'), nullable=True)  # Null if not answered
    is_correct = Column(Boolean, nullable=False, default=False)
    marks_obtained = Column(Float, default=0.0, nullable=False)
    answered_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    session = relationship("MockTestSession", back_populates="answers")
    question = relationship("MockTestQuestion", back_populates="answers")

    # Indexes
    __table_args__ = (
        Index('idx_answer_session_question', 'session_id', 'question_id'),
        {'extend_existing': True}
    )

    def __repr__(self):
        return f"<MockTestAnswer(id={self.id}, session_id={self.session_id}, is_correct={self.is_correct})>"

class MockTestAnalytics(Base):
    """
    Analytics and insights for mock tests using Gemini AI
    """
    __tablename__ = "mock_test_analytics"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("mock_test_sessions.id"), nullable=False)
    ai_analysis = Column(JSON, nullable=True)  # Gemini AI analysis results
    strengths = Column(JSON, nullable=True)  # Areas of strength
    weaknesses = Column(JSON, nullable=True)  # Areas for improvement
    recommendations = Column(JSON, nullable=True)  # AI recommendations
    performance_summary = Column(Text, nullable=True)  # AI-generated summary
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    session = relationship("MockTestSession")

    def __repr__(self):
        return f"<MockTestAnalytics(id={self.id}, session_id={self.session_id})>"
