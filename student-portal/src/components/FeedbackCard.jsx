import React from 'react';
import { Card } from './ui/Card';
import { Button } from './ui/Button';
import { 
  CheckCircle, 
  AlertCircle, 
  Lightbulb, 
  TrendingUp, 
  Target,
  X,
  Eye,
  EyeOff
} from 'lucide-react';

const FeedbackCard = ({ feedback, onMarkAsRead, onArchive, onDismiss }) => {
  const getFeedbackIcon = (type) => {
    switch (type) {
      case 'strength':
        return <CheckCircle className="h-5 w-5 text-green-500" />;
      case 'weakness':
        return <AlertCircle className="h-5 w-5 text-red-500" />;
      case 'recommendation':
        return <Lightbulb className="h-5 w-5 text-yellow-500" />;
      case 'encouragement':
        return <TrendingUp className="h-5 w-5 text-blue-500" />;
      case 'warning':
        return <AlertCircle className="h-5 w-5 text-orange-500" />;
      default:
        return <Lightbulb className="h-5 w-5 text-gray-500" />;
    }
  };

  const getFeedbackColor = (type) => {
    switch (type) {
      case 'strength':
        return 'border-l-green-500 bg-green-50';
      case 'weakness':
        return 'border-l-red-500 bg-red-50';
      case 'recommendation':
        return 'border-l-yellow-500 bg-yellow-50';
      case 'encouragement':
        return 'border-l-blue-500 bg-blue-50';
      case 'warning':
        return 'border-l-orange-500 bg-orange-50';
      default:
        return 'border-l-gray-500 bg-gray-50';
    }
  };

  const getFeedbackBadge = (type) => {
    switch (type) {
      case 'strength':
        return 'bg-green-100 text-green-800';
      case 'weakness':
        return 'bg-red-100 text-red-800';
      case 'recommendation':
        return 'bg-yellow-100 text-yellow-800';
      case 'encouragement':
        return 'bg-blue-100 text-blue-800';
      case 'warning':
        return 'bg-orange-100 text-orange-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  return (
    <Card className={`p-6 border-l-4 ${getFeedbackColor(feedback.feedback_type)} transition-all duration-200 hover:shadow-md`}>
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center space-x-3">
          {getFeedbackIcon(feedback.feedback_type)}
          <div>
            <h3 className="text-lg font-semibold text-gray-900">{feedback.title}</h3>
            <div className="flex items-center space-x-2 mt-1">
              <span className={`px-2 py-1 text-xs font-medium rounded-full ${getFeedbackBadge(feedback.feedback_type)}`}>
                {feedback.feedback_type.charAt(0).toUpperCase() + feedback.feedback_type.slice(1)}
              </span>
              {feedback.subject && (
                <span className="px-2 py-1 text-xs font-medium rounded-full bg-gray-100 text-gray-800">
                  {feedback.subject}
                </span>
              )}
            </div>
          </div>
        </div>
        
        <div className="flex items-center space-x-2">
          {!feedback.is_read && (
            <Button
              onClick={() => onMarkAsRead(feedback.id)}
              className="p-2 text-gray-400 hover:text-blue-600"
              title="Mark as read"
            >
              <Eye className="h-4 w-4" />
            </Button>
          )}
          
          <Button
            onClick={() => onArchive(feedback.id)}
            className="p-2 text-gray-400 hover:text-orange-600"
            title="Archive"
          >
            <EyeOff className="h-4 w-4" />
          </Button>
          
          <Button
            onClick={() => onDismiss(feedback.id)}
            className="p-2 text-gray-400 hover:text-red-600"
            title="Dismiss"
          >
            <X className="h-4 w-4" />
          </Button>
        </div>
      </div>

      <div className="mb-4">
        <p className="text-gray-700 leading-relaxed">{feedback.message}</p>
      </div>

      <div className="flex items-center justify-between text-sm text-gray-500">
        <div className="flex items-center space-x-4">
          <span>{formatDate(feedback.created_at)}</span>
          {feedback.confidence_score && (
            <div className="flex items-center space-x-1">
              <Target className="h-4 w-4" />
              <span>Confidence: {Math.round(feedback.confidence_score * 100)}%</span>
            </div>
          )}
        </div>
        
        {feedback.is_read && (
          <span className="text-green-600 font-medium">Read</span>
        )}
      </div>
    </Card>
  );
};

export default FeedbackCard;
