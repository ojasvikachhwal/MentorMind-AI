#!/usr/bin/env python3
"""
Demonstration script for the AI-powered course recommendation system.
This script shows how the recommendation engine analyzes student performance
and generates personalized course recommendations.
"""

import json
from datetime import datetime
from app.services.recommendation_engine import RecommendationEngine
from app.models.assessment import (
    Subject, Course, Question, AssessmentSession, AssessmentAnswer,
    CourseLevel, QuestionDifficulty, AssessmentStatus
)
from app.models.user import User

def create_sample_data():
    """Create sample data for demonstration purposes."""
    
    # Create sample subjects
    subjects = [
        Subject(id=1, name="Mathematics", description="Mathematical concepts and problem solving"),
        Subject(id=2, name="Physics", description="Physical sciences and natural laws"),
        Subject(id=3, name="Computer Science", description="Programming and computational thinking")
    ]
    
    # Create sample courses
    courses = [
        # Mathematics courses
        Course(id=1, subject_id=1, title="Basic Arithmetic", level=CourseLevel.BEGINNER, description="Fundamental math operations"),
        Course(id=2, subject_id=1, title="Intro to Algebra", level=CourseLevel.BEGINNER, description="Basic algebraic concepts"),
        Course(id=3, subject_id=1, title="Algebra Problem Solving", level=CourseLevel.INTERMEDIATE, description="Intermediate algebra problems"),
        Course(id=4, subject_id=1, title="Advanced Calculus", level=CourseLevel.ADVANCED, description="Complex mathematical analysis"),
        
        # Physics courses
        Course(id=5, subject_id=2, title="Basic Mechanics", level=CourseLevel.BEGINNER, description="Introduction to physics concepts"),
        Course(id=6, subject_id=2, title="Wave Physics", level=CourseLevel.INTERMEDIATE, description="Wave phenomena and properties"),
        Course(id=7, subject_id=2, title="Quantum Mechanics", level=CourseLevel.ADVANCED, description="Advanced quantum theory"),
        
        # Computer Science courses
        Course(id=8, subject_id=3, title="Programming Basics", level=CourseLevel.BEGINNER, description="Introduction to programming"),
        Course(id=9, subject_id=3, title="Data Structures", level=CourseLevel.INTERMEDIATE, description="Advanced programming concepts"),
        Course(id=10, subject_id=3, title="Machine Learning", level=CourseLevel.ADVANCED, description="AI and ML fundamentals")
    ]
    
    # Create sample user
    user = User(id=1, username="demo_student", email="demo@example.com", role="student")
    
    # Create sample assessment session
    session = AssessmentSession(
        id=1,
        user_id=1,
        selected_subject_ids=[1, 2, 3],  # Math, Physics, CS
        num_questions_per_subject=10,
        status=AssessmentStatus.SUBMITTED,
        created_at=datetime.now()
    )
    
    # Create sample questions and answers
    questions = []
    answers = []
    
    # Mathematics questions (mostly incorrect - weak performance)
    for i in range(10):
        question = Question(
            id=i+1,
            subject_id=1,
            text=f"Math question {i+1}",
            options=["A", "B", "C", "D"],
            correct_index=0,
            difficulty=QuestionDifficulty.EASY if i < 4 else QuestionDifficulty.MEDIUM if i < 7 else QuestionDifficulty.HARD
        )
        questions.append(question)
        
        # Student gets mostly wrong answers in math
        is_correct = i < 3  # Only 3 out of 10 correct (30%)
        answer = AssessmentAnswer(
            id=i+1,
            session_id=1,
            question_id=i+1,
            selected_index=1 if not is_correct else 0,
            is_correct=is_correct
        )
        answers.append(answer)
    
    # Physics questions (mixed performance)
    for i in range(10):
        question = Question(
            id=i+11,
            subject_id=2,
            text=f"Physics question {i+1}",
            options=["A", "B", "C", "D"],
            correct_index=0,
            difficulty=QuestionDifficulty.EASY if i < 4 else QuestionDifficulty.MEDIUM if i < 7 else QuestionDifficulty.HARD
        )
        questions.append(question)
        
        # Student gets mixed results in physics
        is_correct = i < 6  # 6 out of 10 correct (60%)
        answer = AssessmentAnswer(
            id=i+11,
            session_id=1,
            question_id=i+11,
            selected_index=1 if not is_correct else 0,
            is_correct=is_correct
        )
        answers.append(answer)
    
    # Computer Science questions (mostly correct - strong performance)
    for i in range(10):
        question = Question(
            id=i+21,
            subject_id=3,
            text=f"CS question {i+1}",
            options=["A", "B", "C", "D"],
            correct_index=0,
            difficulty=QuestionDifficulty.EASY if i < 4 else QuestionDifficulty.MEDIUM if i < 7 else QuestionDifficulty.HARD
        )
        questions.append(question)
        
        # Student gets mostly correct answers in CS
        is_correct = i < 8  # 8 out of 10 correct (80%)
        answer = AssessmentAnswer(
            id=i+21,
            session_id=1,
            question_id=i+21,
            selected_index=1 if not is_correct else 0,
            is_correct=is_correct
        )
        answers.append(answer)
    
    return {
        "subjects": subjects,
        "courses": courses,
        "user": user,
        "session": session,
        "questions": questions,
        "answers": answers
    }

def demonstrate_recommendation_engine():
    """Demonstrate how the recommendation engine works."""
    
    print("🤖 AI-Powered Course Recommendation System Demo")
    print("=" * 60)
    
    # Create sample data
    print("\n📊 Creating sample assessment data...")
    sample_data = create_sample_data()
    
    print(f"   - {len(sample_data['subjects'])} subjects")
    print(f"   - {len(sample_data['courses'])} courses")
    print(f"   - {len(sample_data['questions'])} questions")
    print(f"   - {len(sample_data['answers'])} answers")
    
    # Create mock database session
    class MockDB:
        def query(self, model):
            return MockQuery(model, sample_data)
    
    class MockQuery:
        def __init__(self, model, data):
            self.model = model
            self.data = data
        
        def filter(self, *args, **kwargs):
            return self
        
        def join(self, *args, **kwargs):
            return self
        
        def order_by(self, *args, **kwargs):
            return self
        
        def limit(self, limit):
            return self
        
        def first(self):
            if self.model == User:
                return sample_data['user']
            elif self.model == AssessmentSession:
                return sample_data['session']
            elif self.model == Subject:
                # Return first subject for demonstration
                return sample_data['subjects'][0]
            return None
        
        def all(self):
            if self.model == Subject:
                return sample_data['subjects']
            elif self.model == Course:
                # Return courses for the first subject
                return [c for c in sample_data['courses'] if c.subject_id == 1]
            elif self.model == AssessmentAnswer:
                # Return answers for the first subject (math)
                return [a for a in sample_data['answers'] if a.id <= 10]
            return []
    
    mock_db = MockDB()
    
    # Initialize recommendation engine
    print("\n🔧 Initializing recommendation engine...")
    engine = RecommendationEngine()
    
    # Get recommendations
    print("\n🎯 Generating course recommendations...")
    recommendations = engine.get_course_recommendations(mock_db, 1, 3)
    
    # Display results
    print("\n📋 Recommendation Results:")
    print("-" * 40)
    
    if recommendations and "recommendations" in recommendations:
        for i, rec in enumerate(recommendations["recommendations"], 1):
            print(f"\nSubject {i}: {rec['subject']}")
            print(f"  Performance Level: {rec['performance_level']}")
            print(f"  Score: {rec['percent_correct']}%")
            print(f"  Identified Weaknesses: {rec['weakness']}")
            print(f"  Recommended Courses:")
            
            for j, course in enumerate(rec['recommended_courses'], 1):
                print(f"    {j}. {course['title']} ({course['level']})")
                print(f"       Description: {course['description']}")
    else:
        print("No recommendations generated.")
    
    # Show the logic behind recommendations
    print("\n🧠 How the Recommendation Engine Works:")
    print("-" * 40)
    print("1. Analyzes test results by subject and difficulty level")
    print("2. Calculates performance metrics (percent correct, weighted scores)")
    print("3. Maps performance to course levels:")
    print("   - ≤40% correct → Beginner courses")
    print("   - 41-70% correct → Intermediate courses")
    print("   - >70% correct → Advanced courses")
    print("4. Identifies specific weaknesses based on incorrect answers")
    print("5. Recommends appropriate courses with fallback options")
    
    # Show sample performance analysis
    print("\n📈 Sample Performance Analysis:")
    print("-" * 40)
    print("Mathematics: 30% correct → WEAK → Beginner courses recommended")
    print("Physics: 60% correct → MODERATE → Intermediate courses recommended")
    print("Computer Science: 80% correct → STRONG → Advanced courses recommended")
    
    print("\n✅ Demo completed successfully!")
    print("\n💡 To test with real data, run the FastAPI server and use the API endpoints:")
    print("   GET /courses/recommendations/{student_id}")
    print("   GET /courses/recommendations/me")
    print("   GET /courses/recommendations/ml/{student_id}")

if __name__ == "__main__":
    try:
        demonstrate_recommendation_engine()
    except Exception as e:
        print(f"❌ Error during demonstration: {e}")
        print("Make sure you're running this from the backend directory with proper imports.")
