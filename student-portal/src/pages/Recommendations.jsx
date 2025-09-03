import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { 
  GraduationCap, 
  BookOpen, 
  ExternalLink,
  RotateCcw,
  Filter,
  X
} from 'lucide-react';

const Recommendations = () => {
  const { studentId } = useParams();
  const navigate = useNavigate();
  const [recommendations, setRecommendations] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filteredRecommendations, setFilteredRecommendations] = useState({});
  const [filters, setFilters] = useState({
    subject: 'all',
    level: 'all'
  });

  // Available subjects and levels for filtering
  const subjects = ['all', 'Operating Systems', 'Computer Networks', 'OOPs', 'DBMS', 'Coding'];
  const levels = ['all', 'beginner', 'intermediate', 'advanced'];

  useEffect(() => {
    fetchRecommendations();
  }, [studentId]);

  useEffect(() => {
    applyFilters();
  }, [filters, recommendations]);

  const fetchRecommendations = async () => {
    try {
      setLoading(true);
      setError(null);
      
      // For now, using a mock API call since the backend endpoint requires authentication
      // In production, this would be: `/api/recommend-courses/${studentId}`
      const response = await fetch(`/api/recommend-courses/${studentId || 1}`);
      
      if (!response.ok) {
        throw new Error('Failed to fetch recommendations');
      }
      
      const data = await response.json();
      setRecommendations(data.recommendations || {});
      
    } catch (err) {
      console.error('Error fetching recommendations:', err);
      
      // Fallback to mock data for demonstration
      const mockData = {
        "Operating Systems": [
          "[OS Fundamentals (Power User)](https://www.coursera.org/learn/os-power-user)",
          "[Open Source Operating Systems](https://www.coursera.org/learn/illinois-tech-introduction-to-open-source-operating-systems-bit)"
        ],
        "Computer Networks": [
          "[Computer Networking Full Course](https://www.youtube.com/watch?v=xZ5KzG4g6KA)",
          "[Operating Systems Foundations](https://www.coursera.org/courses?query=operating+systems)"
        ],
        "OOPs": [
          "[Object-Oriented Programming in Java](https://www.coursera.org/learn/object-oriented-java)",
          "[Object-Oriented Design](https://www.coursera.org/learn/object-oriented-design)"
        ],
        "DBMS": [
          "[SQL for Data Science](https://www.coursera.org/learn/sql-for-data-science)",
          "[Database Management Essentials](https://www.coursera.org/learn/database-management)"
        ],
        "Coding": [
          "[Programming Foundations with Python](https://www.coursera.org/learn/python)",
          "[Data Structures and Algorithms](https://www.youtube.com/playlist?list=PLfqMhTWNBTe0b2nM6JHVCnAkhQRGiZMSJ)"
        ]
      };
      
      setRecommendations(mockData);
      setError('Using demo data - backend connection failed');
    } finally {
      setLoading(false);
    }
  };

  const applyFilters = () => {
    let filtered = { ...recommendations };
    
    // Filter by subject
    if (filters.subject !== 'all') {
      filtered = Object.fromEntries(
        Object.entries(filtered).filter(([subject]) => subject === filters.subject)
      );
    }
    
    // Filter by level (this would require parsing the course data to extract levels)
    // For now, we'll just apply subject filtering
    
    setFilteredRecommendations(filtered);
  };

  const parseCourseData = (courseString) => {
    // Parse course strings like "[Course Title](URL)"
    const match = courseString.match(/\[([^\]]+)\]\(([^)]+)\)/);
    if (match) {
      return {
        title: match[1],
        url: match[2],
        level: determineLevel(match[1]), // Simple heuristic
        subject: determineSubject(match[1]) // Simple heuristic
      };
    }
    return {
      title: courseString,
      url: '#',
      level: 'intermediate',
      subject: 'General'
    };
  };

  const determineLevel = (title) => {
    const lowerTitle = title.toLowerCase();
    if (lowerTitle.includes('fundamental') || lowerTitle.includes('basic') || lowerTitle.includes('intro')) {
      return 'beginner';
    } else if (lowerTitle.includes('advanced') || lowerTitle.includes('expert')) {
      return 'advanced';
    }
    return 'intermediate';
  };

  const determineSubject = (title) => {
    // This is a simple heuristic - in production, this would come from the backend
    return 'General';
  };

  const getLevelColor = (level) => {
    switch (level) {
      case 'beginner':
        return 'bg-green-100 text-green-800 border-green-200';
      case 'intermediate':
        return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'advanced':
        return 'bg-red-100 text-red-800 border-red-200';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  const getLevelIcon = (level) => {
    switch (level) {
      case 'beginner':
        return '🟢';
      case 'intermediate':
        return '🟡';
      case 'advanced':
        return '🔴';
      default:
        return '⚪';
    }
  };

  const handleRetakeTest = () => {
    navigate('/assessment/start');
  };

  const handleRefresh = () => {
    fetchRecommendations();
  };

  const clearFilters = () => {
    setFilters({ subject: 'all', level: 'all' });
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-lg text-gray-600">Loading your personalized recommendations...</p>
        </div>
      </div>
    );
  }

  const hasRecommendations = Object.keys(filteredRecommendations).length > 0;

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <div className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <GraduationCap className="h-8 w-8 text-blue-600" />
              <div>
                <h1 className="text-2xl font-bold text-gray-900">Course Recommendations</h1>
                <p className="text-sm text-gray-600">
                  Personalized learning path based on your assessment results
                </p>
              </div>
            </div>
            <div className="flex items-center space-x-3">
              <button
                onClick={handleRefresh}
                className="inline-flex items-center px-3 py-2 border border-gray-300 shadow-sm text-sm leading-4 font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
              >
                <RotateCcw className="h-4 w-4 mr-2" />
                Refresh
              </button>
              <button
                onClick={handleRetakeTest}
                className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
              >
                <BookOpenIcon className="h-4 w-4 mr-2" />
                Retake Test
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Filters */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4 mb-6">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center space-x-2">
              <Filter className="h-5 w-5 text-gray-500" />
              <h3 className="text-lg font-medium text-gray-900">Filter Courses</h3>
            </div>
            <button
              onClick={clearFilters}
              className="text-sm text-gray-500 hover:text-gray-700 flex items-center space-x-1"
            >
              <X className="h-4 w-4" />
              <span>Clear filters</span>
            </button>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label htmlFor="subject-filter" className="block text-sm font-medium text-gray-700 mb-2">
                Subject
              </label>
              <select
                id="subject-filter"
                value={filters.subject}
                onChange={(e) => setFilters(prev => ({ ...prev, subject: e.target.value }))}
                className="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
              >
                {subjects.map(subject => (
                  <option key={subject} value={subject}>
                    {subject === 'all' ? 'All Subjects' : subject}
                  </option>
                ))}
              </select>
            </div>
            
            <div>
              <label htmlFor="level-filter" className="block text-sm font-medium text-gray-700 mb-2">
                Level
              </label>
              <select
                id="level-filter"
                value={filters.level}
                onChange={(e) => setFilters(prev => ({ ...prev, level: e.target.value }))}
                className="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
              >
                {levels.map(level => (
                  <option key={level} value={level}>
                    {level === 'all' ? 'All Levels' : level.charAt(0).toUpperCase() + level.slice(1)}
                  </option>
                ))}
              </select>
            </div>
          </div>
        </div>

        {/* Error Message */}
        {error && (
          <div className="bg-yellow-50 border border-yellow-200 rounded-md p-4 mb-6">
            <div className="flex">
              <div className="flex-shrink-0">
                <svg className="h-5 w-5 text-yellow-400" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                </svg>
              </div>
              <div className="ml-3">
                <p className="text-sm text-yellow-800">{error}</p>
              </div>
            </div>
          </div>
        )}

        {/* No Recommendations Message */}
        {!hasRecommendations && !loading && (
          <div className="text-center py-12">
            <GraduationCap className="mx-auto h-16 w-16 text-gray-400 mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">No recommendations yet</h3>
            <p className="text-gray-600 mb-6">Please take the assessment test first to get personalized course recommendations.</p>
            <button
              onClick={handleRetakeTest}
              className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              <BookOpenIcon className="h-4 w-4 mr-2" />
              Take Assessment Test
            </button>
          </div>
        )}

        {/* Recommendations Grid */}
        {hasRecommendations && (
          <div className="space-y-6">
            {Object.entries(filteredRecommendations).map(([subject, courses]) => (
              <div key={subject} className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
                <div className="px-6 py-4 bg-gradient-to-r from-blue-50 to-indigo-50 border-b border-gray-200">
                  <h2 className="text-xl font-semibold text-gray-900">{subject}</h2>
                  <p className="text-sm text-gray-600 mt-1">
                    {courses.length} course{courses.length !== 1 ? 's' : ''} recommended
                  </p>
                </div>
                
                <div className="p-6">
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    {courses.map((courseString, index) => {
                      const course = parseCourseData(courseString);
                      return (
                        <div
                          key={index}
                          className="group relative bg-white border border-gray-200 rounded-lg p-4 hover:shadow-md hover:border-blue-300 transition-all duration-200 cursor-pointer"
                        >
                          <div className="flex items-start justify-between mb-3">
                            <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border ${getLevelColor(course.level)}`}>
                              {getLevelIcon(course.level)} {course.level.charAt(0).toUpperCase() + course.level.slice(1)}
                            </span>
                          </div>
                          
                          <h3 className="text-lg font-medium text-gray-900 mb-2 group-hover:text-blue-600 transition-colors">
                            {course.title}
                          </h3>
                          
                          <div className="flex items-center justify-between mt-4">
                            <span className="text-sm text-gray-500">{course.subject}</span>
                            <a
                              href={course.url}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="inline-flex items-center px-3 py-1.5 border border-transparent text-xs font-medium rounded-md text-blue-700 bg-blue-100 hover:bg-blue-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors"
                              onClick={(e) => e.stopPropagation()}
                            >
                              <ExternalLink className="h-3 w-3 mr-1" />
                              Open Course
                            </a>
                          </div>
                          
                          {/* Hover overlay */}
                          <div className="absolute inset-0 bg-blue-50 bg-opacity-0 group-hover:bg-opacity-5 rounded-lg transition-all duration-200 pointer-events-none"></div>
                        </div>
                      );
                    })}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default Recommendations;
