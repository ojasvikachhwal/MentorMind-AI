"""
AI Feedback Service using Hugging Face Transformers
Generates personalized feedback and insights for students.
"""

import json
import logging
from typing import List, Dict, Optional, Tuple, Any
from datetime import datetime, timedelta

from app.models.progress import StudentProgress, ActivityType, FeedbackType
from app.models.user import User

logger = logging.getLogger(__name__)

class AIFeedbackService:
    """Service for generating AI-powered feedback and insights."""
    
    def __init__(self):
        self.feedback_templates = {
            "strength": [
                "Excellent work in {subject}! Your consistent performance shows strong understanding.",
                "You're excelling in {subject}. Keep up the great work!",
                "Outstanding progress in {subject}. Your dedication is paying off."
            ],
            "weakness": [
                "Consider focusing more on {subject}. Practice will help improve your understanding.",
                "You might benefit from additional study time in {subject}.",
                "Let's work on strengthening your {subject} skills through targeted practice."
            ],
            "recommendation": [
                "Based on your progress, I recommend focusing on {subject} next.",
                "Try practicing more {subject} problems to improve your skills.",
                "Consider taking advanced courses in {subject} to build on your strengths."
            ],
            "encouragement": [
                "Great job this week! Your consistent effort is showing results.",
                "You're making excellent progress. Keep up the momentum!",
                "Your dedication to learning is impressive. Well done!"
            ],
            "warning": [
                "Your study time has decreased recently. Consider increasing your practice sessions.",
                "I notice you haven't been as active lately. Let's get back on track!",
                "Your performance has dipped in {subject}. Let's focus on improvement."
            ]
        }
    
    def analyze_code_quality(
        self, 
        code: str, 
        language: str, 
        execution_time: Optional[float] = None,
        memory_usage: Optional[float] = None
    ) -> Tuple[str, List[str]]:
        """Analyze code quality and provide feedback."""
        try:
            feedback_parts = []
            suggestions = []
            
            # Basic code analysis
            lines = code.split('\n')
            non_empty_lines = [line for line in lines if line.strip()]
            
            # Check code length
            if len(non_empty_lines) > 50:
                feedback_parts.append("Your solution is quite long. Consider breaking it into smaller functions.")
                suggestions.append("Refactor into smaller, more focused functions")
            
            # Check for common patterns
            if 'for' in code and 'range' in code:
                feedback_parts.append("Good use of loops for iteration.")
            
            if 'if' in code:
                feedback_parts.append("Proper use of conditional statements.")
            
            # Performance analysis
            if execution_time and execution_time > 1.0:
                feedback_parts.append("Your solution works but could be optimized for better performance.")
                suggestions.append("Consider optimizing time complexity")
            
            if memory_usage and memory_usage > 50:
                feedback_parts.append("Memory usage could be improved.")
                suggestions.append("Look for ways to reduce memory consumption")
            
            # Language-specific feedback
            if language.lower() == 'python':
                if 'import' in code:
                    feedback_parts.append("Good use of Python libraries.")
                if 'def ' in code:
                    feedback_parts.append("Well-structured with functions.")
                if 'list(' in code or '[]' in code:
                    feedback_parts.append("Effective use of Python data structures.")
            
            elif language.lower() == 'java':
                if 'public class' in code:
                    feedback_parts.append("Proper Java class structure.")
                if 'private' in code or 'protected' in code:
                    feedback_parts.append("Good encapsulation practices.")
            
            # Generate final feedback
            if not feedback_parts:
                feedback_parts.append("Your code looks good! Keep practicing to improve further.")
            
            feedback = " ".join(feedback_parts)
            
            # Add general suggestions if none provided
            if not suggestions:
                suggestions = [
                    "Practice more problems in this difficulty level",
                    "Study advanced algorithms and data structures",
                    "Focus on code readability and documentation"
                ]
            
            return feedback, suggestions
            
        except Exception as e:
            logger.error(f"Error analyzing code quality: {e}")
            return "Code analysis completed. Keep practicing!", [
                "Continue solving problems regularly",
                "Focus on understanding algorithms",
                "Practice writing clean, readable code"
            ]
    
    def generate_weekly_insights(
        self, 
        subject_performance: Dict[str, Any], 
        activities: List[StudentProgress]
    ) -> Tuple[List[str], List[str], List[str]]:
        """Generate weekly insights based on performance data."""
        try:
            strengths = []
            weaknesses = []
            recommendations = []
            
            # Analyze subject performance
            if subject_performance:
                # Find strongest subject
                best_subject = max(
                    subject_performance.items(), 
                    key=lambda x: x[1].get("average_score", 0)
                )
                if best_subject[1].get("average_score", 0) > 80:
                    strengths.append(best_subject[0])
                
                # Find weakest subject
                worst_subject = min(
                    subject_performance.items(), 
                    key=lambda x: x[1].get("average_score", 100)
                )
                if worst_subject[1].get("average_score", 100) < 60:
                    weaknesses.append(worst_subject[0])
            
            # Analyze activity patterns
            total_activities = len(activities)
            total_study_time = sum(activity.time_spent for activity in activities)
            
            if total_activities > 10:
                strengths.append("Consistent practice")
            elif total_activities < 5:
                weaknesses.append("Study consistency")
                recommendations.append("Increase study frequency")
            
            if total_study_time > 300:  # 5 hours
                strengths.append("Dedicated study time")
            elif total_study_time < 120:  # 2 hours
                weaknesses.append("Study time")
                recommendations.append("Increase weekly study time")
            
            # Analyze quiz performance
            quiz_activities = [a for a in activities if a.activity_type == ActivityType.QUIZ_ATTEMPT]
            if quiz_activities:
                quiz_scores = [a.score for a in quiz_activities if a.score is not None]
                if quiz_scores:
                    avg_quiz_score = sum(quiz_scores) / len(quiz_scores)
                    if avg_quiz_score > 85:
                        strengths.append("Quiz performance")
                    elif avg_quiz_score < 60:
                        weaknesses.append("Quiz performance")
                        recommendations.append("Review quiz materials and practice more")
            
            # Analyze coding performance
            coding_activities = [a for a in activities if a.activity_type == ActivityType.CODING_PRACTICE]
            if coding_activities:
                coding_scores = [a.score for a in coding_activities if a.score is not None]
                if coding_scores:
                    avg_coding_score = sum(coding_scores) / len(coding_scores)
                    if avg_coding_score > 80:
                        strengths.append("Coding skills")
                    elif avg_coding_score < 50:
                        weaknesses.append("Coding skills")
                        recommendations.append("Practice more coding problems")
            
            # Generate recommendations based on weaknesses
            for weakness in weaknesses:
                if weakness in ["Study consistency", "Study time"]:
                    recommendations.append("Create a daily study schedule")
                elif weakness in ["Quiz performance"]:
                    recommendations.append("Review course materials before taking quizzes")
                elif weakness in ["Coding skills"]:
                    recommendations.append("Start with easier coding problems and gradually increase difficulty")
            
            return strengths, weaknesses, recommendations
            
        except Exception as e:
            logger.error(f"Error generating weekly insights: {e}")
            return ["Consistent effort"], ["Areas for improvement"], ["Keep practicing regularly"]
    
    def generate_weekly_report_content(
        self, 
        user: User, 
        analytics: Any, 
        week_start: datetime, 
        week_end: datetime
    ) -> Dict[str, Any]:
        """Generate comprehensive weekly report content."""
        try:
            # Generate summary
            summary = f"Hello {user.full_name or user.username}! Here's your weekly learning report for {week_start.strftime('%B %d')} - {week_end.strftime('%B %d')}."
            
            if analytics.total_study_time > 0:
                hours = analytics.total_study_time / 60
                summary += f" You spent {hours:.1f} hours learning this week."
            
            if analytics.courses_completed > 0:
                summary += f" You completed {analytics.courses_completed} courses."
            
            if analytics.quizzes_taken > 0:
                summary += f" You took {analytics.quizzes_taken} quizzes with an average score of {analytics.average_quiz_score:.1f}%."
            
            if analytics.coding_sessions > 0:
                summary += f" You completed {analytics.coding_sessions} coding sessions with an average score of {analytics.average_coding_score:.1f}%."
            
            # Generate achievements
            achievements = []
            if analytics.courses_completed > 0:
                achievements.append(f"Completed {analytics.courses_completed} course(s)")
            
            if analytics.average_quiz_score > 85:
                achievements.append("Excellent quiz performance")
            
            if analytics.average_coding_score > 80:
                achievements.append("Strong coding skills")
            
            if analytics.total_study_time > 300:  # 5 hours
                achievements.append("Dedicated study time")
            
            if not achievements:
                achievements.append("Consistent learning effort")
            
            # Generate areas for improvement
            areas_for_improvement = []
            if analytics.average_quiz_score < 70:
                areas_for_improvement.append("Quiz performance - review course materials")
            
            if analytics.average_coding_score < 60:
                areas_for_improvement.append("Coding skills - practice more problems")
            
            if analytics.total_study_time < 120:  # 2 hours
                areas_for_improvement.append("Study time - increase weekly practice")
            
            if analytics.courses_completed == 0:
                areas_for_improvement.append("Course completion - focus on finishing courses")
            
            if not areas_for_improvement:
                areas_for_improvement.append("Continue building on your strengths")
            
            # Generate next week goals
            next_week_goals = []
            if analytics.average_quiz_score < 80:
                next_week_goals.append("Improve quiz scores by reviewing materials")
            
            if analytics.coding_sessions < 3:
                next_week_goals.append("Complete at least 3 coding practice sessions")
            
            if analytics.total_study_time < 300:
                next_week_goals.append("Increase study time to 5+ hours")
            
            if analytics.courses_completed == 0:
                next_week_goals.append("Complete at least one course")
            
            if not next_week_goals:
                next_week_goals.append("Maintain current performance level")
                next_week_goals.append("Try more challenging problems")
            
            return {
                "summary": summary,
                "achievements": achievements,
                "areas_for_improvement": areas_for_improvement,
                "next_week_goals": next_week_goals
            }
            
        except Exception as e:
            logger.error(f"Error generating weekly report content: {e}")
            return {
                "summary": f"Hello {user.full_name or user.username}! Here's your weekly learning report.",
                "achievements": ["Consistent learning effort"],
                "areas_for_improvement": ["Continue practicing regularly"],
                "next_week_goals": ["Maintain study consistency"]
            }
    
    def generate_personalized_feedback(
        self, 
        user_id: int, 
        feedback_type: FeedbackType, 
        subject: Optional[str] = None,
        context: Optional[Dict] = None
    ) -> str:
        """Generate personalized feedback message."""
        try:
            templates = self.feedback_templates.get(feedback_type.value, [])
            if not templates:
                return "Keep up the great work!"
            
            # Select template based on context
            template = templates[0]  # Simple selection for now
            
            # Replace placeholders
            if subject:
                message = template.format(subject=subject)
            else:
                message = template.format(subject="your studies")
            
            return message
            
        except Exception as e:
            logger.error(f"Error generating personalized feedback: {e}")
            return "Keep up the great work!"
    
    def analyze_learning_patterns(self, activities: List[StudentProgress]) -> Dict[str, Any]:
        """Analyze learning patterns and provide insights."""
        try:
            if not activities:
                return {"insights": ["Start tracking your learning activities"]}
            
            # Analyze time patterns
            time_patterns = {}
            for activity in activities:
                hour = activity.created_at.hour
                time_patterns[hour] = time_patterns.get(hour, 0) + 1
            
            # Find peak learning hours
            peak_hours = sorted(time_patterns.items(), key=lambda x: x[1], reverse=True)[:3]
            
            # Analyze subject distribution
            subject_counts = {}
            for activity in activities:
                if activity.subject:
                    subject_counts[activity.subject] = subject_counts.get(activity.subject, 0) + 1
            
            # Analyze difficulty progression
            difficulty_progression = []
            for activity in activities:
                if activity.difficulty_level:
                    difficulty_progression.append({
                        "date": activity.created_at.strftime("%Y-%m-%d"),
                        "difficulty": activity.difficulty_level,
                        "score": activity.score
                    })
            
            insights = []
            if peak_hours:
                insights.append(f"You're most active during {peak_hours[0][0]}:00 hours")
            
            if subject_counts:
                most_practiced = max(subject_counts.items(), key=lambda x: x[1])
                insights.append(f"You practice {most_practiced[0]} most frequently")
            
            return {
                "insights": insights,
                "peak_hours": [hour for hour, count in peak_hours],
                "subject_distribution": subject_counts,
                "difficulty_progression": difficulty_progression
            }
            
        except Exception as e:
            logger.error(f"Error analyzing learning patterns: {e}")
            return {"insights": ["Continue tracking your learning activities"]}
