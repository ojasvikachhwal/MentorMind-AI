import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { 
  GraduationCap, 
  BookOpen, 
  ExternalLink,
  RotateCcw,
  Filter,
  X,
  Home as HomeIcon,
  BookText,
  FileText,
  Cpu
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
  const [showUserMenu, setShowUserMenu] = useState(false);
  
  const toggleUserMenu = () => {
    setShowUserMenu(!showUserMenu);
  };

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
    <div className="min-h-screen bg-gradient-to-b from-blue-500 to-purple-600">
      {/* Header with horizontal navigation */}
      <header className="bg-blue-600 p-4 flex justify-between items-center">
        <div className="flex space-x-8">
          <button 
            onClick={() => navigate('/dashboard')} 
            className="text-white flex items-center"
          >
            <HomeIcon className="h-4 w-4 mr-2" />
            <span>Home</span>
          </button>
          <button 
            onClick={() => navigate('/practice')} 
            className="text-white flex items-center"
          >
            <BookText className="h-4 w-4 mr-2" />
            <span>Practice</span>
          </button>
          <button 
            onClick={() => navigate('/resources')} 
            className="text-white flex items-center"
          >
            <FileText className="h-4 w-4 mr-2" />
            <span>Resources</span>
          </button>
          <button 
            onClick={() => navigate('/ved')} 
            className="text-white flex items-center"
          >
            <Cpu className="h-4 w-4 mr-2" />
            <span>Ved</span>
          </button>
        </div>
        
        <div className="relative">
          <button onClick={toggleUserMenu} className="bg-white rounded-full w-8 h-8 flex items-center justify-center">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
            </svg>
          </button>
          
          {showUserMenu && (
            <div className="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg py-1 z-10">
              <a href="#" className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">Profile</a>
              <a href="#" className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">Contact Us</a>
              <a href="#" className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">About Us</a>
              <a href="#" onClick={() => navigate('/login')} className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">Log Out</a>
            </div>
          )}
        </div>
      </header>

      {/* Main Content */}
      <div className="bg-white mx-auto my-4 p-6 rounded-lg shadow-md max-w-6xl">
        <div className="mb-4">
          <h2 className="text-xl font-semibold text-blue-700 mb-2">Recommended Courses</h2>
          
          {/* Course categories in boxes */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
            <div className="bg-purple-200 p-3 rounded-md">
              <h3 className="font-medium text-purple-800">Computer Networks</h3>
              <ul className="text-sm text-gray-600 mt-1">
                <li>• Network Fundamentals</li>
                <li>• TCP/IP Protocol</li>
                <li>• Routing Algorithms</li>
                <li>• Network Security</li>
              </ul>
            </div>
            
            <div className="bg-blue-200 p-3 rounded-md">
              <h3 className="font-medium text-blue-800">Operating System</h3>
              <ul className="text-sm text-gray-600 mt-1">
                <li>• Process Management</li>
                <li>• Memory Management</li>
                <li>• File Systems</li>
                <li>• I/O Systems</li>
              </ul>
            </div>
            
            <div className="bg-pink-200 p-3 rounded-md">
              <h3 className="font-medium text-pink-800">Data Structure & Algorithms</h3>
              <ul className="text-sm text-gray-600 mt-1">
                <li>• Arrays and Linked Lists</li>
                <li>• Trees and Graphs</li>
                <li>• Sorting Algorithms</li>
                <li>• Dynamic Programming</li>
              </ul>
            </div>
            
            <div className="bg-indigo-200 p-3 rounded-md">
              <h3 className="font-medium text-indigo-800">OOPs</h3>
              <ul className="text-sm text-gray-600 mt-1">
                <li>• Classes and Objects</li>
                <li>• Inheritance</li>
                <li>• Polymorphism</li>
                <li>• Encapsulation</li>
              </ul>
            </div>
          </div>
        </div>
      </div>

      <div className="bg-white mx-auto my-4 p-6 rounded-lg shadow-md max-w-6xl">
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
              <BookOpen className="h-4 w-4 mr-2" />
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
