from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Dict, Optional
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity
from app.models.assessment import (
    Subject, Course, AssessmentQuestion as Question, AssessmentSession, AssessmentAnswer,
    CourseLevel, QuestionDifficulty, AssessmentStatus
)
from app.models.user import User
from app.schemas.assessment import CourseResponse

class RecommendationEngine:
    """
    AI-powered recommendation engine for course recommendations based on student performance.
    """
    
    def __init__(self):
        self.scaler = StandardScaler()
    
    def get_course_recommendations(
        self, 
        db: Session, 
        student_id: int,
        num_recommendations: int = 5
    ) -> Dict:
        """
        Get personalized course recommendations for a student based on their assessment performance.
        
        Args:
            db: Database session
            student_id: ID of the student
            num_recommendations: Number of course recommendations to return per subject
            
        Returns:
            Dictionary with recommendations grouped by subject
        """
        try:
            # Get student information
            student = db.query(User).filter(User.id == student_id).first()
            if not student:
                raise ValueError(f"Student with ID {student_id} not found")
            
            # Get latest assessment results
            latest_session = db.query(AssessmentSession).filter(
                AssessmentSession.user_id == student_id,
                AssessmentSession.status == AssessmentStatus.SUBMITTED
            ).order_by(AssessmentSession.created_at.desc()).first()
            
            if not latest_session:
                # No assessment results, return beginner courses for all subjects
                return self._get_fallback_recommendations(db, num_recommendations)
            
            # Calculate performance per subject
            subject_performance = self._analyze_subject_performance(db, latest_session)
            
            # Generate recommendations based on performance
            recommendations = self._generate_recommendations(db, subject_performance, num_recommendations)
            
            return {
                "student_id": student_id,
                "student_name": student.username,
                "recommendations": recommendations
            }
            
        except Exception as e:
            print(f"Error generating recommendations: {e}")
            return self._get_fallback_recommendations(db, num_recommendations)
    
    def _analyze_subject_performance(
        self, 
        db: Session, 
        session: AssessmentSession
    ) -> Dict[int, Dict]:
        """
        Analyze student performance for each subject in the assessment.
        """
        subject_performance = {}
        
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
            
            # Calculate performance metrics
            total_questions = len(subject_answers)
            correct_answers = [a for a in subject_answers if a.is_correct]
            percent_correct = (len(correct_answers) / total_questions) * 100
            
            # Calculate weighted score based on difficulty
            weighted_score = 0
            difficulty_breakdown = {"easy": 0, "medium": 0, "hard": 0}
            
            for answer in subject_answers:
                if answer.question.difficulty == QuestionDifficulty.EASY:
                    weighted_score += 1
                    difficulty_breakdown["easy"] += 1
                elif answer.question.difficulty == QuestionDifficulty.MEDIUM:
                    weighted_score += 2
                    difficulty_breakdown["medium"] += 1
                elif answer.question.difficulty == QuestionDifficulty.HARD:
                    weighted_score += 3
                    difficulty_breakdown["hard"] += 1
            
            # Determine performance level
            performance_level = self._calculate_performance_level(percent_correct)
            recommended_level = self._get_recommended_level(percent_correct)
            
            # Identify specific weaknesses
            weaknesses = self._identify_weaknesses(subject_answers, difficulty_breakdown)
            
            subject_performance[subject_id] = {
                "subject_name": subject.name,
                "percent_correct": round(percent_correct, 1),
                "weighted_score": weighted_score,
                "performance_level": performance_level,
                "recommended_level": recommended_level,
                "weaknesses": weaknesses,
                "difficulty_breakdown": difficulty_breakdown
            }
        
        return subject_performance
    
    def _calculate_performance_level(self, percent_correct: float) -> str:
        """
        Calculate performance level based on percentage correct.
        """
        if percent_correct <= 40:
            return "weak"
        elif percent_correct <= 70:
            return "moderate"
        else:
            return "strong"
    
    def _get_recommended_level(self, percent_correct: float) -> CourseLevel:
        """
        Get recommended course level based on performance.
        """
        if percent_correct <= 40:
            return CourseLevel.BEGINNER
        elif percent_correct <= 70:
            return CourseLevel.INTERMEDIATE
        else:
            return CourseLevel.ADVANCED
    
    def _identify_weaknesses(
        self, 
        answers: List[AssessmentAnswer], 
        difficulty_breakdown: Dict
    ) -> List[str]:
        """
        Identify specific areas of weakness based on incorrect answers.
        """
        weaknesses = []
        
        # Analyze incorrect answers by difficulty
        incorrect_answers = [a for a in answers if not a.is_correct]
        
        if not incorrect_answers:
            return ["No specific weaknesses identified"]
        
        # Count incorrect answers by difficulty
        easy_incorrect = len([a for a in incorrect_answers if a.question.difficulty == QuestionDifficulty.EASY])
        medium_incorrect = len([a for a in incorrect_answers if a.question.difficulty == QuestionDifficulty.MEDIUM])
        hard_incorrect = len([a for a in incorrect_answers if a.question.difficulty == QuestionDifficulty.HARD])
        
        # Identify weaknesses
        if easy_incorrect > 0:
            weaknesses.append("Basic concepts")
        if medium_incorrect > 0:
            weaknesses.append("Intermediate problem solving")
        if hard_incorrect > 0:
            weaknesses.append("Advanced concepts")
        
        # If many easy questions wrong, add fundamental weakness
        if easy_incorrect > len([a for a in answers if a.question.difficulty == QuestionDifficulty.EASY]) * 0.5:
            weaknesses.append("Fundamental understanding")
        
        return weaknesses if weaknesses else ["General concepts"]
    
    def _generate_recommendations(
        self, 
        db: Session, 
        subject_performance: Dict[int, Dict],
        num_recommendations: int
    ) -> List[Dict]:
        """
        Generate course recommendations based on subject performance.
        """
        recommendations = []
        
        for subject_id, performance in subject_performance.items():
            # Get courses for this subject at the recommended level
            recommended_courses = db.query(Course).filter(
                Course.subject_id == subject_id,
                Course.level == performance["recommended_level"]
            ).limit(num_recommendations).all()
            
            # If no courses at recommended level, get courses at adjacent levels
            if not recommended_courses:
                if performance["recommended_level"] == CourseLevel.BEGINNER:
                    # Try intermediate courses
                    recommended_courses = db.query(Course).filter(
                        Course.subject_id == subject_id,
                        Course.level == CourseLevel.INTERMEDIATE
                    ).limit(num_recommendations).all()
                elif performance["recommended_level"] == CourseLevel.ADVANCED:
                    # Try intermediate courses
                    recommended_courses = db.query(Course).filter(
                        Course.subject_id == subject_id,
                        Course.level == CourseLevel.INTERMEDIATE
                    ).limit(num_recommendations).all()
                
                # If still no courses, get any course for this subject
                if not recommended_courses:
                    recommended_courses = db.query(Course).filter(
                        Course.subject_id == subject_id
                    ).limit(num_recommendations).all()
            
            # Convert to response format
            course_responses = []
            for course in recommended_courses:
                course_responses.append({
                    "id": course.id,
                    "title": course.title,
                    "level": course.level.value,
                    "description": course.description
                })
            
            # Create recommendation entry
            recommendation = {
                "subject": performance["subject_name"],
                "weakness": ", ".join(performance["weaknesses"]),
                "performance_level": performance["performance_level"],
                "percent_correct": performance["percent_correct"],
                "recommended_courses": course_responses
            }
            
            recommendations.append(recommendation)
        
        return recommendations
    
    def _get_fallback_recommendations(
        self, 
        db: Session, 
        num_recommendations: int
    ) -> Dict:
        """
        Get fallback recommendations when no assessment data is available.
        """
        # Get all subjects
        subjects = db.query(Subject).all()
        
        recommendations = []
        for subject in subjects:
            # Get beginner courses for each subject
            courses = db.query(Course).filter(
                Course.subject_id == subject.id,
                Course.level == CourseLevel.BEGINNER
            ).limit(num_recommendations).all()
            
            if not courses:
                # Get any course for this subject
                courses = db.query(Course).filter(
                    Course.subject_id == subject.id
                ).limit(num_recommendations).all()
            
            course_responses = []
            for course in courses:
                course_responses.append({
                    "id": course.id,
                    "title": course.title,
                    "level": course.level.value,
                    "description": course.description
                })
            
            recommendation = {
                "subject": subject.name,
                "weakness": "No assessment data available",
                "performance_level": "unknown",
                "percent_correct": 0.0,
                "recommended_courses": course_responses
            }
            
            recommendations.append(recommendation)
        
        return {
            "student_id": None,
            "student_name": "Unknown",
            "recommendations": recommendations
        }
    
    def get_ml_recommendations(
        self, 
        db: Session, 
        student_id: int,
        num_recommendations: int = 5
    ) -> Dict:
        """
        Get ML-powered recommendations using scikit-learn (future enhancement).
        This method can be expanded to use collaborative filtering, content-based filtering, etc.
        """
        # For now, return the rule-based recommendations
        # This can be enhanced with actual ML models later
        return self.get_course_recommendations(db, student_id, num_recommendations)
