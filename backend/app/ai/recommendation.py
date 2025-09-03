import numpy as np
from typing import Dict, List, Tuple, Optional
import pandas as pd
from collections import defaultdict

class RecommendationEngine:
    """
    AI-powered recommendation engine that suggests topics, resources, and quizzes
    based on user performance and collaborative filtering.
    """
    
    def __init__(self):
        self.user_topic_matrix = None
        self.topic_similarity_matrix = None
        self.topic_features = None
        self._initialize_recommendation_system()
    
    def _initialize_recommendation_system(self):
        """Initialize the recommendation system with sample data."""
        # Sample topic features for content-based filtering
        self.topic_features = {
            "database": {
                "difficulty": 3,
                "prerequisites": ["sql", "data_structures"],
                "related_topics": ["sql", "normalization", "indexing"],
                "category": "data_management",
                "popularity": 0.8
            },
            "algorithms": {
                "difficulty": 4,
                "prerequisites": ["programming", "mathematics"],
                "related_topics": ["sorting", "searching", "dynamic_programming"],
                "category": "computer_science",
                "popularity": 0.9
            },
            "networks": {
                "difficulty": 3,
                "prerequisites": ["computer_basics"],
                "related_topics": ["tcp_ip", "osi_model", "routing"],
                "category": "systems",
                "popularity": 0.7
            },
            "dynamic_programming": {
                "difficulty": 5,
                "prerequisites": ["algorithms", "recursion"],
                "related_topics": ["memoization", "optimization", "algorithms"],
                "category": "computer_science",
                "popularity": 0.6
            },
            "oop": {
                "difficulty": 2,
                "prerequisites": ["programming"],
                "related_topics": ["classes", "inheritance", "polymorphism"],
                "category": "programming",
                "popularity": 0.8
            },
            "operating_systems": {
                "difficulty": 4,
                "prerequisites": ["computer_basics", "algorithms"],
                "related_topics": ["processes", "memory", "file_systems"],
                "category": "systems",
                "popularity": 0.7
            },
            "coding_practice": {
                "difficulty": 2,
                "prerequisites": ["programming"],
                "related_topics": ["problem_solving", "algorithms", "data_structures"],
                "category": "programming",
                "popularity": 0.9
            }
        }
        
        # Calculate topic similarity matrix
        self._calculate_topic_similarity()
    
    def _calculate_topic_similarity(self):
        """Calculate similarity between topics using simplified approach."""
        try:
            # Create a simple similarity matrix based on shared features
            topic_names = list(self.topic_features.keys())
            n_topics = len(topic_names)
            self.topic_similarity_matrix = np.zeros((n_topics, n_topics))
            
            for i, topic1 in enumerate(topic_names):
                for j, topic2 in enumerate(topic_names):
                    if i == j:
                        self.topic_similarity_matrix[i][j] = 1.0
                    else:
                        # Simple similarity based on shared category and difficulty
                        features1 = self.topic_features[topic1]
                        features2 = self.topic_features[topic2]
                        
                        # Category similarity
                        category_sim = 1.0 if features1['category'] == features2['category'] else 0.3
                        
                        # Difficulty similarity (closer difficulty = higher similarity)
                        difficulty_diff = abs(features1['difficulty'] - features2['difficulty'])
                        difficulty_sim = max(0, 1.0 - difficulty_diff / 5.0)
                        
                        # Combined similarity
                        self.topic_similarity_matrix[i][j] = (category_sim + difficulty_sim) / 2
            
            print("✅ Topic similarity matrix calculated (simplified)")
            
        except Exception as e:
            print(f"❌ Error calculating topic similarity: {e}")
            self.topic_similarity_matrix = None
    
    def get_topic_recommendations(self, user_id: int, user_performance: Dict, 
                                num_recommendations: int = 5) -> List[Dict]:
        """
        Get personalized topic recommendations based on user performance.
        
        Args:
            user_id: User ID
            user_performance: User's performance data
            num_recommendations: Number of recommendations to return
        
        Returns:
            List of recommended topics with scores
        """
        try:
            # Get user's topic performance
            topic_performances = user_performance.get("topic_performances", {})
            
            # Calculate recommendation scores
            topic_scores = []
            
            for topic, features in self.topic_features.items():
                score = self._calculate_topic_score(topic, features, topic_performances, user_performance)
                topic_scores.append({
                    "topic": topic,
                    "score": score,
                    "difficulty": features["difficulty"],
                    "category": features["category"],
                    "prerequisites": features["prerequisites"],
                    "related_topics": features["related_topics"]
                })
            
            # Sort by score and return top recommendations
            topic_scores.sort(key=lambda x: x["score"], reverse=True)
            
            # Filter out topics user has already mastered
            filtered_recommendations = []
            for rec in topic_scores:
                if rec["topic"] not in topic_performances or \
                   topic_performances[rec["topic"]].get("accuracy_rate", 0) < 0.9:
                    filtered_recommendations.append(rec)
                    if len(filtered_recommendations) >= num_recommendations:
                        break
            
            return filtered_recommendations
            
        except Exception as e:
            print(f"❌ Error generating topic recommendations: {e}")
            return self._get_fallback_recommendations()
    
    def _calculate_topic_score(self, topic: str, features: Dict, 
                             topic_performances: Dict, user_performance: Dict) -> float:
        """Calculate recommendation score for a topic."""
        score = 0.0
        
        # Base popularity score
        score += features["popularity"] * 0.3
        
        # Difficulty match with user level
        user_level = user_performance.get("overall_score", 0.5) * 5  # Scale to 1-5
        difficulty_match = 1.0 - abs(features["difficulty"] - user_level) / 5.0
        score += difficulty_match * 0.4
        
        # Prerequisite satisfaction
        prereq_score = self._calculate_prerequisite_score(features["prerequisites"], topic_performances)
        score += prereq_score * 0.2
        
        # Topic diversity (avoid recommending similar topics)
        diversity_score = self._calculate_diversity_score(topic, topic_performances)
        score += diversity_score * 0.1
        
        return score
    
    def _calculate_prerequisite_score(self, prerequisites: List[str], topic_performances: Dict) -> float:
        """Calculate how well user satisfies topic prerequisites."""
        if not prerequisites:
            return 1.0
        
        satisfied_prereqs = 0
        for prereq in prerequisites:
            if prereq in topic_performances:
                accuracy = topic_performances[prereq].get("accuracy_rate", 0)
                if accuracy >= 0.7:  # Consider 70%+ as satisfied
                    satisfied_prereqs += 1
        
        return satisfied_prereqs / len(prerequisites)
    
    def _calculate_diversity_score(self, topic: str, topic_performances: Dict) -> float:
        """Calculate diversity score to avoid recommending similar topics."""
        if not self.topic_similarity_matrix or topic not in self.topic_features:
            return 0.5
        
        topic_names = list(self.topic_features.keys())
        if topic not in topic_names:
            return 0.5
        
        topic_idx = topic_names.index(topic)
        
        # Calculate average similarity with topics user has studied
        studied_topics = list(topic_performances.keys())
        if not studied_topics:
            return 1.0  # No studied topics, high diversity
        
        similarities = []
        for studied_topic in studied_topics:
            if studied_topic in topic_names:
                studied_idx = topic_names.index(studied_topic)
                similarity = self.topic_similarity_matrix[topic_idx][studied_idx]
                similarities.append(similarity)
        
        if similarities:
            avg_similarity = np.mean(similarities)
            # Lower similarity = higher diversity
            diversity_score = 1.0 - avg_similarity
            return max(0.0, diversity_score)
        
        return 0.5
    
    def get_quiz_recommendations(self, user_id: int, user_performance: Dict,
                                available_quizzes: List[Dict], num_recommendations: int = 3) -> List[Dict]:
        """
        Get personalized quiz recommendations.
        
        Args:
            user_id: User ID
            user_performance: User's performance data
            available_quizzes: List of available quizzes
            num_recommendations: Number of recommendations to return
        
        Returns:
            List of recommended quizzes
        """
        try:
            quiz_scores = []
            
            for quiz in available_quizzes:
                score = self._calculate_quiz_score(quiz, user_performance)
                quiz_scores.append({
                    **quiz,
                    "recommendation_score": score
                })
            
            # Sort by score and return top recommendations
            quiz_scores.sort(key=lambda x: x["recommendation_score"], reverse=True)
            return quiz_scores[:num_recommendations]
            
        except Exception as e:
            print(f"❌ Error generating quiz recommendations: {e}")
            return available_quizzes[:num_recommendations] if available_quizzes else []
    
    def _calculate_quiz_score(self, quiz: Dict, user_performance: Dict) -> float:
        """Calculate recommendation score for a quiz."""
        score = 0.0
        
        # Topic relevance
        topic = quiz.get("topic", "")
        topic_performances = user_performance.get("topic_performances", {})
        
        if topic in topic_performances:
            # User has studied this topic
            accuracy = topic_performances[topic].get("accuracy_rate", 0.5)
            if accuracy < 0.7:
                # User needs practice in this topic
                score += 0.4
            else:
                # User is good at this topic, moderate score
                score += 0.2
        else:
            # New topic, moderate score
            score += 0.3
        
        # Difficulty match
        quiz_difficulty = quiz.get("difficulty_level", "medium")
        user_level = user_performance.get("overall_score", 0.5)
        
        if quiz_difficulty == "easy" and user_level < 0.4:
            score += 0.3
        elif quiz_difficulty == "medium" and 0.3 <= user_level <= 0.7:
            score += 0.3
        elif quiz_difficulty == "hard" and user_level > 0.6:
            score += 0.3
        
        # Quiz popularity/quality (if available)
        if quiz.get("is_popular", False):
            score += 0.1
        
        return score
    
    def get_resource_recommendations(self, topic: str, user_level: float) -> List[Dict]:
        """
        Get learning resource recommendations for a topic.
        
        Args:
            topic: Topic name
            user_level: User's proficiency level (0-1)
        
        Returns:
            List of recommended resources
        """
        resources = []
        
        # Base resources for the topic
        if topic in self.topic_features:
            topic_info = self.topic_features[topic]
            
            # Add topic-specific resources
            if topic == "database":
                resources.extend([
                    {"name": "SQL Tutorial", "type": "tutorial", "level": "beginner"},
                    {"name": "Database Design Principles", "type": "article", "level": "intermediate"},
                    {"name": "ACID Properties Explained", "type": "video", "level": "beginner"}
                ])
            elif topic == "algorithms":
                resources.extend([
                    {"name": "Algorithm Visualization", "type": "interactive", "level": "beginner"},
                    {"name": "Data Structures Guide", "type": "tutorial", "level": "intermediate"},
                    {"name": "Complexity Analysis", "type": "article", "level": "advanced"}
                ])
            elif topic == "networks":
                resources.extend([
                    {"name": "Network Fundamentals", "type": "course", "level": "beginner"},
                    {"name": "TCP/IP Deep Dive", "type": "tutorial", "level": "intermediate"},
                    {"name": "Network Security", "type": "article", "level": "advanced"}
                ])
        
        # Filter resources by user level
        filtered_resources = []
        for resource in resources:
            if user_level < 0.3 and resource["level"] == "beginner":
                filtered_resources.append(resource)
            elif 0.3 <= user_level <= 0.7 and resource["level"] in ["beginner", "intermediate"]:
                filtered_resources.append(resource)
            elif user_level > 0.7:
                filtered_resources.append(resource)
        
        return filtered_resources[:5]  # Limit to 5 resources
    
    def _get_fallback_recommendations(self) -> List[Dict]:
        """Get fallback recommendations when main system fails."""
        return [
            {
                "topic": "database",
                "score": 0.8,
                "difficulty": 3,
                "category": "data_management",
                "prerequisites": ["sql", "data_structures"],
                "related_topics": ["sql", "normalization", "indexing"]
            },
            {
                "topic": "algorithms",
                "score": 0.7,
                "difficulty": 4,
                "category": "computer_science",
                "prerequisites": ["programming", "mathematics"],
                "related_topics": ["sorting", "searching", "dynamic_programming"]
            }
        ]
    
    def update_user_preferences(self, user_id: int, topic_interactions: Dict):
        """Update user preferences based on interactions."""
        # This would typically update the recommendation model
        # For now, just log the interaction
        print(f"📊 Updated preferences for user {user_id}: {topic_interactions}")
    
    def get_collaborative_recommendations(self, user_id: int, similar_users: List[int]) -> List[Dict]:
        """
        Get recommendations based on similar users (collaborative filtering).
        
        Args:
            user_id: Current user ID
            similar_users: List of similar user IDs
        
        Returns:
            List of collaborative recommendations
        """
        # This would implement collaborative filtering
        # For now, return empty list
        return []
