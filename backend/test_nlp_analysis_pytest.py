#!/usr/bin/env python3
"""
Pytest test suite for the NLP analysis system.
Run with: pytest test_nlp_analysis_pytest.py -v
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from app.services.nlp_analysis import QuestionAnalyzer, QuestionAnalysis
from app.schemas.question_analysis import (
    QuestionAnalysisRequest, QuestionAnalysisResponse,
    BatchQuestionAnalysisRequest
)

class TestQuestionAnalyzer:
    """Test cases for the QuestionAnalyzer class."""
    
    @pytest.fixture
    def analyzer(self):
        """Create a QuestionAnalyzer instance for testing."""
        return QuestionAnalyzer()
    
    @pytest.fixture
    def mock_nlp(self):
        """Create a mock spaCy NLP object."""
        mock_nlp = Mock()
        mock_doc = Mock()
        mock_token = Mock()
        mock_chunk = Mock()
        
        # Configure mock token
        mock_token.pos_ = "NOUN"
        mock_token.text = "mathematics"
        
        # Configure mock chunk
        mock_chunk.text = "algebra problem"
        
        # Configure mock document
        mock_doc.__iter__ = lambda self: iter([mock_token])
        mock_doc.noun_chunks = [mock_chunk]
        
        # Configure mock NLP
        mock_nlp.return_value = mock_doc
        
        return mock_nlp
    
    def test_init(self, analyzer):
        """Test QuestionAnalyzer initialization."""
        assert analyzer.future_model is None
        assert analyzer.use_ml is False
        assert "easy" in analyzer.difficulty_thresholds
        assert "medium" in analyzer.difficulty_thresholds
        assert "hard" in analyzer.difficulty_thresholds
        assert "mathematics" in analyzer.subject_keywords
    
    def test_init_with_custom_thresholds(self):
        """Test initialization with custom difficulty thresholds."""
        custom_thresholds = {"easy": 10, "medium": 20, "hard": 30}
        analyzer = QuestionAnalyzer(difficulty_thresholds=custom_thresholds)
        
        assert analyzer.difficulty_thresholds == custom_thresholds
    
    def test_init_with_future_model(self):
        """Test initialization with future ML model."""
        mock_model = Mock()
        analyzer = QuestionAnalyzer(future_model=mock_model, use_ml=True)
        
        assert analyzer.future_model == mock_model
        assert analyzer.use_ml is True
    
    def test_preprocess_text(self, analyzer):
        """Test text preprocessing."""
        text = "  Hello, World!  This is a test.  "
        cleaned = analyzer._preprocess_text(text)
        
        assert cleaned == "hello world this is a test"
        assert "  " not in cleaned  # No double spaces
    
    def test_preprocess_text_with_math_symbols(self, analyzer):
        """Test text preprocessing preserves mathematical symbols."""
        text = "Solve: 2x + 5 = 15, where x > 0"
        cleaned = analyzer._preprocess_text(text)
        
        assert "2x" in cleaned
        assert "+" in cleaned
        assert "=" in cleaned
        assert ">" in cleaned
    
    def test_classify_difficulty_rule_based_easy(self, analyzer):
        """Test rule-based difficulty classification for easy questions."""
        text = "What is 2 + 2?"
        word_count = len(text.split())
        
        difficulty, confidence = analyzer._classify_difficulty_rule_based(text, word_count)
        
        assert difficulty == "easy"
        assert confidence > 0.5
    
    def test_classify_difficulty_rule_based_medium(self, analyzer):
        """Test rule-based difficulty classification for medium questions."""
        text = "Solve the quadratic equation x² + 5x + 6 = 0 using the quadratic formula and explain your reasoning step by step"
        word_count = len(text.split())
        
        difficulty, confidence = analyzer._classify_difficulty_rule_based(text, word_count)
        
        assert difficulty == "medium"
        assert confidence > 0.5
    
    def test_classify_difficulty_rule_based_hard(self, analyzer):
        """Test rule-based difficulty classification for hard questions."""
        text = "Calculate the definite integral of the function f(x) = sin(x)cos(x) from x = 0 to x = π/2, showing all steps and using appropriate trigonometric identities, and then verify your result using a different method"
        word_count = len(text.split())
        
        difficulty, confidence = analyzer._classify_difficulty_rule_based(text, word_count)
        
        assert difficulty == "hard"
        assert confidence > 0.5
    
    def test_analyze_content_complexity(self, analyzer):
        """Test content complexity analysis."""
        text = "Solve the equation 2x + 5 = 15, but first explain why this is a linear equation and then find the value of x"
        
        indicators = analyzer._analyze_content_complexity(text)
        
        assert "mathematical_symbols" in indicators
        assert "technical_terms" in indicators
        assert "question_complexity" in indicators
        assert "syntactic_complexity" in indicators
        
        # All indicators should be between 0 and 1
        for value in indicators.values():
            assert 0.0 <= value <= 1.0
    
    def test_adjust_difficulty_increase(self, analyzer):
        """Test difficulty adjustment that increases level."""
        base_difficulty = "easy"
        base_confidence = 0.8
        complexity_indicators = {
            "mathematical_symbols": 0.8,
            "technical_terms": 0.7,
            "question_complexity": 0.9,
            "syntactic_complexity": 0.6
        }
        
        adjusted_difficulty, confidence = analyzer._adjust_difficulty(
            base_difficulty, base_confidence, complexity_indicators
        )
        
        assert adjusted_difficulty == "medium"
        assert confidence < base_confidence  # Confidence should decrease
    
    def test_adjust_difficulty_decrease(self, analyzer):
        """Test difficulty adjustment that decreases level."""
        base_difficulty = "hard"
        base_confidence = 0.8
        complexity_indicators = {
            "mathematical_symbols": 0.1,
            "technical_terms": 0.2,
            "question_complexity": 0.1,
            "syntactic_complexity": 0.2
        }
        
        adjusted_difficulty, confidence = analyzer._adjust_difficulty(
            base_difficulty, base_confidence, complexity_indicators
        )
        
        assert adjusted_difficulty == "medium"
        assert confidence < base_confidence  # Confidence should decrease
    
    def test_adjust_difficulty_no_change(self, analyzer):
        """Test difficulty adjustment that doesn't change level."""
        base_difficulty = "medium"
        base_confidence = 0.8
        complexity_indicators = {
            "mathematical_symbols": 0.4,
            "technical_terms": 0.5,
            "question_complexity": 0.3,
            "syntactic_complexity": 0.4
        }
        
        adjusted_difficulty, confidence = analyzer._adjust_difficulty(
            base_difficulty, base_confidence, complexity_indicators
        )
        
        assert adjusted_difficulty == base_difficulty
        assert confidence == base_confidence
    
    @patch('app.services.nlp_analysis.spacy.load')
    def test_extract_tags_with_spacy(self, mock_spacy_load, analyzer):
        """Test tag extraction using spaCy."""
        # Mock spaCy document
        mock_doc = Mock()
        mock_token = Mock()
        mock_chunk = Mock()
        
        mock_token.pos_ = "NOUN"
        mock_token.text = "equation"
        mock_chunk.text = "algebra problem"
        
        mock_doc.__iter__ = lambda self: iter([mock_token])
        mock_doc.noun_chunks = [mock_chunk]
        
        mock_spacy_load.return_value = Mock(return_value=mock_doc)
        
        # Reinitialize analyzer to use mock spaCy
        analyzer._initialize_nlp()
        
        text = "Solve the equation for x"
        tags = analyzer._extract_tags(text, "mathematics")
        
        assert "equation" in tags
        assert "algebra problem" in tags
    
    def test_extract_tags_without_spacy(self, analyzer):
        """Test tag extraction when spaCy is not available."""
        # Set spaCy to None
        analyzer.nlp = None
        
        text = "Solve the equation for x"
        tags = analyzer._extract_tags(text, "mathematics")
        
        # Should still return some tags (fallback)
        assert isinstance(tags, list)
        assert len(tags) > 0
    
    def test_extract_tags_with_subject_keywords(self, analyzer):
        """Test tag extraction includes subject-specific keywords."""
        text = "Solve the quadratic equation using the formula"
        
        tags = analyzer._extract_tags(text, "mathematics")
        
        # Should include subject-specific keywords that appear in text
        assert "equation" in tags or "formula" in tags
    
    def test_calculate_complexity_score(self, analyzer):
        """Test complexity score calculation."""
        text = "Solve the equation 2x + 5 = 15"
        word_count = len(text.split())
        tags = ["equation", "algebra"]
        
        score = analyzer._calculate_complexity_score(text, word_count, tags)
        
        assert 0.0 <= score <= 1.0
        assert isinstance(score, float)
    
    def test_analyze_question_success(self, analyzer):
        """Test successful question analysis."""
        question_text = "What is 2 + 2?"
        subject = "Mathematics"
        
        analysis = analyzer.analyze_question(question_text, subject)
        
        assert isinstance(analysis, QuestionAnalysis)
        assert analysis.question_text == question_text
        assert analysis.difficulty in ["easy", "medium", "hard"]
        assert isinstance(analysis.tags, list)
        assert 0.0 <= analysis.confidence <= 1.0
        assert analysis.analysis_method in ["rule_based", "ml_model", "fallback"]
        assert analysis.word_count > 0
        assert 0.0 <= analysis.complexity_score <= 1.0
    
    def test_analyze_question_with_error(self, analyzer):
        """Test question analysis with error handling."""
        # Mock a method to raise an exception
        with patch.object(analyzer, '_preprocess_text', side_effect=Exception("Test error")):
            analysis = analyzer.analyze_question("Test question", "Mathematics")
            
            # Should return fallback analysis
            assert analysis.difficulty == "medium"
            assert analysis.tags == ["general"]
            assert analysis.analysis_method == "fallback"
    
    def test_batch_analyze(self, analyzer):
        """Test batch question analysis."""
        questions = [
            {"text": "What is 2 + 2?", "subject": "Mathematics"},
            {"text": "Solve for x: 2x + 5 = 15", "subject": "Mathematics"}
        ]
        
        results = analyzer.batch_analyze(questions)
        
        assert len(results) == 2
        assert all(isinstance(result, QuestionAnalysis) for result in results)
    
    def test_update_model(self, analyzer):
        """Test ML model update."""
        mock_model = Mock()
        
        analyzer.update_model(mock_model)
        
        assert analyzer.future_model == mock_model
        assert analyzer.use_ml is True
    
    def test_get_analysis_stats(self, analyzer):
        """Test analysis statistics retrieval."""
        stats = analyzer.get_analysis_stats()
        
        assert "analysis_method" in stats
        assert "ml_model_available" in stats
        assert "difficulty_thresholds" in stats
        assert "nlp_components" in stats
    
    def test_ml_classification_fallback(self, analyzer):
        """Test ML classification falls back to rule-based when model unavailable."""
        text = "Test question"
        
        difficulty, confidence = analyzer._classify_difficulty_ml(text)
        
        # Should fall back to rule-based classification
        assert difficulty in ["easy", "medium", "hard"]
        assert confidence > 0.0

class TestQuestionAnalysisSchemas:
    """Test cases for question analysis schemas."""
    
    def test_question_analysis_request(self):
        """Test QuestionAnalysisRequest schema."""
        request = QuestionAnalysisRequest(
            subject="Mathematics",
            text="What is 2 + 2?",
            use_ml=False
        )
        
        assert request.subject == "Mathematics"
        assert request.text == "What is 2 + 2?"
        assert request.use_ml is False
    
    def test_question_analysis_response(self):
        """Test QuestionAnalysisResponse schema."""
        response = QuestionAnalysisResponse(
            question="What is 2 + 2?",
            subject="Mathematics",
            difficulty="easy",
            tags=["arithmetic", "basic"],
            confidence=0.8,
            analysis_method="rule_based",
            word_count=5,
            complexity_score=0.2
        )
        
        assert response.question == "What is 2 + 2?"
        assert response.difficulty == "easy"
        assert "arithmetic" in response.tags
        assert response.confidence == 0.8
    
    def test_batch_question_analysis_request(self):
        """Test BatchQuestionAnalysisRequest schema."""
        questions = [
            QuestionAnalysisRequest(subject="Math", text="Question 1"),
            QuestionAnalysisRequest(subject="Math", text="Question 2")
        ]
        
        request = BatchQuestionAnalysisRequest(
            questions=questions,
            use_ml=False
        )
        
        assert len(request.questions) == 2
        assert request.use_ml is False

def test_difficulty_classification_edge_cases():
    """Test edge cases in difficulty classification."""
    analyzer = QuestionAnalyzer()
    
    # Test very short text
    text = "Hi"
    word_count = len(text.split())
    difficulty, confidence = analyzer._classify_difficulty_rule_based(text, word_count)
    assert difficulty == "easy"
    
    # Test very long text
    text = "This is a very long question that contains many words and should be classified as hard difficulty because it exceeds the threshold for medium difficulty questions"
    word_count = len(text.split())
    difficulty, confidence = analyzer._classify_difficulty_rule_based(text, word_count)
    assert difficulty == "hard"

def test_tag_extraction_edge_cases():
    """Test edge cases in tag extraction."""
    analyzer = QuestionAnalyzer()
    
    # Test empty text
    tags = analyzer._extract_tags("", "mathematics")
    assert tags == ["general"]
    
    # Test text with only stop words
    tags = analyzer._extract_tags("the and or but", "mathematics")
    assert "general" in tags or len(tags) == 0

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
