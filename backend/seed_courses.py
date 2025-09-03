#!/usr/bin/env python3
"""
Seed script to populate the database with the specific courses requested by the user.
This script adds the exact courses with URLs as specified in the requirements.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.models.assessment import Subject, Course, CourseLevel

def seed_courses():
    """Seed the database with the specific courses requested by the user."""
    db = SessionLocal()
    
    try:
        # First, ensure we have the required subjects
        subjects_data = [
            {"name": "Operating Systems", "description": "OS concepts, processes, memory management, and scheduling"},
            {"name": "Computer Networks", "description": "Network protocols, OSI model, TCP/IP, and network devices"},
            {"name": "OOPs", "description": "Object-Oriented Programming principles, inheritance, polymorphism, and design patterns"},
            {"name": "DBMS", "description": "Database Management Systems, SQL, normalization, and database design"},
            {"name": "Coding", "description": "Programming problems, algorithms, and data structures"}
        ]
        
        # Create or get subjects
        subjects = {}
        for subject_data in subjects_data:
            subject = db.query(Subject).filter(Subject.name == subject_data["name"]).first()
            if not subject:
                subject = Subject(**subject_data)
                db.add(subject)
                db.commit()
                db.refresh(subject)
                print(f"Created subject: {subject.name}")
            else:
                print(f"Subject already exists: {subject.name}")
            subjects[subject.name] = subject
        
        # Define the exact courses as requested by the user
        courses_data = [
            # Operating Systems
            {
                "subject_name": "Operating Systems",
                "level": CourseLevel.BEGINNER,
                "title": "OS Fundamentals (Power User)",
                "url": "https://www.coursera.org/learn/os-power-user"
            },
            {
                "subject_name": "Operating Systems",
                "level": CourseLevel.INTERMEDIATE,
                "title": "Open Source Operating Systems",
                "url": "https://www.coursera.org/learn/illinois-tech-introduction-to-open-source-operating-systems-bit"
            },
            {
                "subject_name": "Operating Systems",
                "level": CourseLevel.ADVANCED,
                "title": "Computer Architecture (Princeton)",
                "url": "https://www.coursera.org/learn/computer-architecture"
            },
            {
                "subject_name": "Operating Systems",
                "level": CourseLevel.ADVANCED,
                "title": "Advanced Operating Systems (Udacity)",
                "url": "https://www.udacity.com/course/federated-learning--ud189"
            },
            
            # Computer Networks
            {
                "subject_name": "Computer Networks",
                "level": CourseLevel.BEGINNER,
                "title": "Computer Networking Full Course (YouTube)",
                "url": "https://www.youtube.com/watch?v=xZ5KzG4g6KA"
            },
            {
                "subject_name": "Computer Networks",
                "level": CourseLevel.INTERMEDIATE,
                "title": "Operating Systems Foundations (Coursera – networking fundamentals)",
                "url": "https://www.coursera.org/courses?query=operating+systems"
            },
            {
                "subject_name": "Computer Networks",
                "level": CourseLevel.ADVANCED,
                "title": "Advanced OS Topics (Virtualization & Networks)",
                "url": "https://www.tangolearn.com/ultimate-guide-to-online-operating-system-courses/"
            },
            
            # OOPs
            {
                "subject_name": "OOPs",
                "level": CourseLevel.BEGINNER,
                "title": "Object-Oriented Programming in Java (Coursera)",
                "url": "https://www.coursera.org/learn/object-oriented-java"
            },
            {
                "subject_name": "OOPs",
                "level": CourseLevel.INTERMEDIATE,
                "title": "Object-Oriented Design (Coursera)",
                "url": "https://www.coursera.org/learn/object-oriented-design"
            },
            {
                "subject_name": "OOPs",
                "level": CourseLevel.ADVANCED,
                "title": "Design Patterns in OOP (YouTube playlist)",
                "url": "https://www.youtube.com/playlist?list=PLF206E906175C7E07"
            },
            
            # DBMS
            {
                "subject_name": "DBMS",
                "level": CourseLevel.BEGINNER,
                "title": "SQL for Data Science (Coursera)",
                "url": "https://www.coursera.org/learn/sql-for-data-science"
            },
            {
                "subject_name": "DBMS",
                "level": CourseLevel.INTERMEDIATE,
                "title": "Database Management Essentials (Coursera)",
                "url": "https://www.coursera.org/learn/database-management"
            },
            {
                "subject_name": "DBMS",
                "level": CourseLevel.ADVANCED,
                "title": "Advanced Database Systems (Udacity)",
                "url": "https://www.udacity.com/course/advanced-database-systems--ud150"
            },
            
            # Coding
            {
                "subject_name": "Coding",
                "level": CourseLevel.BEGINNER,
                "title": "Programming Foundations with Python (Coursera)",
                "url": "https://www.coursera.org/learn/python"
            },
            {
                "subject_name": "Coding",
                "level": CourseLevel.INTERMEDIATE,
                "title": "Data Structures and Algorithms (YouTube – Abdul Bari)",
                "url": "https://www.youtube.com/playlist?list=PLfqMhTWNBTe0b2nM6JHVCnAkhQRGiZMSJ"
            },
            {
                "subject_name": "Coding",
                "level": CourseLevel.ADVANCED,
                "title": "System Design Primer (YouTube – Gaurav Sen)",
                "url": "https://www.youtube.com/playlist?list=PLMCXHnjXnTnvo6alSjVkgxV-VH6EPyvoX"
            }
        ]
        
        # Create courses
        created_count = 0
        for course_data in courses_data:
            subject = subjects[course_data["subject_name"]]
            
            # Check if course already exists
            existing_course = db.query(Course).filter(
                Course.subject_id == subject.id,
                Course.title == course_data["title"]
            ).first()
            
            if not existing_course:
                course = Course(
                    subject_id=subject.id,
                    title=course_data["title"],
                    level=course_data["level"],
                    url=course_data["url"],
                    description=f"{course_data['level'].value.title()} level course in {course_data['subject_name']}"
                )
                db.add(course)
                created_count += 1
                print(f"Created course: {course.title} ({course.level.value})")
            else:
                # Update existing course with URL if it doesn't have one
                if not existing_course.url and course_data["url"]:
                    existing_course.url = course_data["url"]
                    print(f"Updated course URL: {existing_course.title}")
        
        db.commit()
        print(f"\nSeeding completed! Created {created_count} new courses.")
        
        # Display summary
        print("\nCourse Summary by Subject:")
        for subject_name, subject in subjects.items():
            courses = db.query(Course).filter(Course.subject_id == subject.id).all()
            print(f"\n{subject_name}:")
            for course in courses:
                level_emoji = "🟢" if course.level == CourseLevel.BEGINNER else "🟡" if course.level == CourseLevel.INTERMEDIATE else "🔴"
                print(f"  {level_emoji} {course.title} ({course.level.value})")
                if course.url:
                    print(f"     URL: {course.url}")
        
    except Exception as e:
        print(f"Error seeding courses: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    print("Starting course seeding...")
    seed_courses()
    print("Course seeding completed!")
