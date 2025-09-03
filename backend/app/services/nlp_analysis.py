"""
NLP Analysis Service for Question Difficulty Classification and Tag Extraction.
Built to be modular and easily extensible for Hugging Face models later.
"""

import re
import logging
from typing import List, Dict, Optional, Any
from dataclasses import dataclass
import spacy
from textblob import TextBlob
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class QuestionAnalysis:
    """Data class for question analysis results."""
    question_text: str
    difficulty: str
    tags: List[str]
    confidence: float
    analysis_method: str
    word_count: int
    complexity_score: float

class QuestionAnalyzer:
    """
    Question Analyzer for difficulty classification and tag extraction.
    
    Features:
    - Rule-based difficulty classification
    - NLP-based tag extraction using spaCy
    - Extensible architecture for ML models
    - Configurable difficulty thresholds
    """
    
    def __init__(
        self, 
        future_model: Optional[Any] = None,
        difficulty_thresholds: Optional[Dict[str, int]] = None,
        use_ml: bool = False
    ):
        """
        Initialize the QuestionAnalyzer.
        
        Args:
            future_model: Future ML model (Hugging Face, etc.)
            difficulty_thresholds: Custom thresholds for difficulty classification
            use_ml: Whether to use ML model instead of rule-based
        """
        self.future_model = future_model
        self.use_ml = use_ml
        
        # Default difficulty thresholds (word count)
        self.difficulty_thresholds = difficulty_thresholds or {
            "easy": 15,
            "medium": 30,
            "hard": 50
        }
        
        # Initialize NLP components
        self._initialize_nlp()
        
        # Subject-specific keywords for better tagging
        self.subject_keywords = {
            "mathematics": [
                "algebra", "geometry", "calculus", "trigonometry", "statistics",
                "equation", "function", "derivative", "integral", "theorem",
                "proof", "solve", "calculate", "graph", "formula"
            ],
            "physics": [
                "force", "energy", "velocity", "acceleration", "momentum",
                "wave", "particle", "field", "quantum", "relativity",
                "motion", "gravity", "electricity", "magnetism", "thermodynamics"
            ],
            "computer_science": [
                "algorithm", "data_structure", "programming", "database",
                "network", "software", "hardware", "artificial_intelligence",
                "machine_learning", "web_development", "cybersecurity"
            ],
            "chemistry": [
                "molecule", "reaction", "element", "compound", "acid",
                "base", "organic", "inorganic", "biochemistry", "analytical"
            ]
        }
    
    def _initialize_nlp(self):
        """Initialize NLP components."""
        try:
            # Try to load spaCy model
            self.nlp = spacy.load("en_core_web_sm")
            logger.info("spaCy model loaded successfully")
        except OSError:
            logger.warning("spaCy model not found. Installing en_core_web_sm...")
            try:
                import subprocess
                subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"], check=True)
                self.nlp = spacy.load("en_core_web_sm")
                logger.info("spaCy model installed and loaded successfully")
            except Exception as e:
                logger.error(f"Failed to load spaCy model: {e}")
                self.nlp = None
        
        # Download NLTK data
        try:
            nltk.download('punkt', quiet=True)
            nltk.download('stopwords', quiet=True)
            nltk.download('averaged_perceptron_tagger', quiet=True)
            self.stop_words = set(stopwords.words('english'))
            logger.info("NLTK components loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load NLTK components: {e}")
            self.stop_words = set()
    
    def analyze_question(
        self, 
        question_text: str, 
        subject: Optional[str] = None
    ) -> QuestionAnalysis:
        """
        Analyze a question to determine difficulty and extract tags.
        
        Args:
            question_text: The question text to analyze
            subject: Optional subject for context-aware analysis
            
        Returns:
            QuestionAnalysis object with results
        """
        try:
            # Clean and preprocess the text
            cleaned_text = self._preprocess_text(question_text)
            word_count = len(cleaned_text.split())
            
            # Classify difficulty
            if self.use_ml and self.future_model:
                difficulty, confidence = self._classify_difficulty_ml(cleaned_text)
                analysis_method = "ml_model"
            else:
                difficulty, confidence = self._classify_difficulty_rule_based(cleaned_text, word_count)
                analysis_method = "rule_based"
            
            # Extract tags
            tags = self._extract_tags(cleaned_text, subject)
            
            # Calculate complexity score
            complexity_score = self._calculate_complexity_score(cleaned_text, word_count, tags)
            
            return QuestionAnalysis(
                question_text=question_text,
                difficulty=difficulty,
                tags=tags,
                confidence=confidence,
                analysis_method=analysis_method,
                word_count=word_count,
                complexity_score=complexity_score
            )
            
        except Exception as e:
            logger.error(f"Error analyzing question: {e}")
            # Return fallback analysis
            return QuestionAnalysis(
                question_text=question_text,
                difficulty="medium",
                tags=["general"],
                confidence=0.5,
                analysis_method="fallback",
                word_count=len(question_text.split()),
                complexity_score=0.5
            )
    
    def _preprocess_text(self, text: str) -> str:
        """Preprocess text for analysis."""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Remove special characters but keep mathematical symbols
        text = re.sub(r'[^\w\s\+\-\*\/\=\<\>\(\)\[\]\{\}\.\,\!\?]', '', text)
        
        return text.lower()
    
    def _classify_difficulty_rule_based(self, text: str, word_count: int) -> tuple[str, float]:
        """
        Rule-based difficulty classification.
        
        Args:
            text: Preprocessed question text
            word_count: Number of words in the question
            
        Returns:
            Tuple of (difficulty, confidence)
        """
        # Base difficulty on word count
        if word_count <= self.difficulty_thresholds["easy"]:
            base_difficulty = "easy"
            base_confidence = 0.8
        elif word_count <= self.difficulty_thresholds["medium"]:
            base_difficulty = "medium"
            base_confidence = 0.7
        else:
            base_difficulty = "hard"
            base_confidence = 0.8
        
        # Adjust based on content complexity
        complexity_indicators = self._analyze_content_complexity(text)
        
        # Adjust difficulty based on complexity indicators
        adjusted_difficulty, confidence_adjustment = self._adjust_difficulty(
            base_difficulty, base_confidence, complexity_indicators
        )
        
        return adjusted_difficulty, confidence_adjustment
    
    def _analyze_content_complexity(self, text: str) -> Dict[str, float]:
        """Analyze content complexity indicators."""
        indicators = {
            "mathematical_symbols": 0.0,
            "technical_terms": 0.0,
            "question_complexity": 0.0,
            "syntactic_complexity": 0.0
        }
        
        # Mathematical symbols
        math_symbols = len(re.findall(r'[\+\-\*\/\=\<\>\(\)\[\]\{\}]', text))
        indicators["mathematical_symbols"] = min(math_symbols / 10.0, 1.0)
        
        # Technical terms (words longer than 8 characters)
        long_words = len([word for word in text.split() if len(word) > 8])
        indicators["technical_terms"] = min(long_words / 5.0, 1.0)
        
        # Question complexity (multiple clauses, conjunctions)
        clauses = len(re.findall(r'\band\b|\bor\b|\bbut\b|\bbecause\b', text))
        indicators["question_complexity"] = min(clauses / 3.0, 1.0)
        
        # Syntactic complexity (punctuation, structure)
        punctuation = len(re.findall(r'[,\;:]', text))
        indicators["syntactic_complexity"] = min(punctuation / 5.0, 1.0)
        
        return indicators
    
    def _adjust_difficulty(
        self, 
        base_difficulty: str, 
        base_confidence: float, 
        complexity_indicators: Dict[str, float]
    ) -> tuple[str, float]:
        """Adjust difficulty based on complexity indicators."""
        # Calculate overall complexity score
        complexity_score = sum(complexity_indicators.values()) / len(complexity_indicators)
        
        # Difficulty mapping
        difficulty_levels = ["easy", "medium", "hard"]
        current_index = difficulty_levels.index(base_difficulty)
        
        # Adjust based on complexity
        if complexity_score > 0.6 and current_index < 2:
            adjusted_difficulty = difficulty_levels[current_index + 1]
            confidence_adjustment = base_confidence * 0.9  # Slightly lower confidence
        elif complexity_score < 0.3 and current_index > 0:
            adjusted_difficulty = difficulty_levels[current_index - 1]
            confidence_adjustment = base_confidence * 0.9
        else:
            adjusted_difficulty = base_difficulty
            confidence_adjustment = base_confidence
        
        return adjusted_difficulty, confidence_adjustment
    
    def _classify_difficulty_ml(self, text: str) -> tuple[str, float]:
        """
        ML-based difficulty classification (placeholder for future implementation).
        
        Args:
            text: Preprocessed question text
            
        Returns:
            Tuple of (difficulty, confidence)
        """
        if not self.future_model:
            logger.warning("ML model not available, falling back to rule-based")
            return self._classify_difficulty_rule_based(text, len(text.split()))
        
        try:
            # This is where Hugging Face model would be used
            # For now, return rule-based as fallback
            logger.info("ML model available but not implemented yet")
            return self._classify_difficulty_rule_based(text, len(text.split()))
        except Exception as e:
            logger.error(f"ML model inference failed: {e}")
            return self._classify_difficulty_rule_based(text, len(text.split()))
    
    def _extract_tags(self, text: str, subject: Optional[str] = None) -> List[str]:
        """
        Extract tags from question text using NLP.
        
        Args:
            text: Preprocessed question text
            subject: Optional subject for context-aware tagging
            
        Returns:
            List of extracted tags
        """
        tags = set()
        
        try:
            # Use spaCy for NLP analysis
            if self.nlp:
                doc = self.nlp(text)
                
                # Extract nouns and proper nouns
                for token in doc:
                    if token.pos_ in ["NOUN", "PROPN"] and len(token.text) > 2:
                        # Clean the token
                        clean_token = re.sub(r'[^\w]', '', token.text.lower())
                        if clean_token and clean_token not in self.stop_words:
                            tags.add(clean_token)
                
                # Extract noun chunks
                for chunk in doc.noun_chunks:
                    clean_chunk = re.sub(r'[^\w\s]', '', chunk.text.lower()).strip()
                    if clean_chunk and len(clean_chunk) > 2:
                        tags.add(clean_chunk)
            
            # Use TextBlob for additional keyword extraction
            try:
                blob = TextBlob(text)
                # Extract noun phrases
                for phrase in blob.noun_phrases:
                    clean_phrase = re.sub(r'[^\w\s]', '', phrase.lower()).strip()
                    if clean_phrase and len(clean_phrase) > 2:
                        tags.add(clean_phrase)
            except Exception as e:
                logger.warning(f"TextBlob analysis failed: {e}")
            
            # Add subject-specific keywords if available
            if subject and subject.lower() in self.subject_keywords:
                subject_keywords = self.subject_keywords[subject.lower()]
                # Check if any subject keywords appear in the text
                for keyword in subject_keywords:
                    if keyword.lower() in text.lower():
                        tags.add(keyword)
            
            # Filter and clean tags
            filtered_tags = []
            for tag in tags:
                # Remove very short tags
                if len(tag) >= 3:
                    # Clean tag
                    clean_tag = re.sub(r'[^\w]', '', tag.lower())
                    if clean_tag and clean_tag not in self.stop_words:
                        filtered_tags.append(clean_tag)
            
            # Limit number of tags
            return filtered_tags[:10] if filtered_tags else ["general"]
            
        except Exception as e:
            logger.error(f"Tag extraction failed: {e}")
            return ["general"]
    
    def _calculate_complexity_score(self, text: str, word_count: int, tags: List[str]) -> float:
        """
        Calculate a complexity score for the question.
        
        Args:
            text: Preprocessed question text
            word_count: Number of words
            tags: Extracted tags
            
        Returns:
            Complexity score between 0 and 1
        """
        # Base score from word count
        word_score = min(word_count / 50.0, 1.0)
        
        # Tag diversity score
        tag_score = min(len(tags) / 10.0, 1.0)
        
        # Mathematical complexity score
        math_score = len(re.findall(r'[\+\-\*\/\=\<\>\(\)\[\]\{\}]', text)) / 20.0
        
        # Syntactic complexity
        syntactic_score = len(re.findall(r'[,\;:]', text)) / 10.0
        
        # Calculate weighted average
        complexity_score = (
            word_score * 0.3 +
            tag_score * 0.2 +
            math_score * 0.3 +
            syntactic_score * 0.2
        )
        
        return min(complexity_score, 1.0)
    
    def batch_analyze(self, questions: List[Dict[str, str]]) -> List[QuestionAnalysis]:
        """
        Analyze multiple questions in batch.
        
        Args:
            questions: List of question dictionaries with 'text' and optional 'subject'
            
        Returns:
            List of QuestionAnalysis objects
        """
        results = []
        for question in questions:
            text = question.get('text', '')
            subject = question.get('subject')
            analysis = self.analyze_question(text, subject)
            results.append(analysis)
        return results
    
    def update_model(self, new_model: Any):
        """
        Update the ML model for future use.
        
        Args:
            new_model: New ML model (e.g., Hugging Face model)
        """
        self.future_model = new_model
        self.use_ml = True
        logger.info("ML model updated successfully")
    
    def get_analysis_stats(self) -> Dict[str, Any]:
        """Get statistics about the analyzer."""
        return {
            "analysis_method": "ml_model" if self.use_ml else "rule_based",
            "ml_model_available": self.future_model is not None,
            "difficulty_thresholds": self.difficulty_thresholds,
            "nlp_components": {
                "spacy_loaded": self.nlp is not None,
                "nltk_loaded": len(self.stop_words) > 0
            }
        }
