import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Clock, CheckCircle, AlertCircle, ArrowRight, ArrowLeft, 
  Flag, BookOpen, Timer, Send, Brain, TrendingUp 
} from 'lucide-react';
import ProfileDropdown from '../../components/ProfileDropdown';

const MockTestTaker = () => {
  const [availableTests, setAvailableTests] = useState([]);
  const [selectedTest, setSelectedTest] = useState(null);
  const [testSession, setTestSession] = useState(null);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [answers, setAnswers] = useState({});
  const [timeRemaining, setTimeRemaining] = useState(0);
  const [testStarted, setTestStarted] = useState(false);
  const [testSubmitted, setTestSubmitted] = useState(false);
  const [testResult, setTestResult] = useState(null);
  const [aiAnalysis, setAiAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [showAnalysis, setShowAnalysis] = useState(false);
  
  const timerRef = useRef(null);

  // Load available tests on component mount
  useEffect(() => {
    loadAvailableTests();
  }, []);

  // Timer effect
  useEffect(() => {
    if (testStarted && timeRemaining > 0) {
      timerRef.current = setInterval(() => {
        setTimeRemaining(prev => {
          if (prev <= 1) {
            handleAutoSubmit();
            return 0;
          }
          return prev - 1;
        });
      }, 1000);
    } else {
      if (timerRef.current) {
        clearInterval(timerRef.current);
      }
    }

    return () => {
      if (timerRef.current) {
        clearInterval(timerRef.current);
      }
    };
  }, [testStarted, timeRemaining]);

  const loadAvailableTests = async () => {
    try {
      setLoading(true);
      const response = await fetch('http://127.0.0.1:8000/api/v1/mock-tests/', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      if (response.ok) {
        const data = await response.json();
        setAvailableTests(data.tests || []);
      }
    } catch (error) {
      console.error('Failed to load tests:', error);
    } finally {
      setLoading(false);
    }
  };

  const startTest = async (testId) => {
    try {
      setLoading(true);
      
      // Start test session
      const sessionResponse = await fetch(`http://127.0.0.1:8000/api/v1/mock-tests/${testId}/start`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });

      if (sessionResponse.ok) {
        const session = await sessionResponse.json();
        setTestSession(session);
        
        // Begin the test
        const beginResponse = await fetch(`http://127.0.0.1:8000/api/v1/mock-tests/sessions/${session.id}/begin`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });

        if (beginResponse.ok) {
          const updatedSession = await beginResponse.json();
          setTestSession(updatedSession);
          setTimeRemaining(selectedTest.time_limit_minutes * 60);
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
    if (currentQuestionIndex < selectedTest.questions.length - 1) {
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

      const response = await fetch(`http://127.0.0.1:8000/api/v1/mock-tests/sessions/${testSession.id}/submit`, {
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

  const getAIAnalysis = async () => {
    try {
      setLoading(true);
      const response = await fetch(`http://127.0.0.1:8000/api/v1/mock-tests/sessions/${testSession.id}/analyze`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });

      if (response.ok) {
        const analysis = await response.json();
        setAiAnalysis(analysis);
        setShowAnalysis(true);
      }
    } catch (error) {
      console.error('Failed to get AI analysis:', error);
      alert('Failed to get AI analysis. Please try again.');
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
    if (timeRemaining <= 300) return 'text-red-600'; // 5 minutes
    if (timeRemaining <= 600) return 'text-orange-600'; // 10 minutes
    return 'text-green-600';
  };

  if (loading && !testStarted) {
    return (
      <div className="flex min-h-screen bg-gray-50">
        <div className="flex-1 flex items-center justify-center">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600 mx-auto mb-4"></div>
            <p className="text-gray-600">Loading...</p>
          </div>
        </div>
      </div>
    );
  }

  // Test Selection View
  if (!selectedTest) {
    return (
      <div className="flex min-h-screen bg-gray-50">
        <div className="flex-1 p-6">
          <div className="flex justify-between items-center mb-8">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Mock Tests</h1>
              <p className="text-gray-600 mt-2">Take practice tests to improve your skills</p>
            </div>
            <ProfileDropdown />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {availableTests.map((test) => (
              <motion.div
                key={test.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                whileHover={{ scale: 1.02 }}
                className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow cursor-pointer"
                onClick={() => setSelectedTest(test)}
              >
                <div className="flex items-center mb-4">
                  <BookOpen className="w-8 h-8 text-purple-600 mr-3" />
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900">{test.title}</h3>
                    <p className="text-sm text-gray-500">Subject ID: {test.subject_id}</p>
                  </div>
                </div>

                <p className="text-gray-600 text-sm mb-4 line-clamp-2">
                  {test.description || 'No description provided'}
                </p>

                <div className="space-y-2 mb-4">
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-500">Questions:</span>
                    <span className="font-medium">{test.question_count || 0}</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-500">Total Marks:</span>
                    <span className="font-medium">{test.total_marks}</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-500">Time Limit:</span>
                    <span className="font-medium">{test.time_limit_minutes} min</span>
                  </div>
                </div>

                <div className="flex items-center justify-between">
                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                    test.status === 'active' ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'
                  }`}>
                    {test.status}
                  </span>
                  <button className="text-purple-600 hover:text-purple-700 font-medium text-sm">
                    Start Test →
                  </button>
                </div>
              </motion.div>
            ))}

            {availableTests.length === 0 && (
              <div className="col-span-full text-center py-12">
                <BookOpen className="w-16 h-16 text-gray-300 mx-auto mb-4" />
                <h3 className="text-lg font-medium text-gray-900 mb-2">No Tests Available</h3>
                <p className="text-gray-500">Check back later for new mock tests.</p>
              </div>
            )}
          </div>
        </div>
      </div>
    );
  }

  // Test Taking View
  if (selectedTest && testStarted && !testSubmitted) {
    const currentQuestion = selectedTest.questions[currentQuestionIndex];
    const totalQuestions = selectedTest.questions.length;
    const answeredQuestions = Object.keys(answers).length;

    return (
      <div className="flex min-h-screen bg-gray-50">
        <div className="flex-1 flex flex-col">
          {/* Header */}
          <div className="bg-white border-b border-gray-200 px-6 py-4">
            <div className="flex justify-between items-center">
              <div>
                <h1 className="text-xl font-semibold text-gray-900">{selectedTest.title}</h1>
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
          <div className="flex-1 p-6">
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
                  {selectedTest.questions.map((_, index) => (
                    <button
                      key={index}
                      onClick={() => setCurrentQuestionIndex(index)}
                      className={`w-8 h-8 rounded-full text-sm font-medium transition-colors ${
                        index === currentQuestionIndex
                          ? 'bg-purple-600 text-white'
                          : answers[selectedTest.questions[index].id]
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
      </div>
    );
  }

  // Results View
  if (testSubmitted && testResult) {
    return (
      <div className="flex min-h-screen bg-gray-50">
        <div className="flex-1 p-6">
          <div className="flex justify-between items-center mb-8">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Test Results</h1>
              <p className="text-gray-600 mt-2">Your performance on {selectedTest.title}</p>
            </div>
            <ProfileDropdown />
          </div>

          <div className="max-w-4xl mx-auto space-y-6">
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

            {/* AI Analysis Button */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 }}
              className="text-center"
            >
              <button
                onClick={getAIAnalysis}
                disabled={loading}
                className="flex items-center px-6 py-3 bg-gradient-to-r from-purple-600 to-pink-600 text-white rounded-lg hover:from-purple-700 hover:to-pink-700 disabled:opacity-50 transition-all mx-auto"
              >
                <Brain className="w-5 h-5 mr-2" />
                {loading ? 'Analyzing...' : 'Get AI Analysis'}
              </button>
            </motion.div>

            {/* AI Analysis Results */}
            <AnimatePresence>
              {showAnalysis && aiAnalysis && (
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
                        {aiAnalysis.analysis?.overall_assessment || aiAnalysis.performance_summary}
                      </p>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                      <div>
                        <h4 className="text-lg font-medium text-green-700 mb-3 flex items-center">
                          <CheckCircle className="w-5 h-5 mr-2" />
                          Strengths
                        </h4>
                        <ul className="space-y-2">
                          {aiAnalysis.strengths?.map((strength, index) => (
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
                          {aiAnalysis.weaknesses?.map((weakness, index) => (
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
                        {aiAnalysis.recommendations?.map((recommendation, index) => (
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
                  setSelectedTest(null);
                  setTestSession(null);
                  setTestResult(null);
                  setAiAnalysis(null);
                  setShowAnalysis(false);
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
                  // Navigate to dashboard or results page
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
    <div className="flex min-h-screen bg-gray-50">
      <div className="flex-1 p-6">
        <div className="max-w-2xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-white rounded-xl shadow-sm border border-gray-200 p-8"
          >
            <div className="text-center mb-8">
              <BookOpen className="w-16 h-16 text-purple-600 mx-auto mb-4" />
              <h1 className="text-2xl font-bold text-gray-900 mb-2">{selectedTest.title}</h1>
              <p className="text-gray-600">{selectedTest.description}</p>
            </div>

            <div className="space-y-4 mb-8">
              <div className="flex justify-between py-3 border-b border-gray-200">
                <span className="text-gray-600">Total Questions:</span>
                <span className="font-medium">{selectedTest.question_count || 0}</span>
              </div>
              <div className="flex justify-between py-3 border-b border-gray-200">
                <span className="text-gray-600">Total Marks:</span>
                <span className="font-medium">{selectedTest.total_marks}</span>
              </div>
              <div className="flex justify-between py-3 border-b border-gray-200">
                <span className="text-gray-600">Time Limit:</span>
                <span className="font-medium">{selectedTest.time_limit_minutes} minutes</span>
              </div>
              <div className="flex justify-between py-3">
                <span className="text-gray-600">Subject:</span>
                <span className="font-medium">Subject ID {selectedTest.subject_id}</span>
              </div>
            </div>

            <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mb-8">
              <div className="flex items-start">
                <AlertCircle className="w-5 h-5 text-yellow-600 mr-3 mt-0.5" />
                <div>
                  <h4 className="font-medium text-yellow-800 mb-1">Important Instructions</h4>
                  <ul className="text-sm text-yellow-700 space-y-1">
                    <li>• You cannot pause or restart the test once started</li>
                    <li>• The test will auto-submit when time runs out</li>
                    <li>• Make sure you have a stable internet connection</li>
                    <li>• You can navigate between questions using the navigation buttons</li>
                  </ul>
                </div>
              </div>
            </div>

            <div className="flex justify-center space-x-4">
              <button
                onClick={() => setSelectedTest(null)}
                className="px-6 py-3 text-gray-600 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={() => startTest(selectedTest.id)}
                disabled={loading}
                className="px-6 py-3 bg-purple-600 text-white rounded-lg hover:bg-purple-700 disabled:opacity-50 transition-colors"
              >
                {loading ? 'Starting...' : 'Start Test'}
              </button>
            </div>
          </motion.div>
        </div>
      </div>
    </div>
  );
};

export default MockTestTaker;
