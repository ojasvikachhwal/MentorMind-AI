from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Dict, Tuple
import random
from app.models.assessment import (
    Subject, Course, AssessmentQuestion as Question, AssessmentSession, AssessmentAnswer,
    CourseLevel, QuestionDifficulty, AssessmentStatus
)
from app.schemas.assessment import SubjectResult, AssessmentResult

class AssessmentService:
    
    @staticmethod
    def get_subjects(db: Session) -> List[Subject]:
        """Get all available subjects."""
        return db.query(Subject).all()
    
    @staticmethod
    def get_all_subject_ids(db: Session) -> List[int]:
        """Get all subject IDs."""
        return [subject.id for subject in db.query(Subject.id).all()]
    
    @staticmethod
    def create_assessment_session(
        db: Session, 
        user_id: int, 
        subject_ids: List[int], 
        num_questions_per_subject: int = 10
    ) -> AssessmentSession:
        """Create a new assessment session."""
        session = AssessmentSession(
            user_id=user_id,
            selected_subject_ids=subject_ids,
            num_questions_per_subject=num_questions_per_subject
        )
        db.add(session)
        db.commit()
        db.refresh(session)
        return session
    
    @staticmethod
    def get_questions_for_session(
        db: Session, 
        session: AssessmentSession
    ) -> List[Question]:
        """Get questions for the assessment session with difficulty stratification."""
        questions = []
        
        for subject_id in session.selected_subject_ids:
            # Get questions for this subject
            subject_questions = db.query(Question).filter(
                Question.subject_id == subject_id
            ).all()
            
            if not subject_questions:
                continue
            
            # Stratify by difficulty
            easy_questions = [q for q in subject_questions if q.difficulty == QuestionDifficulty.EASY]
            medium_questions = [q for q in subject_questions if q.difficulty == QuestionDifficulty.MEDIUM]
            hard_questions = [q for q in subject_questions if q.difficulty == QuestionDifficulty.HARD]
            
            # Calculate how many questions to take from each difficulty
            total_questions = session.num_questions_per_subject
            easy_count = int(total_questions * 0.4)  # 40% easy
            medium_count = int(total_questions * 0.4)  # 40% medium
            hard_count = total_questions - easy_count - medium_count  # 20% hard
            
            # Sample questions from each difficulty level
            selected_questions = []
            selected_questions.extend(random.sample(easy_questions, min(easy_count, len(easy_questions))))
            selected_questions.extend(random.sample(medium_questions, min(medium_count, len(medium_questions))))
            selected_questions.extend(random.sample(hard_questions, min(hard_count, len(hard_questions))))
            
            # If we don't have enough questions, fill with remaining questions
            remaining_needed = total_questions - len(selected_questions)
            if remaining_needed > 0:
                remaining_questions = [q for q in subject_questions if q not in selected_questions]
                if remaining_questions:
                    selected_questions.extend(random.sample(remaining_questions, min(remaining_needed, len(remaining_questions))))
            
            questions.extend(selected_questions[:total_questions])
        
        return questions
    
    @staticmethod
    def submit_assessment_answers(
        db: Session, 
        session_id: int, 
        answers: List[Dict]
    ) -> AssessmentResult:
        """Submit assessment answers and calculate results."""
        # Get the session
        session = db.query(AssessmentSession).filter(AssessmentSession.id == session_id).first()
        if not session:
            raise ValueError("Assessment session not found")
        
        if session.status != AssessmentStatus.ACTIVE:
            raise ValueError("Assessment session is not active")
        
        # Save answers and calculate correctness
        for answer_data in answers:
            question = db.query(Question).filter(Question.id == answer_data["question_id"]).first()
            if not question:
                continue
            
            is_correct = answer_data["selected_index"] == question.correct_index
            
            assessment_answer = AssessmentAnswer(
                session_id=session_id,
                question_id=answer_data["question_id"],
                selected_index=answer_data["selected_index"],
                is_correct=is_correct
            )
            db.add(assessment_answer)
        
        # Mark session as submitted
        session.status = AssessmentStatus.SUBMITTED
        db.commit()
        
        # Calculate results
        return AssessmentService.calculate_assessment_results(db, session)
    
    @staticmethod
    def calculate_assessment_results(
        db: Session, 
        session: AssessmentSession
    ) -> AssessmentResult:
        """Calculate assessment results for a session."""
        results = []
        
        for subject_id in session.selected_subject_ids:
            subject = db.query(Subject).filter(Subject.id == subject_id).first()
            if not subject:
                continue
            
            # Get answers for this subject
            subject_answers = db.query(AssessmentAnswer).join(Question).filter(
                AssessmentAnswer.session_id == session.id,
                Question.subject_id == subject_id
            ).all()
            
            if not subject_answers:
                continue
            
            # Calculate scores
            total_questions = len(subject_answers)
            correct_answers = [a for a in subject_answers if a.is_correct]
            percent_correct = (len(correct_answers) / total_questions) * 100
            
            # Calculate weighted score
            weighted_score = 0
            for answer in correct_answers:
                if answer.question.difficulty == QuestionDifficulty.EASY:
                    weighted_score += 1
                elif answer.question.difficulty == QuestionDifficulty.MEDIUM:
                    weighted_score += 2
                elif answer.question.difficulty == QuestionDifficulty.HARD:
                    weighted_score += 3
            
            # Map to level
            if percent_correct <= 40:
                level = CourseLevel.BEGINNER
            elif percent_correct <= 70:
                level = CourseLevel.INTERMEDIATE
            else:
                level = CourseLevel.ADVANCED
            
            # Get recommended courses
            recommended_courses = db.query(Course).filter(
                Course.subject_id == subject_id,
                Course.level == level
            ).all()
            
            # If no courses at this level, get closest level
            if not recommended_courses:
                if level == CourseLevel.BEGINNER:
                    # Try intermediate
                    recommended_courses = db.query(Course).filter(
                        Course.subject_id == subject_id,
                        Course.level == CourseLevel.INTERMEDIATE
                    ).all()
                elif level == CourseLevel.INTERMEDIATE:
                    # Try beginner
                    recommended_courses = db.query(Course).filter(
                        Course.subject_id == subject_id,
                        Course.level == CourseLevel.BEGINNER
                    ).all()
                elif level == CourseLevel.ADVANCED:
                    # Try intermediate
                    recommended_courses = db.query(Course).filter(
                        Course.subject_id == subject_id,
                        Course.level == CourseLevel.INTERMEDIATE
                    ).all()
                
                # If still no courses, get any course for this subject
                if not recommended_courses:
                    recommended_courses = db.query(Course).filter(
                        Course.subject_id == subject_id
                    ).limit(3).all()
            
            subject_result = SubjectResult(
                subject_id=subject_id,
                subject_name=subject.name,
                percent_correct=round(percent_correct, 1),
                weighted_score=weighted_score,
                level=level,
                recommended_courses=recommended_courses
            )
            results.append(subject_result)
        
        return AssessmentResult(
            session_id=session.id,
            status=session.status,
            created_at=session.created_at,
            results=results
        )
    
    @staticmethod
    def get_latest_assessment_results(db: Session, user_id: int) -> AssessmentResult:
        """Get the latest assessment results for a user."""
        latest_session = db.query(AssessmentSession).filter(
            AssessmentSession.user_id == user_id,
            AssessmentSession.status == AssessmentStatus.SUBMITTED
        ).order_by(AssessmentSession.created_at.desc()).first()
        
        if not latest_session:
            raise ValueError("No completed assessment found for user")
        
        return AssessmentService.calculate_assessment_results(db, latest_session)
