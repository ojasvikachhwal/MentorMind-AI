import numpy as np
from typing import List, Dict, Tuple, Optional
import os
from app.core.config import settings

class AdaptiveQuizEngine:
    """
    AI-powered adaptive quiz engine that adjusts question difficulty
    based on user performance patterns.
    """
    
    def __init__(self):
        print("🆕 Initialized simplified adaptive quiz engine")
    
    def _load_or_create_model(self):
        """Simplified model loading - no ML model for now."""
        pass
    
    def _create_new_model(self):
        """Simplified model creation - no ML model for now."""
        pass
    
    def extract_features(self, user_performance: Dict) -> np.ndarray:
        """Extract features from user performance data."""
        features = [
            user_performance.get('overall_score', 0.0),
            user_performance.get('average_time_per_question', 0.0),
            user_performance.get('current_streak', 0),
            user_performance.get('total_quizzes_taken', 0),
            user_performance.get('accuracy_rate', 0.0),
            user_performance.get('difficulty_preference', 1.0)
        ]
        return np.array(features).reshape(1, -1)
    
    def predict_difficulty_adjustment(self, user_performance: Dict) -> float:
        """Predict the optimal difficulty adjustment factor using simple heuristics."""
        try:
            overall_score = user_performance.get('overall_score', 0.5)
            accuracy_rate = user_performance.get('accuracy_rate', 0.5)
            
            # Simple heuristic: if user is doing well, increase difficulty; if struggling, decrease
            if overall_score > 0.8 and accuracy_rate > 0.8:
                return 1.2  # Increase difficulty
            elif overall_score < 0.4 or accuracy_rate < 0.4:
                return 0.8  # Decrease difficulty
            else:
                return 1.0  # Keep current difficulty
        except Exception as e:
            print(f"⚠️ Error predicting difficulty: {e}")
            return 1.0  # Default to no adjustment
    
    def select_next_question(self, available_questions: List[Dict], 
                           user_performance: Dict, 
                           current_difficulty: float) -> Optional[Dict]:
        """Select the next question based on adaptive difficulty."""
        if not available_questions:
            return None
        
        # Calculate target difficulty
        target_difficulty = current_difficulty * self.predict_difficulty_adjustment(user_performance)
        
        # Score questions based on difficulty match and other factors
        question_scores = []
        for question in available_questions:
            difficulty_diff = abs(question['difficulty_score'] - target_difficulty)
            topic_relevance = self._calculate_topic_relevance(question, user_performance)
            
            # Combined score (lower is better)
            score = difficulty_diff * 0.7 + (1 - topic_relevance) * 0.3
            question_scores.append((score, question))
        
        # Sort by score and return the best match
        question_scores.sort(key=lambda x: x[0])
        return question_scores[0][1]
    
    def _calculate_topic_relevance(self, question: Dict, user_performance: Dict) -> float:
        """Calculate how relevant a question topic is to the user."""
        topic = question.get('topic', '')
        topic_performances = user_performance.get('topic_performances', {})
        
        if topic in topic_performances:
            # Higher accuracy means more relevant (user is good at this topic)
            return topic_performances[topic].get('accuracy_rate', 0.5)
        else:
            # New topic, medium relevance
            return 0.5
    
    def update_model(self, training_data: List[Dict]):
        """Update the model with new training data."""
        try:
            X = []
            y = []
            
            for data_point in training_data:
                features = self.extract_features(data_point['performance'])
                X.append(features.flatten())
                y.append(data_point['optimal_difficulty'])
            
            X = np.array(X)
            y = np.array(y)
            
            # Fit scaler and model
            self.scaler.fit(X)
            X_scaled = self.scaler.transform(X)
            self.model.fit(X_scaled, y)
            
            # Save updated model
            joblib.dump(self.model, self.model_path)
            joblib.dump(self.scaler, self.scaler_path)
            
            print("✅ Model updated successfully")
        except Exception as e:
            print(f"❌ Error updating model: {e}")
    
    def get_difficulty_recommendation(self, user_id: int, topic: str) -> Dict:
        """Get personalized difficulty recommendations for a topic."""
        # This would typically fetch user performance from database
        # For now, return default recommendations
        return {
            'recommended_difficulty': 1.0,
            'confidence': 0.8,
            'reason': 'Based on overall performance patterns'
        }
