from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.quiz import QuizAttempt
from app.models.gamification import Badge, UserBadge, Leaderboard
from app.schemas.gamification import BadgeResponse, LeaderboardResponse

router = APIRouter()

@router.get("/badges", response_model=List[BadgeResponse])
async def get_user_badges(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get badges earned by the current user."""
    try:
        # Get user's earned badges
        user_badges = db.query(UserBadge).filter(
            UserBadge.user_id == current_user.id
        ).all()
        
        # Get badge details
        badges = []
        for user_badge in user_badges:
            badge = db.query(Badge).filter(Badge.id == user_badge.badge_id).first()
            if badge:
                badges.append(BadgeResponse(
                    id=badge.id,
                    name=badge.name,
                    description=badge.description,
                    icon=badge.icon,
                    earned_at=user_badge.earned_at
                ))
        
        # Check for new badges that should be awarded
        await check_and_award_badges(current_user, db)
        
        return badges
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching badges: {str(e)}"
        )

@router.get("/leaderboard", response_model=List[LeaderboardResponse])
async def get_leaderboard(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get the global leaderboard."""
    try:
        # Calculate scores for all users
        users = db.query(User).all()
        leaderboard_entries = []
        
        for user in users:
            # Get user's quiz attempts
            attempts = db.query(QuizAttempt).filter(
                QuizAttempt.user_id == user.id,
                QuizAttempt.completed_at.isnot(None)
            ).all()
            
            if attempts:
                # Calculate total score
                total_score = sum(attempt.score or 0 for attempt in attempts)
                average_score = total_score / len(attempts)
                
                # Calculate bonus points for streaks
                streak_bonus = calculate_streak_bonus(attempts)
                
                # Total points (average score + streak bonus)
                total_points = (average_score * 100) + streak_bonus
                
                leaderboard_entries.append(LeaderboardResponse(
                    username=user.username,
                    score=round(total_points, 1),
                    rank=0  # Will be set after sorting
                ))
        
        # Sort by score (highest first) and assign ranks
        leaderboard_entries.sort(key=lambda x: x.score, reverse=True)
        for i, entry in enumerate(leaderboard_entries):
            entry.rank = i + 1
        
        return leaderboard_entries[:20]  # Return top 20
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching leaderboard: {str(e)}"
        )

@router.get("/achievements", response_model=dict)
async def get_user_achievements(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's achievements and progress."""
    try:
        # Get user's quiz attempts
        attempts = db.query(QuizAttempt).filter(
            QuizAttempt.user_id == current_user.id,
            QuizAttempt.completed_at.isnot(None)
        ).all()
        
        if not attempts:
            return {
                "total_quizzes": 0,
                "total_questions": 0,
                "correct_answers": 0,
                "accuracy": 0.0,
                "current_streak": 0,
                "longest_streak": 0,
                "total_study_time": 0,
                "achievements": []
            }
        
        # Calculate basic stats
        total_quizzes = len(attempts)
        total_questions = sum(attempt.total_questions or 0 for attempt in attempts)
        correct_answers = sum(attempt.correct_answers or 0 for attempt in attempts)
        accuracy = correct_answers / total_questions if total_questions > 0 else 0
        
        # Calculate streaks
        current_streak = calculate_current_streak(attempts)
        longest_streak = calculate_longest_streak(attempts)
        
        # Calculate total study time
        total_study_time = sum(attempt.time_taken or 0 for attempt in attempts)
        
        # Get achievements
        achievements = get_achievements(total_quizzes, accuracy, current_streak, longest_streak, total_study_time)
        
        return {
            "total_quizzes": total_quizzes,
            "total_questions": total_questions,
            "correct_answers": correct_answers,
            "accuracy": round(accuracy * 100, 1),
            "current_streak": current_streak,
            "longest_streak": longest_streak,
            "total_study_time": total_study_time,
            "achievements": achievements
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching achievements: {str(e)}"
        )

async def check_and_award_badges(user: User, db: Session):
    """Check if user should be awarded new badges."""
    try:
        # Get user's quiz attempts
        attempts = db.query(QuizAttempt).filter(
            QuizAttempt.user_id == user.id,
            QuizAttempt.completed_at.isnot(None)
        ).all()
        
        if not attempts:
            return
        
        # Check for First Quiz badge
        if len(attempts) >= 1:
            await award_badge_if_not_earned(user.id, "First Quiz", db)
        
        # Check for Quiz Master badge (10 quizzes)
        if len(attempts) >= 10:
            await award_badge_if_not_earned(user.id, "Quiz Master", db)
        
        # Check for Perfect Score badge
        perfect_scores = [attempt for attempt in attempts if attempt.score == 1.0]
        if perfect_scores:
            await award_badge_if_not_earned(user.id, "Perfect Score", db)
        
        # Check for Streak Master badge (7-day streak)
        current_streak = calculate_current_streak(attempts)
        if current_streak >= 7:
            await award_badge_if_not_earned(user.id, "Streak Master", db)
        
        # Check for Speed Demon badge (fast completion)
        fast_attempts = [attempt for attempt in attempts if attempt.time_taken and attempt.time_taken < 300]  # Less than 5 minutes
        if fast_attempts:
            await award_badge_if_not_earned(user.id, "Speed Demon", db)
        
    except Exception as e:
        print(f"Error checking badges: {e}")

async def award_badge_if_not_earned(user_id: int, badge_name: str, db: Session):
    """Award a badge to a user if they haven't earned it yet."""
    try:
        # Check if user already has this badge
        existing_badge = db.query(UserBadge).join(Badge).filter(
            UserBadge.user_id == user_id,
            Badge.name == badge_name
        ).first()
        
        if existing_badge:
            return
        
        # Get badge
        badge = db.query(Badge).filter(Badge.name == badge_name).first()
        if not badge:
            # Create badge if it doesn't exist
            badge = Badge(
                name=badge_name,
                description=get_badge_description(badge_name),
                icon=get_badge_icon(badge_name)
            )
            db.add(badge)
            db.commit()
            db.refresh(badge)
        
        # Award badge to user
        user_badge = UserBadge(
            user_id=user_id,
            badge_id=badge.id,
            earned_at=datetime.utcnow()
        )
        db.add(user_badge)
        db.commit()
        
    except Exception as e:
        print(f"Error awarding badge: {e}")

def calculate_current_streak(attempts: List[QuizAttempt]) -> int:
    """Calculate the current learning streak."""
    if not attempts:
        return 0
    
    # Sort attempts by completion date
    sorted_attempts = sorted(attempts, key=lambda x: x.completed_at, reverse=True)
    
    current_streak = 0
    today = datetime.utcnow().date()
    
    for attempt in sorted_attempts:
        if attempt.completed_at and attempt.completed_at.date() == today - timedelta(days=current_streak):
            current_streak += 1
        else:
            break
    
    return current_streak

def calculate_longest_streak(attempts: List[QuizAttempt]) -> int:
    """Calculate the longest learning streak."""
    if not attempts:
        return 0
    
    # Sort attempts by completion date
    sorted_attempts = sorted(attempts, key=lambda x: x.completed_at)
    
    longest_streak = 0
    current_streak = 0
    last_date = None
    
    for attempt in sorted_attempts:
        if not attempt.completed_at:
            continue
        
        current_date = attempt.completed_at.date()
        
        if last_date is None or (current_date - last_date).days == 1:
            current_streak += 1
        else:
            longest_streak = max(longest_streak, current_streak)
            current_streak = 1
        
        last_date = current_date
    
    return max(longest_streak, current_streak)

def calculate_streak_bonus(attempts: List[QuizAttempt]) -> float:
    """Calculate bonus points for learning streaks."""
    current_streak = calculate_current_streak(attempts)
    return min(current_streak * 5, 50)  # Max 50 bonus points

def get_achievements(total_quizzes: int, accuracy: float, current_streak: int, longest_streak: int, study_time: int) -> List[dict]:
    """Get list of achievements based on user stats."""
    achievements = []
    
    # Quiz count achievements
    if total_quizzes >= 1:
        achievements.append({"name": "First Steps", "description": "Completed your first quiz", "earned": True})
    if total_quizzes >= 5:
        achievements.append({"name": "Getting Started", "description": "Completed 5 quizzes", "earned": True})
    if total_quizzes >= 10:
        achievements.append({"name": "Quiz Enthusiast", "description": "Completed 10 quizzes", "earned": True})
    if total_quizzes >= 25:
        achievements.append({"name": "Quiz Master", "description": "Completed 25 quizzes", "earned": True})
    
    # Accuracy achievements
    if accuracy >= 0.8:
        achievements.append({"name": "High Achiever", "description": "Maintained 80%+ accuracy", "earned": True})
    if accuracy >= 0.9:
        achievements.append({"name": "Perfectionist", "description": "Maintained 90%+ accuracy", "earned": True})
    
    # Streak achievements
    if current_streak >= 3:
        achievements.append({"name": "Consistent Learner", "description": "3-day learning streak", "earned": True})
    if current_streak >= 7:
        achievements.append({"name": "Week Warrior", "description": "7-day learning streak", "earned": True})
    if longest_streak >= 14:
        achievements.append({"name": "Dedicated Student", "description": "14-day learning streak", "earned": True})
    
    # Study time achievements
    if study_time >= 3600:  # 1 hour
        achievements.append({"name": "Time Invested", "description": "Studied for 1 hour", "earned": True})
    if study_time >= 7200:  # 2 hours
        achievements.append({"name": "Dedicated Learner", "description": "Studied for 2 hours", "earned": True})
    
    return achievements

def get_badge_description(badge_name: str) -> str:
    """Get description for a badge."""
    descriptions = {
        "First Quiz": "Completed your first quiz",
        "Quiz Master": "Completed 10 quizzes",
        "Perfect Score": "Achieved a perfect score",
        "Streak Master": "Maintained a 7-day learning streak",
        "Speed Demon": "Completed a quiz in under 5 minutes"
    }
    return descriptions.get(badge_name, "Achievement unlocked!")

def get_badge_icon(badge_name: str) -> str:
    """Get icon for a badge."""
    icons = {
        "First Quiz": "🏆",
        "Quiz Master": "👑",
        "Perfect Score": "⭐",
        "Streak Master": "🔥",
        "Speed Demon": "⚡"
    }
    return icons.get(badge_name, "🏅")
