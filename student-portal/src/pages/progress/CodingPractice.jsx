import React, { useState, useEffect } from 'react';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import Toast from '../../components/Toast';
import { 
  Code, 
  Clock, 
  CheckCircle, 
  AlertCircle, 
  TrendingUp,
  Filter,
  Search,
  Play,
  RefreshCw
} from 'lucide-react';

const CodingPractice = () => {
  const [practices, setPractices] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [toast, setToast] = useState(null);
  const [filter, setFilter] = useState('all');
  const [searchTerm, setSearchTerm] = useState('');
  const [showSubmitForm, setShowSubmitForm] = useState(false);
  const [submitting, setSubmitting] = useState(false);

  // Form state for new coding practice
  const [formData, setFormData] = useState({
    problem_title: '',
    problem_difficulty: 'easy',
    language: 'python',
    solution_code: '',
    test_cases_passed: 0,
    total_test_cases: 1,
    execution_time: 0,
    memory_usage: 0,
    time_spent: 0
  });

  useEffect(() => {
    fetchCodingPractices();
  }, [filter]);

  const fetchCodingPractices = async () => {
    try {
      setLoading(true);
      const token = localStorage.getItem('token');
      const url = filter === 'all' 
        ? '/api/v1/progress/coding-practices?limit=50'
        : `/api/v1/progress/coding-practices?limit=50&difficulty=${filter}`;
      
      const response = await fetch(url, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (!response.ok) {
        throw new Error('Failed to fetch coding practices');
      }

      const data = await response.json();
      setPractices(data);
    } catch (err) {
      setError(err.message);
      setToast({ type: 'error', message: 'Failed to load coding practices' });
    } finally {
      setLoading(false);
    }
  };

  const handleSubmitPractice = async (e) => {
    e.preventDefault();
    setSubmitting(true);

    try {
      const token = localStorage.getItem('token');
      const response = await fetch('/api/v1/progress/track-coding-practice', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
      });

      if (!response.ok) {
        throw new Error('Failed to submit coding practice');
      }

      const newPractice = await response.json();
      setPractices(prev => [newPractice, ...prev]);
      setShowSubmitForm(false);
      setFormData({
        problem_title: '',
        problem_difficulty: 'easy',
        language: 'python',
        solution_code: '',
        test_cases_passed: 0,
        total_test_cases: 1,
        execution_time: 0,
        memory_usage: 0,
        time_spent: 0
      });
      
      setToast({ type: 'success', message: 'Coding practice submitted successfully!' });
    } catch (err) {
      setToast({ type: 'error', message: 'Failed to submit coding practice' });
    } finally {
      setSubmitting(false);
    }
  };

  const filteredPractices = practices.filter(practice => {
    const matchesSearch = practice.problem_title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         practice.language.toLowerCase().includes(searchTerm.toLowerCase());
    return matchesSearch;
  });

  const getStats = () => {
    const total = practices.length;
    const avgScore = practices.length > 0 
      ? practices.reduce((sum, p) => sum + (p.score || 0), 0) / practices.length 
      : 0;
    const languages = [...new Set(practices.map(p => p.language))];
    const difficulties = practices.reduce((acc, p) => {
      acc[p.problem_difficulty] = (acc[p.problem_difficulty] || 0) + 1;
      return acc;
    }, {});

    return { total, avgScore, languages, difficulties };
  };

  const stats = getStats();

  const getDifficultyColor = (difficulty) => {
    switch (difficulty) {
      case 'easy': return 'bg-green-100 text-green-800';
      case 'medium': return 'bg-yellow-100 text-yellow-800';
      case 'hard': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getScoreColor = (score) => {
    if (score >= 80) return 'text-green-600';
    if (score >= 60) return 'text-yellow-600';
    return 'text-red-600';
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading coding practices...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 mb-2">Coding Practice</h1>
              <p className="text-gray-600">Track your coding progress with AI-powered feedback</p>
            </div>
            <Button
              onClick={() => setShowSubmitForm(true)}
              className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2"
            >
              <Code className="h-4 w-4 mr-2" />
              Submit Practice
            </Button>
          </div>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <Card className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Total Practices</p>
                <p className="text-2xl font-bold text-gray-900">{stats.total}</p>
              </div>
              <Code className="h-8 w-8 text-blue-600" />
            </div>
          </Card>

          <Card className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Average Score</p>
                <p className="text-2xl font-bold text-gray-900">{stats.avgScore.toFixed(1)}%</p>
              </div>
              <TrendingUp className="h-8 w-8 text-green-600" />
            </div>
          </Card>

          <Card className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Languages</p>
                <p className="text-2xl font-bold text-gray-900">{stats.languages.length}</p>
              </div>
              <CheckCircle className="h-8 w-8 text-purple-600" />
            </div>
          </Card>

          <Card className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Hard Problems</p>
                <p className="text-2xl font-bold text-gray-900">{stats.difficulties.hard || 0}</p>
              </div>
              <AlertCircle className="h-8 w-8 text-red-600" />
            </div>
          </Card>
        </div>

        {/* Filters and Search */}
        <div className="flex flex-col sm:flex-row gap-4 mb-6">
          <div className="flex-1">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
              <input
                type="text"
                placeholder="Search problems..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
          </div>
          
          <div className="flex items-center space-x-2">
            <Filter className="h-4 w-4 text-gray-400" />
            <select
              value={filter}
              onChange={(e) => setFilter(e.target.value)}
              className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="all">All Difficulties</option>
              <option value="easy">Easy</option>
              <option value="medium">Medium</option>
              <option value="hard">Hard</option>
            </select>
          </div>
          
          <Button
            onClick={fetchCodingPractices}
            className="flex items-center space-x-2 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2"
          >
            <RefreshCw className="h-4 w-4" />
            <span>Refresh</span>
          </Button>
        </div>

        {/* Coding Practices List */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {filteredPractices.map((practice) => (
            <Card key={practice.id} className="p-6">
              <div className="flex items-start justify-between mb-4">
                <div className="flex-1">
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">
                    {practice.problem_title}
                  </h3>
                  <div className="flex items-center space-x-4 text-sm text-gray-600">
                    <span className="flex items-center">
                      <Code className="h-4 w-4 mr-1" />
                      {practice.language}
                    </span>
                    <span className="flex items-center">
                      <Clock className="h-4 w-4 mr-1" />
                      {practice.time_spent} min
                    </span>
                  </div>
                </div>
                <span className={`px-2 py-1 text-xs font-medium rounded-full ${getDifficultyColor(practice.problem_difficulty)}`}>
                  {practice.problem_difficulty}
                </span>
              </div>

              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">Test Cases</span>
                  <span className="text-sm font-medium">
                    {practice.test_cases_passed}/{practice.total_test_cases}
                  </span>
                </div>

                {practice.score && (
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-600">Score</span>
                    <span className={`text-sm font-bold ${getScoreColor(practice.score)}`}>
                      {practice.score.toFixed(1)}%
                    </span>
                  </div>
                )}

                {practice.execution_time && (
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-600">Execution Time</span>
                    <span className="text-sm font-medium">
                      {practice.execution_time.toFixed(2)}s
                    </span>
                  </div>
                )}

                {practice.memory_usage && (
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-600">Memory Usage</span>
                    <span className="text-sm font-medium">
                      {practice.memory_usage.toFixed(2)} MB
                    </span>
                  </div>
                )}
              </div>

              {practice.ai_feedback && (
                <div className="mt-4 p-3 bg-blue-50 rounded-lg">
                  <h4 className="text-sm font-medium text-blue-900 mb-1">AI Feedback</h4>
                  <p className="text-sm text-blue-800">{practice.ai_feedback}</p>
                </div>
              )}

              {practice.optimization_suggestions && practice.optimization_suggestions.length > 0 && (
                <div className="mt-4 p-3 bg-yellow-50 rounded-lg">
                  <h4 className="text-sm font-medium text-yellow-900 mb-2">Optimization Suggestions</h4>
                  <ul className="text-sm text-yellow-800 space-y-1">
                    {practice.optimization_suggestions.map((suggestion, index) => (
                      <li key={index} className="flex items-start">
                        <span className="mr-2">•</span>
                        <span>{suggestion}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              <div className="mt-4 text-xs text-gray-500">
                {new Date(practice.created_at).toLocaleDateString()}
              </div>
            </Card>
          ))}
        </div>

        {filteredPractices.length === 0 && (
          <Card className="p-12 text-center">
            <Code className="h-12 w-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-semibold text-gray-900 mb-2">No Coding Practices</h3>
            <p className="text-gray-600 mb-4">
              {searchTerm 
                ? "No practices match your search criteria."
                : "Start coding to track your progress!"
              }
            </p>
            <Button
              onClick={() => setShowSubmitForm(true)}
              className="bg-blue-600 hover:bg-blue-700 text-white"
            >
              Submit Your First Practice
            </Button>
          </Card>
        )}
      </div>

      {/* Submit Form Modal */}
      {showSubmitForm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <Card className="w-full max-w-2xl max-h-[90vh] overflow-y-auto">
            <div className="p-6">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-xl font-semibold text-gray-900">Submit Coding Practice</h2>
                <Button
                  onClick={() => setShowSubmitForm(false)}
                  className="text-gray-400 hover:text-gray-600"
                >
                  ×
                </Button>
              </div>

              <form onSubmit={handleSubmitPractice} className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Problem Title
                    </label>
                    <input
                      type="text"
                      required
                      value={formData.problem_title}
                      onChange={(e) => setFormData({...formData, problem_title: e.target.value})}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Difficulty
                    </label>
                    <select
                      value={formData.problem_difficulty}
                      onChange={(e) => setFormData({...formData, problem_difficulty: e.target.value})}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    >
                      <option value="easy">Easy</option>
                      <option value="medium">Medium</option>
                      <option value="hard">Hard</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Language
                    </label>
                    <select
                      value={formData.language}
                      onChange={(e) => setFormData({...formData, language: e.target.value})}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    >
                      <option value="python">Python</option>
                      <option value="java">Java</option>
                      <option value="cpp">C++</option>
                      <option value="javascript">JavaScript</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Time Spent (minutes)
                    </label>
                    <input
                      type="number"
                      min="0"
                      value={formData.time_spent}
                      onChange={(e) => setFormData({...formData, time_spent: parseInt(e.target.value) || 0})}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Test Cases Passed
                    </label>
                    <input
                      type="number"
                      min="0"
                      value={formData.test_cases_passed}
                      onChange={(e) => setFormData({...formData, test_cases_passed: parseInt(e.target.value) || 0})}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Total Test Cases
                    </label>
                    <input
                      type="number"
                      min="1"
                      value={formData.total_test_cases}
                      onChange={(e) => setFormData({...formData, total_test_cases: parseInt(e.target.value) || 1})}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Solution Code
                  </label>
                  <textarea
                    required
                    rows="10"
                    value={formData.solution_code}
                    onChange={(e) => setFormData({...formData, solution_code: e.target.value})}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent font-mono text-sm"
                    placeholder="Paste your solution code here..."
                  />
                </div>

                <div className="flex justify-end space-x-4">
                  <Button
                    type="button"
                    onClick={() => setShowSubmitForm(false)}
                    className="bg-gray-600 hover:bg-gray-700 text-white px-6 py-2"
                  >
                    Cancel
                  </Button>
                  <Button
                    type="submit"
                    disabled={submitting}
                    className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2"
                  >
                    {submitting ? 'Submitting...' : 'Submit Practice'}
                  </Button>
                </div>
              </form>
            </div>
          </Card>
        </div>
      )}

      {/* Toast Notification */}
      {toast && (
        <Toast
          type={toast.type}
          message={toast.message}
          onClose={() => setToast(null)}
        />
      )}
    </div>
  );
};

export default CodingPractice;
