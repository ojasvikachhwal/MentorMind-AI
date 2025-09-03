#!/usr/bin/env python3
"""
Demonstration script for the NLP analysis system.
This script shows how the QuestionAnalyzer classifies question difficulty
and extracts tags using NLP techniques.
"""

import time
from app.services.nlp_analysis import QuestionAnalyzer

def demonstrate_nlp_analysis():
    """Demonstrate the NLP analysis capabilities."""
    
    print("🤖 NLP Analysis System Demonstration")
    print("=" * 60)
    
    # Initialize the analyzer
    print("\n🔧 Initializing Question Analyzer...")
    analyzer = QuestionAnalyzer()
    
    # Show analyzer configuration
    print("✅ Analyzer initialized successfully!")
    stats = analyzer.get_analysis_stats()
    print(f"   - Analysis method: {stats['analysis_method']}")
    print(f"   - ML model available: {stats['ml_model_available']}")
    print(f"   - spaCy loaded: {stats['nlp_components']['spacy_loaded']}")
    print(f"   - NLTK loaded: {stats['nlp_components']['nltk_loaded']}")
    
    # Test questions for different subjects and difficulties
    test_questions = [
        # Mathematics - Easy
        {
            "subject": "Mathematics",
            "text": "What is 2 + 2?",
            "expected_difficulty": "easy"
        },
        # Mathematics - Medium
        {
            "subject": "Mathematics",
            "text": "Solve the quadratic equation x² + 5x + 6 = 0 using the quadratic formula and explain your reasoning step by step.",
            "expected_difficulty": "medium"
        },
        # Mathematics - Hard
        {
            "subject": "Mathematics",
            "text": "Calculate the definite integral of the function f(x) = sin(x)cos(x) from x = 0 to x = π/2, showing all steps and using appropriate trigonometric identities, and then verify your result using a different method.",
            "expected_difficulty": "hard"
        },
        # Physics - Easy
        {
            "subject": "Physics",
            "text": "What is the formula for force?",
            "expected_difficulty": "easy"
        },
        # Physics - Medium
        {
            "subject": "Physics",
            "text": "Calculate the force exerted by a 5kg object accelerating at 2 m/s² and describe the relationship between mass, acceleration, and force.",
            "expected_difficulty": "medium"
        },
        # Computer Science - Easy
        {
            "subject": "Computer Science",
            "text": "What is a variable?",
            "expected_difficulty": "easy"
        },
        # Computer Science - Hard
        {
            "subject": "Computer Science",
            "text": "Implement a binary search algorithm in Python, analyze its time complexity, and compare it with linear search in terms of efficiency for different input sizes.",
            "expected_difficulty": "hard"
        }
    ]
    
    print(f"\n📊 Analyzing {len(test_questions)} test questions...")
    print("-" * 60)
    
    # Analyze each question
    results = []
    total_time = 0
    
    for i, question_data in enumerate(test_questions, 1):
        print(f"\nQuestion {i}: {question_data['subject']}")
        print(f"Text: {question_data['text'][:80]}...")
        print(f"Expected difficulty: {question_data['expected_difficulty']}")
        
        # Time the analysis
        start_time = time.time()
        analysis = analyzer.analyze_question(
            question_data['text'], 
            question_data['subject']
        )
        analysis_time = (time.time() - start_time) * 1000  # Convert to milliseconds
        total_time += analysis_time
        
        # Display results
        print(f"✅ Analysis completed in {analysis_time:.1f}ms")
        print(f"   - Actual difficulty: {analysis.difficulty}")
        print(f"   - Confidence: {analysis.confidence:.2f}")
        print(f"   - Word count: {analysis.word_count}")
        print(f"   - Complexity score: {analysis.complexity_score:.2f}")
        print(f"   - Analysis method: {analysis.analysis_method}")
        print(f"   - Tags: {', '.join(analysis.tags[:5])}")
        
        # Check if difficulty matches expectation
        if analysis.difficulty == question_data['expected_difficulty']:
            print(f"   🎯 Difficulty classification: CORRECT")
        else:
            print(f"   ⚠️  Difficulty classification: {analysis.difficulty} (expected {question_data['expected_difficulty']})")
        
        results.append({
            "question": question_data,
            "analysis": analysis,
            "time": analysis_time
        })
    
    # Show summary statistics
    print("\n📈 Analysis Summary")
    print("-" * 40)
    
    # Difficulty distribution
    difficulty_counts = {}
    for result in results:
        difficulty = result['analysis'].difficulty
        difficulty_counts[difficulty] = difficulty_counts.get(difficulty, 0) + 1
    
    print("Difficulty Distribution:")
    for difficulty, count in difficulty_counts.items():
        print(f"   - {difficulty.capitalize()}: {count} questions")
    
    # Accuracy
    correct_predictions = sum(
        1 for result in results 
        if result['analysis'].difficulty == result['question']['expected_difficulty']
    )
    accuracy = (correct_predictions / len(results)) * 100
    print(f"\nAccuracy: {accuracy:.1f}% ({correct_predictions}/{len(results)})")
    
    # Performance
    avg_time = total_time / len(results)
    print(f"Average analysis time: {avg_time:.1f}ms")
    print(f"Total analysis time: {total_time:.1f}ms")
    
    # Tag analysis
    print("\n🏷️  Tag Analysis")
    print("-" * 40)
    
    all_tags = []
    for result in results:
        all_tags.extend(result['analysis'].tags)
    
    tag_frequency = {}
    for tag in all_tags:
        tag_frequency[tag] = tag_frequency.get(tag, 0) + 1
    
    # Show most common tags
    sorted_tags = sorted(tag_frequency.items(), key=lambda x: x[1], reverse=True)
    print("Most common tags:")
    for tag, count in sorted_tags[:10]:
        print(f"   - {tag}: {count} occurrences")
    
    # Show subject-specific analysis
    print("\n📚 Subject-Specific Analysis")
    print("-" * 40)
    
    subjects = {}
    for result in results:
        subject = result['question']['subject']
        if subject not in subjects:
            subjects[subject] = []
        subjects[subject].append(result)
    
    for subject, subject_results in subjects.items():
        print(f"\n{subject}:")
        avg_confidence = sum(r['analysis'].confidence for r in subject_results) / len(subject_results)
        avg_complexity = sum(r['analysis'].complexity_score for r in subject_results) / len(subject_results)
        
        print(f"   - Questions analyzed: {len(subject_results)}")
        print(f"   - Average confidence: {avg_confidence:.2f}")
        print(f"   - Average complexity: {avg_complexity:.2f}")
        
        # Show difficulty breakdown for this subject
        subject_difficulties = {}
        for result in subject_results:
            difficulty = result['analysis'].difficulty
            subject_difficulties[difficulty] = subject_difficulties.get(difficulty, 0) + 1
        
        print(f"   - Difficulty breakdown:")
        for difficulty, count in subject_difficulties.items():
            print(f"     • {difficulty.capitalize()}: {count}")
    
    # Demonstrate batch analysis
    print("\n🔄 Batch Analysis Demonstration")
    print("-" * 40)
    
    batch_questions = [
        {"text": "What is the derivative of x²?", "subject": "Mathematics"},
        {"text": "Explain Newton's laws of motion", "subject": "Physics"},
        {"text": "What is a function in programming?", "subject": "Computer Science"}
    ]
    
    print(f"Analyzing {len(batch_questions)} questions in batch...")
    start_time = time.time()
    batch_results = analyzer.batch_analyze(batch_questions)
    batch_time = (time.time() - start_time) * 1000
    
    print(f"✅ Batch analysis completed in {batch_time:.1f}ms")
    print(f"   - Individual average time: {batch_time/len(batch_questions):.1f}ms per question")
    
    for i, result in enumerate(batch_results, 1):
        print(f"   Question {i}: {result.difficulty} - {', '.join(result.tags[:3])}")
    
    # Show future ML integration capabilities
    print("\n🔮 Future ML Integration")
    print("-" * 40)
    print("The system is designed to easily integrate with Hugging Face models:")
    print("   • Current: Rule-based classification with NLP tag extraction")
    print("   • Future: ML-powered difficulty classification")
    print("   • Extensible: Easy model swapping without code changes")
    print("   • Batch processing: Efficient for large question sets")
    
    print("\n✅ Demonstration completed successfully!")
    print("\n💡 To test with the API, run the FastAPI server and use:")
    print("   POST /questions/analyze")
    print("   POST /questions/analyze/batch")
    print("   POST /questions/upload")

def demonstrate_difficulty_classification_logic():
    """Demonstrate the difficulty classification logic."""
    
    print("\n🧠 Difficulty Classification Logic")
    print("=" * 50)
    
    analyzer = QuestionAnalyzer()
    
    # Show the thresholds
    print(f"Default difficulty thresholds:")
    for level, threshold in analyzer.difficulty_thresholds.items():
        print(f"   - {level.capitalize()}: ≤{threshold} words")
    
    # Test different question lengths
    test_cases = [
        ("Hi", "Very short"),
        ("What is 2 + 2?", "Short"),
        ("Solve for x: 2x + 5 = 15", "Short"),
        ("Find the derivative of f(x) = x² + 3x + 1 and explain your reasoning step by step", "Medium"),
        ("Calculate the definite integral of the function f(x) = sin(x)cos(x) from x = 0 to x = π/2, showing all steps and using appropriate trigonometric identities, and then verify your result using a different method", "Long")
    ]
    
    print(f"\nTesting difficulty classification:")
    for question, description in test_cases:
        word_count = len(question.split())
        difficulty, confidence = analyzer._classify_difficulty_rule_based(question, word_count)
        
        print(f"\n{description}:")
        print(f"   Question: {question[:60]}...")
        print(f"   Word count: {word_count}")
        print(f"   Classified as: {difficulty}")
        print(f"   Confidence: {confidence:.2f}")
    
    # Show complexity indicators
    print(f"\n🔍 Complexity Indicators Analysis:")
    complex_question = "Solve the equation 2x + 5 = 15, but first explain why this is a linear equation and then find the value of x"
    
    indicators = analyzer._analyze_content_complexity(complex_question)
    print(f"\nQuestion: {complex_question[:60]}...")
    print(f"Complexity indicators:")
    for indicator, value in indicators.items():
        print(f"   - {indicator.replace('_', ' ').title()}: {value:.2f}")

def main():
    """Main demonstration function."""
    try:
        demonstrate_nlp_analysis()
        demonstrate_difficulty_classification_logic()
    except Exception as e:
        print(f"❌ Error during demonstration: {e}")
        print("Make sure you're running this from the backend directory with proper imports.")

if __name__ == "__main__":
    main()
