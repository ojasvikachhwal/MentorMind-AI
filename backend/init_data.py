#!/usr/bin/env python3
"""
Initialize database with sample data
"""

from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine
from app.models import Quiz, Question
from datetime import datetime

def init_db():
    db = SessionLocal()
    try:
        # Check if quizzes already exist
        existing_quizzes = db.query(Quiz).count()
        if existing_quizzes > 0:
            print("Database already has quiz data. Skipping initialization.")
            return
        
        # Create sample quizzes
        quizzes_data = [
            {
                "title": "Basic Algorithms",
                "topic": "algorithms",
                "difficulty_level": "easy",
                "description": "Fundamental algorithms and their time complexities",
                "is_active": True
            },
            {
                "title": "Data Structures",
                "topic": "data_structures",
                "difficulty_level": "medium",
                "description": "Common data structures and their implementations",
                "is_active": True
            },
            {
                "title": "Database Concepts",
                "topic": "database",
                "difficulty_level": "hard",
                "description": "Database design, SQL, and normalization",
                "is_active": True
            }
        ]
        
        for quiz_data in quizzes_data:
            quiz = Quiz(**quiz_data)
            db.add(quiz)
        
        db.commit()
        
        # Get the created quizzes
        basic_algorithms = db.query(Quiz).filter(Quiz.title == "Basic Algorithms").first()
        data_structures = db.query(Quiz).filter(Quiz.title == "Data Structures").first()
        database_concepts = db.query(Quiz).filter(Quiz.title == "Database Concepts").first()
        
        # Create questions for Basic Algorithms
        algorithm_questions = [
            {
                "quiz_id": basic_algorithms.id,
                "question_text": "What is the time complexity of binary search?",
                "options": ["O(1)", "O(log n)", "O(n)", "O(n²)"],
                "correct_answer": 1,
                "question_type": "multiple_choice",
                "explanation": "Binary search divides the search space in half with each iteration, resulting in logarithmic time complexity.",
                "difficulty_score": 3.0
            },
            {
                "quiz_id": basic_algorithms.id,
                "question_text": "Which sorting algorithm has the best average-case time complexity?",
                "options": ["Bubble Sort", "Quick Sort", "Selection Sort", "Insertion Sort"],
                "correct_answer": 1,
                "question_type": "multiple_choice",
                "explanation": "Quick Sort has an average-case time complexity of O(n log n), which is optimal for comparison-based sorting.",
                "difficulty_score": 4.0
            },
            {
                "quiz_id": basic_algorithms.id,
                "question_text": "What is the space complexity of merge sort?",
                "options": ["O(1)", "O(log n)", "O(n)", "O(n²)"],
                "correct_answer": 2,
                "question_type": "multiple_choice",
                "explanation": "Merge sort requires additional space proportional to the input size for the merge operation.",
                "difficulty_score": 4.5
            }
        ]
        
        # Create questions for Data Structures
        ds_questions = [
            {
                "quiz_id": data_structures.id,
                "question_text": "Which data structure is best for implementing a stack?",
                "options": ["Array", "Linked List", "Both A and B", "Tree"],
                "correct_answer": 2,
                "question_type": "multiple_choice",
                "explanation": "Both arrays and linked lists can efficiently implement stack operations (push/pop) in O(1) time.",
                "difficulty_score": 3.5
            },
            {
                "quiz_id": data_structures.id,
                "question_text": "What is the time complexity of inserting an element at the beginning of a linked list?",
                "options": ["O(1)", "O(log n)", "O(n)", "O(n²)"],
                "correct_answer": 0,
                "question_type": "multiple_choice",
                "explanation": "Inserting at the beginning of a linked list only requires updating the head pointer, which is O(1).",
                "difficulty_score": 2.5
            },
            {
                "quiz_id": data_structures.id,
                "question_text": "Which data structure is used for breadth-first search?",
                "options": ["Stack", "Queue", "Heap", "Tree"],
                "correct_answer": 1,
                "question_type": "multiple_choice",
                "explanation": "BFS uses a queue to process nodes level by level, ensuring all nodes at the current level are visited before moving to the next level.",
                "difficulty_score": 3.0
            }
        ]
        
        # Create questions for Database Concepts
        db_questions = [
            {
                "quiz_id": database_concepts.id,
                "question_text": "What does ACID stand for in database transactions?",
                "options": ["Atomicity, Consistency, Isolation, Durability", "Availability, Consistency, Integrity, Durability", "Atomicity, Consistency, Integrity, Durability", "Availability, Consistency, Isolation, Durability"],
                "correct_answer": 0,
                "question_type": "multiple_choice",
                "explanation": "ACID properties ensure reliable database transactions: Atomicity (all or nothing), Consistency (valid state), Isolation (concurrent access), Durability (permanent).",
                "difficulty_score": 5.0
            },
            {
                "quiz_id": database_concepts.id,
                "question_text": "What is the purpose of database normalization?",
                "options": ["To make queries faster", "To reduce data redundancy", "To increase storage space", "To simplify database design"],
                "correct_answer": 1,
                "question_type": "multiple_choice",
                "explanation": "Normalization reduces data redundancy and improves data integrity by organizing data into well-structured tables.",
                "difficulty_score": 4.0
            },
            {
                "quiz_id": database_concepts.id,
                "question_text": "Which SQL command is used to modify existing data?",
                "options": ["INSERT", "UPDATE", "MODIFY", "CHANGE"],
                "correct_answer": 1,
                "question_type": "multiple_choice",
                "explanation": "The UPDATE command is used to modify existing records in a database table.",
                "difficulty_score": 2.0
            }
        ]
        
        # Add all questions
        all_questions = algorithm_questions + ds_questions + db_questions
        
        for question_data in all_questions:
            question = Question(**question_data)
            db.add(question)
        
        db.commit()
        print("✅ Database initialized with sample quiz data!")
        print(f"   - Created {len(quizzes_data)} quizzes")
        print(f"   - Created {len(all_questions)} questions")
        
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_db()
