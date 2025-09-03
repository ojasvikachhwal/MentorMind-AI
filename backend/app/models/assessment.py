from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Enum, Index, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum

class CourseLevel(str, enum.Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

class QuestionDifficulty(str, enum.Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"

class AssessmentStatus(str, enum.Enum):
    ACTIVE = "active"
    SUBMITTED = "submitted"

class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    courses = relationship("Course", back_populates="subject")
    questions = relationship("AssessmentQuestion", back_populates="subject")

    def __repr__(self):
        return f"<Subject(id={self.id}, name='{self.name}')>"

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    title = Column(String(200), nullable=False)
    level = Column(Enum(CourseLevel), nullable=False)
    description = Column(Text, nullable=True)
    url = Column(String(500), nullable=True)  # Course URL for external resources
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    subject = relationship("Subject", back_populates="courses")

    # Indexes
    __table_args__ = (
        Index('idx_course_subject_level', 'subject_id', 'level'),
        {'extend_existing': True}
    )

    def __repr__(self):
        return f"<Course(id={self.id}, title='{self.title}', level='{self.level}')>"

class AssessmentQuestion(Base):
    __tablename__ = "assessment_questions"

    id = Column(Integer, primary_key=True, index=True)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    text = Column(Text, nullable=False)
    options = Column(JSON, nullable=False)  # List of strings
    correct_index = Column(Integer, nullable=False)
    difficulty = Column(Enum(QuestionDifficulty), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    subject = relationship("Subject", back_populates="questions")
    assessment_answers = relationship("AssessmentAnswer", back_populates="assessment_question")

    # Indexes
    __table_args__ = (
        Index('idx_question_subject_difficulty', 'subject_id', 'difficulty'),
        {'extend_existing': True}
    )

    def __repr__(self):
        return f"<AssessmentQuestion(id={self.id}, subject_id={self.subject_id}, difficulty='{self.difficulty}')>"

class AssessmentSession(Base):
    __tablename__ = "assessment_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(Enum(AssessmentStatus), default=AssessmentStatus.ACTIVE, nullable=False)
    selected_subject_ids = Column(JSON, nullable=False)  # List of subject IDs
    num_questions_per_subject = Column(Integer, default=10, nullable=False)

    # Relationships
    user = relationship("User", back_populates="assessment_sessions")
    answers = relationship("AssessmentAnswer", back_populates="session")

    def __repr__(self):
        return f"<AssessmentSession(id={self.id}, user_id={self.user_id}, status='{self.status}')>"

class AssessmentAnswer(Base):
    __tablename__ = "assessment_answers"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("assessment_sessions.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("assessment_questions.id"), nullable=False)
    selected_index = Column(Integer, nullable=False)
    is_correct = Column(Boolean, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    session = relationship("AssessmentSession", back_populates="answers")
    assessment_question = relationship("AssessmentQuestion", back_populates="assessment_answers")

    # Indexes
    __table_args__ = (
        Index('idx_answer_session_question', 'session_id', 'question_id'),
        {'extend_existing': True}
    )

    def __repr__(self):
        return f"<AssessmentAnswer(id={self.id}, session_id={self.session_id}, is_correct={self.is_correct})>"
