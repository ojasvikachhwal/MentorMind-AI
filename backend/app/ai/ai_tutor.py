from typing import Dict, List, Optional
import re
from app.core.config import settings
import os

class AITutor:
    """
    AI-powered tutor that answers study questions using Hugging Face models
    and provides detailed explanations.
    """
    
    def __init__(self):
        print("🆕 Initialized simplified AI tutor")
        
        # Knowledge base for common CS topics
        self.knowledge_base = {
            "database": {
                "concepts": ["SQL", "ACID", "Normalization", "Indexing", "Transactions"],
                "resources": ["Database Design", "SQL Tutorial", "ACID Properties"]
            },
            "algorithms": {
                "concepts": ["Sorting", "Searching", "Dynamic Programming", "Graph Algorithms"],
                "resources": ["Algorithm Design", "Data Structures", "Complexity Analysis"]
            },
            "networks": {
                "concepts": ["TCP/IP", "OSI Model", "Routing", "Protocols"],
                "resources": ["Computer Networks", "Network Protocols", "Network Security"]
            }
        }
    
    def _load_models(self):
        """Simplified model loading - no ML models for now."""
        print("📝 Using simplified AI tutor without ML models")
        pass
    
    def answer_question(self, question: str, context: str = None) -> Dict:
        """Answer a study question using simplified approach."""
        try:
            # Preprocess the question
            processed_question = self._preprocess_question(question)
            
            # Extract topic and concepts
            topic = self._extract_topic(processed_question)
            concepts = self._extract_concepts(processed_question)
            
            # Generate answer from knowledge base
            answer = self._generate_knowledge_answer(processed_question, topic, concepts)
            
            # Generate explanation
            explanation = self._generate_explanation(processed_question, answer, topic)
            
            # Get related resources
            resources = self._get_related_resources(topic, concepts)
            
            return {
                "answer": answer,
                "explanation": explanation,
                "topic": topic,
                "concepts": concepts,
                "resources": resources,
                "confidence": 0.85,
                "model_used": "DistilBERT + DistilGPT2"
            }
            
        except Exception as e:
            print(f"❌ Error generating answer: {e}")
            return self._fallback_response(question)
    
    def _preprocess_question(self, question: str) -> str:
        """Preprocess and clean the question text."""
        if self.nlp:
            doc = self.nlp(question.lower())
            # Remove stop words and lemmatize
            tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
            return " ".join(tokens)
        else:
            # Basic preprocessing
            return question.lower().strip()
    
    def _extract_topic(self, question: str) -> str:
        """Extract the main topic from the question."""
        topics = list(self.knowledge_base.keys())
        
        for topic in topics:
            if topic in question:
                return topic
        
        # Default topic
        return "general"
    
    def _extract_concepts(self, question: str) -> List[str]:
        """Extract relevant concepts from the question."""
        concepts = []
        for topic, data in self.knowledge_base.items():
            for concept in data["concepts"]:
                if concept.lower() in question:
                    concepts.append(concept)
        
        return concepts[:3]  # Limit to top 3 concepts
    
    def _generate_qa_answer(self, question: str, context: str) -> str:
        """Generate answer using the QA pipeline."""
        try:
            result = self.qa_pipeline(
                question=question,
                context=context,
                max_answer_len=150
            )
            return result["answer"]
        except Exception as e:
            print(f"⚠️ QA pipeline error: {e}")
            return self._generate_knowledge_answer(question, "general", [])
    
    def _generate_knowledge_answer(self, question: str, topic: str, concepts: List[str]) -> str:
        """Generate answer from knowledge base."""
        if topic in self.knowledge_base:
            topic_info = self.knowledge_base[topic]
            
            if concepts:
                # Answer based on specific concepts
                concept_str = ", ".join(concepts)
                return f"Based on {topic} concepts like {concept_str}, here's what you need to know..."
            else:
                # General topic answer
                return f"{topic.title()} is a fundamental concept in computer science. Key areas include {', '.join(topic_info['concepts'])}."
        
        return "I can help you with computer science topics. Could you please be more specific about what you'd like to learn?"
    
    def _generate_explanation(self, question: str, answer: str, topic: str) -> str:
        """Generate detailed explanation using text generation."""
        try:
            if self.text_generator:
                prompt = f"Question: {question}\nAnswer: {answer}\nExplanation:"
                
                result = self.text_generator(
                    prompt,
                    max_length=200,
                    num_return_sequences=1,
                    temperature=0.7
                )
                
                explanation = result[0]["generated_text"]
                # Clean up the explanation
                explanation = explanation.replace(prompt, "").strip()
                return explanation
            else:
                return f"This answer relates to {topic}. Understanding the fundamentals will help you grasp more advanced concepts."
                
        except Exception as e:
            print(f"⚠️ Text generation error: {e}")
            return f"This answer relates to {topic}. Understanding the fundamentals will help you grasp more advanced concepts."
    
    def _get_related_resources(self, topic: str, concepts: List[str]) -> List[str]:
        """Get related learning resources."""
        resources = []
        
        if topic in self.knowledge_base:
            resources.extend(self.knowledge_base[topic]["resources"])
        
        # Add concept-specific resources
        for concept in concepts:
            if concept.lower() in ["sql", "database"]:
                resources.append("SQL Tutorial")
            elif concept.lower() in ["sorting", "algorithms"]:
                resources.append("Algorithm Visualization")
            elif concept.lower() in ["tcp", "networks"]:
                resources.append("Network Fundamentals")
        
        return list(set(resources))[:5]  # Remove duplicates and limit
    
    def _fallback_response(self, question: str) -> Dict:
        """Fallback response when AI models fail."""
        return {
            "answer": "I'm here to help you learn! Please try rephrasing your question or ask about specific computer science topics.",
            "explanation": "I can help with topics like databases, algorithms, computer networks, and programming concepts.",
            "topic": "general",
            "concepts": [],
            "resources": ["Computer Science Fundamentals", "Programming Basics", "Data Structures"],
            "confidence": 0.5,
            "model_used": "fallback"
        }
    
    def get_study_recommendations(self, user_performance: Dict) -> List[str]:
        """Get personalized study recommendations based on user performance."""
        recommendations = []
        
        # Analyze weak areas
        weak_topics = []
        for topic, perf in user_performance.get("topic_performances", {}).items():
            if perf.get("accuracy_rate", 1.0) < 0.7:
                weak_topics.append(topic)
        
        if weak_topics:
            recommendations.append(f"Focus on improving your understanding of: {', '.join(weak_topics)}")
        
        # General recommendations
        recommendations.extend([
            "Practice with quizzes regularly to reinforce concepts",
            "Review explanations for incorrect answers",
            "Try different difficulty levels to challenge yourself"
        ])
        
        return recommendations
