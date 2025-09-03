import { useState, useEffect } from 'react';
import { useNavigate, useParams, useLocation } from 'react-router-dom';
import { Button } from '../../components/ui/Button';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '../../components/ui/Card';
import { getResults } from '../../services/api';
import { ArrowLeft, Star, Clock, BookOpen, TrendingUp } from 'lucide-react';

export default function AssessmentResults() {
  const { sessionId } = useParams();
  const location = useLocation();
  const navigate = useNavigate();
  
  const [results, setResults] = useState(location.state?.results || null);
  const [loading, setLoading] = useState(!results);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!results) {
      loadResults();
    }
  }, [results]);

  const loadResults = async () => {
    try {
      const resultsData = await getResults(sessionId);
      setResults(resultsData);
    } catch (err) {
      setError('Failed to load results');
    } finally {
      setLoading(false);
    }
  };

  const getLevelColor = (level) => {
    switch (level) {
      case 'beginner':
        return 'bg-green-100 text-green-800';
      case 'intermediate':
        return 'bg-yellow-100 text-yellow-800';
      case 'advanced':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getScoreColor = (percent) => {
    if (percent >= 70) return 'text-green-600';
    if (percent >= 40) return 'text-yellow-600';
    return 'text-red-600';
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading results...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <p className="text-red-600">{error}</p>
          <Button onClick={() => navigate('/dashboard')} className="mt-4">
            Back to Dashboard
          </Button>
        </div>
      </div>
    );
  }

  if (!results) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <p className="text-gray-600">No results found</p>
          <Button onClick={() => navigate('/dashboard')} className="mt-4">
            Back to Dashboard
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <Button
                variant="outline"
                onClick={() => navigate('/dashboard')}
                className="flex items-center space-x-2"
              >
                <ArrowLeft className="w-4 h-4" />
                <span>Back to Dashboard</span>
              </Button>
              <h1 className="text-2xl font-bold text-gray-900">
                Assessment Results
              </h1>
            </div>
            <div className="text-sm text-gray-600">
              Session ID: {sessionId}
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Summary Card */}
        <Card className="mb-8">
          <CardHeader>
            <CardTitle>Assessment Summary</CardTitle>
            <CardDescription>
              Your performance across all subjects
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div className="text-center p-4 bg-blue-50 rounded-lg">
                <div className="text-2xl font-bold text-blue-600">{results.results.length}</div>
                <div className="text-sm text-gray-600">Subjects Tested</div>
              </div>
              <div className="text-center p-4 bg-green-50 rounded-lg">
                <div className="text-2xl font-bold text-green-600">
                  {Math.round(results.results.reduce((acc, r) => acc + r.percent_correct, 0) / results.results.length)}%
                </div>
                <div className="text-sm text-gray-600">Average Score</div>
              </div>
              <div className="text-center p-4 bg-purple-50 rounded-lg">
                <div className="text-2xl font-bold text-purple-600">
                  {results.results.reduce((acc, r) => acc + r.weighted_score, 0)}
                </div>
                <div className="text-sm text-gray-600">Total Weighted Score</div>
              </div>
              <div className="text-center p-4 bg-yellow-50 rounded-lg">
                <div className="text-2xl font-bold text-yellow-600">
                  {results.results.filter(r => r.level === 'advanced').length}
                </div>
                <div className="text-sm text-gray-600">Advanced Level</div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Subject Results */}
        <div className="space-y-6">
          <h2 className="text-xl font-semibold text-gray-900">Subject-wise Results</h2>
          
          {results.results.map((subjectResult, index) => (
            <Card key={index}>
              <CardHeader>
                <div className="flex justify-between items-start">
                  <div>
                    <CardTitle className="text-lg">{subjectResult.subject_name}</CardTitle>
                    <CardDescription>
                      Performance breakdown and recommendations
                    </CardDescription>
                  </div>
                  <div className="flex items-center space-x-2">
                    <span className={`px-3 py-1 rounded-full text-sm font-medium ${getLevelColor(subjectResult.level)}`}>
                      {subjectResult.level}
                    </span>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                  {/* Performance Metrics */}
                  <div>
                    <h3 className="font-semibold text-gray-900 mb-4">Performance Metrics</h3>
                    <div className="space-y-3">
                      <div className="flex justify-between items-center">
                        <span className="text-sm text-gray-600">Percentage Correct:</span>
                        <span className={`font-semibold ${getScoreColor(subjectResult.percent_correct)}`}>
                          {subjectResult.percent_correct}%
                        </span>
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="text-sm text-gray-600">Weighted Score:</span>
                        <span className="font-semibold text-gray-900">
                          {subjectResult.weighted_score} points
                        </span>
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="text-sm text-gray-600">Skill Level:</span>
                        <span className={`px-2 py-1 rounded text-sm font-medium ${getLevelColor(subjectResult.level)}`}>
                          {subjectResult.level}
                        </span>
                      </div>
                    </div>
                  </div>

                  {/* Recommended Courses */}
                  <div>
                    <h3 className="font-semibold text-gray-900 mb-4">Recommended Courses</h3>
                    <div className="space-y-3">
                      {subjectResult.recommended_courses.map((course, courseIndex) => (
                        <div key={courseIndex} className="p-3 border rounded-lg">
                          <div className="flex items-start justify-between">
                            <div className="flex-1">
                              <h4 className="font-medium text-gray-900">{course.title}</h4>
                              <p className="text-sm text-gray-600 mt-1">{course.description}</p>
                              <div className="flex items-center space-x-4 mt-2">
                                <span className={`px-2 py-1 rounded text-xs font-medium ${getLevelColor(course.level)}`}>
                                  {course.level}
                                </span>
                                <div className="flex items-center space-x-1 text-xs text-gray-500">
                                  <Clock className="w-3 h-3" />
                                  <span>2-4 hours</span>
                                </div>
                              </div>
                            </div>
                            <Button
                              variant="outline"
                              size="sm"
                              onClick={() => navigate('/courses/recommendations')}
                            >
                              View
                            </Button>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Action Buttons */}
        <div className="mt-8 flex justify-center space-x-4">
          <Button
            onClick={() => navigate('/assessment/start')}
            className="flex items-center space-x-2"
            size="lg"
          >
            <BookOpen className="w-4 h-4" />
            <span>Take Another Assessment</span>
          </Button>
          <Button
            onClick={() => navigate('/courses/recommendations')}
            variant="outline"
            className="flex items-center space-x-2"
            size="lg"
          >
            <TrendingUp className="w-4 h-4" />
            <span>Browse All Courses</span>
          </Button>
        </div>
      </div>
    </div>
  );
}
