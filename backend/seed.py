#!/usr/bin/env python3
"""
Seed script to populate the database with initial data for the assessment system.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.models.assessment import (
    Subject, Course, Question, CourseLevel, QuestionDifficulty
)
from app.models.user import User
from app.core.security import get_password_hash

def create_subjects(db):
    """Create sample subjects."""
    subjects_data = [
        {
            "name": "Computer Networks",
            "description": "Network protocols, OSI model, TCP/IP, and network devices"
        },
        {
            "name": "Operating Systems",
            "description": "OS concepts, processes, memory management, and scheduling"
        },
        {
            "name": "Object-Oriented Programming",
            "description": "OOP principles, inheritance, polymorphism, and design patterns"
        },
        {
            "name": "Database Management Systems",
            "description": "SQL, normalization, ACID properties, and database design"
        },
        {
            "name": "Coding",
            "description": "Programming problems and algorithms"
        }
    ]
    
    subjects = []
    for subject_data in subjects_data:
        subject = Subject(**subject_data)
        db.add(subject)
        subjects.append(subject)
    
    db.commit()
    print(f"Created {len(subjects)} subjects")
    return subjects

def create_courses(db, subjects):
    """Create sample courses for each subject and level."""
    courses_data = [
        # Computer Networks
        {"subject_name": "Computer Networks", "title": "Network Fundamentals", "level": CourseLevel.BEGINNER, "description": "Basic networking concepts and OSI model"},
        {"subject_name": "Computer Networks", "title": "TCP/IP Protocol Suite", "level": CourseLevel.INTERMEDIATE, "description": "TCP/IP protocols and addressing"},
        {"subject_name": "Computer Networks", "title": "Network Security", "level": CourseLevel.ADVANCED, "description": "Network security protocols and practices"},
        
        # Operating Systems
        {"subject_name": "Operating Systems", "title": "OS Basics", "level": CourseLevel.BEGINNER, "description": "Basic operating system concepts"},
        {"subject_name": "Operating Systems", "title": "Process Management", "level": CourseLevel.INTERMEDIATE, "description": "Process scheduling and synchronization"},
        {"subject_name": "Operating Systems", "title": "Memory Management", "level": CourseLevel.ADVANCED, "description": "Memory allocation and virtual memory"},
        
        # Object-Oriented Programming
        {"subject_name": "Object-Oriented Programming", "title": "OOP Fundamentals", "level": CourseLevel.BEGINNER, "description": "Basic OOP concepts and principles"},
        {"subject_name": "Object-Oriented Programming", "title": "Advanced OOP", "level": CourseLevel.INTERMEDIATE, "description": "Inheritance, polymorphism, and design patterns"},
        {"subject_name": "Object-Oriented Programming", "title": "OOP Design Patterns", "level": CourseLevel.ADVANCED, "description": "Design patterns and best practices"},
        
        # Database Management Systems
        {"subject_name": "Database Management Systems", "title": "SQL Basics", "level": CourseLevel.BEGINNER, "description": "Basic SQL queries and database concepts"},
        {"subject_name": "Database Management Systems", "title": "Database Design", "level": CourseLevel.INTERMEDIATE, "description": "Normalization and database design"},
        {"subject_name": "Database Management Systems", "title": "Advanced Database Concepts", "level": CourseLevel.ADVANCED, "description": "Advanced database topics and optimization"},
        
        # Coding
        {"subject_name": "Coding", "title": "Programming Fundamentals", "level": CourseLevel.BEGINNER, "description": "Basic programming concepts and algorithms"},
        {"subject_name": "Coding", "title": "Data Structures", "level": CourseLevel.INTERMEDIATE, "description": "Data structures and algorithms"},
        {"subject_name": "Coding", "title": "Advanced Algorithms", "level": CourseLevel.ADVANCED, "description": "Advanced algorithms and problem solving"}
    ]
    
    subject_map = {subject.name: subject for subject in subjects}
    courses = []
    
    for course_data in courses_data:
        subject = subject_map[course_data["subject_name"]]
        course = Course(
            subject_id=subject.id,
            title=course_data["title"],
            level=course_data["level"],
            description=course_data["description"]
        )
        db.add(course)
        courses.append(course)
    
    db.commit()
    print(f"Created {len(courses)} courses")
    return courses

def create_questions(db, subjects):
    """Create sample questions for each subject with varying difficulty levels."""
    questions_data = [
        # Computer Networks - 12 questions
        {
            "subject_name": "Computer Networks",
            "text": "Which layer of the OSI model is responsible for error detection?",
            "options": ["Data Link Layer", "Network Layer", "Transport Layer", "Physical Layer"],
            "correct_index": 0,
            "difficulty": QuestionDifficulty.EASY
        },
        {
            "subject_name": "Computer Networks",
            "text": "Full form of IP in networking?",
            "options": ["Internet Packet", "Internal Protocol", "Internet Protocol", "Interface Program"],
            "correct_index": 2,
            "difficulty": QuestionDifficulty.EASY
        },
        {
            "subject_name": "Computer Networks",
            "text": "Which protocol is used to retrieve emails?",
            "options": ["POP3", "SMTP", "FTP", "HTTP"],
            "correct_index": 0,
            "difficulty": QuestionDifficulty.EASY
        },
        {
            "subject_name": "Computer Networks",
            "text": "In TCP/IP, which layer corresponds to OSI's Transport layer?",
            "options": ["Internet Layer", "Host-to-Host Layer", "Application Layer", "Data Link Layer"],
            "correct_index": 1,
            "difficulty": QuestionDifficulty.MEDIUM
        },
        {
            "subject_name": "Computer Networks",
            "text": "Which device connects multiple networks together?",
            "options": ["Switch", "Hub", "Router", "Repeater"],
            "correct_index": 2,
            "difficulty": QuestionDifficulty.EASY
        },
        {
            "subject_name": "Computer Networks",
            "text": "Switch vs Hub: Which statement is correct?",
            "options": ["Switch broadcasts to all devices, hub is selective", "Hub is faster than switch", "Switch is smarter, sends data to specific device", "Both are same"],
            "correct_index": 2,
            "difficulty": QuestionDifficulty.MEDIUM
        },
        {
            "subject_name": "Computer Networks",
            "text": "Maximum length of IPv4 address in bits?",
            "options": ["16", "32", "64", "128"],
            "correct_index": 1,
            "difficulty": QuestionDifficulty.EASY
        },
        {
            "subject_name": "Computer Networks",
            "text": "Which is connection-oriented?",
            "options": ["TCP", "UDP", "Both", "None"],
            "correct_index": 0,
            "difficulty": QuestionDifficulty.EASY
        },
        {
            "subject_name": "Computer Networks",
            "text": "Default port number of HTTP?",
            "options": ["25", "80", "110", "443"],
            "correct_index": 1,
            "difficulty": QuestionDifficulty.EASY
        },
        {
            "subject_name": "Computer Networks",
            "text": "CSMA/CD is used in?",
            "options": ["Wi-Fi", "Ethernet", "Bluetooth", "WAN"],
            "correct_index": 1,
            "difficulty": QuestionDifficulty.MEDIUM
        },
        {
            "subject_name": "Computer Networks",
            "text": "Which protocol is used for secure transfer over the web?",
            "options": ["FTP", "HTTP", "HTTPS", "POP3"],
            "correct_index": 2,
            "difficulty": QuestionDifficulty.EASY
        },
        {
            "subject_name": "Computer Networks",
            "text": "Which topology has the highest fault tolerance?",
            "options": ["Bus", "Ring", "Star", "Mesh"],
            "correct_index": 3,
            "difficulty": QuestionDifficulty.MEDIUM
        },
        
        # Operating Systems - 12 questions
        {
            "subject_name": "Operating Systems",
            "text": "Which of the following is not an OS?",
            "options": ["Windows", "Linux", "Oracle", "MacOS"],
            "correct_index": 2,
            "difficulty": QuestionDifficulty.EASY
        },
        {
            "subject_name": "Operating Systems",
            "text": "CPU scheduling algorithm used in real-time systems?",
            "options": ["Round Robin", "FCFS", "Priority", "Earliest Deadline First"],
            "correct_index": 3,
            "difficulty": QuestionDifficulty.MEDIUM
        },
        {
            "subject_name": "Operating Systems",
            "text": "Process vs Thread: which is true?",
            "options": ["Process is lighter than thread", "Thread is lighter than process", "Both equal", "None"],
            "correct_index": 1,
            "difficulty": QuestionDifficulty.EASY
        },
        {
            "subject_name": "Operating Systems",
            "text": "What is thrashing?",
            "options": ["Excessive swapping between memory and disk", "CPU overheating", "Deadlock", "Disk crash"],
            "correct_index": 0,
            "difficulty": QuestionDifficulty.MEDIUM
        },
        {
            "subject_name": "Operating Systems",
            "text": "Page replacement algorithm that replaces the oldest page?",
            "options": ["LRU", "FIFO", "Optimal", "MRU"],
            "correct_index": 1,
            "difficulty": QuestionDifficulty.MEDIUM
        },
        {
            "subject_name": "Operating Systems",
            "text": "Deadlock occurs when…",
            "options": ["Multiple processes compete for resources indefinitely", "CPU utilization is 100%", "Memory is fragmented", "Disk scheduling fails"],
            "correct_index": 0,
            "difficulty": QuestionDifficulty.MEDIUM
        },
        {
            "subject_name": "Operating Systems",
            "text": "Which is not a disk scheduling algorithm?",
            "options": ["FCFS", "SSTF", "SCAN", "FIFO"],
            "correct_index": 3,
            "difficulty": QuestionDifficulty.MEDIUM
        },
        {
            "subject_name": "Operating Systems",
            "text": "Context switching means…",
            "options": ["Switching between threads of same process", "Switching between processes", "Saving state of process & loading another", "All of the above"],
            "correct_index": 3,
            "difficulty": QuestionDifficulty.MEDIUM
        },
        {
            "subject_name": "Operating Systems",
            "text": "Linux command to show processes?",
            "options": ["ps", "showproc", "procstat", "listp"],
            "correct_index": 0,
            "difficulty": QuestionDifficulty.EASY
        },
        {
            "subject_name": "Operating Systems",
            "text": "Semaphore is used for…",
            "options": ["File management", "Process synchronization", "CPU scheduling", "Deadlock removal"],
            "correct_index": 1,
            "difficulty": QuestionDifficulty.MEDIUM
        },
        {
            "subject_name": "Operating Systems",
            "text": "Which divides memory into equal-size blocks?",
            "options": ["Paging", "Segmentation", "Virtual Memory", "Fragmentation"],
            "correct_index": 0,
            "difficulty": QuestionDifficulty.MEDIUM
        },
        {
            "subject_name": "Operating Systems",
            "text": "Virtual memory is implemented using…",
            "options": ["RAM", "Cache", "Disk storage", "Registers"],
            "correct_index": 2,
            "difficulty": QuestionDifficulty.MEDIUM
        },
        
        # Object-Oriented Programming - 12 questions
        {
            "subject_name": "Object-Oriented Programming",
            "text": "Which is not a principle of OOP?",
            "options": ["Encapsulation", "Inheritance", "Compilation", "Polymorphism"],
            "correct_index": 2,
            "difficulty": QuestionDifficulty.EASY
        },
        {
            "subject_name": "Object-Oriented Programming",
            "text": "Encapsulation means…",
            "options": ["Wrapping data & methods together", "Hiding implementation details", "Both a & b", "None"],
            "correct_index": 2,
            "difficulty": QuestionDifficulty.EASY
        },
        {
            "subject_name": "Object-Oriented Programming",
            "text": "Overloading vs Overriding: correct statement?",
            "options": ["Overloading: compile-time, Overriding: runtime", "Overloading: runtime, Overriding: compile-time", "Both runtime", "Both compile-time"],
            "correct_index": 0,
            "difficulty": QuestionDifficulty.MEDIUM
        },
        {
            "subject_name": "Object-Oriented Programming",
            "text": "Which inheritance is not supported in Java?",
            "options": ["Single", "Multiple via classes", "Multilevel", "Hierarchical"],
            "correct_index": 1,
            "difficulty": QuestionDifficulty.MEDIUM
        },
        {
            "subject_name": "Object-Oriented Programming",
            "text": "Abstract class means…",
            "options": ["Cannot be instantiated", "Contains only concrete methods", "Is faster than normal class", "Can't be inherited"],
            "correct_index": 0,
            "difficulty": QuestionDifficulty.MEDIUM
        },
        {
            "subject_name": "Object-Oriented Programming",
            "text": "Can we instantiate an interface?",
            "options": ["Yes", "No", "Only once", "Only in Python"],
            "correct_index": 1,
            "difficulty": QuestionDifficulty.EASY
        },
        {
            "subject_name": "Object-Oriented Programming",
            "text": "Example of runtime polymorphism?",
            "options": ["Constructor Overloading", "Operator Overloading", "Method Overriding", "None"],
            "correct_index": 2,
            "difficulty": QuestionDifficulty.MEDIUM
        },
        {
            "subject_name": "Object-Oriented Programming",
            "text": "Keyword used for inheritance in C++?",
            "options": ["implement", "extends", "inherits", ": (colon)"],
            "correct_index": 3,
            "difficulty": QuestionDifficulty.MEDIUM
        },
        {
            "subject_name": "Object-Oriented Programming",
            "text": "Difference between constructor and destructor?",
            "options": ["Constructor initializes, destructor destroys", "Both initialize", "Both destroy", "None"],
            "correct_index": 0,
            "difficulty": QuestionDifficulty.EASY
        },
        {
            "subject_name": "Object-Oriented Programming",
            "text": "Using same function name with different parameters is called…",
            "options": ["Overloading", "Overriding", "Inheritance", "Polymorphism only"],
            "correct_index": 0,
            "difficulty": QuestionDifficulty.EASY
        },
        {
            "subject_name": "Object-Oriented Programming",
            "text": "Which principle is achieved by access modifiers?",
            "options": ["Encapsulation", "Inheritance", "Abstraction", "Polymorphism"],
            "correct_index": 0,
            "difficulty": QuestionDifficulty.EASY
        },
        {
            "subject_name": "Object-Oriented Programming",
            "text": "Multiple inheritance in C++ is implemented using…",
            "options": ["Interfaces", "Virtual base classes", "Abstract classes", "Polymorphism"],
            "correct_index": 1,
            "difficulty": QuestionDifficulty.HARD
        },
        
        # Database Management Systems - 12 questions
        {
            "subject_name": "Database Management Systems",
            "text": "SQL stands for…",
            "options": ["Structured Question Language", "Simple Query Language", "Structured Query Language", "Standard Quick Language"],
            "correct_index": 2,
            "difficulty": QuestionDifficulty.EASY
        },
        {
            "subject_name": "Database Management Systems",
            "text": "Which normal form removes transitive dependency?",
            "options": ["1NF", "2NF", "3NF", "BCNF"],
            "correct_index": 2,
            "difficulty": QuestionDifficulty.MEDIUM
        },
        {
            "subject_name": "Database Management Systems",
            "text": "Difference between primary key and unique key?",
            "options": ["Primary allows NULL, unique doesn't", "Unique allows NULL, primary doesn't", "Both allow NULL", "Both disallow NULL"],
            "correct_index": 1,
            "difficulty": QuestionDifficulty.MEDIUM
        },
        {
            "subject_name": "Database Management Systems",
            "text": "Which is a DML command?",
            "options": ["SELECT", "CREATE", "DROP", "ALTER"],
            "correct_index": 0,
            "difficulty": QuestionDifficulty.EASY
        },
        {
            "subject_name": "Database Management Systems",
            "text": "ACID stands for…",
            "options": ["Atomicity, Consistency, Isolation, Durability", "Access, Control, Isolation, Durability", "Atomic, Consistent, Index, Data", "Automatic, Concurrent, Indexed, Durable"],
            "correct_index": 0,
            "difficulty": QuestionDifficulty.MEDIUM
        },
        {
            "subject_name": "Database Management Systems",
            "text": "Which join returns only matching rows?",
            "options": ["Inner Join", "Left Join", "Right Join", "Full Join"],
            "correct_index": 0,
            "difficulty": QuestionDifficulty.MEDIUM
        },
        {
            "subject_name": "Database Management Systems",
            "text": "A foreign key is…",
            "options": ["Unique identifier in table", "Reference to primary key in another table", "Duplicate key", "None"],
            "correct_index": 1,
            "difficulty": QuestionDifficulty.EASY
        },
        {
            "subject_name": "Database Management Systems",
            "text": "Difference between clustered and non-clustered index?",
            "options": ["Clustered: sorts data rows, Non-clustered: uses pointer", "Non-clustered is faster always", "Both same", "None"],
            "correct_index": 0,
            "difficulty": QuestionDifficulty.HARD
        },
        {
            "subject_name": "Database Management Systems",
            "text": "Which command removes all rows but keeps structure?",
            "options": ["DROP", "DELETE", "TRUNCATE", "ERASE"],
            "correct_index": 2,
            "difficulty": QuestionDifficulty.MEDIUM
        },
        {
            "subject_name": "Database Management Systems",
            "text": "Denormalization means…",
            "options": ["Breaking normal forms for performance", "Removing duplicates", "Adding constraints", "None"],
            "correct_index": 0,
            "difficulty": QuestionDifficulty.MEDIUM
        },
        {
            "subject_name": "Database Management Systems",
            "text": "DELETE vs TRUNCATE: which is true?",
            "options": ["DELETE can't use WHERE, TRUNCATE can", "TRUNCATE can't use WHERE, DELETE can", "Both same", "TRUNCATE is slower"],
            "correct_index": 1,
            "difficulty": QuestionDifficulty.MEDIUM
        },
        {
            "subject_name": "Database Management Systems",
            "text": "In ER diagrams, diamond represents…",
            "options": ["Entity", "Relationship", "Attribute", "Key"],
            "correct_index": 1,
            "difficulty": QuestionDifficulty.EASY
        },
        
        # Coding - 2 questions (open-ended, but we'll create multiple choice versions)
        {
            "subject_name": "Coding",
            "text": "What is the time complexity of checking if a string is palindrome?",
            "options": ["O(1)", "O(n)", "O(n²)", "O(log n)"],
            "correct_index": 1,
            "difficulty": QuestionDifficulty.MEDIUM
        },
        {
            "subject_name": "Coding",
            "text": "What is the time complexity of binary search?",
            "options": ["O(1)", "O(n)", "O(log n)", "O(n²)"],
            "correct_index": 2,
            "difficulty": QuestionDifficulty.EASY
        }
    ]
    
    subject_map = {subject.name: subject for subject in subjects}
    questions = []
    
    for question_data in questions_data:
        subject = subject_map[question_data["subject_name"]]
        question = Question(
            subject_id=subject.id,
            text=question_data["text"],
            options=question_data["options"],
            correct_index=question_data["correct_index"],
            difficulty=question_data["difficulty"]
        )
        db.add(question)
        questions.append(question)
    
    db.commit()
    print(f"Created {len(questions)} questions")
    return questions

def create_test_user(db):
    """Create a test user for development."""
    test_user = User(
        username="student",
        email="student@example.com",
        full_name="Test Student",
        hashed_password=get_password_hash("password"),
        is_active=True,
        is_verified=True
    )
    db.add(test_user)
    db.commit()
    print("Created test user: student/password")
    return test_user

def main():
    """Main seeding function."""
    db = SessionLocal()
    
    try:
        print("Starting database seeding...")
        
        # Create subjects
        subjects = create_subjects(db)
        
        # Create courses
        courses = create_courses(db, subjects)
        
        # Create questions
        questions = create_questions(db, subjects)
        
        # Create test user
        test_user = create_test_user(db)
        
        print("Database seeding completed successfully!")
        print(f"Created {len(subjects)} subjects, {len(courses)} courses, {len(questions)} questions, and 1 test user")
        
    except Exception as e:
        print(f"Error during seeding: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    main()
