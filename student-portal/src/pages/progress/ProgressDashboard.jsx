import React, { useState, useEffect } from 'react';
import { Card } from '../../components/ui/Card';
import { Progress } from '../../components/ui/Progress';
import { Button } from '../../components/ui/Button';
import Toast from '../../components/Toast';
import { 
  LineChart, 
  Line, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  Legend, 
  ResponsiveContainer,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell
} from 'recharts';
import { 
  TrendingUp, 
  BookOpen, 
  Code, 
  Target, 
  Clock, 
  Award,
  AlertCircle,
  CheckCircle,
  Lightbulb
} from 'lucide-react';

const ProgressDashboard = () => {
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedPeriod, setSelectedPeriod] = useState(30);
  const [toast, setToast] = useState(null);

  useEffect(() => {
    fetchDashboardData();
  }, [selectedPeriod]);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      const token = localStorage.getItem('token');
      const response = await fetch(`/api/v1/progress/dashboard?days=${selectedPeriod}`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (!response.ok) {
        throw new Error('Failed to fetch dashboard data');
      }

      const data = await response.json();
      setDashboardData(data);
    } catch (err) {
      setError(err.message);
      setToast({ type: 'error', message: 'Failed to load dashboard data' });
    } finally {
      setLoading(false);
    }
  };

  const formatTime = (minutes) => {
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    return hours > 0 ? `${hours}h ${mins}m` : `${mins}m`;
  };

  const getScoreColor = (score) => {
    if (score >= 80) return '#10b981';
    if (score >= 60) return '#f59e0b';
    return '#ef4444';
  };

  const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6'];

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading your progress...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <AlertCircle className="h-12 w-12 text-red-500 mx-auto mb-4" />
          <h2 className="text-xl font-semibold text-gray-900 mb-2">Error Loading Dashboard</h2>
          <p className="text-gray-600 mb-4">{error}</p>
          <Button onClick={fetchDashboardData} className="bg-blue-600 hover:bg-blue-700">
            Try Again
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Progress Dashboard</h1>
          <p className="text-gray-600">Track your learning journey and AI-powered insights</p>
          
          {/* Period Selector */}
          <div className="mt-4 flex space-x-2">
            {[7, 30, 90].map((period) => (
              <Button
                key={period}
                onClick={() => setSelectedPeriod(period)}
                className={`px-4 py-2 rounded-lg ${
                  selectedPeriod === period
                    ? 'bg-blue-600 text-white'
                    : 'bg-white text-gray-700 border border-gray-300 hover:bg-gray-50'
                }`}
              >
                {period} days
              </Button>
            ))}
          </div>
        </div>

        {/* Summary Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <Card className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Total Study Time</p>
                <p className="text-2xl font-bold text-gray-900">
                  {formatTime(dashboardData?.summary?.total_study_time || 0)}
                </p>
              </div>
              <Clock className="h-8 w-8 text-blue-600" />
            </div>
          </Card>

          <Card className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Activities Completed</p>
                <p className="text-2xl font-bold text-gray-900">
                  {dashboardData?.summary?.total_activities || 0}
                </p>
              </div>
              <Target className="h-8 w-8 text-green-600" />
            </div>
          </Card>

          <Card className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Average Quiz Score</p>
                <p className="text-2xl font-bold text-gray-900">
                  {dashboardData?.summary?.average_quiz_score?.toFixed(1) || 0}%
                </p>
              </div>
              <BookOpen className="h-8 w-8 text-purple-600" />
            </div>
          </Card>

          <Card className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Coding Sessions</p>
                <p className="text-2xl font-bold text-gray-900">
                  {dashboardData?.summary?.total_coding_sessions || 0}
                </p>
              </div>
              <Code className="h-8 w-8 text-orange-600" />
            </div>
          </Card>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
          {/* Daily Activity Chart */}
          <Card className="p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Daily Activity</h3>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={dashboardData?.daily_activity || []}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line 
                  type="monotone" 
                  dataKey="study_time" 
                  stroke="#3b82f6" 
                  strokeWidth={2}
                  name="Study Time (min)"
                />
                <Line 
                  type="monotone" 
                  dataKey="activities" 
                  stroke="#10b981" 
                  strokeWidth={2}
                  name="Activities"
                />
              </LineChart>
            </ResponsiveContainer>
          </Card>

          {/* Subject Performance Chart */}
          <Card className="p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Subject Performance</h3>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={dashboardData?.subject_performance || []}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="subject" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="average_score" fill="#3b82f6" />
              </BarChart>
            </ResponsiveContainer>
          </Card>
        </div>

        {/* AI Feedback Section */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-8">
          {/* Recent Feedback */}
          <Card className="p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
              <Lightbulb className="h-5 w-5 text-yellow-500 mr-2" />
              AI Insights
            </h3>
            <div className="space-y-4">
              {dashboardData?.recent_feedback?.slice(0, 3).map((feedback, index) => (
                <div key={index} className="border-l-4 border-blue-500 pl-4">
                  <h4 className="font-medium text-gray-900">{feedback.title}</h4>
                  <p className="text-sm text-gray-600 mt-1">{feedback.message}</p>
                  <p className="text-xs text-gray-500 mt-2">
                    {new Date(feedback.created_at).toLocaleDateString()}
                  </p>
                </div>
              ))}
              {(!dashboardData?.recent_feedback || dashboardData.recent_feedback.length === 0) && (
                <p className="text-gray-500 text-center py-4">No recent feedback available</p>
              )}
            </div>
          </Card>

          {/* Weekly Analytics */}
          <Card className="p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
              <TrendingUp className="h-5 w-5 text-green-500 mr-2" />
              Weekly Trends
            </h3>
            <div className="space-y-4">
              {dashboardData?.weekly_analytics?.slice(0, 3).map((week, index) => (
                <div key={index} className="border rounded-lg p-4">
                  <h4 className="font-medium text-gray-900">
                    Week of {new Date(week.week_start).toLocaleDateString()}
                  </h4>
                  <div className="grid grid-cols-2 gap-2 mt-2 text-sm">
                    <div>
                      <span className="text-gray-600">Study Time:</span>
                      <span className="ml-1 font-medium">{formatTime(week.total_study_time)}</span>
                    </div>
                    <div>
                      <span className="text-gray-600">Activities:</span>
                      <span className="ml-1 font-medium">{week.activities || 0}</span>
                    </div>
                    <div>
                      <span className="text-gray-600">Quiz Score:</span>
                      <span className="ml-1 font-medium">{week.average_quiz_score?.toFixed(1)}%</span>
                    </div>
                    <div>
                      <span className="text-gray-600">Coding Score:</span>
                      <span className="ml-1 font-medium">{week.average_coding_score?.toFixed(1)}%</span>
                    </div>
                  </div>
                </div>
              ))}
              {(!dashboardData?.weekly_analytics || dashboardData.weekly_analytics.length === 0) && (
                <p className="text-gray-500 text-center py-4">No weekly data available</p>
              )}
            </div>
          </Card>

          {/* Coding Progress */}
          <Card className="p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
              <Code className="h-5 w-5 text-orange-500 mr-2" />
              Coding Progress
            </h3>
            <div className="space-y-4">
              {dashboardData?.coding_progress?.slice(0, 3).map((practice, index) => (
                <div key={index} className="border rounded-lg p-4">
                  <h4 className="font-medium text-gray-900">{practice.problem}</h4>
                  <div className="flex items-center justify-between mt-2">
                    <span className="text-sm text-gray-600">{practice.language}</span>
                    <span className={`text-sm font-medium px-2 py-1 rounded ${
                      practice.difficulty === 'easy' ? 'bg-green-100 text-green-800' :
                      practice.difficulty === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                      'bg-red-100 text-red-800'
                    }`}>
                      {practice.difficulty}
                    </span>
                  </div>
                  {practice.score && (
                    <div className="mt-2">
                      <Progress 
                        value={practice.score} 
                        className="h-2"
                        style={{ backgroundColor: getScoreColor(practice.score) }}
                      />
                      <p className="text-xs text-gray-600 mt-1">
                        Score: {practice.score.toFixed(1)}%
                      </p>
                    </div>
                  )}
                </div>
              ))}
              {(!dashboardData?.coding_progress || dashboardData.coding_progress.length === 0) && (
                <p className="text-gray-500 text-center py-4">No coding practice data</p>
              )}
            </div>
          </Card>
        </div>

        {/* Action Buttons */}
        <div className="flex justify-center space-x-4">
          <Button 
            onClick={fetchDashboardData}
            className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2"
          >
            Refresh Data
          </Button>
          <Button 
            onClick={() => window.location.href = '/courses'}
            className="bg-green-600 hover:bg-green-700 text-white px-6 py-2"
          >
            Continue Learning
          </Button>
        </div>
      </div>

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

export default ProgressDashboard;
