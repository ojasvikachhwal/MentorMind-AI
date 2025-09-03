import React, { useState, useEffect } from 'react';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import Toast from '../../components/Toast';
import FeedbackCard from '../../components/FeedbackCard';
import { 
  Filter, 
  RefreshCw, 
  Search,
  Lightbulb,
  AlertCircle,
  CheckCircle,
  TrendingUp,
  Target
} from 'lucide-react';

const AIFeedback = () => {
  const [feedback, setFeedback] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [toast, setToast] = useState(null);
  const [filter, setFilter] = useState('all');
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    fetchFeedback();
  }, [filter]);

  const fetchFeedback = async () => {
    try {
      setLoading(true);
      const token = localStorage.getItem('token');
      const url = filter === 'all' 
        ? '/api/v1/progress/feedback?limit=50'
        : `/api/v1/progress/feedback?limit=50&feedback_type=${filter}`;
      
      const response = await fetch(url, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (!response.ok) {
        throw new Error('Failed to fetch feedback');
      }

      const data = await response.json();
      setFeedback(data);
    } catch (err) {
      setError(err.message);
      setToast({ type: 'error', message: 'Failed to load AI feedback' });
    } finally {
      setLoading(false);
    }
  };

  const markAsRead = async (feedbackId) => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`/api/v1/progress/feedback/${feedbackId}/read`, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (!response.ok) {
        throw new Error('Failed to mark feedback as read');
      }

      setFeedback(prev => 
        prev.map(f => 
          f.id === feedbackId ? { ...f, is_read: true } : f
        )
      );
      
      setToast({ type: 'success', message: 'Feedback marked as read' });
    } catch (err) {
      setToast({ type: 'error', message: 'Failed to mark feedback as read' });
    }
  };

  const archiveFeedback = async (feedbackId) => {
    try {
      // This would be implemented in the backend
      setFeedback(prev => prev.filter(f => f.id !== feedbackId));
      setToast({ type: 'success', message: 'Feedback archived' });
    } catch (err) {
      setToast({ type: 'error', message: 'Failed to archive feedback' });
    }
  };

  const dismissFeedback = async (feedbackId) => {
    try {
      // This would be implemented in the backend
      setFeedback(prev => prev.filter(f => f.id !== feedbackId));
      setToast({ type: 'success', message: 'Feedback dismissed' });
    } catch (err) {
      setToast({ type: 'error', message: 'Failed to dismiss feedback' });
    }
  };

  const filteredFeedback = feedback.filter(f => {
    const matchesSearch = f.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         f.message.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         (f.subject && f.subject.toLowerCase().includes(searchTerm.toLowerCase()));
    return matchesSearch;
  });

  const getFeedbackStats = () => {
    const total = feedback.length;
    const unread = feedback.filter(f => !f.is_read).length;
    const byType = feedback.reduce((acc, f) => {
      acc[f.feedback_type] = (acc[f.feedback_type] || 0) + 1;
      return acc;
    }, {});

    return { total, unread, byType };
  };

  const stats = getFeedbackStats();

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading AI feedback...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">AI Feedback</h1>
          <p className="text-gray-600">Personalized insights and recommendations from your AI tutor</p>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <Card className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Total Feedback</p>
                <p className="text-2xl font-bold text-gray-900">{stats.total}</p>
              </div>
              <Lightbulb className="h-8 w-8 text-blue-600" />
            </div>
          </Card>

          <Card className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Unread</p>
                <p className="text-2xl font-bold text-gray-900">{stats.unread}</p>
              </div>
              <AlertCircle className="h-8 w-8 text-orange-600" />
            </div>
          </Card>

          <Card className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Strengths</p>
                <p className="text-2xl font-bold text-gray-900">{stats.byType.strength || 0}</p>
              </div>
              <CheckCircle className="h-8 w-8 text-green-600" />
            </div>
          </Card>

          <Card className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Recommendations</p>
                <p className="text-2xl font-bold text-gray-900">{stats.byType.recommendation || 0}</p>
              </div>
              <Target className="h-8 w-8 text-purple-600" />
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
                placeholder="Search feedback..."
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
              <option value="all">All Types</option>
              <option value="strength">Strengths</option>
              <option value="weakness">Weaknesses</option>
              <option value="recommendation">Recommendations</option>
              <option value="encouragement">Encouragement</option>
              <option value="warning">Warnings</option>
            </select>
          </div>
          
          <Button
            onClick={fetchFeedback}
            className="flex items-center space-x-2 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2"
          >
            <RefreshCw className="h-4 w-4" />
            <span>Refresh</span>
          </Button>
        </div>

        {/* Feedback List */}
        <div className="space-y-6">
          {filteredFeedback.length === 0 ? (
            <Card className="p-12 text-center">
              <Lightbulb className="h-12 w-12 text-gray-400 mx-auto mb-4" />
              <h3 className="text-lg font-semibold text-gray-900 mb-2">No Feedback Available</h3>
              <p className="text-gray-600">
                {searchTerm 
                  ? "No feedback matches your search criteria."
                  : "Start learning to receive personalized AI feedback!"
                }
              </p>
            </Card>
          ) : (
            filteredFeedback.map((feedbackItem) => (
              <FeedbackCard
                key={feedbackItem.id}
                feedback={feedbackItem}
                onMarkAsRead={markAsRead}
                onArchive={archiveFeedback}
                onDismiss={dismissFeedback}
              />
            ))
          )}
        </div>

        {/* Load More Button */}
        {filteredFeedback.length > 0 && (
          <div className="text-center mt-8">
            <Button
              onClick={() => {
                // Implement load more functionality
                setToast({ type: 'info', message: 'Load more functionality coming soon!' });
              }}
              className="bg-gray-600 hover:bg-gray-700 text-white px-6 py-2"
            >
              Load More Feedback
            </Button>
          </div>
        )}
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

export default AIFeedback;
