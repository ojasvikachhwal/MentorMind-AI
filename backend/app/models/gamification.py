from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Float, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class Badge(Base):
    __tablename__ = "badges"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    icon_url = Column(String(255), nullable=True)
    category = Column(String(50), nullable=False)  # achievement, skill, milestone
    criteria = Column(JSON, nullable=True)  # Requirements to earn badge
    points_value = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user_badges = relationship("UserBadge", back_populates="badge")
    
    def __repr__(self):
        return f"<Badge(id={self.id}, name='{self.name}', category='{self.category}')>"

class UserBadge(Base):
    __tablename__ = "user_badges"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    badge_id = Column(Integer, ForeignKey("badges.id"), nullable=False)
    earned_at = Column(DateTime(timezone=True), server_default=func.now())
    progress = Column(Float, default=100.0)  # Progress towards badge (0-100)
    
    # Relationships
    user = relationship("User", back_populates="badges")
    badge = relationship("Badge", back_populates="user_badges")
    
    def __repr__(self):
        return f"<UserBadge(id={self.id}, user_id={self.user_id}, badge_id={self.badge_id})>"

class Leaderboard(Base):
    __tablename__ = "leaderboards"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    username = Column(String(50), nullable=False)
    total_score = Column(Float, default=0.0)
    total_quizzes = Column(Integer, default=0)
    average_score = Column(Float, default=0.0)
    streak_days = Column(Integer, default=0)
    rank = Column(Integer, nullable=True)
    last_updated = Column(DateTime(timezone=True), onupdate=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User")
    
    def __repr__(self):
        return f"<Leaderboard(id={self.id}, username='{self.username}', rank={self.rank})>"

class Streak(Base):
    __tablename__ = "streaks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    current_streak = Column(Integer, default=0)
    longest_streak = Column(Integer, default=0)
    last_activity_date = Column(DateTime(timezone=True), nullable=True)
    streak_type = Column(String(50), default="daily")  # daily, weekly, monthly
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="streaks")
    
    def __repr__(self):
        return f"<Streak(id={self.id}, user_id={self.user_id}, current={self.current_streak})>"
