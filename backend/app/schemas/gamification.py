from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class BadgeResponse(BaseModel):
    id: int
    name: str
    description: str
    icon_url: Optional[str] = None
    earned_at: datetime
    category: str

    class Config:
        from_attributes = True

class LeaderboardResponse(BaseModel):
    user_id: int
    username: str
    score: int
    rank: int
    total_quizzes: int
    average_accuracy: float

    class Config:
        from_attributes = True

class StreakResponse(BaseModel):
    user_id: int
    current_streak: int
    longest_streak: int
    last_activity: datetime
    streak_type: str = "daily"  # daily, weekly, etc.

    class Config:
        from_attributes = True
