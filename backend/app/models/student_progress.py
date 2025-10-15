from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class StudentSubjectProgress(Base):
    """
    Track student progress in each subject based on mock test performance
    """
    __tablename__ = "student_subject_progress"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    
    # Progress metrics
    total_tests_taken = Column(Integer, default=0, nullable=False)
    total_marks_earned = Column(Float, default=0.0, nullable=False)
    total_marks_possible = Column(Float, default=0.0, nullable=False)
    current_progress_percentage = Column(Float, default=0.0, nullable=False)
    
    # Performance tracking
    average_score = Column(Float, default=0.0, nullable=False)
    best_score = Column(Float, default=0.0, nullable=False)
    last_test_date = Column(DateTime(timezone=True), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    student = relationship("User")
    subject = relationship("Subject", back_populates="student_progress")

    # Indexes
    __table_args__ = (
        Index('idx_student_subject', 'student_id', 'subject_id'),
        {'extend_existing': True}
    )

    def __repr__(self):
        return f"<StudentSubjectProgress(student_id={self.student_id}, subject_id={self.subject_id}, progress={self.current_progress_percentage}%)>"
