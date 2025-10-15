import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  BookOpen, Play, Clock, CheckCircle, AlertCircle, 
  TrendingUp, Brain, ArrowRight, ArrowLeft, Timer, Send
} from 'lucide-react';
import ProfileDropdown from '../components/ProfileDropdown';

const AutomatedMockTests = () => {
  const [subjects, setSubjects] = useState([]);
  const [selectedSubject, setSelectedSubject] = useState(null);
  const [studentProgress, setStudentProgress] = useState({});
  const [generatedTest, setGeneratedTest] = useState(null);
  const [testSession, setTestSession] = useState(null);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [answers, setAnswers] = useState({});
  const [timeRemaining, setTimeRemaining] = useState(0);
  const [testStarted, setTestStarted] = useState(false);
  const [testSubmitted, setTestSubmitted] = useState(false);
  const [testResult, setTestResult] = useState(null);
  const [aiEvaluation, setAiEvaluation] = useState(null);
  const [loading, setLoading] = useState(false);
  const [showEvaluation, setShowEvaluation] = useState(false);

  // Load subjects and progress on component mount
  useEffect(() => {
    loadSubjects();
    loadStudentProgress();
  }, []);

  // Timer effect
  useEffect(() => {
    let timer;
    if (testStarted && timeRemaining > 0) {
      timer = setInterval(() => {
        setTimeRemaining(prev => {
          if (prev <= 1) {
            handleAutoSubmit();
            return 0;
          }
          return prev - 1;
        });
      }, 1000);
    }
    return () => {
      if (timer) clearInterval(timer);
    };
  }, [testStarted, timeRemaining]);

  const loadSubjects = async () => {
    try {
      const response = await fetch('/api/v1/automated-tests/subjects', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      if (response.ok) {
        const data = await response.json();
        setSubjects(data);
      } else {
        console.error('Failed to load subjects:', response.status, response.statusText);
        // Fallback to sample subjects for testing
        setSubjects([
          { id: 1, name: 'Data Structures & Algorithms', description: 'Fundamental data structures and algorithms' },
          { id: 2, name: 'Object-Oriented Programming', description: 'OOP concepts and design patterns' },
          { id: 3, name: 'Database Management', description: 'SQL and database design' },
          { id: 4, name: 'Operating Systems', description: 'Process management and memory systems' }
        ]);
      }
    } catch (error) {
      console.error('Failed to load subjects:', error);
      // Fallback to sample subjects for testing
      setSubjects([
        { id: 1, name: 'Data Structures & Algorithms', description: 'Fundamental data structures and algorithms' },
        { id: 2, name: 'Object-Oriented Programming', description: 'OOP concepts and design patterns' },
        { id: 3, name: 'Database Management', description: 'SQL and database design' },
        { id: 4, name: 'Operating Systems', description: 'Process management and memory systems' }
      ]);
    }
  };

  const loadStudentProgress = async () => {
    try {
      const response = await fetch('/api/v1/automated-tests/progress/all', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      if (response.ok) {
        const data = await response.json();
        const progressMap = {};
        data.forEach(progress => {
          progressMap[progress.subject_id] = progress;
        });
        setStudentProgress(progressMap);
      } else {
        console.error('Failed to load progress:', response.status, response.statusText);
        // Initialize with empty progress for new users
        setStudentProgress({});
      }
    } catch (error) {
      console.error('Failed to load progress:', error);
      // Initialize with empty progress for new users
      setStudentProgress({});
    }
  };

  const generateTest = async (subjectId) => {
    try {
      setLoading(true);
      const response = await fetch(`/api/v1/automated-tests/subjects/${subjectId}/generate`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });

      if (response.ok) {
        const test = await response.json();
        setGeneratedTest(test);
        setSelectedSubject(subjects.find(s => s.id === subjectId));
      } else {
        const errorData = await response.json().catch(() => ({}));
        console.error('Test generation failed:', errorData);
        alert(`Failed to generate test: ${errorData.detail || 'Please try again.'}`);
      }
    } catch (error) {
      console.error('Failed to generate test:', error);
      alert('Failed to generate test. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const startTest = async () => {
    try {
      setLoading(true);
      
      // Start test session
      const sessionResponse = await fetch(`/api/v1/automated-tests/tests/${generatedTest.id}/start`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });

      if (sessionResponse.ok) {
        const session = await sessionResponse.json();
        setTestSession(session);
        
        // Begin the test
        const beginResponse = await fetch(`/api/v1/automated-tests/sessions/${session.session_id}/begin`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });

        if (beginResponse.ok) {
          setTimeRemaining(generatedTest.time_limit_minutes * 60);
          setTestStarted(true);
        }
      }
    } catch (error) {
      console.error('Failed to start test:', error);
      alert('Failed to start test. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleAnswerSelect = (questionId, option) => {
    setAnswers(prev => ({
      ...prev,
      [questionId]: option
    }));
  };

  const handleNextQuestion = () => {
    if (currentQuestionIndex < generatedTest.questions.length - 1) {
      setCurrentQuestionIndex(currentQuestionIndex + 1);
    }
  };

  const handlePreviousQuestion = () => {
    if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex(currentQuestionIndex - 1);
    }
  };

  const handleSubmitTest = async () => {
    try {
      setLoading(true);
      
      const submissionData = {
        answers: Object.entries(answers).map(([questionId, selectedOption]) => ({
          question_id: parseInt(questionId),
          selected_option: selectedOption
        }))
      };

      const response = await fetch(`/api/v1/automated-tests/sessions/${testSession.session_id}/submit`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify(submissionData)
      });

      if (response.ok) {
        const result = await response.json();
        setTestResult(result);
        setTestSubmitted(true);
        setTestStarted(false);
        
        // Refresh progress
        loadStudentProgress();
      }
    } catch (error) {
      console.error('Failed to submit test:', error);
      alert('Failed to submit test. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleAutoSubmit = () => {
    if (testStarted && !testSubmitted) {
      handleSubmitTest();
    }
  };

  const getAIEvaluation = async () => {
    try {
      setLoading(true);
      const response = await fetch(`/api/v1/automated-tests/sessions/${testSession.session_id}/evaluate`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });

      if (response.ok) {
        const evaluation = await response.json();
        setAiEvaluation(evaluation);
        setShowEvaluation(true);
      }
    } catch (error) {
      console.error('Failed to get AI evaluation:', error);
      alert('Failed to get AI evaluation. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const formatTime = (seconds) => {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    
    if (hours > 0) {
      return `${hours}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    }
    return `${minutes}:${secs.toString().padStart(2, '0')}`;
  };

  const getTimeColor = () => {
    if (timeRemaining <= 300) return 'text-red-600';
    if (timeRemaining <= 600) return 'text-orange-600';
    return 'text-green-600';
  };

  const getDifficultyColor = (progress) => {
    if (progress < 30) return 'text-green-600';
    if (progress < 60) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getDifficultyLabel = (progress) => {
    if (progress < 30) return 'Beginner';
    if (progress < 60) return 'Intermediate';
    return 'Advanced';
  };

  // Subject Selection View
  if (!generatedTest) {
    return (
      <div className="min-h-screen bg-gray-50 p-6">
        <div className="max-w-6xl mx-auto">
          <div className="flex justify-between items-center mb-8">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Automated Mock Tests</h1>
              <p className="text-gray-600 mt-2">AI-generated tests based on your progress in each subject</p>
            </div>
            <ProfileDropdown />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {subjects.map((subject) => {
              const progress = studentProgress[subject.id] || { progress_percentage: 0, total_tests_taken: 0 };
              return (
                <motion.div
                  key={subject.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  whileHover={{ scale: 1.02 }}
                  className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow cursor-pointer"
                  onClick={() => generateTest(subject.id)}
                >
                  <div className="flex items-center mb-4">
                    <BookOpen className="w-8 h-8 text-purple-600 mr-3" />
                    <div>
                      <h3 className="text-lg font-semibold text-gray-900">{subject.name}</h3>
                      <p className="text-sm text-gray-500">{subject.description}</p>
                    </div>
                  </div>

                  <div className="space-y-3 mb-4">
                    <div className="flex justify-between items-center">
                      <span className="text-sm text-gray-600">Progress:</span>
                      <div className="flex items-center">
                        <div className="w-20 bg-gray-200 rounded-full h-2 mr-2">
                          <div 
                            className="bg-purple-600 h-2 rounded-full transition-all duration-300"
                            style={{ width: `${progress.progress_percentage}%` }}
                          ></div>
                        </div>
                        <span className={`text-sm font-medium ${getDifficultyColor(progress.progress_percentage)}`}>
                          {progress.progress_percentage.toFixed(1)}%
                        </span>
                      </div>
                    </div>
                    
                    <div className="flex justify-between text-sm">
                      <span className="text-gray-600">Tests Taken:</span>
                      <span className="font-medium">{progress.total_tests_taken}</span>
                    </div>
                    
                    <div className="flex justify-between text-sm">
                      <span className="text-gray-600">Difficulty Level:</span>
                      <span className={`font-medium ${getDifficultyColor(progress.progress_percentage)}`}>
                        {getDifficultyLabel(progress.progress_percentage)}
                      </span>
                    </div>
                  </div>

                  <div className="flex items-center justify-between">
                    <span className="text-xs text-gray-500">
                      {progress.last_test_date ? 
                        `Last test: ${new Date(progress.last_test_date).toLocaleDateString()}` : 
                        'No tests taken yet'
                      }
                    </span>
                    <button 
                      className="flex items-center px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors text-sm"
                      disabled={loading}
                    >
                      <Play className="w-4 h-4 mr-2" />
                      {loading ? 'Generating...' : 'Generate Test'}
                    </button>
                  </div>
                </motion.div>
              );
            })}
          </div>
        </div>
      </div>
    );
  }

  // Test Taking View
  if (generatedTest && testStarted && !testSubmitted) {
    const currentQuestion = generatedTest.questions[currentQuestionIndex];
    const totalQuestions = generatedTest.questions.length;
    const answeredQuestions = Object.keys(answers).length;

    return (
      <div className="min-h-screen bg-gray-50">
        {/* Header */}
        <div className="bg-white border-b border-gray-200 px-6 py-4">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-xl font-semibold text-gray-900">{generatedTest.title}</h1>
              <p className="text-sm text-gray-500">
                Question {currentQuestionIndex + 1} of {totalQuestions}
              </p>
            </div>
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2">
                <Timer className="w-5 h-5 text-gray-400" />
                <span className={`text-lg font-mono font-semibold ${getTimeColor()}`}>
                  {formatTime(timeRemaining)}
                </span>
              </div>
              <ProfileDropdown />
            </div>
          </div>

          {/* Progress Bar */}
          <div className="mt-4">
            <div className="flex justify-between text-sm text-gray-600 mb-2">
              <span>Progress: {answeredQuestions}/{totalQuestions} answered</span>
              <span>{Math.round(((currentQuestionIndex + 1) / totalQuestions) * 100)}% complete</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div 
                className="bg-purple-600 h-2 rounded-full transition-all duration-300"
                style={{ width: `${((currentQuestionIndex + 1) / totalQuestions) * 100}%` }}
              ></div>
            </div>
          </div>
        </div>

        {/* Question Content */}
        <div className="p-6">
          <div className="max-w-4xl mx-auto">
            <motion.div
              key={currentQuestionIndex}
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              className="bg-white rounded-xl shadow-sm border border-gray-200 p-8"
            >
              <div className="mb-6">
                <div className="flex items-center justify-between mb-4">
                  <h2 className="text-lg font-semibold text-gray-900">
                    Question {currentQuestionIndex + 1}
                  </h2>
                  <span className="text-sm text-gray-500">
                    {currentQuestion.marks} mark{currentQuestion.marks > 1 ? 's' : ''}
                  </span>
                </div>
                <p className="text-gray-800 text-lg leading-relaxed">
                  {currentQuestion.question_text}
                </p>
              </div>

              <div className="space-y-3">
                {['A', 'B', 'C', 'D'].map((option) => {
                  const optionText = currentQuestion[`option_${option.toLowerCase()}`];
                  const isSelected = answers[currentQuestion.id] === option;
                  
                  return (
                    <motion.div
                      key={option}
                      whileHover={{ scale: 1.01 }}
                      className={`border-2 rounded-lg p-4 cursor-pointer transition-all ${
                        isSelected 
                          ? 'border-purple-500 bg-purple-50' 
                          : 'border-gray-200 hover:border-gray-300'
                      }`}
                      onClick={() => handleAnswerSelect(currentQuestion.id, option)}
                    >
                      <div className="flex items-center">
                        <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium mr-4 ${
                          isSelected 
                            ? 'bg-purple-600 text-white' 
                            : 'bg-gray-100 text-gray-600'
                        }`}>
                          {option}
                        </div>
                        <span className="text-gray-800">{optionText}</span>
                      </div>
                    </motion.div>
                  );
                })}
              </div>
            </motion.div>

            {/* Navigation */}
            <div className="flex justify-between items-center mt-6">
              <button
                onClick={handlePreviousQuestion}
                disabled={currentQuestionIndex === 0}
                className="flex items-center px-4 py-2 text-gray-600 border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                <ArrowLeft className="w-4 h-4 mr-2" />
                Previous
              </button>

              <div className="flex space-x-2">
                {generatedTest.questions.map((_, index) => (
                  <button
                    key={index}
                    onClick={() => setCurrentQuestionIndex(index)}
                    className={`w-8 h-8 rounded-full text-sm font-medium transition-colors ${
                      index === currentQuestionIndex
                        ? 'bg-purple-600 text-white'
                        : answers[generatedTest.questions[index].id]
                        ? 'bg-green-100 text-green-800'
                        : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                    }`}
                  >
                    {index + 1}
                  </button>
                ))}
              </div>

              {currentQuestionIndex === totalQuestions - 1 ? (
                <button
                  onClick={handleSubmitTest}
                  disabled={loading}
                  className="flex items-center px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50 transition-colors"
                >
                  <Send className="w-4 h-4 mr-2" />
                  {loading ? 'Submitting...' : 'Submit Test'}
                </button>
              ) : (
                <button
                  onClick={handleNextQuestion}
                  className="flex items-center px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors"
                >
                  Next
                  <ArrowRight className="w-4 h-4 ml-2" />
                </button>
              )}
            </div>
          </div>
        </div>
      </div>
    );
  }

  // Results View
  if (testSubmitted && testResult) {
    return (
      <div className="min-h-screen bg-gray-50 p-6">
        <div className="max-w-4xl mx-auto">
          <div className="flex justify-between items-center mb-8">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Test Results</h1>
              <p className="text-gray-600 mt-2">Your performance on {generatedTest.title}</p>
            </div>
            <ProfileDropdown />
          </div>

          <div className="space-y-6">
            {/* Score Summary */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="bg-white rounded-xl shadow-sm border border-gray-200 p-8"
            >
              <div className="text-center mb-6">
                <div className="w-24 h-24 bg-gradient-to-r from-purple-600 to-pink-600 rounded-full flex items-center justify-center mx-auto mb-4">
                  <span className="text-3xl font-bold text-white">
                    {Math.round(testResult.percentage)}%
                  </span>
                </div>
                <h2 className="text-2xl font-semibold text-gray-900 mb-2">
                  {testResult.percentage >= 80 ? 'Excellent!' : 
                   testResult.percentage >= 60 ? 'Good Job!' : 
                   testResult.percentage >= 40 ? 'Keep Practicing!' : 'Try Again!'}
                </h2>
                <p className="text-gray-600">
                  You scored {testResult.total_score} out of {testResult.total_marks} marks
                </p>
              </div>

              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div className="text-center p-4 bg-green-50 rounded-lg">
                  <CheckCircle className="w-8 h-8 text-green-600 mx-auto mb-2" />
                  <div className="text-2xl font-bold text-green-600">{testResult.correct_answers}</div>
                  <div className="text-sm text-gray-600">Correct</div>
                </div>
                <div className="text-center p-4 bg-red-50 rounded-lg">
                  <AlertCircle className="w-8 h-8 text-red-600 mx-auto mb-2" />
                  <div className="text-2xl font-bold text-red-600">
                    {testResult.total_questions - testResult.correct_answers}
                  </div>
                  <div className="text-sm text-gray-600">Incorrect</div>
                </div>
                <div className="text-center p-4 bg-blue-50 rounded-lg">
                  <Clock className="w-8 h-8 text-blue-600 mx-auto mb-2" />
                  <div className="text-2xl font-bold text-blue-600">{testResult.time_taken_minutes}</div>
                  <div className="text-sm text-gray-600">Minutes</div>
                </div>
                <div className="text-center p-4 bg-purple-50 rounded-lg">
                  <TrendingUp className="w-8 h-8 text-purple-600 mx-auto mb-2" />
                  <div className="text-2xl font-bold text-purple-600">{Math.round(testResult.percentage)}%</div>
                  <div className="text-sm text-gray-600">Score</div>
                </div>
              </div>
            </motion.div>

            {/* AI Evaluation Button */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 }}
              className="text-center"
            >
              <button
                onClick={getAIEvaluation}
                disabled={loading}
                className="flex items-center px-6 py-3 bg-gradient-to-r from-purple-600 to-pink-600 text-white rounded-lg hover:from-purple-700 hover:to-pink-700 disabled:opacity-50 transition-all mx-auto"
              >
                <Brain className="w-5 h-5 mr-2" />
                {loading ? 'Analyzing...' : 'Get AI Evaluation'}
              </button>
            </motion.div>

            {/* AI Evaluation Results */}
            <AnimatePresence>
              {showEvaluation && aiEvaluation && (
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -20 }}
                  className="bg-white rounded-xl shadow-sm border border-gray-200 p-8"
                >
                  <h3 className="text-xl font-semibold text-gray-900 mb-6 flex items-center">
                    <Brain className="w-6 h-6 mr-2 text-purple-600" />
                    AI Performance Analysis
                  </h3>

                  <div className="space-y-6">
                    <div>
                      <h4 className="text-lg font-medium text-gray-900 mb-3">Overall Assessment</h4>
                      <p className="text-gray-700 leading-relaxed">
                        {aiEvaluation.overall_assessment}
                      </p>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                      <div>
                        <h4 className="text-lg font-medium text-green-700 mb-3 flex items-center">
                          <CheckCircle className="w-5 h-5 mr-2" />
                          Strengths
                        </h4>
                        <ul className="space-y-2">
                          {aiEvaluation.strengths?.map((strength, index) => (
                            <li key={index} className="flex items-start">
                              <span className="w-2 h-2 bg-green-500 rounded-full mt-2 mr-3 flex-shrink-0"></span>
                              <span className="text-gray-700">{strength}</span>
                            </li>
                          ))}
                        </ul>
                      </div>

                      <div>
                        <h4 className="text-lg font-medium text-red-700 mb-3 flex items-center">
                          <AlertCircle className="w-5 h-5 mr-2" />
                          Areas for Improvement
                        </h4>
                        <ul className="space-y-2">
                          {aiEvaluation.weaknesses?.map((weakness, index) => (
                            <li key={index} className="flex items-start">
                              <span className="w-2 h-2 bg-red-500 rounded-full mt-2 mr-3 flex-shrink-0"></span>
                              <span className="text-gray-700">{weakness}</span>
                            </li>
                          ))}
                        </ul>
                      </div>
                    </div>

                    <div>
                      <h4 className="text-lg font-medium text-blue-700 mb-3">Recommendations</h4>
                      <ul className="space-y-2">
                        {aiEvaluation.recommendations?.map((recommendation, index) => (
                          <li key={index} className="flex items-start">
                            <span className="w-2 h-2 bg-blue-500 rounded-full mt-2 mr-3 flex-shrink-0"></span>
                            <span className="text-gray-700">{recommendation}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  </div>
                </motion.div>
              )}
            </AnimatePresence>

            {/* Action Buttons */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
              className="flex justify-center space-x-4"
            >
              <button
                onClick={() => {
                  setGeneratedTest(null);
                  setTestSession(null);
                  setTestResult(null);
                  setAiEvaluation(null);
                  setShowEvaluation(false);
                  setAnswers({});
                  setCurrentQuestionIndex(0);
                  setTestSubmitted(false);
                  setTestStarted(false);
                }}
                className="px-6 py-3 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors"
              >
                Take Another Test
              </button>
              <button
                onClick={() => {
                  window.location.href = '/dashboard';
                }}
                className="px-6 py-3 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors"
              >
                Back to Dashboard
              </button>
            </motion.div>
          </div>
        </div>
      </div>
    );
  }

  // Test Start Confirmation
  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-2xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-white rounded-xl shadow-sm border border-gray-200 p-8"
        >
          <div className="text-center mb-8">
            <BookOpen className="w-16 h-16 text-purple-600 mx-auto mb-4" />
            <h1 className="text-2xl font-bold text-gray-900 mb-2">{generatedTest.title}</h1>
            <p className="text-gray-600">{generatedTest.description}</p>
          </div>

          <div className="space-y-4 mb-8">
            <div className="flex justify-between py-3 border-b border-gray-200">
              <span className="text-gray-600">Subject:</span>
              <span className="font-medium">{selectedSubject?.name}</span>
            </div>
            <div className="flex justify-between py-3 border-b border-gray-200">
              <span className="text-gray-600">Total Questions:</span>
              <span className="font-medium">{generatedTest.questions?.length || 0}</span>
            </div>
            <div className="flex justify-between py-3 border-b border-gray-200">
              <span className="text-gray-600">Total Marks:</span>
              <span className="font-medium">{generatedTest.total_marks}</span>
            </div>
            <div className="flex justify-between py-3 border-b border-gray-200">
              <span className="text-gray-600">Time Limit:</span>
              <span className="font-medium">{generatedTest.time_limit_minutes} minutes</span>
            </div>
            <div className="flex justify-between py-3">
              <span className="text-gray-600">Difficulty:</span>
              <span className="font-medium">
                {getDifficultyLabel(studentProgress[selectedSubject?.id]?.progress_percentage || 0)}
              </span>
            </div>
          </div>

          <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mb-8">
            <div className="flex items-start">
              <AlertCircle className="w-5 h-5 text-yellow-600 mr-3 mt-0.5" />
              <div>
                <h4 className="font-medium text-yellow-800 mb-1">Important Instructions</h4>
                <ul className="text-sm text-yellow-700 space-y-1">
                  <li>• This test was automatically generated based on your current progress</li>
                  <li>• You cannot pause or restart the test once started</li>
                  <li>• The test will auto-submit when time runs out</li>
                  <li>• Your progress will be updated after submission</li>
                </ul>
              </div>
            </div>
          </div>

          <div className="flex justify-center space-x-4">
            <button
              onClick={() => {
                setGeneratedTest(null);
                setSelectedSubject(null);
              }}
              className="px-6 py-3 text-gray-600 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
            >
              Cancel
            </button>
            <button
              onClick={startTest}
              disabled={loading}
              className="px-6 py-3 bg-purple-600 text-white rounded-lg hover:bg-purple-700 disabled:opacity-50 transition-colors"
            >
              {loading ? 'Starting...' : 'Start Test'}
            </button>
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default AutomatedMockTests;
