#!/usr/bin/env python3
"""
Script to seed initial subjects for the automated mock test system
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine
from app.models.assessment import Subject
from app.core.database import Base

def create_subjects():
    """Create initial subjects"""
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Check if subjects already exist
        existing_subjects = db.query(Subject).count()
        if existing_subjects > 0:
            print(f"Subjects already exist ({existing_subjects} found). Skipping...")
            return
        
        # Define subjects
        subjects_data = [
            {
                "name": "Data Structures & Algorithms",
                "description": "Fundamental data structures, algorithms, and problem-solving techniques"
            },
            {
                "name": "Object-Oriented Programming",
                "description": "OOP concepts, design patterns, and software architecture principles"
            },
            {
                "name": "Database Management",
                "description": "SQL, database design, normalization, and query optimization"
            },
            {
                "name": "Operating Systems",
                "description": "Process management, memory management, file systems, and concurrency"
            },
            {
                "name": "Computer Networks",
                "description": "Network protocols, TCP/IP, routing, and network security"
            },
            {
                "name": "Software Engineering",
                "description": "Software development lifecycle, testing, and project management"
            },
            {
                "name": "Web Development",
                "description": "Frontend and backend web technologies, frameworks, and best practices"
            },
            {
                "name": "Machine Learning",
                "description": "AI/ML algorithms, data science, and predictive modeling"
            }
        ]
        
        # Create subjects
        for subject_data in subjects_data:
            subject = Subject(
                name=subject_data["name"],
                description=subject_data["description"],
                is_active=True
            )
            db.add(subject)
        
        db.commit()
        print(f"Successfully created {len(subjects_data)} subjects")
        
        # Display created subjects
        subjects = db.query(Subject).all()
        print("\nCreated subjects:")
        for subject in subjects:
            print(f"- {subject.name}: {subject.description}")
            
    except Exception as e:
        print(f"Error creating subjects: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_subjects()
