import google.generativeai as genai
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.core.config import settings
from app.models.mock_test import MockTest, MockTestQuestion, MockTestStatus
from app.models.assessment import Subject
from app.models.student_progress import StudentSubjectProgress
from app.models.user import User
from datetime import datetime
import json
import random

class AutomatedMockTestService:
    """
    Service for generating automated mock tests using Gemini AI
    """
    
    def __init__(self):
        if settings.GEMINI_API_KEY:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            self.model = genai.GenerativeModel('gemini-2.0-flash')
        else:
            self.model = None
    
    def generate_mock_test(
        self, 
        subject_id: int, 
        student_id: int, 
        db: Session
    ) -> Optional[MockTest]:
        """
        Generate an automated mock test for a student based on their progress
        """
        if not self.model:
            # Fallback to sample test generation for testing
            return self._generate_sample_test(subject_id, student_id, db)
        
        # Get subject details
        subject = db.query(Subject).filter(Subject.id == subject_id).first()
        if not subject:
            raise Exception("Subject not found")
        
        # Get student progress
        progress = db.query(StudentSubjectProgress).filter(
            StudentSubjectProgress.student_id == student_id,
            StudentSubjectProgress.subject_id == subject_id
        ).first()
        
        # Determine difficulty and question count based on progress
        if not progress or progress.current_progress_percentage < 30:
            difficulty_level = "easy"
            question_count = 5
            time_limit = 30
        elif progress.current_progress_percentage < 60:
            difficulty_level = "medium"
            question_count = 8
            time_limit = 45
        else:
            difficulty_level = "hard"
            question_count = 10
            time_limit = 60
        
        # Generate test using Gemini AI
        test_data = self._generate_test_with_ai(
            subject_name=subject.name,
            difficulty_level=difficulty_level,
            question_count=question_count
        )
        
        if not test_data:
            raise Exception("Failed to generate test with AI")
        
        # Create mock test in database
        mock_test = MockTest(
            title=f"Auto-Generated {subject.name} Test - {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            description=f"Automatically generated test for {subject.name} at {difficulty_level} level",
            subject_id=subject_id,
            instructor_id=1,  # System user
            time_limit_minutes=time_limit,
            is_public=True,
            status=MockTestStatus.ACTIVE
        )
        
        db.add(mock_test)
        db.flush()  # Get the ID
        
        # Add questions
        total_marks = 0
        for i, question_data in enumerate(test_data.get('questions', [])):
            question = MockTestQuestion(
                mock_test_id=mock_test.id,
                question_text=question_data['question'],
                option_a=question_data['options'][0],
                option_b=question_data['options'][1],
                option_c=question_data['options'][2],
                option_d=question_data['options'][3],
                correct_option=question_data['correct_answer'],
                marks=1,  # Each question worth 1 mark
                explanation=question_data.get('explanation', ''),
                difficulty=difficulty_level
            )
            db.add(question)
            total_marks += 1
        
        mock_test.total_marks = total_marks
        db.commit()
        db.refresh(mock_test)
        
        return mock_test
    
    def _generate_sample_test(
        self, 
        subject_id: int, 
        student_id: int, 
        db: Session
    ) -> MockTest:
        """
        Generate a sample test for testing purposes when Gemini API is not available
        """
        # Get subject details
        subject = db.query(Subject).filter(Subject.id == subject_id).first()
        if not subject:
            raise Exception("Subject not found")
        
        # Get student progress
        progress = db.query(StudentSubjectProgress).filter(
            StudentSubjectProgress.student_id == student_id,
            StudentSubjectProgress.subject_id == subject_id
        ).first()
        
        # Determine difficulty and question count based on progress
        if not progress or progress.current_progress_percentage < 30:
            difficulty_level = "easy"
            question_count = 5
            time_limit = 30
        elif progress.current_progress_percentage < 60:
            difficulty_level = "medium"
            question_count = 8
            time_limit = 45
        else:
            difficulty_level = "hard"
            question_count = 10
            time_limit = 60
        
        # Create mock test in database
        mock_test = MockTest(
            title=f"Sample {subject.name} Test - {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            description=f"Sample test for {subject.name} at {difficulty_level} level",
            subject_id=subject_id,
            instructor_id=1,  # System user
            time_limit_minutes=time_limit,
            is_public=True,
            status=MockTestStatus.ACTIVE
        )
        
        db.add(mock_test)
        db.flush()  # Get the ID
        
        # Add sample questions
        sample_questions = self._get_sample_questions(subject.name, difficulty_level, question_count)
        total_marks = 0
        
        for question_data in sample_questions:
            question = MockTestQuestion(
                mock_test_id=mock_test.id,
                question_text=question_data['question'],
                option_a=question_data['options'][0],
                option_b=question_data['options'][1],
                option_c=question_data['options'][2],
                option_d=question_data['options'][3],
                correct_option=question_data['correct_answer'],
                marks=1,  # Each question worth 1 mark
                explanation=question_data.get('explanation', ''),
                difficulty=difficulty_level
            )
            db.add(question)
            total_marks += 1
        
        mock_test.total_marks = total_marks
        db.commit()
        db.refresh(mock_test)
        
        return mock_test
    
    def _get_sample_questions(self, subject_name: str, difficulty: str, count: int) -> List[Dict]:
        """
        Generate sample questions for testing
        """
        sample_questions = {
            "Data Structures & Algorithms": [
                {
                    "question": "What is the time complexity of binary search?",
                    "options": ["O(n)", "O(log n)", "O(n²)", "O(1)"],
                    "correct_answer": "B",
                    "explanation": "Binary search has O(log n) time complexity as it eliminates half the search space in each iteration."
                },
                {
                    "question": "Which data structure follows LIFO principle?",
                    "options": ["Queue", "Stack", "Array", "Linked List"],
                    "correct_answer": "B",
                    "explanation": "Stack follows Last In First Out (LIFO) principle."
                },
                {
                    "question": "What is the worst-case time complexity of quicksort?",
                    "options": ["O(n log n)", "O(n²)", "O(n)", "O(log n)"],
                    "correct_answer": "B",
                    "explanation": "Quicksort has O(n²) worst-case time complexity when the pivot is always the smallest or largest element."
                }
            ],
            "Object-Oriented Programming": [
                {
                    "question": "What is encapsulation in OOP?",
                    "options": ["Hiding data", "Inheritance", "Polymorphism", "Abstraction"],
                    "correct_answer": "A",
                    "explanation": "Encapsulation is the bundling of data and methods that work on that data within one unit, hiding internal details."
                },
                {
                    "question": "Which keyword is used for inheritance in most OOP languages?",
                    "options": ["extends", "inherits", "implements", "derives"],
                    "correct_answer": "A",
                    "explanation": "The 'extends' keyword is commonly used for inheritance in OOP languages like Java."
                }
            ],
            "Database Management": [
                {
                    "question": "What does ACID stand for in database transactions?",
                    "options": ["Atomicity, Consistency, Isolation, Durability", "Access, Control, Integrity, Data", "Analysis, Control, Integration, Design", "Application, Control, Interface, Database"],
                    "correct_answer": "A",
                    "explanation": "ACID stands for Atomicity, Consistency, Isolation, and Durability - the four key properties of database transactions."
                },
                {
                    "question": "Which SQL command is used to retrieve data?",
                    "options": ["INSERT", "SELECT", "UPDATE", "DELETE"],
                    "correct_answer": "B",
                    "explanation": "The SELECT command is used to retrieve data from a database table."
                }
            ]
        }
        
        # Get questions for the subject or use a default set
        questions = sample_questions.get(subject_name, [
            {
                "question": f"Sample question about {subject_name}?",
                "options": ["Option A", "Option B", "Option C", "Option D"],
                "correct_answer": "A",
                "explanation": "This is a sample explanation."
            }
        ])
        
        # Return the requested number of questions, cycling through if needed
        result = []
        for i in range(count):
            result.append(questions[i % len(questions)])
        
        return result
    
    def _generate_sample_evaluation(self, test_session_id: int, db: Session) -> Dict[str, Any]:
        """
        Generate sample evaluation for testing purposes when Gemini API is not available
        """
        from app.models.mock_test import MockTestSession, MockTestAnswer
        
        session = db.query(MockTestSession).filter(MockTestSession.id == test_session_id).first()
        if not session:
            raise Exception("Test session not found")
        
        # Generate sample evaluation based on performance
        percentage = session.percentage
        
        if percentage >= 80:
            performance_level = "Excellent"
            strengths = ["Strong understanding of concepts", "Good problem-solving skills", "Consistent performance"]
            weaknesses = ["Minor areas for improvement", "Could work on advanced topics"]
            recommendations = ["Continue practicing advanced concepts", "Consider mentoring others", "Explore related subjects"]
        elif percentage >= 60:
            performance_level = "Good"
            strengths = ["Solid foundation", "Good grasp of basic concepts", "Shows improvement"]
            weaknesses = ["Some topics need more practice", "Time management could improve"]
            recommendations = ["Focus on weak areas", "Practice more problems", "Review fundamental concepts"]
        elif percentage >= 40:
            performance_level = "Needs Improvement"
            strengths = ["Basic understanding present", "Shows effort"]
            weaknesses = ["Several concepts unclear", "Needs more practice", "Fundamentals need work"]
            recommendations = ["Review basic concepts thoroughly", "Practice more problems", "Seek help if needed"]
        else:
            performance_level = "Beginner Level"
            strengths = ["Willing to learn", "Starting the journey"]
            weaknesses = ["Many concepts unclear", "Needs significant practice", "Fundamentals missing"]
            recommendations = ["Start with basics", "Take it step by step", "Don't give up"]
        
        return {
            "overall_assessment": f"Your performance shows {performance_level.lower()} level understanding. You scored {percentage:.1f}% on this test.",
            "strengths": strengths,
            "weaknesses": weaknesses,
            "recommendations": recommendations,
            "performance_summary": f"Scored {percentage:.1f}% - {performance_level} performance with room for growth."
        }
    
    def _generate_test_with_ai(
        self, 
        subject_name: str, 
        difficulty_level: str, 
        question_count: int
    ) -> Optional[Dict[str, Any]]:
        """
        Generate test questions using Gemini AI
        """
        try:
            prompt = f"""
            Generate a {difficulty_level} level mock test for the subject: {subject_name}
            
            Requirements:
            - Generate exactly {question_count} multiple choice questions
            - Each question should have 4 options (A, B, C, D)
            - Questions should be appropriate for {difficulty_level} level
            - Include one correct answer for each question
            - Provide brief explanations for correct answers
            - Questions should test practical knowledge and understanding
            
            Format the response as JSON with this structure:
            {{
                "questions": [
                    {{
                        "question": "Question text here",
                        "options": ["Option A", "Option B", "Option C", "Option D"],
                        "correct_answer": "A",
                        "explanation": "Brief explanation of why this is correct"
                    }}
                ]
            }}
            
            Make sure the questions are relevant to {subject_name} and test real understanding.
            """
            
            response = self.model.generate_content(prompt)
            result_text = response.text
            
            # Clean up the response to extract JSON
            if "```json" in result_text:
                json_start = result_text.find("```json") + 7
                json_end = result_text.find("```", json_start)
                result_text = result_text[json_start:json_end].strip()
            elif "```" in result_text:
                json_start = result_text.find("```") + 3
                json_end = result_text.find("```", json_start)
                result_text = result_text[json_start:json_end].strip()
            
            # Parse JSON
            test_data = json.loads(result_text)
            
            # Validate the structure
            if 'questions' not in test_data or not isinstance(test_data['questions'], list):
                raise Exception("Invalid test data structure")
            
            if len(test_data['questions']) != question_count:
                raise Exception(f"Expected {question_count} questions, got {len(test_data['questions'])}")
            
            # Validate each question
            for i, question in enumerate(test_data['questions']):
                if not all(key in question for key in ['question', 'options', 'correct_answer']):
                    raise Exception(f"Invalid question structure at index {i}")
                
                if len(question['options']) != 4:
                    raise Exception(f"Question {i} must have exactly 4 options")
                
                if question['correct_answer'] not in ['A', 'B', 'C', 'D']:
                    raise Exception(f"Question {i} must have correct answer as A, B, C, or D")
            
            return test_data
            
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            print(f"Response text: {result_text}")
            return None
        except Exception as e:
            print(f"Error generating test with AI: {e}")
            return None
    
    def evaluate_test_with_ai(
        self, 
        test_session_id: int, 
        db: Session
    ) -> Dict[str, Any]:
        """
        Evaluate test answers using Gemini AI
        """
        if not self.model:
            # Fallback to sample evaluation for testing
            return self._generate_sample_evaluation(test_session_id, db)
        
        # Get session and answers
        from app.models.mock_test import MockTestSession, MockTestAnswer
        
        session = db.query(MockTestSession).filter(MockTestSession.id == test_session_id).first()
        if not session:
            raise Exception("Test session not found")
        
        answers = db.query(MockTestAnswer).filter(MockTestAnswer.session_id == test_session_id).all()
        
        # Prepare evaluation data
        evaluation_data = {
            "test_title": session.mock_test.title,
            "subject": session.mock_test.subject.name,
            "total_questions": len(answers),
            "correct_answers": sum(1 for answer in answers if answer.is_correct),
            "total_score": session.total_score,
            "total_marks": session.total_marks,
            "percentage": session.percentage,
            "time_taken": session.time_taken_minutes
        }
        
        # Generate AI evaluation
        prompt = f"""
        Evaluate this mock test performance and provide detailed feedback:
        
        Test: {evaluation_data['test_title']}
        Subject: {evaluation_data['subject']}
        Score: {evaluation_data['total_score']}/{evaluation_data['total_marks']} ({evaluation_data['percentage']:.1f}%)
        Correct Answers: {evaluation_data['correct_answers']}/{evaluation_data['total_questions']}
        Time Taken: {evaluation_data['time_taken']} minutes
        
        Provide evaluation in JSON format:
        {{
            "overall_assessment": "Overall performance assessment",
            "strengths": ["List of strengths"],
            "weaknesses": ["List of areas for improvement"],
            "recommendations": ["Specific study recommendations"],
            "performance_summary": "2-3 sentence summary"
        }}
        """
        
        response = self.model.generate_content(prompt)
        evaluation_text = response.text
        
        # Parse AI response
        try:
            if "```json" in evaluation_text:
                json_start = evaluation_text.find("```json") + 7
                json_end = evaluation_text.find("```", json_start)
                evaluation_text = evaluation_text[json_start:json_end].strip()
            
            evaluation_result = json.loads(evaluation_text)
            return evaluation_result
            
        except json.JSONDecodeError:
            # Fallback evaluation
            return {
                "overall_assessment": f"Scored {evaluation_data['percentage']:.1f}% on {evaluation_data['subject']} test",
                "strengths": ["Good attempt on the test"],
                "weaknesses": ["Some areas need improvement"],
                "recommendations": ["Continue practicing", "Review incorrect answers"],
                "performance_summary": f"Completed {evaluation_data['subject']} test with {evaluation_data['percentage']:.1f}% accuracy"
            }
    
    def update_student_progress(
        self, 
        student_id: int, 
        subject_id: int, 
        test_score: float, 
        total_marks: float, 
        db: Session
    ) -> None:
        """
        Update student progress based on test performance
        """
        # Get or create progress record
        progress = db.query(StudentSubjectProgress).filter(
            StudentSubjectProgress.student_id == student_id,
            StudentSubjectProgress.subject_id == subject_id
        ).first()
        
        if not progress:
            progress = StudentSubjectProgress(
                student_id=student_id,
                subject_id=subject_id,
                total_tests_taken=0,
                total_marks_earned=0.0,
                total_marks_possible=0.0,
                current_progress_percentage=0.0,
                average_score=0.0,
                best_score=0.0
            )
            db.add(progress)
        
        # Update progress metrics
        progress.total_tests_taken += 1
        progress.total_marks_earned += test_score
        progress.total_marks_possible += total_marks
        
        # Calculate new progress percentage
        if progress.total_marks_possible > 0:
            progress.current_progress_percentage = (progress.total_marks_earned / progress.total_marks_possible) * 100
        
        # Update average score
        progress.average_score = progress.total_marks_earned / progress.total_tests_taken
        
        # Update best score
        test_percentage = (test_score / total_marks) * 100 if total_marks > 0 else 0
        if test_percentage > progress.best_score:
            progress.best_score = test_percentage
        
        # Update last test date
        progress.last_test_date = datetime.utcnow()
        
        db.commit()
