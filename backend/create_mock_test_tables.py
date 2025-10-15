#!/usr/bin/env python3
"""
Database migration script to create Mock Test tables
Run this script to add the mock test functionality to your existing database
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from app.core.database import Base, engine
from app.models.mock_test import (
    MockTest, MockTestQuestion, MockTestSession, 
    MockTestAnswer, MockTestAnalytics
)
from app.core.config import settings

def create_mock_test_tables():
    """
    Create all mock test related tables
    """
    try:
        print("🚀 Creating Mock Test tables...")
        
        # Create all tables
        Base.metadata.create_all(bind=engine, tables=[
            MockTest.__table__,
            MockTestQuestion.__table__,
            MockTestSession.__table__,
            MockTestAnswer.__table__,
            MockTestAnalytics.__table__
        ])
        
        print("✅ Mock Test tables created successfully!")
        
        # Create indexes for better performance
        with engine.connect() as conn:
            # Index for session lookups
            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_mock_test_session_student_test 
                ON mock_test_sessions (student_id, mock_test_id)
            """))
            
            # Index for answer lookups
            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_mock_test_answer_session_question 
                ON mock_test_answers (session_id, question_id)
            """))
            
            # Index for test filtering
            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_mock_test_subject_status 
                ON mock_tests (subject_id, status)
            """))
            
            # conn.commit()  # Not needed for SQLite with autocommit
        
        print("✅ Indexes created successfully!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating tables: {str(e)}")
        return False

def seed_sample_data():
    """
    Seed the database with sample mock test data
    """
    try:
        print("🌱 Seeding sample mock test data...")
        
        from sqlalchemy.orm import sessionmaker
        from app.models.mock_test import MockTest, MockTestQuestion, MockTestStatus
        from app.models.assessment import Subject
        
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        # Check if we already have mock tests
        existing_tests = db.query(MockTest).count()
        if existing_tests > 0:
            print("ℹ️  Mock tests already exist, skipping seed data")
            db.close()
            return True
        
        # Get or create subjects
        subjects = db.query(Subject).all()
        if not subjects:
            # Create sample subjects if they don't exist
            sample_subjects = [
                Subject(name="Data Structures & Algorithms", description="Core computer science concepts"),
                Subject(name="Object-Oriented Programming", description="OOP principles and design patterns"),
                Subject(name="Database Management", description="SQL and database design"),
                Subject(name="Operating Systems", description="OS concepts and system programming")
            ]
            for subject in sample_subjects:
                db.add(subject)
            db.commit()
            subjects = db.query(Subject).all()
        
        # Create sample mock tests
        sample_tests = [
            {
                "title": "Data Structures Fundamentals",
                "description": "Test your knowledge of basic data structures and algorithms",
                "subject_id": subjects[0].id if subjects else 1,
                "time_limit_minutes": 30,
                "is_public": True,
                "questions": [
                    {
                        "question_text": "What is the time complexity of accessing an element in an array?",
                        "option_a": "O(1)",
                        "option_b": "O(n)",
                        "option_c": "O(log n)",
                        "option_d": "O(n²)",
                        "correct_option": "A",
                        "marks": 2,
                        "explanation": "Array access is constant time O(1) because we can directly access any element using its index.",
                        "difficulty": "easy"
                    },
                    {
                        "question_text": "Which data structure follows LIFO principle?",
                        "option_a": "Queue",
                        "option_b": "Stack",
                        "option_c": "Tree",
                        "option_d": "Graph",
                        "correct_option": "B",
                        "marks": 2,
                        "explanation": "Stack follows Last In, First Out (LIFO) principle.",
                        "difficulty": "easy"
                    },
                    {
                        "question_text": "What is the time complexity of binary search?",
                        "option_a": "O(1)",
                        "option_b": "O(n)",
                        "option_c": "O(log n)",
                        "option_d": "O(n²)",
                        "correct_option": "C",
                        "marks": 3,
                        "explanation": "Binary search has O(log n) time complexity as it eliminates half of the search space in each iteration.",
                        "difficulty": "medium"
                    }
                ]
            },
            {
                "title": "OOP Concepts Quiz",
                "description": "Test your understanding of object-oriented programming principles",
                "subject_id": subjects[1].id if len(subjects) > 1 else 2,
                "time_limit_minutes": 25,
                "is_public": True,
                "questions": [
                    {
                        "question_text": "What is encapsulation?",
                        "option_a": "Hiding data",
                        "option_b": "Inheriting from parent",
                        "option_c": "Multiple forms",
                        "option_d": "Creating objects",
                        "correct_option": "A",
                        "marks": 2,
                        "explanation": "Encapsulation is the bundling of data and methods that work on that data within one unit, and hiding internal details.",
                        "difficulty": "easy"
                    },
                    {
                        "question_text": "What is the difference between overloading and overriding?",
                        "option_a": "Same method, different parameters",
                        "option_b": "Same method, different classes",
                        "option_c": "Different methods, same name",
                        "option_d": "Same method, same parameters",
                        "correct_option": "A",
                        "marks": 3,
                        "explanation": "Overloading is having multiple methods with the same name but different parameters. Overriding is redefining a method in a subclass.",
                        "difficulty": "medium"
                    }
                ]
            }
        ]
        
        # Create mock tests and questions
        for test_data in sample_tests:
            questions_data = test_data.pop('questions')
            
            # Create mock test
            mock_test = MockTest(
                title=test_data['title'],
                description=test_data['description'],
                subject_id=test_data['subject_id'],
                instructor_id=1,  # Assuming user ID 1 is an instructor
                time_limit_minutes=test_data['time_limit_minutes'],
                is_public=test_data['is_public'],
                status=MockTestStatus.ACTIVE
            )
            
            db.add(mock_test)
            db.flush()  # Get the ID
            
            # Calculate total marks
            total_marks = 0
            
            # Add questions
            for question_data in questions_data:
                question = MockTestQuestion(
                    mock_test_id=mock_test.id,
                    question_text=question_data['question_text'],
                    option_a=question_data['option_a'],
                    option_b=question_data['option_b'],
                    option_c=question_data['option_c'],
                    option_d=question_data['option_d'],
                    correct_option=question_data['correct_option'],
                    marks=question_data['marks'],
                    explanation=question_data['explanation'],
                    difficulty=question_data['difficulty']
                )
                db.add(question)
                total_marks += question_data['marks']
            
            # Update total marks
            mock_test.total_marks = total_marks
        
        db.commit()
        print("✅ Sample mock test data seeded successfully!")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ Error seeding data: {str(e)}")
        return False

def main():
    """
    Main function to run the migration
    """
    print("🎯 Mock Test Database Migration")
    print("=" * 50)
    
    # Create tables
    if not create_mock_test_tables():
        print("❌ Migration failed!")
        return False
    
    # Seed sample data
    if not seed_sample_data():
        print("⚠️  Tables created but seeding failed!")
        return False
    
    print("\n🎉 Migration completed successfully!")
    print("\n📋 What was created:")
    print("   • mock_tests table")
    print("   • mock_test_questions table") 
    print("   • mock_test_sessions table")
    print("   • mock_test_answers table")
    print("   • mock_test_analytics table")
    print("   • Performance indexes")
    print("   • Sample test data")
    
    print("\n🚀 You can now use the Mock Test functionality!")
    print("   • Instructors can create tests at /instructor/mock-tests")
    print("   • Students can take tests at /student/mock-tests")
    print("   • AI analysis is available after test completion")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
