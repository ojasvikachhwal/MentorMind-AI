#!/usr/bin/env python3
"""
Script to seed courses from CSV data into the MentorMind database.
This script parses the provided CSV data and creates subjects and courses.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine
from app.models.assessment import Subject, Course, CourseLevel
from app.models import Base

# CSV data provided by user
csv_data = """ID,Title,Subject,Level,Source,URL
1,Introduction to Computer Networks,Computer Networks,Beginner,YouTube,https://www.youtube.com/watch?v=qiQR5rTSshw
2,Computer Networking Fundamentals,Computer Networks,Beginner,Coursera,https://www.coursera.org/learn/computer-networking
3,Advanced Computer Networks,Computer Networks,Advanced,Infosys Springboard,https://infyspringboard.onwingspan.com/en/app/course/advanced-cn
4,Data Communication Basics,Computer Networks,Beginner,Free Platform,https://www.geeksforgeeks.org/data-communication-basics
5,Network Security Essentials,Computer Networks,Intermediate,Coursera,https://www.coursera.org/learn/network-security
6,Object-Oriented Programming in C++,OOPS,Beginner,YouTube,https://www.youtube.com/watch?v=vLnPwxZdW4Y
7,Java OOP Masterclass,OOPS,Intermediate,Coursera,https://www.coursera.org/learn/java-oop
8,Design Patterns in OOP,OOPS,Advanced,Infosys Springboard,https://infyspringboard.onwingspan.com/en/app/course/oop-design-patterns
9,OOP with Python,OOPS,Beginner,Free Platform,https://www.geeksforgeeks.org/python-oops-concepts
10,OOP Advanced Principles,OOPS,Advanced,Coursera,https://www.coursera.org/specializations/object-oriented-design
11,Operating System Basics,Operating System,Beginner,YouTube,https://www.youtube.com/watch?v=26QPDBe-NB8A
12,Operating Systems and You,Operating System,Beginner,Coursera,https://www.coursera.org/learn/os-power-user
13,Advanced Operating System Concepts,Operating System,Advanced,Infosys Springboard,https://infyspringboard.onwingspan.com/en/app/course/advanced-os
14,Concurrency in OS,Operating System,Intermediate,YouTube,https://www.youtube.com/watch?v=qOVAbKKSH10
15,Memory Management Techniques,Operating System,Intermediate,Free Platform,https://www.geeksforgeeks.org/memory-management-in-os
16,Introduction to DBMS,DBMS,Beginner,YouTube,https://www.youtube.com/watch?v=HXV3zeQKqGY
17,SQL for Beginners,DBMS,Beginner,Coursera,https://www.coursera.org/learn/sql-for-data-science
18,Database Design & Modeling,DBMS,Intermediate,Infosys Springboard,https://infyspringboard.onwingspan.com/en/app/course/dbms-design
19,Advanced Database Systems,DBMS,Advanced,Coursera,https://www.coursera.org/learn/advanced-database-systems
20,Normalization in DBMS,DBMS,Intermediate,Free Platform,https://www.geeksforgeeks.org/normalization-in-dbms
21,DSA Coding Practice,Coding,Beginner,YouTube,https://www.youtube.com/watch?v=8hly31xKli0
22,LeetCode Easy Problems,Coding,Beginner,Free Platform,https://leetcode.com/problemset/all/?difficulty=EASY
23,Intermediate Coding in Java,Coding,Intermediate,Coursera,https://www.coursera.org/specializations/java-programming
24,Competitive Programming Guide,Coding,Advanced,Infosys Springboard,https://infyspringboard.onwingspan.com/en/app/course/competitive-programming
25,Dynamic Programming Mastery,Coding,Advanced,YouTube,https://www.youtube.com/watch?v=oBt53YbR9Kk
26,Data Structures Fundamentals,Data Structures,Beginner,YouTube,https://www.youtube.com/watch?v=RBSGKlAvoiM
27,Arrays and Linked Lists,Data Structures,Beginner,Coursera,https://www.coursera.org/learn/data-structures-optimizing-performance
28,Advanced Data Structures,Data Structures,Advanced,Infosys Springboard,https://infyspringboard.onwingspan.com/en/app/course/advanced-data-structures
29,Tree and Graph Algorithms,Data Structures,Intermediate,Free Platform,https://www.geeksforgeeks.org/tree-traversals-inorder-preorder-and-postorder
30,Hash Tables and Heaps,Data Structures,Intermediate,YouTube,https://www.youtube.com/watch?v=shs0KM3wKv8
31,Algorithm Design Techniques,Algorithms,Beginner,YouTube,https://www.youtube.com/watch?v=8hly31xKli0
32,Sorting and Searching,Algorithms,Beginner,Coursera,https://www.coursera.org/learn/algorithms-part1
33,Graph Algorithms,Algorithms,Intermediate,Infosys Springboard,https://infyspringboard.onwingspan.com/en/app/course/graph-algorithms
34,Dynamic Programming Basics,Algorithms,Intermediate,Free Platform,https://www.geeksforgeeks.org/dynamic-programming
35,Advanced Algorithm Analysis,Algorithms,Advanced,YouTube,https://www.youtube.com/watch?v=oBt53YbR9Kk
36,Software Engineering Principles,Software Engineering,Beginner,YouTube,https://www.youtube.com/watch?v=O753uuutqH8
37,Agile Development,Software Engineering,Intermediate,Coursera,https://www.coursera.org/learn/agile-development
38,Software Architecture Patterns,Software Engineering,Advanced,Infosys Springboard,https://infyspringboard.onwingspan.com/en/app/course/software-architecture
39,Testing and Quality Assurance,Software Engineering,Intermediate,Free Platform,https://www.geeksforgeeks.org/software-testing-basics
40,DevOps Fundamentals,Software Engineering,Advanced,YouTube,https://www.youtube.com/watch?v=9pZ2xmsSDdo
41,Web Development Basics,Web Development,Beginner,YouTube,https://www.youtube.com/watch?v=qz0aGYrrlhU
42,HTML and CSS Fundamentals,Web Development,Beginner,Coursera,https://www.coursera.org/learn/html-css-javascript-for-web-developers
43,JavaScript for Beginners,Web Development,Beginner,Free Platform,https://www.geeksforgeeks.org/javascript-tutorial
44,React Development,Web Development,Intermediate,YouTube,https://www.youtube.com/watch?v=DLX62G4lc44
45,Full Stack Development,Web Development,Advanced,Coursera,https://www.coursera.org/specializations/full-stack-react
46,Python Programming Basics,Python,Beginner,YouTube,https://www.youtube.com/watch?v=kqtD5dpn9C8
47,Python Data Science,Python,Intermediate,Coursera,https://www.coursera.org/specializations/python
48,Advanced Python Concepts,Python,Advanced,Infosys Springboard,https://infyspringboard.onwingspan.com/en/app/course/advanced-python
49,Python Web Frameworks,Python,Intermediate,Free Platform,https://www.geeksforgeeks.org/python-web-development
50,Machine Learning with Python,Python,Advanced,YouTube,https://www.youtube.com/watch?v=7eh4d6sabA0
51,Java Programming Fundamentals,Java,Beginner,YouTube,https://www.youtube.com/watch?v=eIrMbAQSU34
52,Java Spring Framework,Java,Intermediate,Coursera,https://www.coursera.org/learn/spring-framework
53,Advanced Java Concepts,Java,Advanced,Infosys Springboard,https://infyspringboard.onwingspan.com/en/app/course/advanced-java
54,Java Enterprise Development,Java,Intermediate,Free Platform,https://www.geeksforgeeks.org/java-enterprise-development
55,Microservices with Java,Java,Advanced,YouTube,https://www.youtube.com/watch?v=mPPhcUfOz5s
56,C++ Programming Basics,C++,Beginner,YouTube,https://www.youtube.com/watch?v=vLnPwxZdW4Y
57,C++ STL and Templates,C++,Intermediate,Coursera,https://www.coursera.org/learn/c-plus-plus-a
58,Advanced C++ Programming,C++,Advanced,Infosys Springboard,https://infyspringboard.onwingspan.com/en/app/course/advanced-cpp
59,Game Development with C++,C++,Intermediate,Free Platform,https://www.geeksforgeeks.org/cpp-game-development
60,System Programming in C++,C++,Advanced,YouTube,https://www.youtube.com/watch?v=8jLOx1hD3_o
61,JavaScript Fundamentals,JavaScript,Beginner,YouTube,https://www.youtube.com/watch?v=PkZNo7MFNFg
62,Node.js Development,JavaScript,Intermediate,Coursera,https://www.coursera.org/learn/server-side-nodejs
63,Advanced JavaScript Concepts,JavaScript,Advanced,Infosys Springboard,https://infyspringboard.onwingspan.com/en/app/course/advanced-javascript
64,Frontend Frameworks,JavaScript,Intermediate,Free Platform,https://www.geeksforgeeks.org/javascript-frameworks
65,Full Stack JavaScript,JavaScript,Advanced,YouTube,https://www.youtube.com/watch?v=7nafaH9SddU
66,Cloud Computing Basics,Cloud Computing,Beginner,YouTube,https://www.youtube.com/watch?v=M988_fsOSWo
67,AWS Fundamentals,Cloud Computing,Intermediate,Coursera,https://www.coursera.org/specializations/aws-fundamentals
68,Azure Cloud Services,Cloud Computing,Advanced,Infosys Springboard,https://infyspringboard.onwingspan.com/en/app/course/azure-cloud
69,Google Cloud Platform,Cloud Computing,Intermediate,Free Platform,https://www.geeksforgeeks.org/google-cloud-platform
70,Cloud Architecture Design,Cloud Computing,Advanced,YouTube,https://www.youtube.com/watch?v=Ia-UEYYR44s
71,Cybersecurity Fundamentals,Security,Beginner,YouTube,https://www.youtube.com/watch?v=inWWhr5tnEA
72,Network Security,Security,Intermediate,Coursera,https://www.coursera.org/learn/network-security
73,Ethical Hacking,Security,Advanced,Infosys Springboard,https://infyspringboard.onwingspan.com/en/app/course/ethical-hacking
74,Information Security,Security,Intermediate,Free Platform,https://www.geeksforgeeks.org/information-security
75,Penetration Testing,Security,Advanced,YouTube,https://www.youtube.com/watch?v=3Kq1MIfTWCE
76,Artificial Intelligence Basics,AI/ML,Beginner,YouTube,https://www.youtube.com/watch?v=JMUxmLyrhSk
77,Machine Learning Fundamentals,AI/ML,Intermediate,Coursera,https://www.coursera.org/learn/machine-learning
78,Deep Learning,AI/ML,Advanced,Infosys Springboard,https://infyspringboard.onwingspan.com/en/app/course/deep-learning
79,Neural Networks,AI/ML,Intermediate,Free Platform,https://www.geeksforgeeks.org/neural-networks
80,Computer Vision,AI/ML,Advanced,YouTube,https://www.youtube.com/watch?v=2hXG8v8p0KM
81,Data Science Fundamentals,Data Science,Beginner,YouTube,https://www.youtube.com/watch?v=ua-CiDNNj30
82,Statistics for Data Science,Data Science,Intermediate,Coursera,https://www.coursera.org/specializations/statistics
83,Big Data Analytics,Data Science,Advanced,Infosys Springboard,https://infyspringboard.onwingspan.com/en/app/course/big-data
84,Data Visualization,Data Science,Intermediate,Free Platform,https://www.geeksforgeeks.org/data-visualization
85,Predictive Analytics,Data Science,Advanced,YouTube,https://www.youtube.com/watch?v=7nafaH9SddU
86,Mobile App Development,Mobile Development,Beginner,YouTube,https://www.youtube.com/watch?v=09TeUXjzpKs
87,React Native,Mobile Development,Intermediate,Coursera,https://www.coursera.org/learn/react-native
88,Flutter Development,Mobile Development,Advanced,Infosys Springboard,https://infyspringboard.onwingspan.com/en/app/course/flutter
89,iOS Development,Mobile Development,Intermediate,Free Platform,https://www.geeksforgeeks.org/ios-development
90,Android Development,Mobile Development,Advanced,YouTube,https://www.youtube.com/watch?v=fis26HvvDII
91,Blockchain Fundamentals,Blockchain,Beginner,YouTube,https://www.youtube.com/watch?v=SSo_EIwHSd4
92,Smart Contracts,Blockchain,Intermediate,Coursera,https://www.coursera.org/learn/smart-contracts
93,DeFi Development,Blockchain,Advanced,Infosys Springboard,https://infyspringboard.onwingspan.com/en/app/course/defi
94,Cryptocurrency Trading,Blockchain,Intermediate,Free Platform,https://www.geeksforgeeks.org/cryptocurrency
95,Web3 Development,Blockchain,Advanced,YouTube,https://www.youtube.com/watch?v=gyMwXuJ86Jk
96,UI/UX Design Principles,UI/UX,Beginner,YouTube,https://www.youtube.com/watch?v=68w2VwalD5w
97,User Research Methods,UI/UX,Intermediate,Coursera,https://www.coursera.org/specializations/user-research
98,Prototyping Tools,UI/UX,Advanced,Infosys Springboard,https://infyspringboard.onwingspan.com/en/app/course/prototyping
99,Design Systems,UI/UX,Intermediate,Free Platform,https://www.geeksforgeeks.org/design-systems
100,Accessibility in Design,UI/UX,Advanced,YouTube,https://www.youtube.com/watch?v=20SHvU2PKsM"""

def parse_csv_data(csv_string):
    """Parse CSV data and return list of course dictionaries."""
    lines = csv_string.strip().split('\n')
    header = lines[0].split(',')
    courses = []
    
    for line in lines[1:]:
        if line.strip():
            values = line.split(',')
            course_data = {
                'id': int(values[0]),
                'title': values[1],
                'subject': values[2],
                'level': values[3].lower(),
                'source': values[4],
                'url': values[5]
            }
            courses.append(course_data)
    
    return courses

def get_or_create_subject(db: Session, subject_name: str):
    """Get existing subject or create new one."""
    subject = db.query(Subject).filter(Subject.name == subject_name).first()
    if not subject:
        subject = Subject(
            name=subject_name,
            description=f"Course materials and resources for {subject_name}"
        )
        db.add(subject)
        db.commit()
        db.refresh(subject)
        print(f"Created new subject: {subject_name}")
    else:
        print(f"Found existing subject: {subject_name}")
    return subject

def create_course(db: Session, course_data: dict, subject: Subject):
    """Create a new course."""
    # Map level to CourseLevel enum
    level_mapping = {
        'beginner': CourseLevel.BEGINNER,
        'intermediate': CourseLevel.INTERMEDIATE,
        'advanced': CourseLevel.ADVANCED
    }
    
    course = Course(
        subject_id=subject.id,
        title=course_data['title'],
        level=level_mapping[course_data['level']],
        description=f"Learn {course_data['title']} from {course_data['source']}",
        url=course_data['url']
    )
    
    db.add(course)
    return course

def seed_courses():
    """Main function to seed courses from CSV data."""
    print("Starting course seeding process...")
    
    # Create database tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    # Parse CSV data
    courses_data = parse_csv_data(csv_data)
    print(f"Parsed {len(courses_data)} courses from CSV data")
    
    # Create database session
    db = SessionLocal()
    
    try:
        # Track subjects to avoid duplicate queries
        subjects_cache = {}
        
        # Process each course
        for course_data in courses_data:
            subject_name = course_data['subject']
            
            # Get or create subject
            if subject_name not in subjects_cache:
                subjects_cache[subject_name] = get_or_create_subject(db, subject_name)
            
            subject = subjects_cache[subject_name]
            
            # Check if course already exists
            existing_course = db.query(Course).filter(
                Course.title == course_data['title'],
                Course.subject_id == subject.id
            ).first()
            
            if existing_course:
                print(f"Course already exists: {course_data['title']}")
                continue
            
            # Create new course
            course = create_course(db, course_data, subject)
            print(f"Created course: {course_data['title']} ({course_data['level']})")
        
        # Commit all changes
        db.commit()
        print(f"\nSuccessfully seeded {len(courses_data)} courses!")
        
        # Print summary
        total_subjects = db.query(Subject).count()
        total_courses = db.query(Course).count()
        print(f"Total subjects in database: {total_subjects}")
        print(f"Total courses in database: {total_courses}")
        
    except Exception as e:
        print(f"Error during seeding: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_courses()
