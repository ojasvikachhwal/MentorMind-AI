#!/usr/bin/env python3
"""
Seed script to populate the database with the new courses from CSV data.
This script adds 100 courses across different subjects and levels.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.models.assessment import Subject, Course, CourseLevel

def seed_new_courses():
    """Seed the database with the new courses from CSV data."""
    db = SessionLocal()
    
    try:
        # First, ensure we have the required subjects
        subjects_data = [
            {"name": "Computer Networks", "description": "Network protocols, OSI model, TCP/IP, and network devices"},
            {"name": "OOPS", "description": "Object-Oriented Programming principles, inheritance, polymorphism, and design patterns"},
            {"name": "Operating System", "description": "OS concepts, processes, memory management, and scheduling"},
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
        
        # Define all the courses from the CSV data
        courses_data = [
            # Computer Networks (1-5)
            {"subject_name": "Computer Networks", "level": CourseLevel.BEGINNER, "title": "Introduction to Computer Networks", "url": "https://www.youtube.com/watch?v=qiQR5rTSshw"},
            {"subject_name": "Computer Networks", "level": CourseLevel.BEGINNER, "title": "Computer Networking Fundamentals", "url": "https://www.coursera.org/learn/computer-networking"},
            {"subject_name": "Computer Networks", "level": CourseLevel.ADVANCED, "title": "Advanced Computer Networks", "url": "https://infyspringboard.onwingspan.com/en/app/course/advanced-cn"},
            {"subject_name": "Computer Networks", "level": CourseLevel.BEGINNER, "title": "Data Communication Basics", "url": "https://www.geeksforgeeks.org/data-communication-basics"},
            {"subject_name": "Computer Networks", "level": CourseLevel.INTERMEDIATE, "title": "Network Security Essentials", "url": "https://www.coursera.org/learn/network-security"},
            
            # OOPS (6-10)
            {"subject_name": "OOPS", "level": CourseLevel.BEGINNER, "title": "Object-Oriented Programming in C++", "url": "https://www.youtube.com/watch?v=vLnPwxZdW4Y"},
            {"subject_name": "OOPS", "level": CourseLevel.INTERMEDIATE, "title": "Java OOP Masterclass", "url": "https://www.coursera.org/learn/java-oop"},
            {"subject_name": "OOPS", "level": CourseLevel.ADVANCED, "title": "Design Patterns in OOP", "url": "https://infyspringboard.onwingspan.com/en/app/course/oop-design-patterns"},
            {"subject_name": "OOPS", "level": CourseLevel.BEGINNER, "title": "OOP with Python", "url": "https://www.geeksforgeeks.org/python-oops-concepts"},
            {"subject_name": "OOPS", "level": CourseLevel.ADVANCED, "title": "OOP Advanced Principles", "url": "https://www.coursera.org/specializations/object-oriented-design"},
            
            # Operating System (11-15)
            {"subject_name": "Operating System", "level": CourseLevel.BEGINNER, "title": "Operating System Basics", "url": "https://www.youtube.com/watch?v=26QPDBe-NB8A"},
            {"subject_name": "Operating System", "level": CourseLevel.BEGINNER, "title": "Operating Systems and You", "url": "https://www.coursera.org/learn/os-power-user"},
            {"subject_name": "Operating System", "level": CourseLevel.ADVANCED, "title": "Advanced Operating System Concepts", "url": "https://infyspringboard.onwingspan.com/en/app/course/advanced-os"},
            {"subject_name": "Operating System", "level": CourseLevel.INTERMEDIATE, "title": "Concurrency in OS", "url": "https://www.youtube.com/watch?v=qOVAbKKSH10"},
            {"subject_name": "Operating System", "level": CourseLevel.INTERMEDIATE, "title": "Memory Management Techniques", "url": "https://www.geeksforgeeks.org/memory-management-in-os"},
            
            # DBMS (16-20)
            {"subject_name": "DBMS", "level": CourseLevel.BEGINNER, "title": "Introduction to DBMS", "url": "https://www.youtube.com/watch?v=HXV3zeQKqGY"},
            {"subject_name": "DBMS", "level": CourseLevel.BEGINNER, "title": "SQL for Beginners", "url": "https://www.coursera.org/learn/sql-for-data-science"},
            {"subject_name": "DBMS", "level": CourseLevel.INTERMEDIATE, "title": "Database Design & Modeling", "url": "https://infyspringboard.onwingspan.com/en/app/course/dbms-design"},
            {"subject_name": "DBMS", "level": CourseLevel.ADVANCED, "title": "Advanced Database Systems", "url": "https://www.coursera.org/learn/advanced-database-systems"},
            {"subject_name": "DBMS", "level": CourseLevel.INTERMEDIATE, "title": "Normalization in DBMS", "url": "https://www.geeksforgeeks.org/normalization-in-dbms"},
            
            # Coding (21-25)
            {"subject_name": "Coding", "level": CourseLevel.BEGINNER, "title": "DSA Coding Practice", "url": "https://www.youtube.com/watch?v=8hly31xKli0"},
            {"subject_name": "Coding", "level": CourseLevel.BEGINNER, "title": "LeetCode Easy Problems", "url": "https://leetcode.com/problemset/all/?difficulty=EASY"},
            {"subject_name": "Coding", "level": CourseLevel.INTERMEDIATE, "title": "Intermediate Coding in Java", "url": "https://www.coursera.org/specializations/java-programming"},
            {"subject_name": "Coding", "level": CourseLevel.ADVANCED, "title": "Competitive Programming Guide", "url": "https://infyspringboard.onwingspan.com/en/app/course/competitive-programming"},
            {"subject_name": "Coding", "level": CourseLevel.ADVANCED, "title": "Dynamic Programming Mastery", "url": "https://www.youtube.com/watch?v=oBt53YbR9Kk"},
            
            # Additional Computer Networks courses (26-30)
            {"subject_name": "Computer Networks", "level": CourseLevel.INTERMEDIATE, "title": "TCP/IP Protocol Suite", "url": "https://www.youtube.com/watch?v=qiQR5rTSshw"},
            {"subject_name": "Computer Networks", "level": CourseLevel.BEGINNER, "title": "Network Topology Basics", "url": "https://www.coursera.org/learn/computer-networking"},
            {"subject_name": "Computer Networks", "level": CourseLevel.ADVANCED, "title": "Wireless Network Security", "url": "https://infyspringboard.onwingspan.com/en/app/course/advanced-cn"},
            {"subject_name": "Computer Networks", "level": CourseLevel.INTERMEDIATE, "title": "Network Performance Optimization", "url": "https://www.geeksforgeeks.org/data-communication-basics"},
            {"subject_name": "Computer Networks", "level": CourseLevel.BEGINNER, "title": "Internet Protocol Fundamentals", "url": "https://www.coursera.org/learn/network-security"},
            
            # Additional OOPS courses (31-35)
            {"subject_name": "OOPS", "level": CourseLevel.INTERMEDIATE, "title": "C++ Advanced OOP Concepts", "url": "https://www.youtube.com/watch?v=vLnPwxZdW4Y"},
            {"subject_name": "OOPS", "level": CourseLevel.BEGINNER, "title": "OOP with JavaScript", "url": "https://www.coursera.org/learn/java-oop"},
            {"subject_name": "OOPS", "level": CourseLevel.ADVANCED, "title": "SOLID Principles in OOP", "url": "https://infyspringboard.onwingspan.com/en/app/course/oop-design-patterns"},
            {"subject_name": "OOPS", "level": CourseLevel.INTERMEDIATE, "title": "OOP with C#", "url": "https://www.geeksforgeeks.org/python-oops-concepts"},
            {"subject_name": "OOPS", "level": CourseLevel.BEGINNER, "title": "OOP Fundamentals", "url": "https://www.coursera.org/specializations/object-oriented-design"},
            
            # Additional Operating System courses (36-40)
            {"subject_name": "Operating System", "level": CourseLevel.INTERMEDIATE, "title": "Process Scheduling Algorithms", "url": "https://www.youtube.com/watch?v=26QPDBe-NB8A"},
            {"subject_name": "Operating System", "level": CourseLevel.ADVANCED, "title": "Virtual Memory Management", "url": "https://www.coursera.org/learn/os-power-user"},
            {"subject_name": "Operating System", "level": CourseLevel.BEGINNER, "title": "File System Management", "url": "https://infyspringboard.onwingspan.com/en/app/course/advanced-os"},
            {"subject_name": "Operating System", "level": CourseLevel.ADVANCED, "title": "Distributed Operating Systems", "url": "https://www.youtube.com/watch?v=qOVAbKKSH10"},
            {"subject_name": "Operating System", "level": CourseLevel.INTERMEDIATE, "title": "Device Driver Programming", "url": "https://www.geeksforgeeks.org/memory-management-in-os"},
            
            # Additional DBMS courses (41-45)
            {"subject_name": "DBMS", "level": CourseLevel.ADVANCED, "title": "NoSQL Database Systems", "url": "https://www.youtube.com/watch?v=HXV3zeQKqGY"},
            {"subject_name": "DBMS", "level": CourseLevel.INTERMEDIATE, "title": "Database Indexing Strategies", "url": "https://www.coursera.org/learn/sql-for-data-science"},
            {"subject_name": "DBMS", "level": CourseLevel.BEGINNER, "title": "Relational Database Design", "url": "https://infyspringboard.onwingspan.com/en/app/course/dbms-design"},
            {"subject_name": "DBMS", "level": CourseLevel.ADVANCED, "title": "Database Performance Tuning", "url": "https://www.coursera.org/learn/advanced-database-systems"},
            {"subject_name": "DBMS", "level": CourseLevel.INTERMEDIATE, "title": "Transaction Management", "url": "https://www.geeksforgeeks.org/normalization-in-dbms"},
            
            # Additional Coding courses (46-50)
            {"subject_name": "Coding", "level": CourseLevel.INTERMEDIATE, "title": "Algorithm Design Techniques", "url": "https://www.youtube.com/watch?v=8hly31xKli0"},
            {"subject_name": "Coding", "level": CourseLevel.ADVANCED, "title": "LeetCode Hard Problems", "url": "https://leetcode.com/problemset/all/?difficulty=HARD"},
            {"subject_name": "Coding", "level": CourseLevel.BEGINNER, "title": "Python Programming Basics", "url": "https://www.coursera.org/specializations/java-programming"},
            {"subject_name": "Coding", "level": CourseLevel.ADVANCED, "title": "System Design Interview Prep", "url": "https://infyspringboard.onwingspan.com/en/app/course/competitive-programming"},
            {"subject_name": "Coding", "level": CourseLevel.INTERMEDIATE, "title": "Graph Algorithms", "url": "https://www.youtube.com/watch?v=oBt53YbR9Kk"},
            
            # More Computer Networks courses (51-60)
            {"subject_name": "Computer Networks", "level": CourseLevel.ADVANCED, "title": "Network Virtualization", "url": "https://www.youtube.com/watch?v=qiQR5rTSshw"},
            {"subject_name": "Computer Networks", "level": CourseLevel.INTERMEDIATE, "title": "Network Monitoring Tools", "url": "https://www.coursera.org/learn/computer-networking"},
            {"subject_name": "Computer Networks", "level": CourseLevel.BEGINNER, "title": "Network Troubleshooting", "url": "https://infyspringboard.onwingspan.com/en/app/course/advanced-cn"},
            {"subject_name": "Computer Networks", "level": CourseLevel.ADVANCED, "title": "Software Defined Networking", "url": "https://www.geeksforgeeks.org/data-communication-basics"},
            {"subject_name": "Computer Networks", "level": CourseLevel.INTERMEDIATE, "title": "Network Quality of Service", "url": "https://www.coursera.org/learn/network-security"},
            {"subject_name": "Computer Networks", "level": CourseLevel.BEGINNER, "title": "Network Hardware Components", "url": "https://www.youtube.com/watch?v=qiQR5rTSshw"},
            {"subject_name": "Computer Networks", "level": CourseLevel.ADVANCED, "title": "Network Forensics", "url": "https://www.coursera.org/learn/computer-networking"},
            {"subject_name": "Computer Networks", "level": CourseLevel.INTERMEDIATE, "title": "Network Load Balancing", "url": "https://infyspringboard.onwingspan.com/en/app/course/advanced-cn"},
            {"subject_name": "Computer Networks", "level": CourseLevel.BEGINNER, "title": "Network Configuration Basics", "url": "https://www.geeksforgeeks.org/data-communication-basics"},
            {"subject_name": "Computer Networks", "level": CourseLevel.ADVANCED, "title": "Network Automation", "url": "https://www.coursera.org/learn/network-security"},
            
            # More OOPS courses (61-70)
            {"subject_name": "OOPS", "level": CourseLevel.ADVANCED, "title": "Advanced Java OOP", "url": "https://www.youtube.com/watch?v=vLnPwxZdW4Y"},
            {"subject_name": "OOPS", "level": CourseLevel.INTERMEDIATE, "title": "OOP with Ruby", "url": "https://www.coursera.org/learn/java-oop"},
            {"subject_name": "OOPS", "level": CourseLevel.BEGINNER, "title": "OOP with PHP", "url": "https://infyspringboard.onwingspan.com/en/app/course/oop-design-patterns"},
            {"subject_name": "OOPS", "level": CourseLevel.ADVANCED, "title": "Advanced Design Patterns", "url": "https://www.geeksforgeeks.org/python-oops-concepts"},
            {"subject_name": "OOPS", "level": CourseLevel.INTERMEDIATE, "title": "OOP with Swift", "url": "https://www.coursera.org/specializations/object-oriented-design"},
            {"subject_name": "OOPS", "level": CourseLevel.BEGINNER, "title": "OOP with Kotlin", "url": "https://www.youtube.com/watch?v=vLnPwxZdW4Y"},
            {"subject_name": "OOPS", "level": CourseLevel.ADVANCED, "title": "Enterprise OOP Patterns", "url": "https://www.coursera.org/learn/java-oop"},
            {"subject_name": "OOPS", "level": CourseLevel.INTERMEDIATE, "title": "OOP with TypeScript", "url": "https://infyspringboard.onwingspan.com/en/app/course/oop-design-patterns"},
            {"subject_name": "OOPS", "level": CourseLevel.BEGINNER, "title": "OOP with Go", "url": "https://www.geeksforgeeks.org/python-oops-concepts"},
            {"subject_name": "OOPS", "level": CourseLevel.ADVANCED, "title": "Microservices OOP Design", "url": "https://www.coursera.org/specializations/object-oriented-design"},
            
            # More Operating System courses (71-80)
            {"subject_name": "Operating System", "level": CourseLevel.ADVANCED, "title": "Real-time Operating Systems", "url": "https://www.youtube.com/watch?v=26QPDBe-NB8A"},
            {"subject_name": "Operating System", "level": CourseLevel.INTERMEDIATE, "title": "Embedded Systems OS", "url": "https://www.coursera.org/learn/os-power-user"},
            {"subject_name": "Operating System", "level": CourseLevel.BEGINNER, "title": "Linux System Administration", "url": "https://infyspringboard.onwingspan.com/en/app/course/advanced-os"},
            {"subject_name": "Operating System", "level": CourseLevel.ADVANCED, "title": "Kernel Programming", "url": "https://www.youtube.com/watch?v=qOVAbKKSH10"},
            {"subject_name": "Operating System", "level": CourseLevel.INTERMEDIATE, "title": "System Programming", "url": "https://www.geeksforgeeks.org/memory-management-in-os"},
            {"subject_name": "Operating System", "level": CourseLevel.BEGINNER, "title": "Windows System Administration", "url": "https://www.youtube.com/watch?v=26QPDBe-NB8A"},
            {"subject_name": "Operating System", "level": CourseLevel.ADVANCED, "title": "Container Technologies", "url": "https://www.coursera.org/learn/os-power-user"},
            {"subject_name": "Operating System", "level": CourseLevel.INTERMEDIATE, "title": "System Security", "url": "https://infyspringboard.onwingspan.com/en/app/course/advanced-os"},
            {"subject_name": "Operating System", "level": CourseLevel.BEGINNER, "title": "Process Management", "url": "https://www.youtube.com/watch?v=qOVAbKKSH10"},
            {"subject_name": "Operating System", "level": CourseLevel.ADVANCED, "title": "Performance Optimization", "url": "https://www.geeksforgeeks.org/memory-management-in-os"},
            
            # More DBMS courses (81-90)
            {"subject_name": "DBMS", "level": CourseLevel.INTERMEDIATE, "title": "Database Backup & Recovery", "url": "https://www.youtube.com/watch?v=HXV3zeQKqGY"},
            {"subject_name": "DBMS", "level": CourseLevel.ADVANCED, "title": "Distributed Database Systems", "url": "https://www.coursera.org/learn/sql-for-data-science"},
            {"subject_name": "DBMS", "level": CourseLevel.BEGINNER, "title": "Database Security", "url": "https://infyspringboard.onwingspan.com/en/app/course/dbms-design"},
            {"subject_name": "DBMS", "level": CourseLevel.INTERMEDIATE, "title": "Data Warehousing", "url": "https://www.coursera.org/learn/advanced-database-systems"},
            {"subject_name": "DBMS", "level": CourseLevel.ADVANCED, "title": "Big Data Technologies", "url": "https://www.geeksforgeeks.org/normalization-in-dbms"},
            {"subject_name": "DBMS", "level": CourseLevel.BEGINNER, "title": "Database Administration", "url": "https://www.youtube.com/watch?v=HXV3zeQKqGY"},
            {"subject_name": "DBMS", "level": CourseLevel.INTERMEDIATE, "title": "Data Mining", "url": "https://www.coursera.org/learn/sql-for-data-science"},
            {"subject_name": "DBMS", "level": CourseLevel.ADVANCED, "title": "Graph Databases", "url": "https://infyspringboard.onwingspan.com/en/app/course/dbms-design"},
            {"subject_name": "DBMS", "level": CourseLevel.BEGINNER, "title": "Database Optimization", "url": "https://www.coursera.org/learn/advanced-database-systems"},
            {"subject_name": "DBMS", "level": CourseLevel.INTERMEDIATE, "title": "Cloud Database Services", "url": "https://www.geeksforgeeks.org/normalization-in-dbms"},
            
            # More Coding courses (91-100)
            {"subject_name": "Coding", "level": CourseLevel.BEGINNER, "title": "LeetCode Medium Problems", "url": "https://leetcode.com/problemset/all/?difficulty=MEDIUM"},
            {"subject_name": "Coding", "level": CourseLevel.ADVANCED, "title": "Advanced Data Structures", "url": "https://www.youtube.com/watch?v=8hly31xKli0"},
            {"subject_name": "Coding", "level": CourseLevel.INTERMEDIATE, "title": "Algorithm Complexity Analysis", "url": "https://www.coursera.org/specializations/java-programming"},
            {"subject_name": "Coding", "level": CourseLevel.BEGINNER, "title": "C++ Programming Basics", "url": "https://infyspringboard.onwingspan.com/en/app/course/competitive-programming"},
            {"subject_name": "Coding", "level": CourseLevel.ADVANCED, "title": "Machine Learning Algorithms", "url": "https://www.youtube.com/watch?v=oBt53YbR9Kk"},
            {"subject_name": "Coding", "level": CourseLevel.INTERMEDIATE, "title": "String Algorithms", "url": "https://leetcode.com/problemset/all/?difficulty=EASY"},
            {"subject_name": "Coding", "level": CourseLevel.BEGINNER, "title": "Array Manipulation", "url": "https://www.youtube.com/watch?v=8hly31xKli0"},
            {"subject_name": "Coding", "level": CourseLevel.ADVANCED, "title": "Advanced Graph Theory", "url": "https://www.coursera.org/specializations/java-programming"},
            {"subject_name": "Coding", "level": CourseLevel.INTERMEDIATE, "title": "Tree Data Structures", "url": "https://infyspringboard.onwingspan.com/en/app/course/competitive-programming"},
            {"subject_name": "Coding", "level": CourseLevel.BEGINNER, "title": "Basic Sorting Algorithms", "url": "https://www.youtube.com/watch?v=oBt53YbR9Kk"}
        ]
        
        # Create courses
        created_count = 0
        updated_count = 0
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
                    updated_count += 1
                    print(f"Updated course URL: {existing_course.title}")
        
        db.commit()
        print(f"\nSeeding completed! Created {created_count} new courses and updated {updated_count} existing courses.")
        
        # Display summary
        print("\nCourse Summary by Subject:")
        for subject_name, subject in subjects.items():
            courses = db.query(Course).filter(Course.subject_id == subject.id).all()
            print(f"\n{subject_name} ({len(courses)} courses):")
            beginner_count = len([c for c in courses if c.level == CourseLevel.BEGINNER])
            intermediate_count = len([c for c in courses if c.level == CourseLevel.INTERMEDIATE])
            advanced_count = len([c for c in courses if c.level == CourseLevel.ADVANCED])
            print(f"  🟢 Beginner: {beginner_count} courses")
            print(f"  🟡 Intermediate: {intermediate_count} courses")
            print(f"  🔴 Advanced: {advanced_count} courses")
        
        total_courses = db.query(Course).count()
        print(f"\nTotal courses in database: {total_courses}")
        
    except Exception as e:
        print(f"Error seeding courses: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    print("Starting new course seeding...")
    seed_new_courses()
    print("New course seeding completed!")
